"""app/schemas/filial.py — serializacao e validacao de Filial."""

from app.database import row_para_dict
from app.validators import (
    validar_campos_obrigatorios, validar_data_iso, validar_uf,
)


def serializar_filial(row) -> dict:
    """Converte linha da tabela filiais em dict JSON-friendly."""
    d = row_para_dict(row)
    if d is None:
        return None
    # Converter INTEGER (0/1) em bool
    d["ativa"] = bool(d.get("ativa", 0))
    return d


def validar_payload_filial(payload: dict, criacao: bool = True) -> dict:
    """Valida payload de POST/PUT de filial.

    Args:
        payload: dict recebido no body.
        criacao: True para POST (valida obrigatorios), False para PUT.

    Retorna dict {campo: erro}. Vazio se OK.
    """
    if not isinstance(payload, dict):
        return {"body": "esperado objeto JSON"}

    erros = {}

    if criacao:
        obrigatorios = ["codigo", "nome", "cidade", "estado"]
        erros.update(validar_campos_obrigatorios(payload, obrigatorios))

    # Codigo
    if "codigo" in payload and payload["codigo"] is not None:
        cod = str(payload["codigo"]).strip()
        if not cod:
            erros["codigo"] = "nao pode ser vazio"
        elif len(cod) > 10:
            erros["codigo"] = "maximo 10 caracteres"

    # Nome
    if "nome" in payload and payload["nome"] is not None:
        nome = str(payload["nome"]).strip()
        if not nome:
            erros["nome"] = "nao pode ser vazio"
        elif len(nome) < 3:
            erros["nome"] = "minimo 3 caracteres"

    # Estado (UF)
    if "estado" in payload and payload["estado"] is not None:
        erro_uf = validar_uf(payload["estado"])
        if erro_uf:
            erros["estado"] = erro_uf

    # Data de abertura (opcional)
    if "data_abertura" in payload and payload["data_abertura"]:
        erro_data = validar_data_iso(payload["data_abertura"])
        if erro_data:
            erros["data_abertura"] = erro_data

    return erros
