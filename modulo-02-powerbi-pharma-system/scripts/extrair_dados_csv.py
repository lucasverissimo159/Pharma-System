"""
Extrai os dados do PharmaSystem (Semana 1) e exporta para CSV.
Cada tabela vira um arquivo CSV pronto para importar no Power BI.

Autor: Lucas Verissimo
Uso: python extrair_dados_csv.py
"""

import sqlite3
import csv
import re
import sys
from pathlib import Path

# Caminhos
BASE_MODULO_02 = Path(__file__).parent.parent
BASE_MODULO_01 = BASE_MODULO_02.parent / "modulo-01-sql-pharma-system"
PASTA_CSV = BASE_MODULO_02 / "dados"


def adaptar_para_sqlite(sql: str) -> str:
    """Adapta o SQL PostgreSQL para SQLite (apenas para gerar os dados)."""
    s = sql
    s = re.sub(r"SERIAL", "INTEGER", s)
    s = re.sub(r"BOOLEAN", "INTEGER", s)
    s = re.sub(r"\bTIMESTAMP\b(?! DEFAULT)", "TEXT", s)
    s = re.sub(r"TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP",
               "TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP", s)
    s = re.sub(r"CHAR\(2\)", "TEXT", s)
    s = re.sub(r"DECIMAL\(\d+, \d+\)", "REAL", s)
    s = re.sub(r"VARCHAR\(\d+\)", "TEXT", s)
    s = re.sub(r"COMMENT ON.*?;", "", s, flags=re.DOTALL)
    s = re.sub(r"(DROP (?:TABLE|VIEW) IF EXISTS \w+) CASCADE", r"\1", s)
    lines = [l for l in s.split("\n") if "~" not in l]
    s = "\n".join(lines)
    s = re.sub(r",(\s*\))", r"\1", s)
    s = s.replace("TRUE", "1").replace("FALSE", "0")
    return s


def criar_banco():
    """Cria banco em memoria e popula com os dados do Modulo 01."""
    schema_path = BASE_MODULO_01 / "01_schema.sql"
    inserts_path = BASE_MODULO_01 / "02_inserts.sql"

    if not schema_path.exists() or not inserts_path.exists():
        print(f"[ERRO] Nao encontrei os arquivos do Modulo 01 em: {BASE_MODULO_01}")
        print("       Voce precisa executar este script com o Modulo 01 na pasta irma.")
        print(f"       Esperado: {schema_path}")
        sys.exit(1)

    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys = ON")

    print("Criando schema...")
    con.executescript(adaptar_para_sqlite(schema_path.read_text()))

    print("Inserindo dados...")
    con.executescript(adaptar_para_sqlite(inserts_path.read_text()))

    return con


def exportar_tabela(con, tabela: str, arquivo_saida: Path,
                    ordem_colunas: list = None, transformador=None):
    """Exporta uma tabela para CSV.

    - tabela: nome da tabela no SQLite
    - arquivo_saida: Path do CSV
    - ordem_colunas: se fornecida, usa essa ordem (senao usa PRAGMA table_info)
    - transformador: funcao opcional que recebe uma linha (dict) e retorna dict
    """
    if ordem_colunas is None:
        cur = con.execute(f"PRAGMA table_info({tabela})")
        ordem_colunas = [row[1] for row in cur.fetchall()]

    cur = con.execute(f"SELECT {', '.join(ordem_colunas)} FROM {tabela}")
    linhas = cur.fetchall()

    with arquivo_saida.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(ordem_colunas)
        for linha in linhas:
            if transformador:
                d = dict(zip(ordem_colunas, linha))
                d = transformador(d)
                linha = [d[c] for c in ordem_colunas]
            writer.writerow(linha)

    print(f"  [OK] {arquivo_saida.name}: {len(linhas)} linhas")
    return len(linhas)


def transformar_booleanos(row: dict) -> dict:
    """Converte 0/1 para 'Sim'/'Nao' onde apropriado."""
    mapa = {
        'ativa': 'ativa',
        'ativo': 'ativo',
        'exige_receita': 'exige_receita',
    }
    for k in mapa:
        if k in row and row[k] is not None:
            row[k] = 'Sim' if row[k] == 1 else 'Nao'
    return row


def main():
    print("=" * 70)
    print("Exportador de dados PharmaSystem para CSV (Power BI)")
    print("=" * 70)
    print()

    PASTA_CSV.mkdir(exist_ok=True)
    con = criar_banco()

    print("\nExportando tabelas...")

    # filiais
    exportar_tabela(
        con, "filiais",
        PASTA_CSV / "filiais.csv",
        ordem_colunas=["id", "codigo", "nome", "cidade", "estado",
                       "endereco", "telefone", "data_abertura", "ativa"],
        transformador=transformar_booleanos
    )

    # categorias
    exportar_tabela(
        con, "categorias",
        PASTA_CSV / "categorias.csv",
        ordem_colunas=["id", "nome", "descricao"]
    )

    # produtos
    exportar_tabela(
        con, "produtos",
        PASTA_CSV / "produtos.csv",
        ordem_colunas=["id", "codigo_barras", "nome", "categoria_id",
                       "fabricante", "preco_custo", "preco_venda",
                       "estoque_minimo", "exige_receita", "ativo"],
        transformador=transformar_booleanos
    )

    # estoque
    exportar_tabela(
        con, "estoque",
        PASTA_CSV / "estoque.csv",
        ordem_colunas=["id", "produto_id", "filial_id", "quantidade"]
    )

    # clientes
    exportar_tabela(
        con, "clientes",
        PASTA_CSV / "clientes.csv",
        ordem_colunas=["id", "nome", "cpf", "email", "telefone",
                       "data_nascimento", "cidade", "estado", "data_cadastro"]
    )

    # vendas
    exportar_tabela(
        con, "vendas",
        PASTA_CSV / "vendas.csv",
        ordem_colunas=["id", "filial_id", "cliente_id", "data_venda",
                       "valor_total", "desconto", "forma_pagamento", "status"]
    )

    # itens_venda
    exportar_tabela(
        con, "itens_venda",
        PASTA_CSV / "itens_venda.csv",
        ordem_colunas=["id", "venda_id", "produto_id", "quantidade",
                       "preco_unitario", "subtotal"]
    )

    # Tabela calendario
    print("\nGerando tabela calendario...")
    cur = con.execute("SELECT MIN(data_venda), MAX(data_venda) FROM vendas")
    dt_min, dt_max = cur.fetchone()
    from datetime import date, timedelta
    d_ini = date.fromisoformat(dt_min[:10])
    d_fim = date.fromisoformat(dt_max[:10])

    meses_pt = ["", "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    dias_semana_pt = ["Segunda", "Terca", "Quarta", "Quinta",
                      "Sexta", "Sabado", "Domingo"]

    arq_cal = PASTA_CSV / "calendario.csv"
    with arq_cal.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            "data", "ano", "trimestre", "mes_num", "mes_nome",
            "ano_mes", "dia", "dia_semana_num", "dia_semana_nome",
            "eh_final_de_semana"
        ])
        atual = d_ini
        cont = 0
        while atual <= d_fim:
            writer.writerow([
                atual.isoformat(),
                atual.year,
                (atual.month - 1) // 3 + 1,
                atual.month,
                meses_pt[atual.month],
                f"{atual.year}-{atual.month:02d}",
                atual.day,
                atual.weekday() + 1,  # 1=segunda, 7=domingo
                dias_semana_pt[atual.weekday()],
                "Sim" if atual.weekday() >= 5 else "Nao"
            ])
            atual += timedelta(days=1)
            cont += 1

    print(f"  [OK] calendario.csv: {cont} linhas (de {d_ini} a {d_fim})")

    print("\n" + "=" * 70)
    print(f"Todos os CSVs gerados em: {PASTA_CSV}")
    print("=" * 70)


if __name__ == "__main__":
    main()
