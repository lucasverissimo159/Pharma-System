"""
limpeza.py
----------
Limpa os DataFrames, cria colunas derivadas e faz os merges principais.

Fluxo:
    dados_limpos = limpar_e_derivar(dados_brutos)
    df_master = criar_dataframe_master(dados_limpos)
"""

from typing import Dict
import pandas as pd
import numpy as np


def diagnosticar(df: pd.DataFrame, nome: str) -> pd.DataFrame:
    """Retorna diagnostico de nulos e duplicatas por coluna."""
    return pd.DataFrame({
        "coluna": df.columns,
        "tipo": df.dtypes.astype(str).values,
        "nulos": df.isna().sum().values,
        "pct_nulos": (df.isna().sum() / len(df) * 100).round(2).values,
        "unicos": [df[c].nunique() for c in df.columns],
    })


def limpar_vendas(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa e enriquece a tabela vendas com colunas derivadas."""
    df = df.copy()

    # Coluna valor liquido (valor - desconto)
    df["valor_liquido"] = df["valor_total"] - df["desconto"]

    # Derivar dimensoes de tempo de data_venda
    df["ano"] = df["data_venda"].dt.year.astype("Int64")
    df["mes"] = df["data_venda"].dt.month.astype("Int64")
    df["ano_mes"] = df["data_venda"].dt.strftime("%Y-%m")
    df["dia"] = df["data_venda"].dt.day.astype("Int64")
    df["dia_semana_num"] = df["data_venda"].dt.dayofweek.astype("Int64")

    dias_pt = {0: "Segunda", 1: "Terca", 2: "Quarta", 3: "Quinta",
               4: "Sexta", 5: "Sabado", 6: "Domingo"}
    df["dia_semana_nome"] = df["dia_semana_num"].map(dias_pt).astype("string")
    df["eh_final_de_semana"] = df["dia_semana_num"].isin([5, 6])
    df["hora"] = df["data_venda"].dt.hour.astype("Int64")

    # Flag: venda com cliente identificado?
    df["cliente_identificado"] = df["cliente_id"].notna()

    return df


def limpar_produtos(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona margem de lucro na tabela produtos."""
    df = df.copy()
    df["margem_lucro"] = df["preco_venda"] - df["preco_custo"]
    df["margem_percentual"] = (df["margem_lucro"] / df["preco_venda"] * 100).round(2)
    return df


def limpar_clientes(df: pd.DataFrame, hoje=None) -> pd.DataFrame:
    """Deriva idade e faixa etaria dos clientes."""
    df = df.copy()

    if hoje is None:
        hoje = pd.Timestamp.now().normalize()

    idade_float = (hoje - df["data_nascimento"]).dt.days / 365.25
    df["idade"] = idade_float.round().astype("Int64")

    def faixa(idade):
        if pd.isna(idade):
            return pd.NA
        if idade < 25:
            return "1. Ate 24 anos"
        if idade < 35:
            return "2. 25 a 34"
        if idade < 45:
            return "3. 35 a 44"
        if idade < 60:
            return "4. 45 a 59"
        return "5. 60+ anos"

    df["faixa_etaria"] = df["idade"].apply(faixa).astype("string")

    return df


def limpar_e_derivar(dados: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Aplica limpezas em todas as tabelas relevantes."""
    dados_limpos = {k: v.copy() for k, v in dados.items()}
    dados_limpos["vendas"] = limpar_vendas(dados["vendas"])
    dados_limpos["produtos"] = limpar_produtos(dados["produtos"])
    dados_limpos["clientes"] = limpar_clientes(dados["clientes"])
    return dados_limpos


def criar_dataframe_master(dados: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Faz merge itens_venda + vendas + produtos + categorias + filiais + clientes.

    Retorna um DataFrame "denormalizado" com todas as informacoes por linha de item.
    Util para agregacoes complexas em uma unica consulta.
    """
    # Comeco por itens_venda (linha por item)
    df = dados["itens_venda"].copy()

    # + vendas
    df = df.merge(
        dados["vendas"][["id", "filial_id", "cliente_id", "data_venda",
                         "forma_pagamento", "status", "ano_mes", "dia_semana_nome",
                         "eh_final_de_semana", "ano", "mes"]],
        left_on="venda_id",
        right_on="id",
        suffixes=("_item", "_venda"),
    ).drop(columns=["id_venda"]).rename(columns={"id_item": "item_id"})

    # + produtos (com margem)
    df = df.merge(
        dados["produtos"][["id", "nome", "categoria_id", "fabricante",
                           "preco_custo", "preco_venda", "margem_lucro",
                           "margem_percentual", "exige_receita"]],
        left_on="produto_id",
        right_on="id",
        suffixes=("", "_produto"),
    ).drop(columns=["id"]).rename(columns={
        "nome": "produto_nome",
        "fabricante": "produto_fabricante",
    })

    # + categorias
    df = df.merge(
        dados["categorias"][["id", "nome"]].rename(columns={"nome": "categoria_nome"}),
        left_on="categoria_id",
        right_on="id",
    ).drop(columns=["id"])

    # + filiais
    df = df.merge(
        dados["filiais"][["id", "nome", "cidade", "estado"]].rename(columns={
            "nome": "filial_nome",
            "cidade": "filial_cidade",
            "estado": "filial_estado",
        }),
        left_on="filial_id",
        right_on="id",
    ).drop(columns=["id"])

    # + clientes (LEFT — pode ter venda sem cliente)
    df = df.merge(
        dados["clientes"][["id", "nome", "cidade", "estado", "idade", "faixa_etaria"]].rename(columns={
            "nome": "cliente_nome",
            "cidade": "cliente_cidade",
            "estado": "cliente_estado",
            "idade": "cliente_idade",
        }),
        left_on="cliente_id",
        right_on="id",
        how="left",
    ).drop(columns=["id"])

    # Margem de cada item vendido
    df["margem_item"] = df["margem_lucro"] * df["quantidade"]

    return df


if __name__ == "__main__":
    from carregamento import carregar_todas_tabelas
    dados = carregar_todas_tabelas("../dados")
    dados_limpos = limpar_e_derivar(dados)
    master = criar_dataframe_master(dados_limpos)
    print(f"Master: {master.shape[0]} linhas x {master.shape[1]} colunas")
    print(f"Colunas: {master.columns.tolist()}")
