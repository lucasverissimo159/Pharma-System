"""
app/validators.py
-----------------
Validadores reutilizaveis para os schemas.

Cada funcao recebe um valor e retorna:
    - None: se valido
    - str : mensagem de erro se invalido
"""

import re
from datetime import datetime


CPF_REGEX = re.compile(r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
FORMAS_PAGAMENTO_VALIDAS = {"PIX", "DINHEIRO", "DEBITO", "CREDITO", "CONVENIO"}
STATUS_VENDA_VALIDOS = {"CONCLUIDA", "CANCELADA", "PENDENTE"}


def somente_digitos(valor: str) -> str:
    """Remove tudo que nao e digito."""
    if valor is None:
        return None
    return re.sub(r"\D", "", str(valor))


def validar_cpf(valor: str) -> str:
    """Valida formato E digitos verificadores do CPF.

    Retorna None se valido, ou mensagem de erro.
    """
    if valor is None or valor == "":
        return None  # nullable

    if not CPF_REGEX.match(str(valor)):
        return "CPF deve estar no formato XXX.XXX.XXX-XX ou 11 digitos"

    digitos = somente_digitos(valor)

    if len(digitos) != 11:
        return "CPF deve ter 11 digitos"

    # CPFs com todos digitos iguais sao invalidos
    if digitos == digitos[0] * 11:
        return "CPF invalido (digitos repetidos)"

    # Verificador 1
    soma = sum(int(digitos[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10) % 11
    if d1 == 10:
        d1 = 0
    if d1 != int(digitos[9]):
        return "CPF invalido (digito verificador incorreto)"

    # Verificador 2
    soma = sum(int(digitos[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10) % 11
    if d2 == 10:
        d2 = 0
    if d2 != int(digitos[10]):
        return "CPF invalido (digito verificador incorreto)"

    return None


def validar_email(valor: str) -> str:
    """Valida formato basico de email."""
    if valor is None or valor == "":
        return None  # nullable
    if not EMAIL_REGEX.match(str(valor)):
        return "Email invalido"
    return None


def validar_forma_pagamento(valor: str) -> str:
    """Valida se e uma forma de pagamento aceita."""
    if valor is None or valor == "":
        return "Forma de pagamento e obrigatoria"
    if str(valor).upper() not in FORMAS_PAGAMENTO_VALIDAS:
        return (
            f"Forma de pagamento invalida. "
            f"Aceitas: {sorted(FORMAS_PAGAMENTO_VALIDAS)}"
        )
    return None


def validar_status_venda(valor: str) -> str:
    """Valida status da venda."""
    if valor is None or valor == "":
        return None
    if str(valor).upper() not in STATUS_VENDA_VALIDOS:
        return f"Status invalido. Aceitos: {sorted(STATUS_VENDA_VALIDOS)}"
    return None


def validar_data_iso(valor: str, formato: str = None) -> str:
    """Valida se a string e uma data ISO ou no formato dado."""
    if valor is None or valor == "":
        return None
    formatos = [formato] if formato else [
        "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S",
    ]
    for fmt in formatos:
        try:
            datetime.strptime(str(valor), fmt)
            return None
        except ValueError:
            continue
    return f"Data invalida: {valor} (formato esperado: {formatos})"


def validar_positivo(valor, nome_campo: str = "valor") -> str:
    """Valida que o valor e numerico e positivo."""
    if valor is None:
        return f"{nome_campo} e obrigatorio"
    try:
        v = float(valor)
    except (ValueError, TypeError):
        return f"{nome_campo} deve ser numerico"
    if v <= 0:
        return f"{nome_campo} deve ser positivo"
    return None


def validar_nao_negativo(valor, nome_campo: str = "valor") -> str:
    """Valida que o valor e numerico e >= 0."""
    if valor is None:
        return f"{nome_campo} e obrigatorio"
    try:
        v = float(valor)
    except (ValueError, TypeError):
        return f"{nome_campo} deve ser numerico"
    if v < 0:
        return f"{nome_campo} nao pode ser negativo"
    return None


def validar_campos_obrigatorios(payload: dict, campos: list) -> dict:
    """Verifica presenca de campos obrigatorios num payload dict.

    Retorna dict {campo: mensagem} para campos faltando (vazio se todos OK).
    """
    erros = {}
    for c in campos:
        if c not in payload or payload[c] is None or payload[c] == "":
            erros[c] = f"campo obrigatorio"
    return erros


def validar_uf(valor: str) -> str:
    """Valida se e uma UF brasileira valida."""
    if valor is None or valor == "":
        return None
    ufs = {
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO",
    }
    if str(valor).upper() not in ufs:
        return f"UF invalida: {valor}"
    return None
