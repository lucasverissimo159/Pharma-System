"""
extract.py
----------
Camada Extract do ETL: le CSVs de dados_brutos/, valida schema e retorna
DataFrames prontos para transformacao.

Regras:
- Tenta encoding utf-8-sig; se falhar, cai para latin-1
- Valida presenca das colunas obrigatorias definidas no schema.yaml
- Arquivo vazio ou com colunas faltando e REJEITADO (nao carregado)
- Retorna: DataFrame + metadados (nome, tamanho, encoding usado)
"""

import glob
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import pandas as pd

from src.logger import obter_logger

log = obter_logger("extract")


@dataclass
class ArquivoExtraido:
    """Resultado da extracao de um arquivo."""
    caminho: Path
    df: Optional[pd.DataFrame] = None
    encoding: str = ""
    linhas_brutas: int = 0
    sucesso: bool = False
    motivo_falha: str = ""
    colunas_faltantes: List[str] = field(default_factory=list)


class ExtratorCSV:
    """Extrai CSVs de vendas com validacao de schema."""

    def __init__(self, schema: dict, encoding_padrao: str = "utf-8-sig"):
        self.schema = schema["vendas_filial"]
        self.encoding_padrao = encoding_padrao

        # Extrair nomes das colunas obrigatorias
        self.colunas_obrigatorias = [
            c["nome"] for c in self.schema.get("obrigatorias", [])
        ]

    def _ler_csv_com_fallback(self, caminho: Path) -> tuple:
        """Tenta ler com utf-8-sig; se falhar, tenta latin-1.

        Retorna (df, encoding_usado) ou levanta a excecao.
        """
        encodings_tentar = [self.encoding_padrao, "latin-1", "cp1252"]

        for enc in encodings_tentar:
            try:
                df = pd.read_csv(caminho, encoding=enc, dtype=str, keep_default_na=False)
                if enc != self.encoding_padrao:
                    log.warning(
                        f"Arquivo {caminho.name} lido com encoding fallback: {enc}"
                    )
                return df, enc
            except UnicodeDecodeError:
                continue
            except pd.errors.EmptyDataError:
                # Arquivo completamente vazio
                raise
            except Exception as e:
                # Outro tipo de erro (parse, etc)
                log.error(f"Erro ao ler {caminho.name} com {enc}: {e}")
                raise

        raise UnicodeDecodeError(
            "encoding", b"", 0, 1,
            f"Nenhum encoding funcionou: {encodings_tentar}"
        )

    def _validar_schema(self, df: pd.DataFrame) -> List[str]:
        """Retorna lista de colunas obrigatorias que estao faltando."""
        cols_presentes = set(df.columns)
        faltantes = [c for c in self.colunas_obrigatorias if c not in cols_presentes]
        return faltantes

    def extrair_arquivo(self, caminho: Path) -> ArquivoExtraido:
        """Extrai um unico arquivo. Nunca levanta excecao — todos os erros
        viram ArquivoExtraido(sucesso=False, motivo_falha=...).
        """
        resultado = ArquivoExtraido(caminho=caminho)

        # 1. Arquivo existe?
        if not caminho.exists():
            resultado.motivo_falha = "Arquivo nao encontrado"
            log.error(f"[{caminho.name}] Arquivo nao encontrado")
            return resultado

        # 2. Tamanho > 0?
        tamanho = caminho.stat().st_size
        if tamanho == 0:
            resultado.motivo_falha = "Arquivo vazio (0 bytes)"
            log.warning(f"[{caminho.name}] Arquivo vazio, sera rejeitado")
            return resultado

        # 3. Ler
        try:
            df, encoding = self._ler_csv_com_fallback(caminho)
            resultado.encoding = encoding
            resultado.linhas_brutas = len(df)
        except pd.errors.EmptyDataError:
            resultado.motivo_falha = "CSV sem dados (so cabecalho ou vazio)"
            log.warning(f"[{caminho.name}] CSV sem dados")
            return resultado
        except UnicodeDecodeError as e:
            resultado.motivo_falha = f"Encoding invalido: {e.reason}"
            log.error(f"[{caminho.name}] Erro de encoding")
            return resultado
        except Exception as e:
            resultado.motivo_falha = f"Erro na leitura: {type(e).__name__}: {e}"
            log.error(f"[{caminho.name}] {resultado.motivo_falha}")
            return resultado

        log.info(
            f"[{caminho.name}] Lido: {resultado.linhas_brutas} linhas, "
            f"{len(df.columns)} colunas, encoding={encoding}"
        )

        # 4. Validar schema
        faltantes = self._validar_schema(df)
        if faltantes:
            resultado.colunas_faltantes = faltantes
            resultado.motivo_falha = (
                f"Schema invalido: colunas obrigatorias faltando: {', '.join(faltantes)}"
            )
            log.error(
                f"[{caminho.name}] {resultado.motivo_falha}. "
                f"Presentes: {list(df.columns)}"
            )
            return resultado

        # Tudo ok
        resultado.df = df
        resultado.sucesso = True
        return resultado

    def extrair_pasta(self, pasta: Path, padrao: str = "*.csv") -> List[ArquivoExtraido]:
        """Extrai todos os arquivos que casam com o padrao."""
        pasta = Path(pasta)
        if not pasta.exists():
            log.error(f"Pasta nao encontrada: {pasta}")
            return []

        arquivos = sorted(glob.glob(str(pasta / padrao)))
        log.info(f"Encontrados {len(arquivos)} arquivos em {pasta} (padrao: {padrao})")

        if not arquivos:
            log.warning(f"Nenhum arquivo com padrao '{padrao}' em {pasta}")
            return []

        resultados = []
        for arq in arquivos:
            resultado = self.extrair_arquivo(Path(arq))
            resultados.append(resultado)

        # Resumo
        ok = sum(1 for r in resultados if r.sucesso)
        falha = len(resultados) - ok
        log.info(f"Extract concluido: {ok} sucesso, {falha} rejeitados")

        return resultados
