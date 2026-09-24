"""app/routes/vendas.py — Vendas com criacao transacional de itens."""

import sqlite3
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app

from app.database import obter_conexao
from app.errors import NaoEncontradoError, ValidacaoError, ConflitoError
from app.schemas.venda import serializar_venda, validar_payload_venda


bp = Blueprint("vendas", __name__, url_prefix="/api/vendas")


@bp.route("", methods=["GET"])
def listar_vendas():
    """Lista vendas com filtros.

    Query params:
        filial_id (int)
        cliente_id (int)
        status (str) — CONCLUIDA / CANCELADA / PENDENTE
        data_inicio (YYYY-MM-DD)
        data_fim (YYYY-MM-DD)
        pagina, por_pagina
    """
    cfg = current_app.config["PHARMA_CONFIG"]

    where = []
    params = []

    filial_id = request.args.get("filial_id")
    if filial_id:
        try:
            where.append("v.filial_id = ?")
            params.append(int(filial_id))
        except ValueError:
            raise ValidacaoError({"filial_id": "deve ser inteiro"})

    cliente_id = request.args.get("cliente_id")
    if cliente_id:
        try:
            where.append("v.cliente_id = ?")
            params.append(int(cliente_id))
        except ValueError:
            raise ValidacaoError({"cliente_id": "deve ser inteiro"})

    status = request.args.get("status")
    if status:
        where.append("v.status = ?")
        params.append(status.upper())

    data_inicio = request.args.get("data_inicio")
    if data_inicio:
        where.append("v.data_venda >= ?")
        params.append(data_inicio)

    data_fim = request.args.get("data_fim")
    if data_fim:
        where.append("v.data_venda <= ?")
        params.append(data_fim + " 23:59:59")

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

    cur = conn.execute(f"SELECT COUNT(*) FROM vendas v {where_sql}", params)
    total = cur.fetchone()[0]

    offset = (pagina - 1) * por_pagina
    # Join basico para trazer nome da filial e cliente
    sql = f"""
        SELECT v.*, f.nome as filial_nome, c.nome as cliente_nome
        FROM vendas v
        LEFT JOIN filiais f ON f.id = v.filial_id
        LEFT JOIN clientes c ON c.id = v.cliente_id
        {where_sql}
        ORDER BY v.data_venda DESC
        LIMIT ? OFFSET ?
    """
    cur = conn.execute(sql, params + [por_pagina, offset])
    rows = cur.fetchall()

    return jsonify({
        "dados": [dict(r) for r in rows],
        "paginacao": {
            "pagina": pagina,
            "por_pagina": por_pagina,
            "total": total,
            "total_paginas": (total + por_pagina - 1) // por_pagina,
        },
    })


@bp.route("/<int:id_venda>", methods=["GET"])
def buscar_venda(id_venda):
    """Busca venda por ID (com itens aninhados)."""
    conn = obter_conexao()

    cur = conn.execute("""
        SELECT v.*, f.nome as filial_nome, c.nome as cliente_nome
        FROM vendas v
        LEFT JOIN filiais f ON f.id = v.filial_id
        LEFT JOIN clientes c ON c.id = v.cliente_id
        WHERE v.id = ?
    """, (id_venda,))
    row = cur.fetchone()
    if row is None:
        raise NaoEncontradoError("venda", id_venda)

    # Itens da venda
    cur = conn.execute("""
        SELECT iv.*, p.nome as produto_nome, p.codigo_barras
        FROM itens_venda iv
        JOIN produtos p ON p.id = iv.produto_id
        WHERE iv.venda_id = ?
        ORDER BY iv.id
    """, (id_venda,))
    itens = cur.fetchall()

    resultado = dict(row)
    resultado["itens"] = [dict(i) for i in itens]

    return jsonify(resultado)


@bp.route("", methods=["POST"])
def criar_venda():
    """Cria uma venda com N itens em uma transacao atomica.

    Payload:
        {
          "filial_id": 1,
          "cliente_id": 5,       // opcional
          "forma_pagamento": "PIX",
          "desconto": 0.0,       // opcional
          "itens": [
            {"produto_id": 10, "quantidade": 2, "preco_unitario": 15.90},
            ...
          ]
        }

    O preco_unitario pode ser omitido — sera puxado da tabela produtos.
    """
    payload = request.get_json(silent=True)
    if payload is None:
        raise ValidacaoError({"body": "corpo JSON invalido ou ausente"})

    erros = validar_payload_venda(payload, criacao=True)
    if erros:
        raise ValidacaoError(erros)

    conn = obter_conexao()

    # Verificar existencia de filial e cliente
    cur = conn.execute("SELECT id FROM filiais WHERE id = ?", (payload["filial_id"],))
    if cur.fetchone() is None:
        raise ValidacaoError({"filial_id": f"filial {payload['filial_id']} nao existe"})

    if payload.get("cliente_id") is not None:
        cur = conn.execute("SELECT id FROM clientes WHERE id = ?", (payload["cliente_id"],))
        if cur.fetchone() is None:
            raise ValidacaoError({
                "cliente_id": f"cliente {payload['cliente_id']} nao existe"
            })

    # Buscar precos dos produtos (para calcular subtotal)
    produto_ids = [int(i["produto_id"]) for i in payload["itens"]]
    placeholders = ", ".join("?" * len(produto_ids))
    cur = conn.execute(
        f"SELECT id, preco_venda FROM produtos WHERE id IN ({placeholders})",
        produto_ids
    )
    precos = {r["id"]: r["preco_venda"] for r in cur.fetchall()}

    # Verificar que todos os produtos existem
    faltantes = [pid for pid in produto_ids if pid not in precos]
    if faltantes:
        raise ValidacaoError({
            "itens": f"produtos nao encontrados: {faltantes}"
        })

    # Calcular subtotais e valor total
    itens_processados = []
    valor_total = 0.0
    for item in payload["itens"]:
        pid = int(item["produto_id"])
        qty = int(item["quantidade"])
        preco = float(item.get("preco_unitario") or precos[pid])
        subtotal = round(preco * qty, 2)
        itens_processados.append({
            "produto_id": pid,
            "quantidade": qty,
            "preco_unitario": preco,
            "subtotal": subtotal,
        })
        valor_total += subtotal

    valor_total = round(valor_total, 2)
    desconto = round(float(payload.get("desconto", 0)), 2)
    status = payload.get("status", "CONCLUIDA").upper()
    forma = payload["forma_pagamento"].upper()
    data_venda = payload.get("data_venda") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # INSERT venda + itens em transacao
    try:
        cur = conn.execute(
            """INSERT INTO vendas (filial_id, cliente_id, data_venda,
                                     valor_total, desconto, forma_pagamento, status)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (payload["filial_id"], payload.get("cliente_id"), data_venda,
             valor_total, desconto, forma, status),
        )
        nova_venda_id = cur.lastrowid

        for item in itens_processados:
            conn.execute(
                """INSERT INTO itens_venda (venda_id, produto_id, quantidade,
                                              preco_unitario, subtotal)
                   VALUES (?, ?, ?, ?, ?)""",
                (nova_venda_id, item["produto_id"], item["quantidade"],
                 item["preco_unitario"], item["subtotal"])
            )

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise ConflitoError(f"erro ao gravar venda: {e}")

    # Retornar a venda criada (com itens) - reusando a query de busca
    cur = conn.execute("""
        SELECT v.*, f.nome as filial_nome, c.nome as cliente_nome
        FROM vendas v
        LEFT JOIN filiais f ON f.id = v.filial_id
        LEFT JOIN clientes c ON c.id = v.cliente_id
        WHERE v.id = ?
    """, (nova_venda_id,))
    venda_criada = dict(cur.fetchone())

    cur = conn.execute("""
        SELECT iv.*, p.nome as produto_nome, p.codigo_barras
        FROM itens_venda iv
        JOIN produtos p ON p.id = iv.produto_id
        WHERE iv.venda_id = ?
        ORDER BY iv.id
    """, (nova_venda_id,))
    venda_criada["itens"] = [dict(i) for i in cur.fetchall()]

    return jsonify(venda_criada), 201


@bp.route("/<int:id_venda>/cancelar", methods=["POST"])
def cancelar_venda(id_venda):
    """Cancela uma venda (soft cancel: muda status)."""
    conn = obter_conexao()
    cur = conn.execute("SELECT * FROM vendas WHERE id = ?", (id_venda,))
    row = cur.fetchone()
    if row is None:
        raise NaoEncontradoError("venda", id_venda)

    if row["status"] == "CANCELADA":
        raise ConflitoError("venda ja esta cancelada")

    conn.execute(
        "UPDATE vendas SET status = 'CANCELADA' WHERE id = ?", (id_venda,)
    )
    conn.commit()

    return jsonify({
        "id": id_venda,
        "status": "CANCELADA",
        "mensagem": "venda cancelada com sucesso",
    })
