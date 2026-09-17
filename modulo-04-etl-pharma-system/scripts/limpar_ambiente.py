"""
limpar_ambiente.py
------------------
Reseta o ambiente para um novo teste:
- Remove arquivos em dados_brutos/, dados_processados/, dados_rejeitados/
- Remove logs/
- Remove o banco SQLite

Uso:
    python scripts/limpar_ambiente.py
    python scripts/limpar_ambiente.py --confirmar   (executa sem pedir confirmacao)
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))

from src.config import Config


def limpar_pasta(pasta: Path, extensoes: list = None):
    """Remove arquivos da pasta (opcionalmente filtrando por extensao)."""
    if not pasta.exists():
        return 0

    n = 0
    for arq in pasta.iterdir():
        if arq.is_file():
            if extensoes is None or arq.suffix.lower() in extensoes:
                arq.unlink()
                n += 1
    return n


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirmar", action="store_true",
                        help="Executa sem pedir confirmacao")
    args = parser.parse_args()

    cfg = Config.carregar()

    print("Este script vai APAGAR:")
    print(f"  - Todos os CSVs em {cfg.path('dados_brutos').relative_to(ROOT)}/")
    print(f"  - Todos os CSVs em {cfg.path('dados_processados').relative_to(ROOT)}/")
    print(f"  - Todos os CSVs em {cfg.path('dados_rejeitados').relative_to(ROOT)}/")
    print(f"  - Todos os logs em {cfg.path('logs').relative_to(ROOT)}/")
    print(f"  - O banco {cfg.caminho_sqlite().relative_to(ROOT)}")
    print()

    if not args.confirmar:
        resp = input("Confirma? (digite 'sim'): ")
        if resp.strip().lower() != "sim":
            print("Cancelado.")
            sys.exit(0)

    total = 0
    total += limpar_pasta(cfg.path("dados_brutos"), [".csv"])
    total += limpar_pasta(cfg.path("dados_processados"), [".csv"])
    total += limpar_pasta(cfg.path("dados_rejeitados"), [".csv"])
    total += limpar_pasta(cfg.path("logs"), [".log"])

    # Banco
    db_path = cfg.caminho_sqlite()
    if db_path.exists():
        db_path.unlink()
        print(f"Banco removido: {db_path}")
        total += 1

    print(f"\nAmbiente limpo. {total} arquivos removidos.")


if __name__ == "__main__":
    main()
