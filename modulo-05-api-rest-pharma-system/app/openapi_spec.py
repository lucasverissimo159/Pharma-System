"""
app/openapi_spec.py
-------------------
Gera a especificacao OpenAPI 3.0 da API programaticamente.

Retorna um dict pronto para ser servido como JSON pelo endpoint /api/openapi.json.
Um SwaggerUI (via CDN) consome esse JSON e renderiza a documentacao interativa.

Optamos por escrever a spec a mao (em vez de gerar a partir de docstrings)
para ser explicito sobre o contrato da API — o que e didatico.
"""


def _schema_paginacao():
    return {
        "type": "object",
        "properties": {
            "pagina": {"type": "integer", "example": 1},
            "por_pagina": {"type": "integer", "example": 20},
            "total": {"type": "integer", "example": 15},
            "total_paginas": {"type": "integer", "example": 1},
        }
    }


def _schema_erro():
    return {
        "type": "object",
        "properties": {
            "erro": {"type": "string", "example": "requisicao_invalida"},
            "mensagem": {"type": "string", "example": "Dados invalidos"},
            "status": {"type": "integer", "example": 400},
            "detalhes": {"type": "object"},
        }
    }


def _schema_filial():
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer", "example": 1},
            "codigo": {"type": "string", "example": "FIL001"},
            "nome": {"type": "string", "example": "PharmaMinas Centro Montes Claros"},
            "cidade": {"type": "string", "example": "Montes Claros"},
            "estado": {"type": "string", "example": "MG"},
            "endereco": {"type": "string", "nullable": True},
            "telefone": {"type": "string", "nullable": True},
            "data_abertura": {"type": "string", "format": "date", "nullable": True},
            "ativa": {"type": "boolean", "example": True},
        }
    }


def _schema_categoria():
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "nome": {"type": "string", "example": "Medicamentos Genericos"},
            "descricao": {"type": "string", "nullable": True},
        }
    }


def _schema_produto():
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "codigo_barras": {"type": "string", "example": "7891234567890"},
            "nome": {"type": "string", "example": "Dipirona 500mg 20cp"},
            "categoria_id": {"type": "integer"},
            "fabricante": {"type": "string", "nullable": True},
            "preco_custo": {"type": "number", "example": 8.50},
            "preco_venda": {"type": "number", "example": 15.90},
            "margem_lucro": {"type": "number", "example": 7.40},
            "margem_percentual": {"type": "number", "example": 46.54},
            "estoque_minimo": {"type": "integer"},
            "exige_receita": {"type": "boolean"},
            "ativo": {"type": "boolean"},
        }
    }


def _schema_cliente():
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "nome": {"type": "string", "example": "Maria da Silva"},
            "cpf": {"type": "string", "example": "12345678901"},
            "email": {"type": "string", "format": "email"},
            "telefone": {"type": "string"},
            "data_nascimento": {"type": "string", "format": "date"},
            "cidade": {"type": "string"},
            "estado": {"type": "string"},
            "data_cadastro": {"type": "string", "format": "date-time"},
        }
    }


def _schema_venda():
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "filial_id": {"type": "integer"},
            "cliente_id": {"type": "integer", "nullable": True},
            "data_venda": {"type": "string", "format": "date-time"},
            "valor_total": {"type": "number"},
            "desconto": {"type": "number"},
            "forma_pagamento": {
                "type": "string",
                "enum": ["PIX", "DINHEIRO", "DEBITO", "CREDITO", "CONVENIO"]
            },
            "status": {
                "type": "string",
                "enum": ["CONCLUIDA", "CANCELADA", "PENDENTE"]
            },
            "itens": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "produto_id": {"type": "integer"},
                        "quantidade": {"type": "integer"},
                        "preco_unitario": {"type": "number"},
                        "subtotal": {"type": "number"},
                    }
                }
            }
        }
    }


def _resposta_lista(schema_ref):
    return {
        "200": {
            "description": "Lista com paginacao",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "dados": {
                                "type": "array",
                                "items": {"$ref": f"#/components/schemas/{schema_ref}"}
                            },
                            "paginacao": {
                                "$ref": "#/components/schemas/Paginacao"
                            }
                        }
                    }
                }
            }
        }
    }


def _resposta_recurso(schema_ref, codigo="200", descricao="OK"):
    return {
        codigo: {
            "description": descricao,
            "content": {
                "application/json": {
                    "schema": {"$ref": f"#/components/schemas/{schema_ref}"}
                }
            }
        }
    }


def _respostas_erros_comuns(*codigos):
    """Retorna respostas de erro para os codigos especificados."""
    mapa = {
        400: "Requisicao invalida (payload malformado)",
        404: "Recurso nao encontrado",
        409: "Conflito (violacao de constraint unico)",
        500: "Erro interno do servidor",
    }
    return {
        str(c): {
            "description": mapa.get(c, "Erro"),
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Erro"}
                }
            }
        } for c in codigos
    }


def gerar_openapi(config) -> dict:
    """Gera a spec OpenAPI 3.0 completa."""
    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": config.API_TITLE,
            "version": config.API_VERSION,
            "description": config.API_DESCRICAO,
            "contact": {
                "name": "PharmaSystem",
                "url": "https://github.com/lucasverissimo/pharma-system"
            }
        },
        "servers": [
            {"url": f"http://{config.HOST}:{config.PORT}", "description": "Servidor local"}
        ],
        "tags": [
            {"name": "Health", "description": "Health checks e metadados"},
            {"name": "Filiais", "description": "CRUD de filiais da rede"},
            {"name": "Categorias", "description": "CRUD de categorias de produtos"},
            {"name": "Produtos", "description": "CRUD de produtos"},
            {"name": "Clientes", "description": "CRUD de clientes"},
            {"name": "Vendas", "description": "Consulta e registro de vendas"},
            {"name": "Indicadores", "description": "Metricas agregadas de negocio"},
        ],
        "paths": {},
        "components": {
            "schemas": {
                "Erro": _schema_erro(),
                "Paginacao": _schema_paginacao(),
                "Filial": _schema_filial(),
                "Categoria": _schema_categoria(),
                "Produto": _schema_produto(),
                "Cliente": _schema_cliente(),
                "Venda": _schema_venda(),
            }
        }
    }

    paths = spec["paths"]

    # === Health ===
    paths["/api/health"] = {
        "get": {
            "tags": ["Health"],
            "summary": "Health check simples",
            "responses": {"200": {"description": "OK"}},
        }
    }
    paths["/api/health/db"] = {
        "get": {
            "tags": ["Health"],
            "summary": "Health check com banco",
            "responses": {"200": {"description": "OK"}, "500": {"description": "Banco fora"}},
        }
    }
    paths["/api/versao"] = {
        "get": {
            "tags": ["Health"],
            "summary": "Metadados da API",
            "responses": {"200": {"description": "OK"}},
        }
    }

    # === Filiais (CRUD) ===
    _adicionar_crud(paths, "filiais", "Filial", "Filiais",
                     filtros_get=[
                         {"name": "cidade", "in": "query", "schema": {"type": "string"}},
                         {"name": "estado", "in": "query", "schema": {"type": "string"}},
                         {"name": "ativa", "in": "query", "schema": {"type": "boolean"}},
                     ])

    # === Categorias (CRUD sem paginacao) ===
    paths["/api/categorias"] = {
        "get": {
            "tags": ["Categorias"],
            "summary": "Listar todas as categorias",
            "responses": _resposta_lista("Categoria"),
        },
        "post": {
            "tags": ["Categorias"],
            "summary": "Criar categoria",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Categoria"},
                        "example": {"nome": "Homeopaticos", "descricao": "Medicamentos naturais"}
                    }
                }
            },
            "responses": {
                **_resposta_recurso("Categoria", "201", "Categoria criada"),
                **_respostas_erros_comuns(400, 409),
            }
        }
    }
    paths["/api/categorias/{id}"] = _crud_por_id("Categoria", "Categorias")

    # === Produtos ===
    _adicionar_crud(paths, "produtos", "Produto", "Produtos",
                     filtros_get=[
                         {"name": "categoria_id", "in": "query", "schema": {"type": "integer"}},
                         {"name": "fabricante", "in": "query", "schema": {"type": "string"}},
                         {"name": "nome", "in": "query", "schema": {"type": "string"}},
                         {"name": "preco_min", "in": "query", "schema": {"type": "number"}},
                         {"name": "preco_max", "in": "query", "schema": {"type": "number"}},
                         {"name": "exige_receita", "in": "query", "schema": {"type": "boolean"}},
                         {"name": "ativo", "in": "query", "schema": {"type": "boolean"}},
                     ])

    # === Clientes ===
    _adicionar_crud(paths, "clientes", "Cliente", "Clientes",
                     filtros_get=[
                         {"name": "cidade", "in": "query", "schema": {"type": "string"}},
                         {"name": "estado", "in": "query", "schema": {"type": "string"}},
                         {"name": "nome", "in": "query", "schema": {"type": "string"}},
                         {"name": "cpf", "in": "query", "schema": {"type": "string"}},
                     ])

    # === Vendas ===
    paths["/api/vendas"] = {
        "get": {
            "tags": ["Vendas"],
            "summary": "Listar vendas com filtros",
            "parameters": [
                {"name": "filial_id", "in": "query", "schema": {"type": "integer"}},
                {"name": "cliente_id", "in": "query", "schema": {"type": "integer"}},
                {"name": "status", "in": "query", "schema": {"type": "string", "enum": ["CONCLUIDA", "CANCELADA", "PENDENTE"]}},
                {"name": "data_inicio", "in": "query", "schema": {"type": "string", "format": "date"}},
                {"name": "data_fim", "in": "query", "schema": {"type": "string", "format": "date"}},
                {"name": "pagina", "in": "query", "schema": {"type": "integer", "default": 1}},
                {"name": "por_pagina", "in": "query", "schema": {"type": "integer", "default": 20}},
            ],
            "responses": _resposta_lista("Venda"),
        },
        "post": {
            "tags": ["Vendas"],
            "summary": "Registrar nova venda (com itens)",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Venda"},
                        "example": {
                            "filial_id": 1,
                            "cliente_id": 5,
                            "forma_pagamento": "PIX",
                            "desconto": 0,
                            "itens": [
                                {"produto_id": 10, "quantidade": 2},
                                {"produto_id": 15, "quantidade": 1, "preco_unitario": 25.50}
                            ]
                        }
                    }
                }
            },
            "responses": {
                **_resposta_recurso("Venda", "201", "Venda criada"),
                **_respostas_erros_comuns(400, 409),
            }
        }
    }
    paths["/api/vendas/{id}"] = {
        "get": {
            "tags": ["Vendas"],
            "summary": "Buscar venda por ID (com itens)",
            "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
            "responses": {**_resposta_recurso("Venda"), **_respostas_erros_comuns(404)}
        }
    }
    paths["/api/vendas/{id}/cancelar"] = {
        "post": {
            "tags": ["Vendas"],
            "summary": "Cancelar uma venda (soft cancel)",
            "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
            "responses": {
                "200": {"description": "Venda cancelada"},
                **_respostas_erros_comuns(404, 409),
            }
        }
    }

    # === Indicadores ===
    paths["/api/indicadores/kpis-gerais"] = {
        "get": {
            "tags": ["Indicadores"],
            "summary": "KPIs principais da rede",
            "responses": {"200": {"description": "OK"}},
        }
    }
    paths["/api/indicadores/faturamento-mensal"] = {
        "get": {
            "tags": ["Indicadores"],
            "summary": "Faturamento agregado por mes",
            "parameters": [
                {"name": "ano", "in": "query", "schema": {"type": "integer"}},
                {"name": "limite", "in": "query", "schema": {"type": "integer", "default": 24}},
            ],
            "responses": {"200": {"description": "OK"}},
        }
    }
    paths["/api/indicadores/top-produtos"] = {
        "get": {
            "tags": ["Indicadores"],
            "summary": "Top N produtos",
            "parameters": [
                {"name": "limite", "in": "query", "schema": {"type": "integer", "default": 10}},
                {"name": "ordem", "in": "query", "schema": {"type": "string", "enum": ["faturamento", "quantidade"]}},
            ],
            "responses": {"200": {"description": "OK"}},
        }
    }
    paths["/api/indicadores/top-filiais"] = {
        "get": {
            "tags": ["Indicadores"],
            "summary": "Ranking de filiais por faturamento",
            "parameters": [{"name": "limite", "in": "query", "schema": {"type": "integer", "default": 10}}],
            "responses": {"200": {"description": "OK"}},
        }
    }
    paths["/api/indicadores/faturamento-por-categoria"] = {
        "get": {
            "tags": ["Indicadores"],
            "summary": "Faturamento por categoria",
            "responses": {"200": {"description": "OK"}},
        }
    }
    paths["/api/indicadores/formas-pagamento"] = {
        "get": {
            "tags": ["Indicadores"],
            "summary": "Distribuicao por forma de pagamento",
            "responses": {"200": {"description": "OK"}},
        }
    }

    return spec


def _adicionar_crud(paths: dict, recurso: str, schema_ref: str, tag: str,
                     filtros_get: list = None):
    """Adiciona endpoints CRUD padrao para um recurso."""
    filtros_get = filtros_get or []
    parametros_paginacao = [
        {"name": "pagina", "in": "query", "schema": {"type": "integer", "default": 1}},
        {"name": "por_pagina", "in": "query", "schema": {"type": "integer", "default": 20}},
    ]

    paths[f"/api/{recurso}"] = {
        "get": {
            "tags": [tag],
            "summary": f"Listar {recurso} com filtros e paginacao",
            "parameters": filtros_get + parametros_paginacao,
            "responses": _resposta_lista(schema_ref),
        },
        "post": {
            "tags": [tag],
            "summary": f"Criar {recurso[:-1]}",  # remove o "s" final
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": f"#/components/schemas/{schema_ref}"}
                    }
                }
            },
            "responses": {
                **_resposta_recurso(schema_ref, "201", f"{schema_ref} criado"),
                **_respostas_erros_comuns(400, 409),
            }
        }
    }
    paths[f"/api/{recurso}/{{id}}"] = _crud_por_id(schema_ref, tag)


def _crud_por_id(schema_ref: str, tag: str):
    return {
        "get": {
            "tags": [tag],
            "summary": f"Buscar {schema_ref} por ID",
            "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
            "responses": {**_resposta_recurso(schema_ref), **_respostas_erros_comuns(404)}
        },
        "put": {
            "tags": [tag],
            "summary": f"Atualizar {schema_ref}",
            "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
            "requestBody": {
                "required": True,
                "content": {"application/json": {
                    "schema": {"$ref": f"#/components/schemas/{schema_ref}"}
                }}
            },
            "responses": {
                **_resposta_recurso(schema_ref),
                **_respostas_erros_comuns(400, 404, 409),
            }
        },
        "delete": {
            "tags": [tag],
            "summary": f"Deletar {schema_ref}",
            "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
            "responses": {
                "204": {"description": "Deletado"},
                **_respostas_erros_comuns(404, 409),
            }
        }
    }
