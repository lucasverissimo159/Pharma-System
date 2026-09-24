"""
app/routes/__init__.py
----------------------
Ponto central que registra todos os Blueprints no app Flask.

Cada recurso REST tem seu proprio blueprint em um arquivo separado, seguindo
o principio de responsabilidade unica.
"""

from flask import Flask

from app.routes.filiais import bp as bp_filiais
from app.routes.categorias import bp as bp_categorias
from app.routes.produtos import bp as bp_produtos
from app.routes.clientes import bp as bp_clientes
from app.routes.vendas import bp as bp_vendas
from app.routes.indicadores import bp as bp_indicadores
from app.routes.docs import bp as bp_docs
from app.routes.health import bp as bp_health


BLUEPRINTS = [
    bp_health,
    bp_filiais,
    bp_categorias,
    bp_produtos,
    bp_clientes,
    bp_vendas,
    bp_indicadores,
    bp_docs,
]


def registrar_blueprints(app: Flask):
    """Registra todos os blueprints no app."""
    for bp in BLUEPRINTS:
        app.register_blueprint(bp)
