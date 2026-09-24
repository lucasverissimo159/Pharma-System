"""app/routes/health.py — endpoints de saude e versao."""

from flask import Blueprint, current_app, jsonify
from datetime import datetime

from app.database import obter_conexao


bp = Blueprint("health", __name__, url_prefix="/api")


@bp.route("/health", methods=["GET"])
def health():
    """Health check simples — sempre retorna 200 se a API esta viva.

    ---
    tags: [Health]
    responses:
      200: OK
    """
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
    })


@bp.route("/health/db", methods=["GET"])
def health_db():
    """Health check com banco: valida conexao SQLite.

    ---
    tags: [Health]
    responses:
      200: banco respondeu
      500: banco fora do ar
    """
    conn = obter_conexao()
    cur = conn.execute("SELECT COUNT(*) FROM filiais")
    n_filiais = cur.fetchone()[0]

    return jsonify({
        "status": "ok",
        "banco": "conectado",
        "filiais": n_filiais,
        "timestamp": datetime.now().isoformat(),
    })


@bp.route("/versao", methods=["GET"])
def versao():
    """Retorna metadados da API."""
    cfg = current_app.config["PHARMA_CONFIG"]
    return jsonify({
        "nome": cfg.API_TITLE,
        "versao": cfg.API_VERSION,
        "descricao": cfg.API_DESCRICAO,
    })
