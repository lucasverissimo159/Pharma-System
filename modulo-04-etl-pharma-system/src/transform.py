"""
transform.py
------------
Camada Transform do ETL: limpa, valida e enriquece os DataFrames vindos do
Extract.

Etapas em ordem:
1. Padroniza nomes de colunas (strip, lower, snake_case)
2. Trata linhas em branco e strings vazias como nulos
3. Converte tipos (numericos, decimais com virgula BR, datas em multiplos formatos)
4. Valida regras de negocio (quantidade > 0, preco > 0, forma_pagamento valida)
5. Remove duplicatas pela chave natural
6. Enriquece com colunas derivadas (valor_total, ano_mes)
7. Retorna DataFrame limpo + relatorio de transformacao
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import numpy as np

from src.logger import obter_logger

log = obter_logger("transform")


@dataclass
class RelatorioTransform:
    """Relatorio de tudo que aconteceu no transform de um arquivo."""
    arquivo: str = ""
    linhas_entrada: int = 0
    linhas_saida: int = 0
    linhas_em_branco_removidas: int = 0
    linhas_com_nulos_criticos_removidas: int = 0
    linhas_com_valores_invalidos_removidas: int = 0
    linhas_duplicadas_removidas: int = 0
    linhas_data_invalida_removidas: int = 0
    warnings: List[str] = field(default_factory=list)

    def resumir(self) -> str:
        removidas = (
            self.linhas_entrada - self.linhas_saida
        )
        return (
            f"{self.linhas_entrada} -> {self.linhas_saida} linhas "
            f"({removidas} removidas: "
            f"branco={self.linhas_em_branco_removidas}, "
            f"nulos={self.linhas_com_nulos_criticos_removidas}, "
            f"invalido={self.linhas_com_valores_invalidos_removidas}, "
            f"duplicata={self.linhas_duplicadas_removidas}, "
            f"data_inv={self.linhas_data_invalida_removidas})"
        )


def _para_snake_case(nome: str) -> str:
    """Converte 'Data Venda' ou 'DataVenda' para 'data_venda'."""
    # CamelCase -> camel_case
    nome = re.sub(r"(?<!^)(?=[A-Z])", "_", nome)
    # Remover acentos comuns manualmente (evita dependencia externa)
    trad = str.maketrans(
        "áàâãäéèêëíìîïóòôõöúùûüçÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇ",
        "aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC"
    )
    nome = nome.translate(trad)
    # Espacos e hifens -> underscore
    nome = re.sub(r"[\s\-]+", "_", nome)
    # Remover caracteres especiais
    nome = re.sub(r"[^a-zA-Z0-9_]", "", nome)
    # Multiplo underscore -> um so
    nome = re.sub(r"_+", "_", nome)
    return nome.strip("_").lower()


class Transformador:
    """Aplica as transformacoes definidas em regras + schema."""

    def __init__(self, schema: dict, regras: dict, chave_natural: List[str]):
        self.schema = schema["vendas_filial"]
        self.regras = regras
        self.chave_natural = chave_natural
        self.formatos_data = regras.get("formatos_data", ["%Y-%m-%d %H:%M:%S"])

        # Cache: valores aceitos por coluna
        self.valores_aceitos = {}
        for col in self.schema["obrigatorias"] + self.schema.get("opcionais", []):
            if "valores_aceitos" in col:
                self.valores_aceitos[col["nome"]] = set(col["valores_aceitos"])

    # -----------------------------------------------------------------
    # Passos individuais (sao chamados em sequencia por transformar())
    # -----------------------------------------------------------------

    def padronizar_colunas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Renomeia colunas para snake_case."""
        mapa = {c: _para_snake_case(c) for c in df.columns}
        df = df.rename(columns=mapa)
        return df

    def remover_linhas_brancas(self, df: pd.DataFrame, rel: RelatorioTransform) -> pd.DataFrame:
        """Remove linhas onde TODAS as colunas sao NaN/vazias."""
        # Substituir strings vazias por NaN primeiro
        df = df.replace(r"^\s*$", np.nan, regex=True)

        antes = len(df)
        df = df.dropna(how="all")
        removidas = antes - len(df)

        if removidas:
            rel.linhas_em_branco_removidas = removidas
            log.debug(f"Removidas {removidas} linhas em branco")

        return df

    def parse_data_flex(self, valor) -> pd.Timestamp:
        """Tenta parsear data em varios formatos. Retorna NaT se nao conseguir."""
        if pd.isna(valor) or (isinstance(valor, str) and not valor.strip()):
            return pd.NaT

        valor_str = str(valor).strip()

        for fmt in self.formatos_data:
            try:
                return pd.to_datetime(valor_str, format=fmt)
            except (ValueError, TypeError):
                continue

        # Ultimo recurso: parse generico do pandas (mas gera warning)
        try:
            return pd.to_datetime(valor_str)
        except Exception:
            return pd.NaT

    def _parse_decimal_br(self, valor) -> float:
        """Converte string com virgula ou ponto para float."""
        if pd.isna(valor):
            return np.nan
        if isinstance(valor, (int, float)):
            return float(valor)

        valor_str = str(valor).strip()
        if not valor_str or valor_str.lower() in ("nan", "null", "none"):
            return np.nan

        # Se tem virgula E ponto, o ponto e milhar (formato BR)
        if "," in valor_str and "." in valor_str:
            valor_str = valor_str.replace(".", "").replace(",", ".")
        elif "," in valor_str:
            # So virgula: assumir separador decimal BR
            valor_str = valor_str.replace(",", ".")

        try:
            return float(valor_str)
        except ValueError:
            return np.nan

    def _parse_int(self, valor) -> Any:
        """Converte para int, retorna None em caso de erro."""
        if pd.isna(valor):
            return None
        try:
            return int(float(str(valor).strip()))
        except (ValueError, TypeError):
            return None

    def converter_tipos(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica conversao de tipos por coluna baseado no schema."""
        for col_spec in self.schema["obrigatorias"] + self.schema.get("opcionais", []):
            nome = col_spec["nome"]
            tipo = col_spec["tipo"]

            if nome not in df.columns:
                continue

            if tipo == "datetime":
                df[nome] = df[nome].apply(self.parse_data_flex)
            elif tipo in ("decimal", "float"):
                df[nome] = df[nome].apply(self._parse_decimal_br)
            elif tipo == "int":
                df[nome] = df[nome].apply(self._parse_int)
                df[nome] = pd.array(df[nome], dtype="Int64")
            elif tipo == "str":
                df[nome] = df[nome].astype(str).replace(
                    {"nan": np.nan, "None": np.nan, "": np.nan}
                )
                df[nome] = df[nome].str.strip()

        return df

    def validar_regras_negocio(
        self, df: pd.DataFrame, rel: RelatorioTransform
    ) -> pd.DataFrame:
        """Filtra linhas que quebram regras de negocio."""
        antes = len(df)

        # Regra 1: colunas obrigatorias NAO nullable nao podem estar vazias
        for col_spec in self.schema["obrigatorias"]:
            nome = col_spec["nome"]
            if nome in df.columns and not col_spec.get("nullable", False):
                mask = df[nome].isna()
                if mask.any():
                    n = int(mask.sum())
                    log.warning(
                        f"Removendo {n} linhas com {nome} nulo (obrigatoria)"
                    )
                    df = df[~mask]

        removidas_nulos = antes - len(df)
        rel.linhas_com_nulos_criticos_removidas = removidas_nulos

        # Regra 2: quantidade > 0
        antes = len(df)
        if not self.regras.get("aceitar_quantidade_negativa", False):
            mask = df["quantidade"] <= 0
            if mask.any():
                n = int(mask.sum())
                log.warning(f"Removendo {n} linhas com quantidade <= 0")
                df = df[~mask]

        # Regra 3: preco > 0
        if not self.regras.get("aceitar_preco_negativo", False):
            mask = df["preco_unitario"] <= 0
            if mask.any():
                n = int(mask.sum())
                log.warning(f"Removendo {n} linhas com preco_unitario <= 0")
                df = df[~mask]

        # Regra 4: forma_pagamento em lista de aceitos
        if "forma_pagamento" in self.valores_aceitos:
            aceitos = self.valores_aceitos["forma_pagamento"]
            df["forma_pagamento"] = df["forma_pagamento"].str.upper()
            mask = ~df["forma_pagamento"].isin(aceitos) & df["forma_pagamento"].notna()
            if mask.any():
                invalidos = df.loc[mask, "forma_pagamento"].unique().tolist()
                n = int(mask.sum())
                log.warning(
                    f"Removendo {n} linhas com forma_pagamento invalida: {invalidos}"
                )
                df = df[~mask]

        # Regra 5: data no intervalo aceito
        d_min = pd.Timestamp(self.regras.get("data_minima", "2000-01-01"))
        d_max = pd.Timestamp(self.regras.get("data_maxima", "2099-12-31"))
        mask_data = (df["data_venda"].isna() |
                     (df["data_venda"] < d_min) |
                     (df["data_venda"] > d_max))
        if mask_data.any():
            n = int(mask_data.sum())
            log.warning(
                f"Removendo {n} linhas com data fora do intervalo "
                f"[{d_min.date()}, {d_max.date()}]"
            )
            df = df[~mask_data]
            rel.linhas_data_invalida_removidas = n

        rel.linhas_com_valores_invalidos_removidas = (
            (antes - len(df)) - rel.linhas_data_invalida_removidas
        )

        return df.reset_index(drop=True)

    def remover_duplicatas(
        self, df: pd.DataFrame, rel: RelatorioTransform
    ) -> pd.DataFrame:
        """Remove duplicatas pela chave natural (mantem primeira ocorrencia)."""
        chaves_existentes = [c for c in self.chave_natural if c in df.columns]
        if not chaves_existentes:
            log.warning("Nenhuma coluna da chave natural encontrada — pulando dedup")
            return df

        antes = len(df)
        df = df.drop_duplicates(subset=chaves_existentes, keep="first")
        removidas = antes - len(df)

        if removidas:
            rel.linhas_duplicadas_removidas = removidas
            log.info(f"Removidas {removidas} duplicatas por chave natural")

        return df.reset_index(drop=True)

    def enriquecer(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona colunas derivadas para o load."""
        df = df.copy()

        # valor_total = quantidade x preco_unitario - desconto
        if "desconto" not in df.columns:
            df["desconto"] = 0.0
        df["desconto"] = df["desconto"].fillna(0.0)

        df["valor_total"] = (
            df["quantidade"].astype(float) * df["preco_unitario"] - df["desconto"]
        ).round(2)

        # Derivar ano_mes para particionamento futuro
        df["ano_mes"] = df["data_venda"].dt.strftime("%Y-%m")

        # Padronizar CPF: so digitos; nulo vira "SEM_CPF" para idempotencia
        # (o SQL trata NULL != NULL, quebrando UPSERT quando cpf e chave natural)
        if "cliente_cpf" in df.columns:
            df["cliente_cpf"] = df["cliente_cpf"].astype(str).str.replace(
                r"[^\d]", "", regex=True
            ).replace({"nan": None, "": None})
            df["cliente_cpf"] = df["cliente_cpf"].fillna("SEM_CPF")

        return df

    # -----------------------------------------------------------------
    # Ponto de entrada
    # -----------------------------------------------------------------

    def transformar(
        self, df: pd.DataFrame, nome_arquivo: str = ""
    ) -> tuple:
        """Aplica todas as transformacoes em ordem.

        Retorna (df_limpo, relatorio).
        """
        rel = RelatorioTransform(arquivo=nome_arquivo, linhas_entrada=len(df))

        df = self.padronizar_colunas(df)
        df = self.remover_linhas_brancas(df, rel)
        df = self.converter_tipos(df)
        df = self.validar_regras_negocio(df, rel)
        df = self.remover_duplicatas(df, rel)
        df = self.enriquecer(df)

        rel.linhas_saida = len(df)
        log.info(f"[{nome_arquivo}] Transform: {rel.resumir()}")

        return df, rel
