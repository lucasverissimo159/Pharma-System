"""
app/services/indicadores.py
--------------------------
Servicos de agregacao/indicadores. Toda logica SQL fica isolada aqui,
separada das rotas HTTP. Facilita testes e reuso.
"""

import sqlite3


def kpis_gerais(conn: sqlite3.Connection) -> dict:
    """Retorna KPIs principais da rede em um unico dict."""
    cur = conn.cursor()

    # Faturamento total (concluidas)
    cur.execute("""
        SELECT COALESCE(ROUND(SUM(iv.subtotal), 2), 0)
        FROM itens_venda iv
        JOIN vendas v ON v.id = iv.venda_id
        WHERE v.status = 'CONCLUIDA'
    """)
    faturamento_total = cur.fetchone()[0]

    # Numero de vendas
    cur.execute("SELECT COUNT(*) FROM vendas WHERE status = 'CONCLUIDA'")
    total_vendas = cur.fetchone()[0]

    # Vendas canceladas
    cur.execute("SELECT COUNT(*) FROM vendas WHERE status = 'CANCELADA'")
    total_canceladas = cur.fetchone()[0]

    # Ticket medio
    ticket_medio = round(faturamento_total / total_vendas, 2) if total_vendas else 0

    # Itens vendidos
    cur.execute("""
        SELECT COALESCE(SUM(iv.quantidade), 0)
        FROM itens_venda iv
        JOIN vendas v ON v.id = iv.venda_id
        WHERE v.status = 'CONCLUIDA'
    """)
    total_itens = cur.fetchone()[0]

    # Clientes ativos
    cur.execute("""
        SELECT COUNT(DISTINCT cliente_id) FROM vendas
        WHERE cliente_id IS NOT NULL AND status = 'CONCLUIDA'
    """)
    clientes_ativos = cur.fetchone()[0]

    # Produtos vendidos distintos
    cur.execute("""
        SELECT COUNT(DISTINCT produto_id) FROM itens_venda iv
        JOIN vendas v ON v.id = iv.venda_id
        WHERE v.status = 'CONCLUIDA'
    """)
    produtos_distintos = cur.fetchone()[0]

    # Filiais ativas
    cur.execute("""
        SELECT COUNT(DISTINCT filial_id) FROM vendas
        WHERE status = 'CONCLUIDA'
    """)
    filiais_com_venda = cur.fetchone()[0]

    # Margem bruta
    cur.execute("""
        SELECT COALESCE(ROUND(SUM(iv.quantidade * (p.preco_venda - p.preco_custo)), 2), 0)
        FROM itens_venda iv
        JOIN vendas v ON v.id = iv.venda_id
        JOIN produtos p ON p.id = iv.produto_id
        WHERE v.status = 'CONCLUIDA'
    """)
    margem_bruta = cur.fetchone()[0]

    percentual_margem = (
        round(margem_bruta / faturamento_total * 100, 2)
        if faturamento_total else 0
    )
    taxa_cancelamento = (
        round(total_canceladas / (total_vendas + total_canceladas) * 100, 2)
        if (total_vendas + total_canceladas) else 0
    )

    return {
        "faturamento_total": faturamento_total,
        "total_vendas_concluidas": total_vendas,
        "total_vendas_canceladas": total_canceladas,
        "taxa_cancelamento_pct": taxa_cancelamento,
        "ticket_medio": ticket_medio,
        "total_itens_vendidos": total_itens,
        "clientes_ativos": clientes_ativos,
        "produtos_distintos_vendidos": produtos_distintos,
        "filiais_com_venda": filiais_com_venda,
        "margem_bruta_total": margem_bruta,
        "percentual_margem": percentual_margem,
    }


def faturamento_mensal(conn: sqlite3.Connection, ano: int = None,
                        limite: int = 24) -> list:
    """Faturamento agregado por mes.

    Args:
        ano: filtra por ano (opcional)
        limite: N ultimos meses (default 24)
    """
    where = "WHERE v.status = 'CONCLUIDA'"
    params = []
    if ano is not None:
        where += " AND SUBSTR(v.data_venda, 1, 4) = ?"
        params.append(str(ano))

    sql = f"""
        SELECT SUBSTR(v.data_venda, 1, 7) as ano_mes,
               COUNT(DISTINCT v.id) as n_vendas,
               ROUND(SUM(iv.subtotal), 2) as faturamento,
               ROUND(SUM(iv.subtotal) / COUNT(DISTINCT v.id), 2) as ticket_medio
        FROM vendas v
        JOIN itens_venda iv ON iv.venda_id = v.id
        {where}
        GROUP BY ano_mes
        ORDER BY ano_mes DESC
        LIMIT ?
    """
    params.append(limite)
    cur = conn.execute(sql, params)

    # Retorna em ordem cronologica
    return list(reversed([dict(r) for r in cur.fetchall()]))


def top_produtos(conn: sqlite3.Connection, limite: int = 10,
                  ordem: str = "faturamento") -> list:
    """Top N produtos ordenados por faturamento ou quantidade."""
    coluna_ordem = {
        "faturamento": "faturamento",
        "quantidade": "unidades_vendidas",
    }.get(ordem, "faturamento")

    sql = f"""
        SELECT p.id, p.nome as produto_nome, p.codigo_barras,
               c.nome as categoria,
               SUM(iv.quantidade) as unidades_vendidas,
               ROUND(SUM(iv.subtotal), 2) as faturamento
        FROM itens_venda iv
        JOIN vendas v ON v.id = iv.venda_id
        JOIN produtos p ON p.id = iv.produto_id
        JOIN categorias c ON c.id = p.categoria_id
        WHERE v.status = 'CONCLUIDA'
        GROUP BY p.id, p.nome, p.codigo_barras, c.nome
        ORDER BY {coluna_ordem} DESC
        LIMIT ?
    """
    cur = conn.execute(sql, (limite,))
    return [dict(r) for r in cur.fetchall()]


def top_filiais(conn: sqlite3.Connection, limite: int = 10) -> list:
    """Top N filiais por faturamento."""
    sql = """
        SELECT f.id, f.codigo, f.nome as filial_nome, f.cidade,
               COUNT(DISTINCT v.id) as n_vendas,
               ROUND(SUM(iv.subtotal), 2) as faturamento,
               ROUND(SUM(iv.subtotal) / COUNT(DISTINCT v.id), 2) as ticket_medio
        FROM vendas v
        JOIN itens_venda iv ON iv.venda_id = v.id
        JOIN filiais f ON f.id = v.filial_id
        WHERE v.status = 'CONCLUIDA'
        GROUP BY f.id, f.codigo, f.nome, f.cidade
        ORDER BY faturamento DESC
        LIMIT ?
    """
    cur = conn.execute(sql, (limite,))
    resultados = [dict(r) for r in cur.fetchall()]

    # Adicionar percentual do total
    total = sum(r["faturamento"] for r in resultados)
    if total > 0:
        for i, r in enumerate(resultados, 1):
            r["ranking"] = i
            r["percentual_do_total"] = round(r["faturamento"] / total * 100, 2)

    return resultados


def faturamento_por_categoria(conn: sqlite3.Connection) -> list:
    """Faturamento e margem por categoria."""
    sql = """
        SELECT c.id, c.nome as categoria,
               COUNT(DISTINCT p.id) as n_produtos,
               SUM(iv.quantidade) as unidades_vendidas,
               ROUND(SUM(iv.subtotal), 2) as faturamento,
               ROUND(SUM(iv.quantidade * (p.preco_venda - p.preco_custo)), 2) as margem
        FROM itens_venda iv
        JOIN vendas v ON v.id = iv.venda_id
        JOIN produtos p ON p.id = iv.produto_id
        JOIN categorias c ON c.id = p.categoria_id
        WHERE v.status = 'CONCLUIDA'
        GROUP BY c.id, c.nome
        ORDER BY faturamento DESC
    """
    cur = conn.execute(sql)
    resultados = [dict(r) for r in cur.fetchall()]

    total = sum(r["faturamento"] for r in resultados)
    for r in resultados:
        r["percentual_do_total"] = round(r["faturamento"] / total * 100, 2) if total else 0
        r["margem_percentual"] = round(r["margem"] / r["faturamento"] * 100, 2) if r["faturamento"] else 0

    return resultados


def vendas_por_forma_pagamento(conn: sqlite3.Connection) -> list:
    """Distribuicao de vendas por forma de pagamento."""
    sql = """
        SELECT forma_pagamento,
               COUNT(*) as n_vendas,
               ROUND(SUM(valor_total), 2) as faturamento
        FROM vendas
        WHERE status = 'CONCLUIDA'
        GROUP BY forma_pagamento
        ORDER BY faturamento DESC
    """
    cur = conn.execute(sql)
    resultados = [dict(r) for r in cur.fetchall()]

    total = sum(r["faturamento"] for r in resultados)
    for r in resultados:
        r["percentual_do_total"] = round(r["faturamento"] / total * 100, 2) if total else 0

    return resultados
