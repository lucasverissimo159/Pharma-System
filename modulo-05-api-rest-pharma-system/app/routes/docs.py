"""app/routes/docs.py — Serve o Swagger UI e a spec OpenAPI."""

from flask import Blueprint, jsonify, current_app, Response

from app.openapi_spec import gerar_openapi


bp = Blueprint("docs", __name__, url_prefix="/api")


@bp.route("/openapi.json", methods=["GET"])
def openapi_json():
    """Retorna a especificacao OpenAPI 3.0 em JSON.

    E consumida pelo Swagger UI em /api/docs.
    """
    cfg = current_app.config["PHARMA_CONFIG"]
    return jsonify(gerar_openapi(cfg))


SWAGGER_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>PharmaSystem API — Swagger UI</title>
  <link rel="stylesheet" type="text/css"
        href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css">
  <link rel="icon" type="image/png"
        href="https://unpkg.com/swagger-ui-dist@5.11.0/favicon-32x32.png"
        sizes="32x32">
  <style>
    html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
    *, *:before, *:after { box-sizing: inherit; }
    body { margin: 0; background: #fafafa; }
    .swagger-ui .topbar { background-color: #00695C; }
    .swagger-ui .topbar .download-url-wrapper { display: none; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js"></script>
  <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-standalone-preset.js"></script>
  <script>
    window.onload = function() {
      window.ui = SwaggerUIBundle({
        url: "/api/openapi.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [SwaggerUIBundle.plugins.DownloadUrl],
        layout: "StandaloneLayout",
        tryItOutEnabled: true,
        displayRequestDuration: true,
        docExpansion: "list",
        defaultModelsExpandDepth: 1,
        filter: true
      });
    };
  </script>
</body>
</html>"""


@bp.route("/docs", methods=["GET"])
def swagger_ui():
    """Serve o Swagger UI (carrega recursos de CDN unpkg)."""
    return Response(SWAGGER_HTML, mimetype="text/html")


@bp.route("/", methods=["GET"])
@bp.route("", methods=["GET"])
def raiz():
    """Endpoint raiz da API — retorna metadados e links uteis."""
    return jsonify({
        "nome": "PharmaSystem API",
        "documentacao": "/api/docs",
        "openapi": "/api/openapi.json",
        "recursos": [
            "/api/health",
            "/api/versao",
            "/api/filiais",
            "/api/categorias",
            "/api/produtos",
            "/api/clientes",
            "/api/vendas",
            "/api/indicadores/kpis-gerais",
            "/api/indicadores/faturamento-mensal",
            "/api/indicadores/top-produtos",
            "/api/indicadores/top-filiais",
            "/api/indicadores/faturamento-por-categoria",
            "/api/indicadores/formas-pagamento",
        ]
    })
