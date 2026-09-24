"""app/schemas/venda.py"""

from app.database import row_para_dict
from app.validators import (
    validar_campos_obrigatorios, validar_forma_pagamento,
    validar_status_venda, validar_positivo,
)


def serializar_venda(row, itens: list = None) -> dict:
    d = row_para_dict(row)
    if d is None:
        return None
    if itens is not None:
        d["itens"] = [row_para_dict(i) for i in itens]
    return d


def validar_payload_venda(payload: dict, criacao: bool = True) -> dict:
    """Valida payload de POST de venda (com itens no body)."""
    if not isinstance(payload, dict):
        return {"body": "esperado objeto JSON"}

    erros = {}

    if criacao:
        obrigatorios = ["filial_id", "forma_pagamento", "itens"]
        erros.update(validar_campos_obrigatorios(payload, obrigatorios))

    # filial_id
    if "filial_id" in payload and payload["filial_id"] is not None:
        try:
            int(payload["filial_id"])
        except (ValueError, TypeError):
            erros["filial_id"] = "deve ser um inteiro"

    # cliente_id (opcional)
    if payload.get("cliente_id") is not None:
        try:
            int(payload["cliente_id"])
        except (ValueError, TypeError):
            erros["cliente_id"] = "deve ser um inteiro"

    # forma_pagamento
    if "forma_pagamento" in payload:
        erro = validar_forma_pagamento(payload["forma_pagamento"])
        if erro:
            erros["forma_pagamento"] = erro

    # status (opcional)
    if payload.get("status"):
        erro = validar_status_venda(payload["status"])
        if erro:
            erros["status"] = erro

    # desconto (opcional, >= 0)
    if "desconto" in payload and payload["desconto"] is not None:
        try:
            v = float(payload["desconto"])
            if v < 0:
                erros["desconto"] = "nao pode ser negativo"
        except (ValueError, TypeError):
            erros["desconto"] = "deve ser numerico"

    # Itens
    itens = payload.get("itens")
    if criacao and (not itens or not isinstance(itens, list)):
        erros["itens"] = "deve ser uma lista com pelo menos 1 item"
    elif itens is not None:
        if not isinstance(itens, list):
            erros["itens"] = "deve ser uma lista"
        elif len(itens) == 0:
            erros["itens"] = "deve ter pelo menos 1 item"
        else:
            erros_itens = {}
            for i, item in enumerate(itens):
                erros_item = _validar_item(item)
                if erros_item:
                    erros_itens[f"item[{i}]"] = erros_item
            if erros_itens:
                erros["itens"] = erros_itens

    return erros


def _validar_item(item: dict) -> dict:
    """Valida um item da venda."""
    if not isinstance(item, dict):
        return {"item": "deve ser um objeto"}

    erros = {}

    for campo in ["produto_id", "quantidade"]:
        if campo not in item or item[campo] is None:
            erros[campo] = "obrigatorio"

    if "produto_id" in item and item["produto_id"] is not None:
        try:
            int(item["produto_id"])
        except (ValueError, TypeError):
            erros["produto_id"] = "deve ser um inteiro"

    if "quantidade" in item and item["quantidade"] is not None:
        try:
            q = int(item["quantidade"])
            if q <= 0:
                erros["quantidade"] = "deve ser positiva"
        except (ValueError, TypeError):
            erros["quantidade"] = "deve ser um inteiro"

    # preco_unitario e opcional (busca do produto se nao fornecido)
    if "preco_unitario" in item and item["preco_unitario"] is not None:
        erro = validar_positivo(item["preco_unitario"], "preco_unitario")
        if erro:
            erros["preco_unitario"] = erro

    return erros
