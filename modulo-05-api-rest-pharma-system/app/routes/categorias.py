"""app/routes/categorias.py — CRUD de Categorias."""

import sqlite3
from flask import Blueprint, request, jsonify

from app.database import obter_conexao
from app.errors import NaoEncontradoError, ValidacaoError, ConflitoError
from app.schemas.categoria import serializar_categoria, validar_payload_categoria


bp = Blueprint("categorias", __name__, url_prefix="/api/categorias")


@bp.route("", methods=["GET"])
def listar_categorias():
    """Lista todas as categorias (sem paginacao — sao poucas)."""
    conn = obter_conexao()
    cur = conn.execute("SELECT * FROM categorias ORDER BY nome")
    rows = cur.fetchall()
    return jsonify({
        "dados": [serializar_categoria(r) for r in rows],
        "total": len(rows),
    })


@bp.route("/<int:id_cat>", methods=["GET"])
def buscar_categoria(id_cat):
    """Busca categoria por ID, com contagem de produtos associados."""
    conn = obter_conexao()
    cur = conn.execute("SELECT * FROM categorias WHERE id = ?", (id_cat,))
    row = cur.fetchone()
    if row is None:
        raise NaoEncontradoError("categoria", id_cat)

    resultado = serializar_categoria(row)

    # Contagem de produtos
    cur = conn.execute(
        "SELECT COUNT(*) FROM produtos WHERE categoria_id = ?", (id_cat,)
    )
    resultado["total_produtos"] = cur.fetchone()[0]

    return jsonify(resultado)


@bp.route("", methods=["POST"])
def criar_categoria():
    """Cria uma nova categoria."""
    payload = request.get_json(silent=True)
    if payload is None:
        raise ValidacaoError({"body": "corpo JSON invalido ou ausente"})

    erros = validar_payload_categoria(payload, criacao=True)
    if erros:
        raise ValidacaoError(erros)

    conn = obter_conexao()
    try:
        cur = conn.execute(
            "INSERT INTO categorias (nome, descricao) VALUES (?, ?)",
            (payload["nome"].strip(), payload.get("descricao")),
        )
        conn.commit()
        nova_id = cur.lastrowid
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE" in str(e):
            raise ConflitoError(f"Categoria '{payload['nome']}' ja existe")
        raise

    cur = conn.execute("SELECT * FROM categorias WHERE id = ?", (nova_id,))
    return jsonify(serializar_categoria(cur.fetchone())), 201


@bp.route("/<int:id_cat>", methods=["PUT"])
def atualizar_categoria(id_cat):
    """Atualiza categoria."""
    payload = request.get_json(silent=True)
    if payload is None:
        raise ValidacaoError({"body": "corpo JSON invalido ou ausente"})

    conn = obter_conexao()
    cur = conn.execute("SELECT * FROM categorias WHERE id = ?", (id_cat,))
    atual = cur.fetchone()
    if atual is None:
        raise NaoEncontradoError("categoria", id_cat)

    erros = validar_payload_categoria(payload, criacao=False)
    if erros:
        raise ValidacaoError(erros)

    nome = payload.get("nome", atual["nome"])
    descricao = payload.get("descricao", atual["descricao"])

    try:
        conn.execute(
            "UPDATE categorias SET nome = ?, descricao = ? WHERE id = ?",
            (nome, descricao, id_cat),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE" in str(e):
            raise ConflitoError(f"Categoria '{nome}' ja existe")
        raise

    cur = conn.execute("SELECT * FROM categorias WHERE id = ?", (id_cat,))
    return jsonify(serializar_categoria(cur.fetchone()))


@bp.route("/<int:id_cat>", methods=["DELETE"])
def deletar_categoria(id_cat):
    """Deleta categoria (soh se nao tiver produtos)."""
    conn = obter_conexao()
    cur = conn.execute("SELECT id FROM categorias WHERE id = ?", (id_cat,))
    if cur.fetchone() is None:
        raise NaoEncontradoError("categoria", id_cat)

    cur = conn.execute(
        "SELECT COUNT(*) FROM produtos WHERE categoria_id = ?", (id_cat,)
    )
    n_produtos = cur.fetchone()[0]
    if n_produtos > 0:
        raise ConflitoError(
            f"categoria tem {n_produtos} produtos associados — nao pode ser deletada",
            {"produtos_associados": n_produtos}
        )

    conn.execute("DELETE FROM categorias WHERE id = ?", (id_cat,))
    conn.commit()
    return "", 204
