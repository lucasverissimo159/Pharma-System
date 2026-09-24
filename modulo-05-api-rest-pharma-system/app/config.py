"""
app/config.py
-------------
Configuracoes da aplicacao. Le variaveis de ambiente quando disponiveis,
usa defaults sensatos caso contrario.
"""

import os
from pathlib import Path


ROOT = Path(__file__).parent.parent.resolve()


class Config:
    """Configuracao da API."""

    # Banco
    DATABASE = os.environ.get(
        "PHARMA_DB_PATH",
        str(ROOT / "db" / "pharma.db"),
    )

    # Servidor
    HOST = os.environ.get("PHARMA_HOST", "127.0.0.1")
    PORT = int(os.environ.get("PHARMA_PORT", "5000"))
    DEBUG = os.environ.get("PHARMA_DEBUG", "false").lower() == "true"

    # Paginacao
    LIMITE_PADRAO_PAGINA = 20
    LIMITE_MAXIMO_PAGINA = 100

    # Titulos e metadados (usados pelo Swagger)
    API_TITLE = "PharmaSystem API"
    API_VERSION = "1.0.0"
    API_DESCRICAO = (
        "API REST para a rede de farmacias PharmaMinas. "
        "Expoe recursos de filiais, categorias, produtos, clientes, "
        "vendas e indicadores agregados."
    )


class TestConfig(Config):
    """Configuracao para testes."""
    DATABASE = str(ROOT / "db" / "test_pharma.db")
    DEBUG = True
