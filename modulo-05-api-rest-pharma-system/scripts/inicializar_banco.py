"""
inicializar_banco.py
--------------------
Cria o banco SQLite e popula com os dados dos CSVs.

Fluxo:
    1. Cria/recria as tabelas usando db/schema.sql
    2. Le os CSVs em db/dados/ (embarcados no pacote)
    3. Insere os dados em cada tabela na ordem correta (respeita FKs)

Uso:
    python scripts/inicializar_banco.py
"""

import csv
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))

DB_PATH = ROOT / "db" / "pharma.db"
SCHEMA_PATH = ROOT / "db" / "schema.sql"
DADOS_PATH = ROOT / "db" / "dados"


def _bool_para_int(valor: str) -> int:
    """Converte 'Sim'/'Nao' para 1/0."""
    if valor is None or valor == "":
        return 0
    return 1 if str(valor).lower() in ("sim", "true", "1", "yes") else 0


def _int_ou_none(valor):
    """Converte string vazia em None."""
    if valor is None or valor == "":
        return None
    try:
        return int(valor)
    except (ValueError, TypeError):
        return None


def _float_ou_zero(valor):
    """Converte string vazia em 0.0."""
    if valor is None or valor == "":
        return 0.0
    try:
        return float(valor)
    except (ValueError, TypeError):
        return 0.0


def _texto_ou_none(valor):
    """Converte string vazia em None (para colunas nullable)."""
    if valor is None or valor == "":
        return None
    return str(valor).strip()


def carregar_csv(caminho: Path):
    """Le um CSV UTF-8-BOM e retorna lista de dicts."""
    with caminho.open("r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def popular(conn: sqlite3.Connection):
    """Popula o banco a partir dos CSVs em db/dados/."""

    # Filiais
    linhas = carregar_csv(DADOS_PATH / "filiais.csv")
    for l in linhas:
        conn.execute(
            """INSERT INTO filiais (id, codigo, nome, cidade, estado, endereco,
                                     telefone, data_abertura, ativa)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                int(l["id"]), l["codigo"], l["nome"], l["cidade"], l["estado"],
                _texto_ou_none(l["endereco"]), _texto_ou_none(l["telefone"]),
                l["data_abertura"], _bool_para_int(l["ativa"]),
            ),
        )
    print(f"  [OK] filiais: {len(linhas)} linhas")

    # Categorias
    linhas = carregar_csv(DADOS_PATH / "categorias.csv")
    for l in linhas:
        conn.execute(
            "INSERT INTO categorias (id, nome, descricao) VALUES (?, ?, ?)",
            (int(l["id"]), l["nome"], _texto_ou_none(l["descricao"])),
        )
    print(f"  [OK] categorias: {len(linhas)} linhas")

    # Produtos
    linhas = carregar_csv(DADOS_PATH / "produtos.csv")
    for l in linhas:
        conn.execute(
            """INSERT INTO produtos (id, codigo_barras, nome, categoria_id, fabricante,
                                       preco_custo, preco_venda, estoque_minimo,
                                       exige_receita, ativo)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                int(l["id"]), l["codigo_barras"], l["nome"],
                int(l["categoria_id"]), _texto_ou_none(l["fabricante"]),
                float(l["preco_custo"]), float(l["preco_venda"]),
                int(l["estoque_minimo"]),
                _bool_para_int(l["exige_receita"]),
                _bool_para_int(l["ativo"]),
            ),
        )
    print(f"  [OK] produtos: {len(linhas)} linhas")

    # Estoque
    linhas = carregar_csv(DADOS_PATH / "estoque.csv")
    for l in linhas:
        conn.execute(
            "INSERT INTO estoque (id, produto_id, filial_id, quantidade) VALUES (?, ?, ?, ?)",
            (int(l["id"]), int(l["produto_id"]), int(l["filial_id"]),
             int(l["quantidade"])),
        )
    print(f"  [OK] estoque: {len(linhas)} linhas")

    # Clientes
    linhas = carregar_csv(DADOS_PATH / "clientes.csv")
    for l in linhas:
        conn.execute(
            """INSERT INTO clientes (id, nome, cpf, email, telefone,
                                      data_nascimento, cidade, estado, data_cadastro)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                int(l["id"]), l["nome"], _texto_ou_none(l["cpf"]),
                _texto_ou_none(l["email"]), _texto_ou_none(l["telefone"]),
                _texto_ou_none(l["data_nascimento"]),
                _texto_ou_none(l["cidade"]), _texto_ou_none(l["estado"]),
                l["data_cadastro"],
            ),
        )
    print(f"  [OK] clientes: {len(linhas)} linhas")

    # Vendas
    linhas = carregar_csv(DADOS_PATH / "vendas.csv")
    for l in linhas:
        conn.execute(
            """INSERT INTO vendas (id, filial_id, cliente_id, data_venda,
                                    valor_total, desconto, forma_pagamento, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                int(l["id"]), int(l["filial_id"]),
                _int_ou_none(l["cliente_id"]),
                l["data_venda"],
                _float_ou_zero(l["valor_total"]),
                _float_ou_zero(l["desconto"]),
                l["forma_pagamento"], l["status"],
            ),
        )
    print(f"  [OK] vendas: {len(linhas)} linhas")

    # Itens de venda
    linhas = carregar_csv(DADOS_PATH / "itens_venda.csv")
    for l in linhas:
        conn.execute(
            """INSERT INTO itens_venda (id, venda_id, produto_id, quantidade,
                                         preco_unitario, subtotal)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                int(l["id"]), int(l["venda_id"]), int(l["produto_id"]),
                int(l["quantidade"]), float(l["preco_unitario"]),
                float(l["subtotal"]),
            ),
        )
    print(f"  [OK] itens_venda: {len(linhas)} linhas")


def main():
    print("=" * 70)
    print(f"Inicializando banco em {DB_PATH}")
    print("=" * 70)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        print(f"\nBanco existente encontrado. Removendo...")
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        # Schema
        print("\nCriando schema...")
        with SCHEMA_PATH.open("r", encoding="utf-8") as f:
            conn.executescript(f.read())
        print("  [OK] 7 tabelas criadas com indices e constraints")

        # Dados
        print("\nPopulando com dados dos CSVs...")
        popular(conn)

        conn.commit()

        # Estatisticas
        print("\n" + "=" * 70)
        print("Estatisticas do banco:")
        print("=" * 70)
        cur = conn.cursor()
        for tabela in ["filiais", "categorias", "produtos", "estoque",
                       "clientes", "vendas", "itens_venda"]:
            cur.execute(f"SELECT COUNT(*) FROM {tabela}")
            print(f"  {tabela:<15} {cur.fetchone()[0]:>6,} linhas")

        cur.execute(
            "SELECT ROUND(SUM(subtotal), 2) FROM itens_venda "
            "JOIN vendas ON itens_venda.venda_id = vendas.id "
            "WHERE vendas.status = 'CONCLUIDA'"
        )
        print(f"\n  Faturamento total (concluidas): R$ {cur.fetchone()[0]:,.2f}")

    except Exception as e:
        conn.rollback()
        print(f"\nERRO: {e}")
        raise
    finally:
        conn.close()

    print(f"\nBanco pronto: {DB_PATH}")
    print(f"Tamanho: {DB_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
