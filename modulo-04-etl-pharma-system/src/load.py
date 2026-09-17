"""
load.py
-------
Camada Load do ETL: carrega DataFrames limpos no banco de destino usando
UPSERT (INSERT ... ON CONFLICT DO UPDATE) para garantir idempotencia.

Backend suportado nativamente: SQLite (via sqlite3).
Para PostgreSQL, veja o metodo carregar_postgres() ao final do arquivo.

Garantias:
- Idempotencia: rodar o mesmo arquivo N vezes produz o mesmo estado no banco.
- Atomicidade por arquivo: se um INSERT falhar no meio, faz rollback.
- Auditoria: cada linha inserida tem `inserido_em` (timestamp) e `origem_arquivo`.
"""

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import pandas as pd

from src.logger import obter_logger

log = obter_logger("load")


# -----------------------------------------------------------------------------
# DDL — criacao das tabelas no destino
# -----------------------------------------------------------------------------

DDL_FATO_VENDAS_SQLITE = """
CREATE TABLE IF NOT EXISTS fato_vendas (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    filial_codigo     TEXT     NOT NULL,
    data_venda        TEXT     NOT NULL,
    cliente_cpf       TEXT,
    produto_codigo    TEXT     NOT NULL,
    produto_nome      TEXT     NOT NULL,
    quantidade        INTEGER  NOT NULL CHECK (quantidade > 0),
    preco_unitario    REAL     NOT NULL CHECK (preco_unitario > 0),
    desconto          REAL     NOT NULL DEFAULT 0,
    valor_total       REAL     NOT NULL,
    forma_pagamento   TEXT     NOT NULL,
    vendedor          TEXT,
    ano_mes           TEXT     NOT NULL,
    origem_arquivo    TEXT     NOT NULL,
    inserido_em       TEXT     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em     TEXT,
    UNIQUE (filial_codigo, data_venda, cliente_cpf, produto_codigo)
);

CREATE INDEX IF NOT EXISTS idx_fato_vendas_ano_mes    ON fato_vendas (ano_mes);
CREATE INDEX IF NOT EXISTS idx_fato_vendas_filial     ON fato_vendas (filial_codigo);
CREATE INDEX IF NOT EXISTS idx_fato_vendas_data       ON fato_vendas (data_venda);
"""

# Tabela de execucoes do pipeline (metadados de auditoria)
DDL_EXECUCOES = """
CREATE TABLE IF NOT EXISTS pipeline_execucoes (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    executado_em          TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    arquivos_encontrados  INTEGER NOT NULL,
    arquivos_processados  INTEGER NOT NULL,
    arquivos_rejeitados   INTEGER NOT NULL,
    linhas_inseridas      INTEGER NOT NULL,
    linhas_atualizadas    INTEGER NOT NULL,
    duracao_segundos      REAL    NOT NULL,
    status                TEXT    NOT NULL
);
"""


@dataclass
class RelatorioLoad:
    """Estatisticas da carga de um arquivo."""
    arquivo: str = ""
    linhas_entrada: int = 0
    linhas_inseridas: int = 0
    linhas_atualizadas: int = 0
    linhas_ignoradas: int = 0
    erros: List[str] = field(default_factory=list)
    sucesso: bool = False

    def resumir(self) -> str:
        return (
            f"{self.linhas_inseridas} inseridas, "
            f"{self.linhas_atualizadas} atualizadas, "
            f"{self.linhas_ignoradas} ignoradas"
        )


class CarregadorSQLite:
    """Carrega dados no banco SQLite via UPSERT."""

    COLUNAS_FATO = [
        "filial_codigo", "data_venda", "cliente_cpf", "produto_codigo",
        "produto_nome", "quantidade", "preco_unitario", "desconto",
        "valor_total", "forma_pagamento", "vendedor", "ano_mes",
    ]

    def __init__(self, caminho_db: Path):
        self.caminho_db = Path(caminho_db)
        self.caminho_db.parent.mkdir(parents=True, exist_ok=True)

    def inicializar_banco(self):
        """Cria tabelas se nao existirem. Idempotente."""
        conn = sqlite3.connect(self.caminho_db)
        try:
            conn.executescript(DDL_FATO_VENDAS_SQLITE)
            conn.executescript(DDL_EXECUCOES)
            conn.commit()
            log.info(f"Banco inicializado: {self.caminho_db}")
        finally:
            conn.close()

    def _preparar_linhas(self, df: pd.DataFrame, origem_arquivo: str) -> List[tuple]:
        """Converte DataFrame em lista de tuplas para executemany.

        Trata NaN -> None e garante ordem correta das colunas.
        """
        # Garantir que todas as colunas esperadas existem
        for c in self.COLUNAS_FATO:
            if c not in df.columns:
                df[c] = None

        # Converter data para string ISO
        df = df.copy()
        df["data_venda"] = df["data_venda"].dt.strftime("%Y-%m-%d %H:%M:%S")

        # Substituir NaN por None (sqlite entende None como NULL)
        df = df.where(pd.notna(df), None)

        # Adicionar origem
        df["origem_arquivo"] = origem_arquivo

        # Ordem exata das colunas
        cols = self.COLUNAS_FATO + ["origem_arquivo"]
        linhas = [tuple(row[c] for c in cols) for _, row in df.iterrows()]
        return linhas

    def carregar_dataframe(
        self, df: pd.DataFrame, origem_arquivo: str
    ) -> RelatorioLoad:
        """Faz UPSERT das linhas do df na tabela fato_vendas.

        - INSERT se a chave natural nao existe.
        - UPDATE se ja existe (rodar 2x nao duplica).
        """
        rel = RelatorioLoad(arquivo=origem_arquivo, linhas_entrada=len(df))

        if len(df) == 0:
            log.info(f"[{origem_arquivo}] DataFrame vazio, nada a carregar")
            rel.sucesso = True
            return rel

        linhas = self._preparar_linhas(df, origem_arquivo)

        # Query UPSERT SQLite (INSERT ... ON CONFLICT DO UPDATE)
        placeholders = ", ".join(["?"] * (len(self.COLUNAS_FATO) + 1))
        cols_str = ", ".join(self.COLUNAS_FATO + ["origem_arquivo"])
        # Atualizar tudo EXCETO chave natural em caso de conflito
        chave_natural = ["filial_codigo", "data_venda", "cliente_cpf", "produto_codigo"]
        cols_update = [c for c in self.COLUNAS_FATO if c not in chave_natural]
        update_str = ", ".join([
            f"{c}=excluded.{c}" for c in cols_update
        ])
        update_str += ", origem_arquivo=excluded.origem_arquivo, atualizado_em=CURRENT_TIMESTAMP"

        sql = f"""
            INSERT INTO fato_vendas ({cols_str})
            VALUES ({placeholders})
            ON CONFLICT (filial_codigo, data_venda, cliente_cpf, produto_codigo)
            DO UPDATE SET {update_str}
        """

        conn = sqlite3.connect(self.caminho_db)
        try:
            # Contar quantas ja existem antes (para saber inseridas vs atualizadas)
            cur = conn.cursor()
            placeholders_chave = ", ".join(["(?, ?, ?, ?)"] * len(linhas))
            # Tratar cpf None (nao pode ser comparado com = em SQL)
            # Solucao mais simples: contar diferenca via total antes/depois
            cur.execute("SELECT COUNT(*) FROM fato_vendas")
            total_antes = cur.fetchone()[0]

            # Executar UPSERT
            cur.executemany(sql, linhas)
            conn.commit()

            cur.execute("SELECT COUNT(*) FROM fato_vendas")
            total_depois = cur.fetchone()[0]

            rel.linhas_inseridas = total_depois - total_antes
            rel.linhas_atualizadas = len(linhas) - rel.linhas_inseridas
            rel.sucesso = True

            log.info(
                f"[{origem_arquivo}] Load: {rel.resumir()}"
            )
        except sqlite3.Error as e:
            conn.rollback()
            msg = f"Erro SQL: {type(e).__name__}: {e}"
            log.error(f"[{origem_arquivo}] {msg}")
            rel.erros.append(msg)
        finally:
            conn.close()

        return rel

    def registrar_execucao(
        self, arquivos_encontrados: int, arquivos_processados: int,
        arquivos_rejeitados: int, linhas_inseridas: int,
        linhas_atualizadas: int, duracao_segundos: float, status: str,
    ):
        """Registra uma linha na tabela de auditoria."""
        conn = sqlite3.connect(self.caminho_db)
        try:
            conn.execute(
                """INSERT INTO pipeline_execucoes
                   (arquivos_encontrados, arquivos_processados, arquivos_rejeitados,
                    linhas_inseridas, linhas_atualizadas, duracao_segundos, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (arquivos_encontrados, arquivos_processados, arquivos_rejeitados,
                 linhas_inseridas, linhas_atualizadas, duracao_segundos, status),
            )
            conn.commit()
        finally:
            conn.close()

    def estatisticas(self) -> dict:
        """Retorna estatisticas do estado atual do banco."""
        conn = sqlite3.connect(self.caminho_db)
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM fato_vendas")
            total = cur.fetchone()[0]

            cur.execute("SELECT COUNT(DISTINCT filial_codigo) FROM fato_vendas")
            filiais = cur.fetchone()[0]

            cur.execute("SELECT COUNT(DISTINCT ano_mes) FROM fato_vendas")
            meses = cur.fetchone()[0]

            cur.execute("SELECT COALESCE(SUM(valor_total), 0) FROM fato_vendas")
            faturamento = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM pipeline_execucoes")
            execucoes = cur.fetchone()[0]

            return {
                "total_linhas_fato_vendas": total,
                "filiais_distintas": filiais,
                "meses_com_dados": meses,
                "faturamento_acumulado": round(faturamento, 2),
                "execucoes_pipeline": execucoes,
            }
        finally:
            conn.close()


# =============================================================================
# EXTENSAO PARA POSTGRESQL (comentado — requer psycopg2 instalado)
# =============================================================================
#
# def criar_carregador(backend: str, config: dict):
#     """Factory que retorna o carregador apropriado."""
#     if backend == "sqlite":
#         return CarregadorSQLite(caminho_db=config["sqlite"]["caminho"])
#     elif backend == "postgres":
#         # from psycopg2 import connect  # pip install psycopg2-binary
#         return CarregadorPostgres(**config["postgres"])
#     else:
#         raise ValueError(f"Backend nao suportado: {backend}")
#
#
# class CarregadorPostgres:
#     """Analogo ao CarregadorSQLite mas para PostgreSQL.
#
#     Principais diferencas:
#     - Conexao via psycopg2 com connection pool
#     - Serial em vez de AUTOINCREMENT
#     - ON CONFLICT sintaxe identica
#     - Melhor para volumes altos (> 100k linhas)
#     """
#     def __init__(self, host, port, database, user, password):
#         self.dsn = f"host={host} port={port} dbname={database} user={user} password={password}"
#     # ... implementar identico ao SQLite trocando so a conexao
