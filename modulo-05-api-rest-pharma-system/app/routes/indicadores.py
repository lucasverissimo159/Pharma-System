"""app/routes/indicadores.py — Endpoints de indicadores agregados."""

from flask import Blueprint, request, jsonify

from app.database import obter_conexao
from app.errors import ValidacaoError
from app.services import indicadores as srv


bp = Blueprint("indicadores", __name__, url_prefix="/api/indicadores")


@bp.route("/kpis-gerais", methods=["GET"])
def kpis_gerais():
    """Retorna os KPIs gerais da rede.

    Nao aceita filtros — sempre traz o snapshot global.
    """
    conn = obter_conexao()
    return jsonify(srv.kpis_gerais(conn))


@bp.route("/faturamento-mensal", methods=["GET"])
def faturamento_mensal():
    """Faturamento agregado por mes.

    Query params:
        ano (int)     — filtra por ano
        limite (int)  — N ultimos meses (default 24, max 60)
    """
    conn = obter_conexao()

    ano = request.args.get("ano")
    if ano:
        try:
            ano = int(ano)
        except ValueError:
            raise ValidacaoError({"ano": "deve ser inteiro (ex: 2026)"})

    try:
        limite = min(60, max(1, int(request.args.get("limite", 24))))
    except ValueError:
        raise ValidacaoError({"limite": "deve ser inteiro entre 1 e 60"})

    dados = srv.faturamento_mensal(conn, ano=ano, limite=limite)
    return jsonify({
        "dados": dados,
        "total_meses": len(dados),
    })


@bp.route("/top-produtos", methods=["GET"])
def top_produtos():
    """Top N produtos.

    Query params:
        limite (int)  — default 10, max 50
        ordem (str)   — 'faturamento' (default) ou 'quantidade'
    """
    conn = obter_conexao()

    try:
        limite = min(50, max(1, int(request.args.get("limite", 10))))
    except ValueError:
        raise ValidacaoError({"limite": "deve ser inteiro entre 1 e 50"})

    ordem = request.args.get("ordem", "faturamento").lower()
    if ordem not in ("faturamento", "quantidade"):
        raise ValidacaoError({
            "ordem": "deve ser 'faturamento' ou 'quantidade'"
        })

    dados = srv.top_produtos(conn, limite=limite, ordem=ordem)
    return jsonify({
        "dados": dados,
        "total": len(dados),
        "ordem": ordem,
    })


@bp.route("/top-filiais", methods=["GET"])
def top_filiais():
    """Top N filiais por faturamento.

    Query params:
        limite (int) — default 10, max 50
    """
    conn = obter_conexao()

    try:
        limite = min(50, max(1, int(request.args.get("limite", 10))))
    except ValueError:
        raise ValidacaoError({"limite": "deve ser inteiro entre 1 e 50"})

    dados = srv.top_filiais(conn, limite=limite)
    return jsonify({
        "dados": dados,
        "total": len(dados),
    })


@bp.route("/faturamento-por-categoria", methods=["GET"])
def faturamento_por_categoria():
    """Faturamento e margem por categoria de produto."""
    conn = obter_conexao()
    dados = srv.faturamento_por_categoria(conn)
    return jsonify({
        "dados": dados,
        "total_categorias": len(dados),
    })


@bp.route("/formas-pagamento", methods=["GET"])
def formas_pagamento():
    """Distribuicao de vendas por forma de pagamento."""
    conn = obter_conexao()
    dados = srv.vendas_por_forma_pagamento(conn)
    return jsonify({
        "dados": dados,
    })
