"""
executar_api.py
---------------
Inicia o servidor da API PharmaSystem.

Uso:
    python scripts/executar_api.py                # localhost:5000
    PHARMA_HOST=0.0.0.0 python scripts/executar_api.py    # acessivel externamente
    PHARMA_PORT=8080 python scripts/executar_api.py       # porta customizada
    PHARMA_DEBUG=true python scripts/executar_api.py      # modo debug
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))

from app import create_app
from app.config import Config


def main():
    cfg = Config()
    app = create_app(cfg)

    print("=" * 70)
    print(f"  {cfg.API_TITLE} v{cfg.API_VERSION}")
    print("=" * 70)
    print(f"  Banco: {cfg.DATABASE}")
    print(f"  URL:   http://{cfg.HOST}:{cfg.PORT}")
    print(f"  Docs:  http://{cfg.HOST}:{cfg.PORT}/api/docs")
    print(f"  Debug: {cfg.DEBUG}")
    print("=" * 70)
    print()
    print("  Pressione Ctrl+C para parar")
    print()

    app.run(host=cfg.HOST, port=cfg.PORT, debug=cfg.DEBUG)


if __name__ == "__main__":
    main()
