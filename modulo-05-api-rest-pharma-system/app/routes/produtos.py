"""app/routes/produtos.py — CRUD de Produtos com filtros avancados."""

import sqlite3
from flask import Blueprint, request, jsonify, current_app

from app.database import obter_conexao
from app.errors import NaoEncontradoError, ValidacaoError, ConflitoError
from app.schemas.produto import serializar_produto, validar_payload_produto


bp = Blueprint("produtos", __name__, url_prefix="/api/produtos")


@bp.route("", methods=["GET"])
def listar_produtos():
    """Lista produtos com filtros e paginacao.

    Query params:
        categoria_id (int) — filtra por categoria
        fabricante (str)   — filtra por fabricante (LIKE)
        nome (str)         — busca por nome (LIKE)
        preco_min (float)  — preco minimo
        preco_max (float)  — preco maximo
        exige_receita (bool)
        ativo (bool)       — default true
        pagina, por_pagina
    """
    cfg = current_app.config["PHARMA_CONFIG"]

    where = []
    params = []

    cat_id = request.args.get("categoria_id")
    if cat_id:
        try:
            where.append("categoria_id = ?")
            params.append(int(cat_id))
        except ValueError:
            raise ValidacaoError({"categoria_id": "deve ser inteiro"})

    fabricante = request.args.get("fabricante")
    if fabricante:
        where.append("fabricante LIKE ?")
        params.append(f"%{fabricante}%")

    nome = request.args.get("nome")
    if nome:
        where.append("nome LIKE ?")
        params.append(f"%{nome}%")

    preco_min = request.args.get("preco_min")
    if preco_min:
        try:
            where.append("preco_venda >= ?")
            params.append(float(preco_min))
        except ValueError:
            raise ValidacaoError({"preco_min": "deve ser numerico"})

    preco_max = request.args.get("preco_max")
    if preco_max:
        try:
            where.append("preco_venda <= ?")
            params.append(float(preco_max))
        except ValueError:
            raise ValidacaoError({"preco_max": "deve ser numerico"})

    exige_receita = request.args.get("exige_receita")
    if exige_receita is not None:
        val = 1 if exige_receita.lower() in ("true", "1", "sim") else 0
        where.append("exige_receita = ?")
        params.append(val)

    ativo = request.args.get("ativo")
    if ativo is not None:
        val = 1 if ativo.lower() in ("true", "1", "sim") else 0
        where.append("ativo = ?")
        params.append(val)

    try:
        pagina = max(1, int(request.args.get("pagina", 1)))
        por_pagina = min(
            cfg.LIMITE_MAXIMO_PAGINA,
            max(1, int(request.args.get("por_pagina", cfg.LIMITE_PADRAO_PAGINA)))
        )
    except ValueError:
        raise ValidacaoError({"paginacao": "pagina e por_pagina devem ser inteiros"})

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    conn = obter_conexao()

    cur = conn.execute(f"SELECT COUNT(*) FROM produtos {where_sql}", params)
    total = cur.fetchone()[0]

    offset = (pagina - 1) * por_pagina
    cur = conn.execute(
        f"SELECT * FROM produtos {where_sql} ORDER BY id LIMIT ? OFFSET ?",
        params + [por_pagina, offset]
    )
    rows = cur.fetchall()

    return jsonify({
        "dados": [serializar_produto(r) for r in rows],
        "paginacao": {
            "pagina": pagina,
            "por_pagina": por_pagina,
            "total": total,
            "total_paginas": (total + por_pagina - 1) // por_pagina,
        },
    })


@bp.route("/<int:id_prod>", methods=["GET"])
def buscar_produto(id_prod):
    """Busca produto por ID (com informacoes de estoque agregadas)."""
    conn = obter_conexao()
    cur = conn.execute("SELECT * FROM produtos WHERE id = ?", (id_prod,))
    row = cur.fetchone()
    if row is None:
        raise NaoEncontradoError("produto", id_prod)

    d = serializar_produto(row)

    # Estoque total agregado
    cur = conn.execute(
        "SELECT COALESCE(SUM(quantidade), 0) FROM estoque WHERE produto_id = ?",
        (id_prod,)
    )
    d["estoque_total"] = cur.fetchone()[0]

    # Numero de filiais com estoque > 0
    cur = conn.execute(
        "SELECT COUNT(*) FROM estoque WHERE produto_id = ? AND quantidade > 0",
        (id_prod,)
    )
    d["filiais_com_estoque"] = cur.fetchone()[0]

    return jsonify(d)


@bp.route("", methods=["POST"])
def criar_produto():
    """Cria um novo produto."""
    payload = request.get_json(silent=True)
    if payload is None:
        raise ValidacaoError({"body": "corpo JSON invalido ou ausente"})

    erros = validar_payload_produto(payload, criacao=True)
    if erros:
        raise ValidacaoError(erros)

    conn = obter_conexao()

    # Verifica se categoria existe
    cur = conn.execute("SELECT id FROM categorias WHERE id = ?", (payload["categoria_id"],))
    if cur.fetchone() is None:
        raise ValidacaoError({"categoria_id": f"categoria {payload['categoria_id']} nao existe"})

    try:
        cur = conn.execute(
            """INSERT INTO produtos (codigo_barras, nome, categoria_id, fabricante,
                                       preco_custo, preco_venda, estoque_minimo,
                                       exige_receita, ativo)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                payload["codigo_barras"], payload["nome"],
                int(payload["categoria_id"]), payload.get("fabricante"),
                float(payload["preco_custo"]), float(payload["preco_venda"]),
                int(payload.get("estoque_minimo", 0)),
                1 if payload.get("exige_receita", False) else 0,
                1 if payload.get("ativo", True) else 0,
            ),
        )
        conn.commit()
        nova_id = cur.lastrowid
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE" in str(e):
            raise ConflitoError(
                f"codigo de barras '{payload['codigo_barras']}' ja existe",
                {"codigo_barras": payload["codigo_barras"]}
            )
        raise

    cur = conn.execute("SELECT * FROM produtos WHERE id = ?", (nova_id,))
    return jsonify(serializar_produto(cur.fetchone())), 201


@bp.route("/<int:id_prod>", methods=["PUT"])
def atualizar_produto(id_prod):
    """Atualiza um produto."""
    payload = request.get_json(silent=True)
    if payload is None:
        raise ValidacaoError({"body": "corpo JSON invalido ou ausente"})

    conn = obter_conexao()
    cur = conn.execute("SELECT * FROM produtos WHERE id = ?", (id_prod,))
    atual = cur.fetchone()
    if atual is None:
        raise NaoEncontradoError("produto", id_prod)

    erros = validar_payload_produto(payload, criacao=False)
    if erros:
        raise ValidacaoError(erros)

    # Se mudou categoria, valida
    if "categoria_id" in payload:
        cur = conn.execute(
            "SELECT id FROM categorias WHERE id = ?", (payload["categoria_id"],)
        )
        if cur.fetchone() is None:
            raise ValidacaoError({
                "categoria_id": f"categoria {payload['categoria_id']} nao existe"
            })

    campos = ["codigo_barras", "nome", "categoria_id", "fabricante",
              "preco_custo", "preco_venda", "estoque_minimo",
              "exige_receita", "ativo"]
    novos = {c: payload.get(c, atual[c]) for c in campos}
    if "exige_receita" in payload:
        novos["exige_receita"] = 1 if payload["exige_receita"] else 0
    if "ativo" in payload:
        novos["ativo"] = 1 if payload["ativo"] else 0

    try:
        conn.execute(
            """UPDATE produtos SET codigo_barras=?, nome=?, categoria_id=?,
                                     fabricante=?, preco_custo=?, preco_venda=?,
                                     estoque_minimo=?, exige_receita=?, ativo=?
               WHERE id = ?""",
            (
                novos["codigo_barras"], novos["nome"], int(novos["categoria_id"]),
                novos["fabricante"], float(novos["preco_custo"]),
                float(novos["preco_venda"]), int(novos["estoque_minimo"]),
                novos["exige_receita"], novos["ativo"], id_prod,
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE" in str(e):
            raise ConflitoError(f"codigo de barras ja existe")
        raise

    cur = conn.execute("SELECT * FROM produtos WHERE id = ?", (id_prod,))
    return jsonify(serializar_produto(cur.fetchone()))


@bp.route("/<int:id_prod>", methods=["DELETE"])
def deletar_produto(id_prod):
    """Deleta produto se nao tiver vendas ou estoque."""
    conn = obter_conexao()
    cur = conn.execute("SELECT id FROM produtos WHERE id = ?", (id_prod,))
    if cur.fetchone() is None:
        raise NaoEncontradoError("produto", id_prod)

    cur = conn.execute(
        "SELECT COUNT(*) FROM itens_venda WHERE produto_id = ?", (id_prod,)
    )
    n_vendas = cur.fetchone()[0]
    if n_vendas > 0:
        raise ConflitoError(
            f"produto tem {n_vendas} itens de venda associados. "
            "Considere marcar como inativo (ativo=false).",
            {"itens_venda_associados": n_vendas}
        )

    # Remove estoque
    conn.execute("DELETE FROM estoque WHERE produto_id = ?", (id_prod,))
    conn.execute("DELETE FROM produtos WHERE id = ?", (id_prod,))
    conn.commit()
    return "", 204
