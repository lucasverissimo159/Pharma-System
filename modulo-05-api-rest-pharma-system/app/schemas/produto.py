"""app/schemas/produto.py"""

from app.database import row_para_dict
from app.validators import (
    validar_campos_obrigatorios, validar_positivo, validar_nao_negativo,
)


def serializar_produto(row) -> dict:
    d = row_para_dict(row)
    if d is None:
        return None
    d["exige_receita"] = bool(d.get("exige_receita", 0))
    d["ativo"] = bool(d.get("ativo", 1))
    # Adiciona margem calculada
    if d.get("preco_custo") is not None and d.get("preco_venda"):
        d["margem_lucro"] = round(d["preco_venda"] - d["preco_custo"], 2)
        d["margem_percentual"] = round(
            (d["preco_venda"] - d["preco_custo"]) / d["preco_venda"] * 100, 2
        )
    return d


def validar_payload_produto(payload: dict, criacao: bool = True) -> dict:
    if not isinstance(payload, dict):
        return {"body": "esperado objeto JSON"}

    erros = {}

    if criacao:
        obrigatorios = ["codigo_barras", "nome", "categoria_id",
                        "preco_custo", "preco_venda"]
        erros.update(validar_campos_obrigatorios(payload, obrigatorios))

    if "nome" in payload and payload["nome"] is not None:
        nome = str(payload["nome"]).strip()
        if not nome:
            erros["nome"] = "nao pode ser vazio"

    if "codigo_barras" in payload and payload["codigo_barras"] is not None:
        cb = str(payload["codigo_barras"]).strip()
        if not cb.isdigit():
            erros["codigo_barras"] = "deve conter apenas digitos"
        elif len(cb) < 8:
            erros["codigo_barras"] = "minimo 8 digitos"

    if "preco_custo" in payload and payload["preco_custo"] is not None:
        erro = validar_nao_negativo(payload["preco_custo"], "preco_custo")
        if erro:
            erros["preco_custo"] = erro

    if "preco_venda" in payload and payload["preco_venda"] is not None:
        erro = validar_positivo(payload["preco_venda"], "preco_venda")
        if erro:
            erros["preco_venda"] = erro

    # Validacao cruzada: preco_venda deve ser >= preco_custo
    if "preco_venda" in payload and "preco_custo" in payload:
        try:
            pv = float(payload["preco_venda"])
            pc = float(payload["preco_custo"])
            if pv < pc:
                erros["preco_venda"] = "nao pode ser menor que preco_custo"
        except (ValueError, TypeError):
            pass  # ja capturado nas validacoes individuais

    if "categoria_id" in payload and payload["categoria_id"] is not None:
        try:
            int(payload["categoria_id"])
        except (ValueError, TypeError):
            erros["categoria_id"] = "deve ser um inteiro"

    return erros
