"""
pipeline.py
-----------
Orquestrador do ETL: coordena Extract -> Transform -> Load.

Fluxo por arquivo:
    1. Extract  -> ArquivoExtraido
       - Se falha: move para dados_rejeitados/, proximo arquivo
    2. Transform -> DataFrame limpo + Relatorio
       - Registra no log as linhas removidas
    3. Load     -> Grava no banco via UPSERT
    4. Move arquivo original para dados_processados/ com timestamp

Ao final:
    - Registra execucao na tabela pipeline_execucoes
    - Loga resumo agregado
"""

import shutil
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List

from src.config import Config
from src.extract import ExtratorCSV
from src.transform import Transformador
from src.load import CarregadorSQLite
from src.logger import obter_logger

log = obter_logger("pipeline")


@dataclass
class ResumoExecucao:
    """Estatisticas agregadas de uma execucao do pipeline."""
    inicio: datetime = field(default_factory=datetime.now)
    fim: datetime = None
    arquivos_encontrados: int = 0
    arquivos_processados: int = 0
    arquivos_rejeitados: int = 0
    linhas_entrada: int = 0
    linhas_apos_transform: int = 0
    linhas_inseridas: int = 0
    linhas_atualizadas: int = 0

    @property
    def duracao_segundos(self) -> float:
        fim = self.fim or datetime.now()
        return (fim - self.inicio).total_seconds()

    @property
    def status(self) -> str:
        if self.arquivos_rejeitados == 0 and self.arquivos_processados > 0:
            return "SUCESSO"
        if self.arquivos_processados == 0:
            return "FALHA"
        return "SUCESSO_PARCIAL"

    def imprimir_resumo(self):
        log.info("=" * 70)
        log.info("RESUMO DA EXECUCAO")
        log.info("=" * 70)
        log.info(f"  Duracao total:         {self.duracao_segundos:.2f}s")
        log.info(f"  Status:                {self.status}")
        log.info(f"  Arquivos encontrados:  {self.arquivos_encontrados}")
        log.info(f"  Arquivos processados:  {self.arquivos_processados}")
        log.info(f"  Arquivos rejeitados:   {self.arquivos_rejeitados}")
        log.info(f"  Linhas de entrada:     {self.linhas_entrada:,}")
        log.info(f"  Linhas apos transform: {self.linhas_apos_transform:,}")
        log.info(f"  Linhas inseridas:      {self.linhas_inseridas:,}")
        log.info(f"  Linhas atualizadas:    {self.linhas_atualizadas:,}")
        log.info("=" * 70)


class Pipeline:
    """Orquestra o ETL usando as configuracoes do config.yaml."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.extrator = ExtratorCSV(
            schema=cfg.schema,
            encoding_padrao=cfg.pipeline.get("encoding_padrao", "utf-8-sig"),
        )
        self.transformador = Transformador(
            schema=cfg.schema,
            regras=cfg.regras,
            chave_natural=cfg.pipeline.get("chave_natural", []),
        )
        self.carregador = CarregadorSQLite(caminho_db=cfg.caminho_sqlite())

    def _mover_arquivo(self, origem: Path, destino_pasta: Path, prefixo: str = ""):
        """Move arquivo com timestamp para evitar sobrescrita."""
        destino_pasta.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_novo = f"{prefixo}{ts}_{origem.name}" if prefixo else f"{ts}_{origem.name}"
        destino = destino_pasta / nome_novo
        shutil.move(str(origem), str(destino))
        log.debug(f"Movido: {origem.name} -> {destino_pasta.name}/{nome_novo}")
        return destino

    def executar(self) -> ResumoExecucao:
        """Executa o pipeline completo."""
        resumo = ResumoExecucao()

        log.info("=" * 70)
        log.info(f"INICIANDO PIPELINE ETL — {resumo.inicio:%Y-%m-%d %H:%M:%S}")
        log.info("=" * 70)

        # Inicializar banco (idempotente)
        self.carregador.inicializar_banco()

        pasta_brutos = self.cfg.path("dados_brutos")
        pasta_processados = self.cfg.path("dados_processados")
        pasta_rejeitados = self.cfg.path("dados_rejeitados")
        padrao = self.cfg.pipeline.get("padrao_arquivo", "*.csv")

        # ---- Extract ----
        log.info(">> ETAPA: Extract")
        resultados_extract = self.extrator.extrair_pasta(pasta_brutos, padrao)
        resumo.arquivos_encontrados = len(resultados_extract)

        # ---- Loop por arquivo: Transform + Load ----
        em_caso_erro = self.cfg.pipeline.get("em_caso_de_erro", "continuar")
        mover_processados = self.cfg.pipeline.get("mover_processados", True)

        for res_extract in resultados_extract:
            arquivo = res_extract.caminho

            if not res_extract.sucesso:
                # Arquivo rejeitado no extract
                resumo.arquivos_rejeitados += 1
                log.warning(
                    f"REJEITADO: {arquivo.name} — {res_extract.motivo_falha}"
                )
                # Mover para rejeitados com motivo no nome
                try:
                    self._mover_arquivo(
                        arquivo, pasta_rejeitados,
                        prefixo="REJEITADO_"
                    )
                except Exception as e:
                    log.error(f"Erro ao mover rejeitado: {e}")

                if em_caso_erro == "abortar":
                    log.critical("Abortando por configuracao (em_caso_de_erro=abortar)")
                    break
                continue

            # ---- Transform ----
            try:
                log.info(f">> ETAPA: Transform [{arquivo.name}]")
                df_limpo, rel_transform = self.transformador.transformar(
                    res_extract.df, nome_arquivo=arquivo.name
                )
                resumo.linhas_entrada += rel_transform.linhas_entrada
                resumo.linhas_apos_transform += rel_transform.linhas_saida
            except Exception as e:
                log.error(f"ERRO no Transform de {arquivo.name}: {e}", exc_info=True)
                resumo.arquivos_rejeitados += 1
                if mover_processados:
                    self._mover_arquivo(arquivo, pasta_rejeitados, prefixo="ERRO_TRANSFORM_")
                if em_caso_erro == "abortar":
                    break
                continue

            # ---- Load ----
            try:
                log.info(f">> ETAPA: Load [{arquivo.name}]")
                rel_load = self.carregador.carregar_dataframe(
                    df_limpo, origem_arquivo=arquivo.name
                )
                resumo.linhas_inseridas += rel_load.linhas_inseridas
                resumo.linhas_atualizadas += rel_load.linhas_atualizadas
            except Exception as e:
                log.error(f"ERRO no Load de {arquivo.name}: {e}", exc_info=True)
                resumo.arquivos_rejeitados += 1
                if mover_processados:
                    self._mover_arquivo(arquivo, pasta_rejeitados, prefixo="ERRO_LOAD_")
                if em_caso_erro == "abortar":
                    break
                continue

            # Sucesso completo
            resumo.arquivos_processados += 1
            if mover_processados:
                self._mover_arquivo(arquivo, pasta_processados)

        # Finalizar
        resumo.fim = datetime.now()

        # Registrar execucao
        self.carregador.registrar_execucao(
            arquivos_encontrados=resumo.arquivos_encontrados,
            arquivos_processados=resumo.arquivos_processados,
            arquivos_rejeitados=resumo.arquivos_rejeitados,
            linhas_inseridas=resumo.linhas_inseridas,
            linhas_atualizadas=resumo.linhas_atualizadas,
            duracao_segundos=resumo.duracao_segundos,
            status=resumo.status,
        )

        resumo.imprimir_resumo()

        # Estatisticas do banco apos execucao
        stats = self.carregador.estatisticas()
        log.info("Estado atual do banco:")
        for k, v in stats.items():
            log.info(f"  {k}: {v:,}" if isinstance(v, (int, float)) else f"  {k}: {v}")

        return resumo
