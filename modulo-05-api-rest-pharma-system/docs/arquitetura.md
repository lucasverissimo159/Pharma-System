# Arquitetura da API

## Visão Geral

API REST em **Flask puro** (sem ORM, sem plugins de Swagger) para o PharmaSystem. O objetivo é mostrar os **fundamentos** de uma API REST profissional sem depender de "mágica" de framework.

## Camadas

```
      HTTP Request
          │
          ▼
    ┌──────────┐
    │  Routes  │  ← Blueprints (um arquivo por recurso)
    │  (HTTP)  │     Extrai query params, valida payload
    └────┬─────┘     Chama serviços ou banco direto
         │
         ├──────────────────┐
         ▼                  ▼
    ┌──────────┐      ┌──────────┐
    │ Services │      │ Database │  ← sqlite3 nativo
    │ (Domain) │◀─────│  (SQL)   │     Uma conexão por request
    └──────────┘      └──────────┘
         │
         │
         ▼
    ┌──────────┐
    │ Schemas  │  ← Serializa row → dict
    │  (JSON)  │     Valida payload → erros
    └────┬─────┘
         │
         ▼
      HTTP Response (JSON)
```

## Estrutura de pastas

```
app/
├── __init__.py         factory create_app(): monta a app Flask
├── config.py           Config: valores lidos de env vars com defaults
├── database.py         obter_conexao(): SQLite por request via flask.g
├── errors.py           Handlers globais + ErroAPI custom + NaoEncontradoError, etc
├── validators.py       CPF, email, UF, forma_pagamento — reutilizáveis
├── openapi_spec.py     Gera dict OpenAPI 3.0 programaticamente
├── routes/             1 blueprint por recurso
│   ├── health.py
│   ├── filiais.py
│   ├── categorias.py
│   ├── produtos.py
│   ├── clientes.py
│   ├── vendas.py
│   ├── indicadores.py
│   └── docs.py         Swagger UI (via CDN) + OpenAPI JSON
├── schemas/            Serialização + validação (sem Marshmallow)
│   ├── filial.py
│   ├── categoria.py
│   ├── produto.py
│   ├── cliente.py
│   └── venda.py
└── services/           Lógica de negócio (agregações SQL complexas)
    └── indicadores.py
```

## Decisões de design

### 1. Por que Flask puro sem SQLAlchemy?

**Motivo:** módulo pedagógico. O objetivo é ver os fundamentos:
- Uma query SQL por rota, escrita à mão — você entende o que acontece
- Sem "mágica" — cada erro é rastreável
- Dependência única: Flask (o mínimo)

**Trade-off:** em produção real com 50+ modelos, SQLAlchemy pouparia tempo. Aqui, os 6 recursos cabem confortavelmente em SQL puro.

### 2. Por que sqlite3, não MySQL/PostgreSQL?

**Motivo:** roda em qualquer máquina sem instalação. O SQL usado é padrão — se você trocar para PostgreSQL, precisa mudar:
- Nada nas queries (SQL padrão)
- Apenas `sqlite3.connect(caminho)` → `psycopg2.connect(dsn)` em `database.py`
- Autoincrement muda de `AUTOINCREMENT` para `SERIAL` no schema.sql

### 3. Por que sem Marshmallow?

Serializar `sqlite3.Row` → `dict` é 1 linha. Validar payloads é uma função simples. Marshmallow é ótimo para APIs complexas com relacionamentos aninhados profundos — aqui seria excessivo.

### 4. Por que OpenAPI escrito à mão?

**Motivo:** transparência. Frameworks como Flask-Smorest geram OpenAPI a partir de docstrings ou decoradores, o que é conveniente mas esconde o que a spec realmente é. Aqui você vê **exatamente** o JSON que o Swagger consome — didático.

**Alternativa em produção:** `flask-smorest` ou `flasgger` para gerar automaticamente.

### 5. Blueprints em vez de rotas planas

Cada recurso é um Blueprint próprio (`bp = Blueprint("filiais", ...)`) registrado em `routes/__init__.py`. Isso permite:
- Adicionar/remover recursos sem tocar em outros arquivos
- Prefixo comum (`/api/filiais/...`) declarado uma vez
- Testar cada blueprint isoladamente

### 6. Conexão SQLite por request

```python
def obter_conexao():
    if "db_conn" not in g:
        g.db_conn = sqlite3.connect(cfg.DATABASE)
        g.db_conn.row_factory = sqlite3.Row
    return g.db_conn
```

- Uma conexão por request (armazenada em `flask.g`)
- Fechada automaticamente no `teardown_appcontext`
- `row_factory = sqlite3.Row` permite acesso `row["nome"]`

Em produção com carga alta, usar um **connection pool** (ex: SQLAlchemy engine ou pool nativo do psycopg2).

### 7. Serviços separados de rotas

Rotas cuidam de HTTP (parâmetros, status codes). Serviços cuidam de lógica de negócio (SQL, agregações).

Exemplo:
```python
# route
@bp.route("/kpis-gerais")
def kpis_gerais():
    conn = obter_conexao()
    return jsonify(srv.kpis_gerais(conn))  # ← delega para service

# service
def kpis_gerais(conn):  # sem HTTP, sem Flask — pura lógica
    cur = conn.execute("SELECT SUM(...) FROM ...")
    return {"faturamento_total": ...}
```

Vantagem: consegue **testar o serviço** sem subir a API.

### 8. Erros centralizados via exceptions custom

```python
raise NaoEncontradoError("filial", 999)
raise ValidacaoError({"cpf": "invalido"})
raise ConflitoError("cpf ja cadastrado")
```

Cada uma vira automaticamente um HTTP com status + JSON formatado — sem precisar `try/except` em cada rota.

## Fluxo de uma request típica

```
1. Cliente:                       POST /api/produtos  { ... }

2. Flask roteia para:             criar_produto() em routes/produtos.py

3. Rota extrai payload:           payload = request.get_json()

4. Chama validador:               erros = validar_payload_produto(payload)
                                  → se erros: raise ValidacaoError(erros) → 400

5. Chama banco:                   conn = obter_conexao()
                                  cur = conn.execute("INSERT ...", (...))
                                  → se UNIQUE conflict: raise ConflitoError → 409

6. Serializa resposta:            return jsonify(serializar_produto(row)), 201

7. Flask fecha conexão:           teardown_appcontext → conn.close()
```

## Testando

O smoke test `scripts/testar_endpoints.py` usa o `test_client` do Flask (sem subir servidor):

```python
app = create_app(ConfigTeste())
client = app.test_client()
resp = client.get("/api/produtos")
assert resp.status_code == 200
```

**60 testes cobrem:** happy paths + validações + conflitos + 404 + 405 + auth futura + docs. Todos rodam em ~1 segundo.

## Migrando para produção

Passos para levar essa API para produção:

1. **WSGI server:** trocar `app.run(debug=True)` por Gunicorn ou uWSGI.
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'
   ```

2. **Banco de produção:** trocar SQLite por PostgreSQL. Ajustar `database.py` para usar `psycopg2` com pool.

3. **HTTPS:** por trás de Nginx/Traefik com TLS.

4. **Autenticação:** hoje qualquer request funciona. Adicionar JWT via `flask-jwt-extended` ou API Key via header.

5. **Rate limiting:** `flask-limiter` para proteger contra abuso.

6. **CORS:** `flask-cors` se algum frontend consumir de outro domínio.

7. **Logging estruturado:** JSON logs para observabilidade (ex: `python-json-logger`).

8. **Métricas:** `prometheus-flask-exporter` para expor `/metrics`.

9. **CI/CD:** pytest no pipeline + deploy automatizado.

10. **Docker:** dockerfile com Python slim + gunicorn.
