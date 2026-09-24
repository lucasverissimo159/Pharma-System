"""
app/__init__.py
---------------
Application Factory do Flask: cria a instancia da app com todos os
blueprints registrados e handlers de erro.

Uso:
    from app import create_app
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
"""

from flask import Flask

from app.config import Config
from app.database import fechar_conexao_ao_final_da_request
from app.errors import registrar_handlers_erro
from app.routes import registrar_blueprints


def create_app(config_override: Config = None) -> Flask:
    """Cria e configura a aplicacao Flask.

    Args:
        config_override: instancia de Config alternativa (util para testes).
    """
    app = Flask(__name__)

    # Configuracao
    cfg = config_override or Config()
    app.config["PHARMA_CONFIG"] = cfg
    app.config["JSON_SORT_KEYS"] = False   # preserva ordem das chaves na resposta

    # Registrar hook para fechar conexao SQLite ao final da request
    app.teardown_appcontext(fechar_conexao_ao_final_da_request)

    # Registrar todos os blueprints (rotas)
    registrar_blueprints(app)

    # Registrar handlers globais de erro
    registrar_handlers_erro(app)

    return app
