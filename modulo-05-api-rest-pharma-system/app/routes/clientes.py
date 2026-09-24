"""app/routes/clientes.py — CRUD de Clientes."""

import sqlite3
from flask import Blueprint, request, jsonify, current_app

from app.database import obter_conexao
from app.errors import NaoEncontradoError, ValidacaoError, ConflitoError
from app.schemas.cliente import serializar_cliente, validar_payload_cliente
from app.validators import somente_digitos


bp = Blueprint("clientes", __name__, url_prefix="/api/clientes")


@bp.route("", methods=["GET"])
def listar_clientes():
    """Lista clientes com filtros e paginacao.

    Query params:
        cidade (str)
        estado (str)
        nome (str)  — busca por nome (LIKE)
        cpf (str)   — busca exata
        pagina, por_pagina
    """
    cfg = current_app.config["PHARMA_CONFIG"]

    where = []
    params = []

    cidade = request.args.get("cidade")
    if cidade:
        where.append("cidade = ?")
        params.append(cidade)

    estado = request.args.get("estado")
    if estado:
        where.append("estado = ?")
        params.append(estado.upper())

    nome = request.args.get("nome")
    if nome:
        where.append("nome LIKE ?")
        params.append(f"%{nome}%")

    cpf = request.args.get("cpf")
    if cpf:
        # Normalizar (aceita com ou sem pontuacao)
        digitos = somente_digitos(cpf)
        where.append("REPLACE(REPLACE(REPLACE(cpf, '.', ''), '-', ''), ' ', '') = ?")
        params.append(digitos)

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

    cur = conn.execute(f"SELECT COUNT(*) FROM clientes {where_sql}", params)
    total = cur.fetchone()[0]

    offset = (pagina - 1) * por_pagina
    cur = conn.execute(
        f"SELECT * FROM clientes {where_sql} ORDER BY id LIMIT ? OFFSET ?",
        params + [por_pagina, offset]
    )
    rows = cur.fetchall()

    return jsonify({
        "dados": [serializar_cliente(r) for r in rows],
        "paginacao": {
            "pagina": pagina,
            "por_pagina": por_pagina,
            "total": total,
            "total_paginas": (total + por_pagina - 1) // por_pagina,
        },
    })


@bp.route("/<int:id_cli>", methods=["GET"])
def buscar_cliente(id_cli):
    """Busca cliente por ID (com resumo de compras)."""
    conn = obter_conexao()
    cur = conn.execute("SELECT * FROM clientes WHERE id = ?", (id_cli,))
    row = cur.fetchone()
    if row is None:
        raise NaoEncontradoError("cliente", id_cli)

    d = serializar_cliente(row)

    # Metricas basicas
    cur = conn.execute(
        """SELECT COUNT(*) as n_compras,
                  COALESCE(ROUND(SUM(valor_total), 2), 0) as valor_total,
                  MAX(data_venda) as ultima_compra
           FROM vendas
           WHERE cliente_id = ? AND status = 'CONCLUIDA'""",
        (id_cli,)
    )
    resumo = cur.fetchone()
    d["n_compras"] = resumo["n_compras"]
    d["valor_total_compras"] = resumo["valor_total"]
    d["ultima_compra"] = resumo["ultima_compra"]

    return jsonify(d)


@bp.route("", methods=["POST"])
def criar_cliente():
    """Cria um novo cliente."""
    payload = request.get_json(silent=True)
    if payload is None:
        raise ValidacaoError({"body": "corpo JSON invalido ou ausente"})

    erros = validar_payload_cliente(payload, criacao=True)
    if erros:
        raise ValidacaoError(erros)

    conn = obter_conexao()

    # Normalizar CPF (guardar so digitos)
    cpf_normalizado = somente_digitos(payload.get("cpf")) if payload.get("cpf") else None

    try:
        cur = conn.execute(
            """INSERT INTO clientes (nome, cpf, email, telefone,
                                       data_nascimento, cidade, estado)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                payload["nome"].strip(), cpf_normalizado,
                payload.get("email"), payload.get("telefone"),
                payload.get("data_nascimento"),
                payload.get("cidade"),
                payload["estado"].upper() if payload.get("estado") else None,
            ),
        )
        conn.commit()
        nova_id = cur.lastrowid
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE" in str(e):
            raise ConflitoError(f"CPF ja cadastrado", {"cpf": payload.get("cpf")})
        raise

    cur = conn.execute("SELECT * FROM clientes WHERE id = ?", (nova_id,))
    return jsonify(serializar_cliente(cur.fetchone())), 201


@bp.route("/<int:id_cli>", methods=["PUT"])
def atualizar_cliente(id_cli):
    """Atualiza cliente."""
    payload = request.get_json(silent=True)
    if payload is None:
        raise ValidacaoError({"body": "corpo JSON invalido ou ausente"})

    conn = obter_conexao()
    cur = conn.execute("SELECT * FROM clientes WHERE id = ?", (id_cli,))
    atual = cur.fetchone()
    if atual is None:
        raise NaoEncontradoError("cliente", id_cli)

    erros = validar_payload_cliente(payload, criacao=False)
    if erros:
        raise ValidacaoError(erros)

    campos = ["nome", "cpf", "email", "telefone", "data_nascimento", "cidade", "estado"]
    novos = {c: payload.get(c, atual[c]) for c in campos}

    # Normalizar CPF se veio no payload
    if "cpf" in payload:
        novos["cpf"] = somente_digitos(payload["cpf"]) if payload["cpf"] else None
    if novos.get("estado"):
        novos["estado"] = str(novos["estado"]).upper()

    try:
        conn.execute(
            """UPDATE clientes SET nome=?, cpf=?, email=?, telefone=?,
                                    data_nascimento=?, cidade=?, estado=?
               WHERE id = ?""",
            (novos["nome"], novos["cpf"], novos["email"], novos["telefone"],
             novos["data_nascimento"], novos["cidade"], novos["estado"], id_cli),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE" in str(e):
            raise ConflitoError(f"CPF ja cadastrado")
        raise

    cur = conn.execute("SELECT * FROM clientes WHERE id = ?", (id_cli,))
    return jsonify(serializar_cliente(cur.fetchone()))


@bp.route("/<int:id_cli>", methods=["DELETE"])
def deletar_cliente(id_cli):
    """Deleta cliente se nao tiver compras."""
    conn = obter_conexao()
    cur = conn.execute("SELECT id FROM clientes WHERE id = ?", (id_cli,))
    if cur.fetchone() is None:
        raise NaoEncontradoError("cliente", id_cli)

    cur = conn.execute(
        "SELECT COUNT(*) FROM vendas WHERE cliente_id = ?", (id_cli,)
    )
    n_vendas = cur.fetchone()[0]
    if n_vendas > 0:
        raise ConflitoError(
            f"cliente tem {n_vendas} compras associadas — nao pode ser deletado",
            {"compras_associadas": n_vendas}
        )

    conn.execute("DELETE FROM clientes WHERE id = ?", (id_cli,))
    conn.commit()
    return "", 204
