"""app/routes/filiais.py — CRUD de Filiais.

Endpoints:
    GET    /api/filiais        listar (com filtros)
    GET    /api/filiais/<id>   buscar por id
    POST   /api/filiais        criar
    PUT    /api/filiais/<id>   atualizar
    DELETE /api/filiais/<id>   deletar
"""

import sqlite3
from flask import Blueprint, request, jsonify, current_app

from app.database import obter_conexao, rows_para_dicts
from app.errors import NaoEncontradoError, ValidacaoError, ConflitoError
from app.schemas.filial import serializar_filial, validar_payload_filial


bp = Blueprint("filiais", __name__, url_prefix="/api/filiais")


# -----------------------------------------------------------------------------
# GET /api/filiais — listar com filtros e paginacao
# -----------------------------------------------------------------------------

@bp.route("", methods=["GET"])
def listar_filiais():
    """Lista filiais com filtros e paginacao.

    Query params:
        cidade (str)   — filtra por cidade
        estado (str)   — filtra por UF
        ativa (bool)   — filtra ativas (true) ou inativas (false)
        pagina (int)   — pagina, default 1
        por_pagina (int) — itens por pagina, default 20, max 100
    """
    cfg = current_app.config["PHARMA_CONFIG"]

    # Query params
    cidade = request.args.get("cidade")
    estado = request.args.get("estado")
    ativa = request.args.get("ativa")
    try:
        pagina = max(1, int(request.args.get("pagina", 1)))
    except ValueError:
        raise ValidacaoError({"pagina": "deve ser inteiro >= 1"})
    try:
        por_pagina = min(
            cfg.LIMITE_MAXIMO_PAGINA,
            max(1, int(request.args.get("por_pagina", cfg.LIMITE_PADRAO_PAGINA)))
        )
    except ValueError:
        raise ValidacaoError({"por_pagina": "deve ser inteiro entre 1 e 100"})

    # SQL dinamico
    where = []
    params = []
    if cidade:
        where.append("cidade = ?")
        params.append(cidade)
    if estado:
        where.append("estado = ?")
        params.append(estado.upper())
    if ativa is not None:
        val = 1 if ativa.lower() in ("true", "1", "sim") else 0
        where.append("ativa = ?")
        params.append(val)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    conn = obter_conexao()

    # Total (para paginacao)
    cur = conn.execute(
        f"SELECT COUNT(*) FROM filiais {where_sql}", params
    )
    total = cur.fetchone()[0]

    # Pagina de dados
    offset = (pagina - 1) * por_pagina
    cur = conn.execute(
        f"SELECT * FROM filiais {where_sql} ORDER BY id LIMIT ? OFFSET ?",
        params + [por_pagina, offset]
    )
    rows = cur.fetchall()

    return jsonify({
        "dados": [serializar_filial(r) for r in rows],
        "paginacao": {
            "pagina": pagina,
            "por_pagina": por_pagina,
            "total": total,
            "total_paginas": (total + por_pagina - 1) // por_pagina,
        },
    })


# -----------------------------------------------------------------------------
# GET /api/filiais/<id>
# -----------------------------------------------------------------------------

@bp.route("/<int:id_filial>", methods=["GET"])
def buscar_filial(id_filial):
    """Busca filial por ID."""
    conn = obter_conexao()
    cur = conn.execute("SELECT * FROM filiais WHERE id = ?", (id_filial,))
    row = cur.fetchone()
    if row is None:
        raise NaoEncontradoError("filial", id_filial)
    return jsonify(serializar_filial(row))


# -----------------------------------------------------------------------------
# POST /api/filiais
# -----------------------------------------------------------------------------

@bp.route("", methods=["POST"])
def criar_filial():
    """Cria uma nova filial."""
    payload = request.get_json(silent=True)
    if payload is None:
        raise ValidacaoError({"body": "corpo JSON invalido ou ausente"})

    erros = validar_payload_filial(payload, criacao=True)
    if erros:
        raise ValidacaoError(erros)

    conn = obter_conexao()
    try:
        cur = conn.execute(
            """INSERT INTO filiais (codigo, nome, cidade, estado, endereco,
                                     telefone, data_abertura, ativa)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                payload["codigo"], payload["nome"],
                payload["cidade"], payload["estado"].upper(),
                payload.get("endereco"), payload.get("telefone"),
                payload.get("data_abertura"),
                1 if payload.get("ativa", True) else 0,
            ),
        )
        conn.commit()
        nova_id = cur.lastrowid
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE" in str(e):
            raise ConflitoError(
                f"Codigo '{payload['codigo']}' ja existe",
                {"codigo": payload["codigo"]}
            )
        raise

    # Retorna a filial criada
    cur = conn.execute("SELECT * FROM filiais WHERE id = ?", (nova_id,))
    return jsonify(serializar_filial(cur.fetchone())), 201


# -----------------------------------------------------------------------------
# PUT /api/filiais/<id>
# -----------------------------------------------------------------------------

@bp.route("/<int:id_filial>", methods=["PUT"])
def atualizar_filial(id_filial):
    """Atualiza uma filial existente (parcial ou total)."""
    payload = request.get_json(silent=True)
    if payload is None:
        raise ValidacaoError({"body": "corpo JSON invalido ou ausente"})

    conn = obter_conexao()
    cur = conn.execute("SELECT * FROM filiais WHERE id = ?", (id_filial,))
    atual = cur.fetchone()
    if atual is None:
        raise NaoEncontradoError("filial", id_filial)

    erros = validar_payload_filial(payload, criacao=False)
    if erros:
        raise ValidacaoError(erros)

    # Mescla payload com valores atuais (PATCH-style)
    campos = ["codigo", "nome", "cidade", "estado", "endereco",
              "telefone", "data_abertura", "ativa"]
    novos = {c: payload.get(c, atual[c]) for c in campos}
    if novos["estado"]:
        novos["estado"] = str(novos["estado"]).upper()
    if "ativa" in payload:
        novos["ativa"] = 1 if payload["ativa"] else 0

    try:
        conn.execute(
            """UPDATE filiais SET codigo = ?, nome = ?, cidade = ?, estado = ?,
                                    endereco = ?, telefone = ?, data_abertura = ?,
                                    ativa = ?
               WHERE id = ?""",
            (
                novos["codigo"], novos["nome"], novos["cidade"], novos["estado"],
                novos["endereco"], novos["telefone"], novos["data_abertura"],
                novos["ativa"], id_filial,
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE" in str(e):
            raise ConflitoError(f"Codigo '{novos['codigo']}' ja existe")
        raise

    cur = conn.execute("SELECT * FROM filiais WHERE id = ?", (id_filial,))
    return jsonify(serializar_filial(cur.fetchone()))


# -----------------------------------------------------------------------------
# DELETE /api/filiais/<id>
# -----------------------------------------------------------------------------

@bp.route("/<int:id_filial>", methods=["DELETE"])
def deletar_filial(id_filial):
    """Deleta uma filial. Retorna 204 No Content em caso de sucesso.

    Nota: usa DELETE fisico. Em producao real, faria SOFT DELETE
    (marcar ativa=false) para nao quebrar as FKs em vendas historicas.
    """
    conn = obter_conexao()
    cur = conn.execute("SELECT id FROM filiais WHERE id = ?", (id_filial,))
    if cur.fetchone() is None:
        raise NaoEncontradoError("filial", id_filial)

    # Verifica se ha vendas associadas (nao permitiria delete fisico)
    cur = conn.execute(
        "SELECT COUNT(*) FROM vendas WHERE filial_id = ?", (id_filial,)
    )
    n_vendas = cur.fetchone()[0]
    if n_vendas > 0:
        raise ConflitoError(
            "filial tem vendas associadas — nao pode ser deletada. "
            "Considere desativar (ativa=false) em vez de deletar.",
            {"vendas_associadas": n_vendas}
        )

    conn.execute("DELETE FROM filiais WHERE id = ?", (id_filial,))
    conn.commit()
    return "", 204
