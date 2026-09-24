"""
app/database.py
---------------
Camada fina sobre sqlite3.

- `obter_conexao()`: retorna uma conexao SQLite por request (armazenada em `g`).
- `fechar_conexao_ao_final_da_request()`: hook chamado no teardown da request.
- Configura `row_factory = sqlite3.Row` para acesso por nome de coluna.
- Ativa `PRAGMA foreign_keys = ON` em toda conexao.

Nao usamos ORM (SQLAlchemy) de proposito — o objetivo do modulo e mostrar
os fundamentos de uma API REST sem "magica" de framework.
"""

import sqlite3
from flask import current_app, g


def obter_conexao() -> sqlite3.Connection:
    """Retorna a conexao SQLite da request atual (cria se necessario)."""
    if "db_conn" not in g:
        cfg = current_app.config["PHARMA_CONFIG"]
        g.db_conn = sqlite3.connect(cfg.DATABASE)
        g.db_conn.row_factory = sqlite3.Row
        g.db_conn.execute("PRAGMA foreign_keys = ON")
    return g.db_conn


def fechar_conexao_ao_final_da_request(exc=None):
    """Hook chamado ao final de cada request. Fecha a conexao."""
    conn = g.pop("db_conn", None)
    if conn is not None:
        try:
            conn.close()
        except sqlite3.Error:
            pass


def row_para_dict(row: sqlite3.Row) -> dict:
    """Converte sqlite3.Row em dict — util para retornar JSON."""
    if row is None:
        return None
    return {k: row[k] for k in row.keys()}


def rows_para_dicts(rows) -> list:
    """Converte lista de sqlite3.Row em lista de dicts."""
    return [row_para_dict(r) for r in rows]
