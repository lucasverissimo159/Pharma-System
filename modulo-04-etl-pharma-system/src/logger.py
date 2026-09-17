"""
logger.py
---------
Configura logging estruturado para o pipeline.

- Console: colorido, so mensagens importantes (INFO+)
- Arquivo: TUDO (DEBUG+), rotacionado por dia
- Formato: timestamp | nivel | modulo | mensagem

Uso:
    from src.logger import obter_logger
    log = obter_logger(__name__)
    log.info("Iniciando processamento")
"""

import logging
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# Codigos ANSI para cores no console
CORES = {
    "DEBUG": "\033[90m",       # cinza
    "INFO": "\033[36m",        # ciano
    "WARNING": "\033[33m",     # amarelo
    "ERROR": "\033[31m",       # vermelho
    "CRITICAL": "\033[41m\033[97m",  # fundo vermelho + texto branco
    "RESET": "\033[0m",
}


class ConsoleFormatterColorido(logging.Formatter):
    """Formatter que colore o nivel do log no console."""

    def format(self, record):
        cor = CORES.get(record.levelname, "")
        reset = CORES["RESET"]
        # Salvar levelname original
        levelname_original = record.levelname
        record.levelname = f"{cor}{record.levelname:<8}{reset}"
        try:
            resultado = super().format(record)
        finally:
            record.levelname = levelname_original
        return resultado


def obter_logger(
    nome: str = "pipeline",
    pasta_logs: Path = None,
    nivel: str = "INFO",
    formato: str = None,
    formato_data: str = None,
) -> logging.Logger:
    """Retorna logger configurado com console + arquivo rotacionado.

    Uso da hierarquia:
    - `obter_logger("pipeline")` — logger raiz do pipeline com console (e arquivo se pasta_logs).
    - `obter_logger("extract")`, `"transform"`, `"load"` — loggers filhos ("pipeline.extract" etc)
      que propagam para o raiz, herdando os handlers.

    Se ja foi configurado antes com esses parametros, retorna o existente.
    """
    # Nomes reservados dos modulos: normalizar para "pipeline.<nome>"
    if nome in ("extract", "transform", "load"):
        nome = f"pipeline.{nome}"

    logger = logging.getLogger(nome)

    # Se e um filho, deixa propagar para o pai
    if "." in nome:
        logger.propagate = True
        logger.setLevel(logging.DEBUG)  # aceita tudo; o pai filtra
        return logger

    # E o logger raiz "pipeline"
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formato = formato or "%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s"
    formato_data = formato_data or "%Y-%m-%d %H:%M:%S"

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    nivel_console = getattr(logging, nivel.upper(), logging.INFO)
    console.setLevel(nivel_console)
    console.setFormatter(ConsoleFormatterColorido(formato, formato_data))
    logger.addHandler(console)

    # Arquivo handler (so se pasta_logs foi passado)
    if pasta_logs is not None:
        pasta_logs = Path(pasta_logs)
        pasta_logs.mkdir(parents=True, exist_ok=True)
        arquivo_log = pasta_logs / "pipeline.log"

        arquivo = TimedRotatingFileHandler(
            arquivo_log, when="midnight", backupCount=30, encoding="utf-8"
        )
        arquivo.setLevel(logging.DEBUG)
        arquivo.setFormatter(logging.Formatter(formato, formato_data))
        logger.addHandler(arquivo)

    # Nao propagar para o root logger (evita duplicacao)
    logger.propagate = False
    return logger


def configurar_do_config(cfg) -> logging.Logger:
    """Configura o logger RAIZ do pipeline a partir de um objeto Config.

    Chame no inicio do script principal. Todos os loggers filhos
    (extract, transform, load, pipeline.*) propagam para este e herdam
    seus handlers.
    """
    # Se ja existe com handlers, adiciona o arquivo se ainda nao tem
    logger = logging.getLogger("pipeline")
    if logger.handlers:
        # Ja configurado — verifica se falta o arquivo
        tem_arquivo = any(
            isinstance(h, TimedRotatingFileHandler) for h in logger.handlers
        )
        if not tem_arquivo:
            pasta_logs = Path(cfg.path("logs"))
            pasta_logs.mkdir(parents=True, exist_ok=True)
            arquivo = TimedRotatingFileHandler(
                pasta_logs / "pipeline.log", when="midnight",
                backupCount=30, encoding="utf-8"
            )
            arquivo.setLevel(logging.DEBUG)
            formato = cfg.logging.get(
                "formato",
                "%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s"
            )
            formato_data = cfg.logging.get("formato_data", "%Y-%m-%d %H:%M:%S")
            arquivo.setFormatter(logging.Formatter(formato, formato_data))
            logger.addHandler(arquivo)
        return logger

    return obter_logger(
        nome="pipeline",
        pasta_logs=cfg.path("logs"),
        nivel=cfg.logging.get("nivel", "INFO"),
        formato=cfg.logging.get("formato"),
        formato_data=cfg.logging.get("formato_data"),
    )
