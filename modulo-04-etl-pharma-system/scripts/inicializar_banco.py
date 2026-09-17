"""
inicializar_banco.py
--------------------
Cria as tabelas no banco de dados. Idempotente — pode rodar quantas vezes
quiser.

Uso:
    python scripts/inicializar_banco.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))

from src.config import Config
from src.load import CarregadorSQLite


def main():
    cfg = Config.carregar()

    backend = cfg.banco.get("backend")
    if backend != "sqlite":
        print(f"Backend {backend} nao suportado neste script. Use SQLite.")
        sys.exit(1)

    caminho = cfg.caminho_sqlite()
    print(f"Inicializando banco em: {caminho}")

    carregador = CarregadorSQLite(caminho)
    carregador.inicializar_banco()

    stats = carregador.estatisticas()
    print("\nEstado do banco:")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
