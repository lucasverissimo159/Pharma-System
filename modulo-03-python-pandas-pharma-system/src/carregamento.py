"""
carregamento.py
---------------
Le os CSVs do PharmaSystem em DataFrames com tipos ja corretos.

Uso:
    from src.carregamento import carregar_todas_tabelas
    dados = carregar_todas_tabelas("dados/")
    df_vendas = dados["vendas"]
"""

from pathlib import Path
from typing import Dict
import pandas as pd


# Tipos esperados por tabela — ajuda a evitar surpresas
TIPOS = {
    "filiais": {
        "id": "Int64",
        "codigo": "string",
        "nome": "string",
        "cidade": "string",
        "estado": "string",
        "endereco": "string",
        "telefone": "string",
        "ativa": "string",
    },
    "categorias": {
        "id": "Int64",
        "nome": "string",
        "descricao": "string",
    },
    "produtos": {
        "id": "Int64",
        "codigo_barras": "string",
        "nome": "string",
        "categoria_id": "Int64",
        "fabricante": "string",
        "preco_custo": "float64",
        "preco_venda": "float64",
        "estoque_minimo": "Int64",
        "exige_receita": "string",
        "ativo": "string",
    },
    "estoque": {
        "id": "Int64",
        "produto_id": "Int64",
        "filial_id": "Int64",
        "quantidade": "Int64",
    },
    "clientes": {
        "id": "Int64",
        "nome": "string",
        "cpf": "string",
        "email": "string",
        "telefone": "string",
        "cidade": "string",
        "estado": "string",
    },
    "vendas": {
        "id": "Int64",
        "filial_id": "Int64",
        "cliente_id": "Int64",
        "valor_total": "float64",
        "desconto": "float64",
        "forma_pagamento": "string",
        "status": "string",
    },
    "itens_venda": {
        "id": "Int64",
        "venda_id": "Int64",
        "produto_id": "Int64",
        "quantidade": "Int64",
        "preco_unitario": "float64",
        "subtotal": "float64",
    },
    "calendario": {
        "ano": "Int64",
        "trimestre": "Int64",
        "mes_num": "Int64",
        "mes_nome": "string",
        "ano_mes": "string",
        "dia": "Int64",
        "dia_semana_num": "Int64",
        "dia_semana_nome": "string",
        "eh_final_de_semana": "string",
    },
}

# Colunas de data por tabela — parseadas separadamente
DATAS = {
    "filiais": ["data_abertura"],
    "clientes": ["data_nascimento", "data_cadastro"],
    "vendas": ["data_venda"],
    "calendario": ["data"],
}


def carregar_tabela(caminho_csv: Path, nome: str) -> pd.DataFrame:
    """Le um CSV aplicando os tipos definidos em TIPOS/DATAS."""
    if not caminho_csv.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {caminho_csv}")

    df = pd.read_csv(
        caminho_csv,
        dtype=TIPOS.get(nome, {}),
        parse_dates=DATAS.get(nome, []),
        encoding="utf-8-sig",
    )

    return df


def carregar_todas_tabelas(pasta_dados: str = "dados") -> Dict[str, pd.DataFrame]:
    """Le todas as tabelas do PharmaSystem e retorna dicionario nome->DataFrame."""
    pasta = Path(pasta_dados)

    if not pasta.exists():
        raise FileNotFoundError(f"Pasta de dados nao encontrada: {pasta}")

    tabelas = [
        "filiais", "categorias", "produtos", "estoque",
        "clientes", "vendas", "itens_venda", "calendario",
    ]

    dados = {}
    for nome in tabelas:
        caminho = pasta / f"{nome}.csv"
        dados[nome] = carregar_tabela(caminho, nome)

    return dados


def resumir_tabelas(dados: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Retorna um DataFrame com uma linha por tabela: linhas, colunas, memoria."""
    resumo = []
    for nome, df in dados.items():
        resumo.append({
            "tabela": nome,
            "linhas": len(df),
            "colunas": df.shape[1],
            "memoria_kb": round(df.memory_usage(deep=True).sum() / 1024, 1),
            "colunas_lista": ", ".join(df.columns.tolist()),
        })

    return pd.DataFrame(resumo)


if __name__ == "__main__":
    # Modo diagnostico: rode direto para ver se tudo carrega
    dados = carregar_todas_tabelas("dados")
    print(resumir_tabelas(dados).to_string(index=False))
