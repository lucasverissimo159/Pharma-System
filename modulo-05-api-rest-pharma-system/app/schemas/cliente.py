"""app/schemas/cliente.py"""

from app.database import row_para_dict
from app.validators import (
    validar_campos_obrigatorios, validar_cpf, validar_email,
    validar_data_iso, validar_uf,
)


def serializar_cliente(row) -> dict:
    return row_para_dict(row)


def validar_payload_cliente(payload: dict, criacao: bool = True) -> dict:
    if not isinstance(payload, dict):
        return {"body": "esperado objeto JSON"}

    erros = {}

    if criacao:
        erros.update(validar_campos_obrigatorios(payload, ["nome"]))

    if "nome" in payload and payload["nome"] is not None:
        nome = str(payload["nome"]).strip()
        if not nome:
            erros["nome"] = "nao pode ser vazio"
        elif len(nome) < 3:
            erros["nome"] = "minimo 3 caracteres"

    # CPF (opcional mas validado se presente)
    if payload.get("cpf"):
        erro_cpf = validar_cpf(payload["cpf"])
        if erro_cpf:
            erros["cpf"] = erro_cpf

    # Email (opcional mas validado)
    if payload.get("email"):
        erro_email = validar_email(payload["email"])
        if erro_email:
            erros["email"] = erro_email

    # Data de nascimento
    if payload.get("data_nascimento"):
        erro_data = validar_data_iso(payload["data_nascimento"], "%Y-%m-%d")
        if erro_data:
            erros["data_nascimento"] = erro_data

    # Estado
    if payload.get("estado"):
        erro_uf = validar_uf(payload["estado"])
        if erro_uf:
            erros["estado"] = erro_uf

    return erros
