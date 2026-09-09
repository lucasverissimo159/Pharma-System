"""
analises.py
-----------
Funcoes de agregacao e analise de negocio.

Cada funcao recebe o DataFrame master (denormalizado) e retorna um DataFrame
resumido pronto para exportacao ou plot.
"""

import pandas as pd
import numpy as np
from typing import Dict


# ---------------------------------------------------------------------------
# Filtro base
# ---------------------------------------------------------------------------

def apenas_concluidas(master: pd.DataFrame) -> pd.DataFrame:
    """Filtra apenas vendas com status CONCLUIDA."""
    return master[master["status"] == "CONCLUIDA"].copy()


# ---------------------------------------------------------------------------
# Estatisticas gerais
# ---------------------------------------------------------------------------

def kpis_gerais(master: pd.DataFrame) -> Dict[str, float]:
    """Retorna KPIs de alto nivel para o relatorio executivo."""
    concluidas = apenas_concluidas(master)
    vendas_unicas = concluidas["venda_id"].nunique()

    return {
        "faturamento_total": float(concluidas["subtotal"].sum()),
        "total_vendas": int(vendas_unicas),
        "total_itens_vendidos": int(concluidas["quantidade"].sum()),
        "ticket_medio": float(concluidas.groupby("venda_id")["subtotal"].sum().mean()),
        "margem_bruta_total": float(concluidas["margem_item"].sum()),
        "percentual_margem": float(
            concluidas["margem_item"].sum() / concluidas["subtotal"].sum() * 100
        ),
        "clientes_ativos": int(concluidas["cliente_id"].nunique()),
        "produtos_vendidos_distintos": int(concluidas["produto_id"].nunique()),
        "filiais_ativas": int(concluidas["filial_id"].nunique()),
    }


# ---------------------------------------------------------------------------
# Faturamento por dimensao
# ---------------------------------------------------------------------------

def faturamento_mensal(master: pd.DataFrame) -> pd.DataFrame:
    """Faturamento por ano_mes com contagem de vendas e ticket medio."""
    concluidas = apenas_concluidas(master)
    por_venda = concluidas.groupby(["ano_mes", "venda_id"]).agg(
        valor=("subtotal", "sum")
    ).reset_index()

    resumo = por_venda.groupby("ano_mes").agg(
        faturamento=("valor", "sum"),
        n_vendas=("venda_id", "nunique"),
        ticket_medio=("valor", "mean"),
    ).reset_index().sort_values("ano_mes")

    return resumo


def faturamento_por_filial(master: pd.DataFrame) -> pd.DataFrame:
    """Ranking de filiais por faturamento."""
    concluidas = apenas_concluidas(master)
    por_venda = concluidas.groupby(["filial_nome", "filial_cidade", "venda_id"]).agg(
        valor=("subtotal", "sum")
    ).reset_index()

    resumo = por_venda.groupby(["filial_nome", "filial_cidade"]).agg(
        faturamento=("valor", "sum"),
        n_vendas=("venda_id", "nunique"),
        ticket_medio=("valor", "mean"),
    ).reset_index().sort_values("faturamento", ascending=False)

    total = resumo["faturamento"].sum()
    resumo["percentual_do_total"] = (resumo["faturamento"] / total * 100).round(2)
    resumo["ranking"] = range(1, len(resumo) + 1)

    return resumo


def faturamento_por_categoria(master: pd.DataFrame) -> pd.DataFrame:
    """Faturamento e margem por categoria de produto."""
    concluidas = apenas_concluidas(master)

    resumo = concluidas.groupby("categoria_nome").agg(
        faturamento=("subtotal", "sum"),
        margem=("margem_item", "sum"),
        unidades=("quantidade", "sum"),
        n_produtos=("produto_id", "nunique"),
    ).reset_index()

    resumo["margem_percentual"] = (resumo["margem"] / resumo["faturamento"] * 100).round(2)
    resumo = resumo.sort_values("faturamento", ascending=False)

    total = resumo["faturamento"].sum()
    resumo["percentual_do_total"] = (resumo["faturamento"] / total * 100).round(2)

    return resumo


def faturamento_por_pagamento(master: pd.DataFrame) -> pd.DataFrame:
    """Distribuicao de faturamento por forma de pagamento."""
    concluidas = apenas_concluidas(master)
    por_venda = concluidas.groupby(["forma_pagamento", "venda_id"]).agg(
        valor=("subtotal", "sum")
    ).reset_index()

    resumo = por_venda.groupby("forma_pagamento").agg(
        faturamento=("valor", "sum"),
        n_vendas=("venda_id", "nunique"),
    ).reset_index().sort_values("faturamento", ascending=False)

    total = resumo["faturamento"].sum()
    resumo["percentual_do_total"] = (resumo["faturamento"] / total * 100).round(2)

    return resumo


def vendas_por_dia_semana(master: pd.DataFrame) -> pd.DataFrame:
    """Numero de vendas por dia da semana."""
    concluidas = apenas_concluidas(master)
    ordem = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]

    por_venda = concluidas.groupby(["dia_semana_nome", "venda_id"]).size().reset_index(name="n")
    resumo = por_venda.groupby("dia_semana_nome").agg(
        n_vendas=("venda_id", "nunique"),
    ).reset_index()

    resumo["dia_semana_nome"] = pd.Categorical(
        resumo["dia_semana_nome"], categories=ordem, ordered=True
    )
    resumo = resumo.sort_values("dia_semana_nome").reset_index(drop=True)

    return resumo


# ---------------------------------------------------------------------------
# Ranking de produtos
# ---------------------------------------------------------------------------

def ranking_produtos(master: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Ranking de produtos por faturamento (top N)."""
    concluidas = apenas_concluidas(master)

    resumo = concluidas.groupby(["produto_id", "produto_nome", "categoria_nome"]).agg(
        unidades_vendidas=("quantidade", "sum"),
        faturamento=("subtotal", "sum"),
        margem=("margem_item", "sum"),
    ).reset_index()

    resumo["ticket_medio_item"] = (resumo["faturamento"] / resumo["unidades_vendidas"]).round(2)
    resumo["margem_percentual"] = (resumo["margem"] / resumo["faturamento"] * 100).round(2)
    resumo = resumo.sort_values("faturamento", ascending=False).reset_index(drop=True)
    resumo["ranking"] = resumo.index + 1

    if top_n:
        return resumo.head(top_n)
    return resumo


def concentracao_top_10(master: pd.DataFrame) -> Dict[str, float]:
    """Analise 80/20: qual % do faturamento vem do top 10 produtos."""
    ranking = ranking_produtos(master, top_n=None)
    total = ranking["faturamento"].sum()
    top10 = ranking.head(10)["faturamento"].sum()

    # Encontrar quantos produtos concentram 80% do faturamento
    ranking_ordenado = ranking.sort_values("faturamento", ascending=False).copy()
    ranking_ordenado["acumulado"] = ranking_ordenado["faturamento"].cumsum()
    ranking_ordenado["acumulado_pct"] = ranking_ordenado["acumulado"] / total * 100
    produtos_80 = int((ranking_ordenado["acumulado_pct"] <= 80).sum()) + 1

    return {
        "faturamento_total": float(total),
        "faturamento_top10": float(top10),
        "concentracao_top10_pct": float(top10 / total * 100),
        "produtos_para_80pct": produtos_80,
        "total_produtos_com_venda": int(len(ranking)),
    }


# ---------------------------------------------------------------------------
# Analise de clientes
# ---------------------------------------------------------------------------

def analise_clientes(master: pd.DataFrame) -> pd.DataFrame:
    """Retorna DataFrame de metricas por cliente (RFM basico)."""
    concluidas = apenas_concluidas(master)
    identificados = concluidas[concluidas["cliente_id"].notna()].copy()

    data_ref = identificados["data_venda"].max()

    # Agregar por venda primeiro para nao contar itens em duplicidade
    por_venda = identificados.groupby(["cliente_id", "cliente_nome", "cliente_cidade",
                                        "faixa_etaria", "venda_id"]).agg(
        valor=("subtotal", "sum"),
        data=("data_venda", "first"),
    ).reset_index()

    resumo = por_venda.groupby(["cliente_id", "cliente_nome", "cliente_cidade",
                                 "faixa_etaria"]).agg(
        n_compras=("venda_id", "nunique"),
        ltv=("valor", "sum"),
        ticket_medio=("valor", "mean"),
        primeira_compra=("data", "min"),
        ultima_compra=("data", "max"),
    ).reset_index()

    resumo["dias_desde_ultima"] = (data_ref - resumo["ultima_compra"]).dt.days
    resumo["status"] = resumo["dias_desde_ultima"].apply(
        lambda d: "Ativo" if d <= 90 else "Em risco" if d <= 180 else "Inativo"
    )

    # Quartis de LTV
    resumo["quartil_ltv"] = pd.qcut(
        resumo["ltv"], q=4,
        labels=["Q1 (baixo)", "Q2 (medio-baixo)", "Q3 (medio-alto)", "Q4 (alto)"]
    ).astype("string")

    return resumo.sort_values("ltv", ascending=False).reset_index(drop=True)


def top_clientes(master: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Top clientes por LTV."""
    return analise_clientes(master).head(top_n)


def segmentacao_faixa_etaria(master: pd.DataFrame) -> pd.DataFrame:
    """Distribuicao de faturamento por faixa etaria dos clientes."""
    concluidas = apenas_concluidas(master)
    identificados = concluidas[concluidas["faixa_etaria"].notna()]

    resumo = identificados.groupby("faixa_etaria").agg(
        faturamento=("subtotal", "sum"),
        n_clientes=("cliente_id", "nunique"),
        n_vendas=("venda_id", "nunique"),
    ).reset_index().sort_values("faixa_etaria")

    resumo["ticket_medio"] = (resumo["faturamento"] / resumo["n_vendas"]).round(2)
    total = resumo["faturamento"].sum()
    resumo["percentual"] = (resumo["faturamento"] / total * 100).round(2)

    return resumo


# ---------------------------------------------------------------------------
# Correlacoes
# ---------------------------------------------------------------------------

def matriz_correlacao(master: pd.DataFrame) -> pd.DataFrame:
    """Correlacao entre variaveis numericas relevantes."""
    concluidas = apenas_concluidas(master)

    colunas = ["quantidade", "preco_unitario", "subtotal", "preco_custo",
               "preco_venda", "margem_lucro", "margem_percentual", "margem_item"]

    subset = concluidas[colunas].astype(float)
    return subset.corr()


# ---------------------------------------------------------------------------
# Padrao temporal
# ---------------------------------------------------------------------------

def vendas_por_hora(master: pd.DataFrame) -> pd.DataFrame:
    """Distribuicao de vendas por hora do dia."""
    concluidas = apenas_concluidas(master)
    concluidas = concluidas.copy()
    concluidas["hora"] = concluidas["data_venda"].dt.hour

    por_venda = concluidas.groupby(["hora", "venda_id"]).size().reset_index()

    resumo = por_venda.groupby("hora").agg(
        n_vendas=("venda_id", "nunique"),
    ).reset_index()

    return resumo


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "..")
    from carregamento import carregar_todas_tabelas
    from limpeza import limpar_e_derivar, criar_dataframe_master

    dados = carregar_todas_tabelas("../dados")
    dados_limpos = limpar_e_derivar(dados)
    master = criar_dataframe_master(dados_limpos)

    kpis = kpis_gerais(master)
    print("KPIs Gerais:")
    for k, v in kpis.items():
        print(f"  {k}: {v}")

    print("\nTop 5 Filiais:")
    print(faturamento_por_filial(master).head())
