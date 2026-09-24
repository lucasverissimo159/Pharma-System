"""app/schemas/categoria.py"""

from app.database import row_para_dict
from app.validators import validar_campos_obrigatorios


def serializar_categoria(row) -> dict:
    return row_para_dict(row)


def validar_payload_categoria(payload: dict, criacao: bool = True) -> dict:
    if not isinstance(payload, dict):
        return {"body": "esperado objeto JSON"}

    erros = {}
    if criacao:
        erros.update(validar_campos_obrigatorios(payload, ["nome"]))

    if "nome" in payload and payload["nome"] is not None:
        nome = str(payload["nome"]).strip()
        if not nome:
            erros["nome"] = "nao pode ser vazio"
        elif len(nome) < 2:
            erros["nome"] = "minimo 2 caracteres"

    return erros
