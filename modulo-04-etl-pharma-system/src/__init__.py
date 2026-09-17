"""
PharmaSystem — Modulo 04: ETL Pipeline
=======================================

Pipeline ETL modular para consumir CSVs de vendas de filiais e carregar em
banco de dados com idempotencia via UPSERT.

Uso rapido:

    from src.config import Config
    from src.pipeline import Pipeline

    cfg = Config.carregar()
    pipeline = Pipeline(cfg)
    resumo = pipeline.executar()
"""

__version__ = "1.0.0"
__author__ = "Lucas Verissimo"
