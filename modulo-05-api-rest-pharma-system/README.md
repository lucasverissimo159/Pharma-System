# Módulo 05 — API REST em Flask

**PharmaSystem — Semana 5 de 12 do portfólio**

API REST completa em **Flask puro** (sem ORM, sem plugins de Swagger) para o PharmaSystem. Expõe filiais, categorias, produtos, clientes, vendas e indicadores de negócio como recursos consumíveis por qualquer cliente HTTP (curl, Postman, JS, app mobile).

---

## Números

Rodando localmente com o banco populado dos módulos anteriores:

| Métrica | Valor |
|---|---|
| Endpoints registrados | **37** (a apostila pede ≥15) |
| Recursos REST | 6 (filiais, categorias, produtos, clientes, vendas, indicadores) |
| Testes automáticos passando | **60/60** ✅ |
| Faturamento retornado nos indicadores | R$ 226.548,60 |
| Dependências externas | 1 (só Flask) |
| Documentação | Swagger UI interativa em `/api/docs` |

---

## Decisão importante: Flask puro sem ORM

A apostila sugere Flask com SQLAlchemy + Marshmallow + Flask-Smorest. Escolhi ir para os fundamentos:

- **Flask puro** para as rotas
- **sqlite3 nativo** (mesmo do Módulo 04) para o banco
- **Validação/serialização manuais** com funções em `app/schemas/`
- **OpenAPI 3.0 escrito à mão** em `app/openapi_spec.py`
- **Swagger UI via CDN** carregando o `openapi.json` da própria API

Motivos:
1. **Didático** — você vê cada consulta SQL, cada validação, cada serialização. Sem "mágica".
2. **Menos dependências** — `pip install flask` e pronto.
3. **Portável** — roda em qualquer máquina sem esperar `psycopg2` ou `Marshmallow` instalarem.

Se você quiser exercitar SQLAlchemy depois, é um refactor natural. Aprende os fundamentos aqui e depois adiciona a camada.

---

## Estrutura

```
modulo-05-api-rest-pharma-system/
├── README.md                        (este arquivo)
├── COMO_ESTUDAR.md                  Roteiro de reversa (7 dias)
├── requirements.txt                 Só flask
├── .gitignore
│
├── app/
│   ├── __init__.py                  Factory create_app()
│   ├── config.py                    Config lida de env vars
│   ├── database.py                  obter_conexao() via flask.g
│   ├── errors.py                    ErroAPI, NaoEncontradoError, ValidacaoError, ConflitoError
│   ├── validators.py                CPF (com DV), email, UF, forma_pagamento
│   ├── openapi_spec.py              Gera OpenAPI 3.0 programaticamente
│   ├── routes/                      Blueprints (1 por recurso)
│   │   ├── health.py                /health, /health/db, /versao
│   │   ├── filiais.py               CRUD (5 endpoints)
│   │   ├── categorias.py            CRUD (5 endpoints)
│   │   ├── produtos.py              CRUD com filtros (5 endpoints)
│   │   ├── clientes.py              CRUD (5 endpoints)
│   │   ├── vendas.py                GET, POST com itens, cancelar (4 endpoints)
│   │   ├── indicadores.py           6 endpoints agregados
│   │   └── docs.py                  Swagger UI + openapi.json + raiz
│   ├── schemas/                     Serializar/validar por recurso
│   │   ├── filial.py, categoria.py, produto.py,
│   │   └── cliente.py, venda.py
│   └── services/
│       └── indicadores.py           SQL agregations (KPIs, top produtos, top filiais...)
│
├── db/
│   ├── schema.sql                   DDL das 7 tabelas
│   ├── pharma.db                    SQLite 528KB (gerado por inicializar_banco.py)
│   └── dados/                       8 CSVs de origem (herdados do Módulo 03)
│
├── scripts/
│   ├── inicializar_banco.py         Popula SQLite dos CSVs
│   ├── executar_api.py              Roda o servidor
│   └── testar_endpoints.py          Smoke test (60 casos)
│
├── docs/
│   ├── arquitetura.md               Design decisions
│   ├── endpoints.md                 Lista dos 37 endpoints
│   ├── exemplos_curl.md             Exemplos práticos
│   └── postman_collection.json      Import direto no Postman
│
└── tests/                           (reservado para pytest futuro)
```

---

## Como usar

### 1. Instalar

```bash
pip install -r requirements.txt   # instala apenas flask
```

### 2. Inicializar o banco

```bash
python scripts/inicializar_banco.py
```

Isso cria `db/pharma.db` (528 KB) com 7 tabelas populadas: 15 filiais, 71 produtos, 200 clientes, 1500 vendas, 3253 itens, faturamento total R$ 226.548,60.

### 3. Rodar a API

```bash
python scripts/executar_api.py
```

Você verá:
```
======================================================================
  PharmaSystem API v1.0.0
======================================================================
  Banco: /caminho/db/pharma.db
  URL:   http://127.0.0.1:5000
  Docs:  http://127.0.0.1:5000/api/docs
  Debug: False
======================================================================
```

### 4. Abrir o Swagger UI

http://localhost:5000/api/docs

Você vai ver a documentação interativa com todos os endpoints. Clique em qualquer um, "Try it out" → "Execute" e teste sem sair do navegador.

### 5. Testar com curl

```bash
# KPIs gerais
curl http://localhost:5000/api/indicadores/kpis-gerais

# Top 5 filiais
curl "http://localhost:5000/api/indicadores/top-filiais?limite=5"

# Criar uma venda
curl -X POST http://localhost:5000/api/vendas \
  -H "Content-Type: application/json" \
  -d '{
    "filial_id": 1,
    "cliente_id": 5,
    "forma_pagamento": "PIX",
    "itens": [
      {"produto_id": 1, "quantidade": 2},
      {"produto_id": 5, "quantidade": 1}
    ]
  }'
```

Ver mais em `docs/exemplos_curl.md`.

### 6. Rodar o smoke test (sem precisar do servidor rodando)

```bash
python scripts/testar_endpoints.py
```

60 testes automatizados em ~1 segundo — usa o `test_client` do Flask.

---

## Endpoints (resumo)

| Recurso | Endpoints | Destaque |
|---|---|---|
| **Health** (3) | GET `/api/health`, `/api/health/db`, `/api/versao` | Prontidão para load balancer |
| **Filiais** (5) | CRUD completo | Filtros: cidade, estado, ativa |
| **Categorias** (5) | CRUD completo | Contagem de produtos por categoria |
| **Produtos** (5) | CRUD completo | 7 filtros combinados + validação preço_venda ≥ custo |
| **Clientes** (5) | CRUD completo | CPF com dígito verificador + resumo de compras |
| **Vendas** (4) | GET, POST, cancelar | Transação atômica: venda + itens em um só request |
| **Indicadores** (6) | Agregações SQL | KPIs, faturamento mensal, top produtos, top filiais |
| **Docs** (3) | Swagger UI + OpenAPI | Documentação interativa |

Lista completa e detalhada em `docs/endpoints.md`.

---

## O que a API faz de bonito

### 1. Validação estruturada

CPF com dígito verificador, e-mail regex, UF whitelist (27 UFs), forma de pagamento whitelist, `preco_venda >= preco_custo` — tudo com mensagens de erro específicas por campo:

```json
{
  "erro": "requisicao_invalida",
  "mensagem": "Dados invalidos",
  "status": 400,
  "detalhes": {
    "campos": {
      "cpf": "CPF invalido (digito verificador incorreto)",
      "email": "Email invalido"
    }
  }
}
```

### 2. Integridade referencial

Não permite deletar filial que tem vendas, produto que tem vendas, categoria que tem produtos, cliente que tem compras. Retorna 409 com o número de dependências.

### 3. Paginação em tudo

```json
{
  "dados": [...],
  "paginacao": {
    "pagina": 1,
    "por_pagina": 20,
    "total": 71,
    "total_paginas": 4
  }
}
```

Configurável via query params (`pagina`, `por_pagina`, máximo 100).

### 4. Vendas transacionais

Uma venda com múltiplos itens em um único POST — se qualquer item falhar, rollback total. Preço unitário puxado automaticamente do produto se omitido.

### 5. Indicadores agregados

- **KPIs gerais** — 11 métricas de alto nível em uma única query
- **Faturamento mensal** — série temporal para gráfico
- **Top produtos** — ranking por faturamento ou quantidade
- **Top filiais** — ranking com percentual do total
- **Faturamento por categoria** — com margem % calculada
- **Formas de pagamento** — distribuição

### 6. Swagger UI real (não mock)

O `openapi.json` é gerado programaticamente com **7 schemas de componentes reutilizáveis** (Erro, Paginação, Filial, Categoria, Produto, Cliente, Venda) e todas as rotas documentadas com parâmetros, exemplos e respostas de erro.

### 7. Health checks para produção

`/api/health` (simples) e `/api/health/db` (com verificação de conexão) — o que um load balancer precisa.

### 8. Erros centralizados

Todo erro passa pelo mesmo handler global. Nenhuma rota precisa de `try/except` para erros HTTP comuns — basta `raise NaoEncontradoError("produto", 999)` e o Flask converte automaticamente para `404 { "erro": "nao_encontrado", ... }`.

---

## Prova empírica: 60/60 testes

O `scripts/testar_endpoints.py` é um smoke test que cobre:

- 3 health
- 15 filiais (CRUD + validações + conflitos + 404)
- 5 categorias
- 10 produtos (CRUD + filtros combinados + validação de preço)
- 7 clientes (CPF válido, CPF inválido, e-mail inválido, CPF duplicado)
- 8 vendas (criar com itens, cancelar, forma pagamento inválida, produto inexistente)
- 8 indicadores
- 3 docs
- 2 erros globais (404 na rota, 405 no método)

Roda em **~1 segundo** com `test_client` do Flask (não precisa subir servidor).

---

## Publicação no GitHub

Estrutura sugerida:

```
pharma-system/
├── modulo-01-sql/
├── modulo-02-powerbi/
├── modulo-03-python-pandas/
├── modulo-04-etl/
└── modulo-05-api-rest/       ← este módulo
    ├── app/
    ├── db/
    ├── scripts/
    ├── docs/
    ├── README.md
    └── requirements.txt
```

---

## Post do LinkedIn — Rascunho

> 🚀 Semana 5 do meu portfólio: API REST completa em Flask puro
>
> Construí uma API REST para o PharmaSystem cobrindo 6 recursos e 37 endpoints — mais que os 15 pedidos pelo cronograma. Destaques:
>
> ✅ **Flask puro** (sem ORM) — decisão didática para expor os fundamentos: cada query SQL, cada validação, cada serialização estão explícitas no código.
> ✅ **Swagger UI interativa** em `/api/docs` — OpenAPI 3.0 gerado programaticamente com 7 schemas de componentes reutilizáveis.
> ✅ **60 testes automáticos** cobrindo happy paths + validações + conflitos + 404 + 405 — rodam em 1 segundo com `test_client`.
> ✅ **Validação de CPF com dígito verificador**, integridade referencial (não deleta filial com vendas), paginação em todas as listagens.
> ✅ **Vendas transacionais** — POST com N itens em uma única request, rollback total em caso de erro.
> ✅ **Indicadores agregados** — KPIs, top produtos, top filiais, faturamento mensal, tudo consumível por dashboards.
>
> Dependência única: **Flask** (o mínimo). Roda em qualquer máquina.
>
> Repo: github.com/lucasverissimo/pharma-system
>
> #API #REST #Flask #Backend #Python #EngenhariaDeSistemas #PortfólioDev

Anexe prints do Swagger UI + resultado do smoke test colorido.

---

## Próximos módulos

- **Módulo 06** — Sistema Web (Help Desk) com MVC, templates Jinja2, autenticação
- **Módulos 07+** — ML, Docker, CI/CD

---

## Créditos

- **Autor:** Lucas Veríssimo (UNIMONTES — Engenharia de Sistemas)
- **Assistência técnica:** Claude (Anthropic)
- **Ferramentas:** Python 3.10+, Flask 3, sqlite3 (nativo), Swagger UI (via CDN)
