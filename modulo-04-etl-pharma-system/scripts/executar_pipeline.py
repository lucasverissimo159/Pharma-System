"""
executar_pipeline.py
--------------------
Ponto de entrada do pipeline ETL.

Uso:
    python scripts/executar_pipeline.py                # execucao normal
    python scripts/executar_pipeline.py --config path  # com config custom
"""

import argparse
import sys
from pathlib import Path

# Adicionar raiz ao path
ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))

from src.config import Config
from src.logger import configurar_do_config
from src.pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline ETL PharmaSystem"
    )
    parser.add_argument(
        "--config",
        default=str(ROOT / "config" / "config.yaml"),
        help="Caminho do arquivo config.yaml",
    )
    parser.add_argument(
        "--schema",
        default=str(ROOT / "config" / "schema.yaml"),
        help="Caminho do arquivo schema.yaml",
    )
    args = parser.parse_args()

    # Carregar config
    cfg = Config.carregar(args.config, args.schema)

    # Configurar logger a partir do config
    configurar_do_config(cfg)

    # Executar pipeline
    pipeline = Pipeline(cfg)
    resumo = pipeline.executar()

    # Codigo de saida diferente para CI/CD
    if resumo.status == "SUCESSO":
        sys.exit(0)
    elif resumo.status == "SUCESSO_PARCIAL":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
