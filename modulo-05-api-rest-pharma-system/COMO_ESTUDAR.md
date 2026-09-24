# Como Estudar Este Módulo — Roteiro de Engenharia Reversa

Este módulo é sobre **API REST profissional** — os fundamentos que aparecem em qualquer processo seletivo backend. A ideia é reconstruir cada camada olhando o código pronto, sem consultar durante a implementação.

**Carga total:** 10 a 14 horas em 7 dias (~1,5-2h por dia).

---

## Filosofia

Aqui não tem gráfico bonito nem transformação de dados espetacular. O produto final é uma **URL que retorna JSON** — o que a maioria dos backends do mundo faz.

O objetivo é ver **cada camada** com clareza:
- Como uma request HTTP vira função Python
- Como validação estruturada funciona
- Como serializar row de banco → JSON
- Como um erro é convertido para 400/404/409
- Como Swagger é gerado
- Como paginação funciona

---

## Pré-requisitos

- Python 3.10+
- Familiaridade com Flask **ou** disponibilidade para aprender básico em 1h
- Postman ou Insomnia instalado (opcional, curl funciona)
- Ter feito o Módulo 04 ou entender SQLite básico

---

## Setup (10 min)

```bash
cd modulo-05-api-rest-pharma-system

# Ambiente virtual
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows

# Instala só Flask
pip install -r requirements.txt

# Inicializa o banco (528 KB, 7 tabelas)
python scripts/inicializar_banco.py

# Roda a API
python scripts/executar_api.py
```

Abra outro terminal e:
```bash
curl http://localhost:5000/api/health
# {"status": "ok", "timestamp": "2026-..."}
```

Abra o navegador: http://localhost:5000/api/docs — o Swagger UI.

---

## Roteiro de 7 Dias

### Dia 1 — Explorar (1,5h)

**Sem código.**

1. Rode a API (`executar_api.py`) e abra o Swagger UI (30 min):
   - Expanda cada tag (Health, Filiais, Categorias, etc)
   - Clique num GET, "Try it out", "Execute". Observe o request e o response.
   - Tente um POST em `/api/filiais` — quais campos são obrigatórios?
2. Rode o smoke test (`scripts/testar_endpoints.py`) e observe as 60 linhas coloridas (10 min).
3. Leia `docs/arquitetura.md` inteiro (30 min).
4. Leia `docs/endpoints.md` (20 min).

**Entregável mental:** você entende o que a API expõe e como responde.

---

### Dia 2 — Recriar Health + estrutura base do Flask (1,5h)

**Objetivo:** entender factory pattern do Flask.

1. Em `meus_estudos/`, crie do zero:
   - `app/__init__.py` com uma `create_app()` que retorna uma app Flask com `/api/health`
   - `scripts/executar_api.py` que importa e roda
2. Adicione um segundo endpoint `/api/versao` retornando `{"nome": "..", "versao": "1.0"}`.
3. Compare com o meu `app/__init__.py` e `app/routes/health.py`. O que fiz diferente do seu? Por quê?

**Ponto a estudar:** o padrão **application factory** (`create_app()`) é o que permite ter múltiplas instâncias da app para testes. Sem ele, a app é global e você não pode usar `test_client` com configs diferentes.

**Desafio:** faça `/api/health/db` que verifica se o banco está conectado. Retorne 500 se não estiver.

---

### Dia 3 — Recriar CRUD de Filiais (2h)

**Objetivo:** o padrão REST completo em uma entidade.

1. Em `meus_estudos/app/routes/`, crie `filiais.py` do zero com Blueprint e cinco rotas: GET all, GET one, POST, PUT, DELETE.
2. Sem consultar minha versão, implemente:
   - GET com paginação (`?pagina=1&por_pagina=20`)
   - GET com filtros (`?cidade=X&estado=Y`)
   - GET por ID retornando 404 se não achar
   - POST validando campos obrigatórios
   - PUT validando existência antes
   - DELETE bloqueando se tiver vendas associadas
3. Compare com `app/routes/filiais.py`.

**Ponto a estudar (importante):** a **separação route ↔ serializer ↔ validador**:
- Route só cuida do HTTP (extrair params, retornar jsonify)
- Serializer converte `sqlite3.Row` → dict
- Validator recebe dict e retorna erros por campo

Quando essa separação está clara, adicionar novos recursos vira quase copy-paste.

**Desafio:** implemente um endpoint bônus `GET /api/filiais/{id}/estoque` que retorna todos os produtos + quantidades daquela filial.

---

### Dia 4 — Recriar Produtos com filtros combinados (2h)

**Objetivo:** filtros dinâmicos + validação cruzada.

1. Refaça o CRUD de Produtos aplicando o que aprendeu no dia 3.
2. Foco especial: **filtro combinado** (`?categoria_id=1&preco_max=50&exige_receita=false`).

O truque é construir a query SQL dinamicamente:
```python
where = []
params = []
if cat_id:
    where.append("categoria_id = ?")
    params.append(cat_id)
if preco_max:
    where.append("preco_venda <= ?")
    params.append(preco_max)
# ...
where_sql = f"WHERE {' AND '.join(where)}" if where else ""
conn.execute(f"SELECT * FROM produtos {where_sql}", params)
```

Compare com `app/routes/produtos.py`. Note como cada filtro é opcional e independente.

**Ponto a estudar:** validação cruzada. No POST de produto, `preco_venda` precisa ser >= `preco_custo`. Isso não pode ser validado por campo individualmente — precisa olhar ambos. Veja como está em `app/schemas/produto.py`.

**Desafio:** adicione um filtro `?margem_min=X` (produtos com margem percentual >= X). Isso exige calcular no SQL — `WHERE ((preco_venda - preco_custo) / preco_venda) * 100 >= ?`.

---

### Dia 5 — Recriar Vendas (transação atômica) (2h)

**Objetivo:** o endpoint mais complexo — venda + itens em uma request.

1. Estude a estrutura do payload:
```json
{
  "filial_id": 1,
  "cliente_id": 5,
  "forma_pagamento": "PIX",
  "itens": [
    {"produto_id": 10, "quantidade": 2},
    {"produto_id": 15, "quantidade": 1, "preco_unitario": 25.90}
  ]
}
```
2. Refaça o POST /api/vendas passo a passo:
   - Validar payload (com nested validation dos itens)
   - Verificar existência da filial e cliente
   - Buscar preços dos produtos (para calcular subtotais)
   - Verificar que todos os produtos existem
   - INSERT venda + N INSERTs de itens em transação
   - Rollback se qualquer coisa falhar
3. Compare com `app/routes/vendas.py`.

**Ponto a estudar (importante):** transações atômicas em SQLite. Todas as escritas dentro de um `try` — se qualquer uma falhar, `conn.rollback()`. Só depois de todas terem sucesso: `conn.commit()`.

**Ponto a estudar 2:** dependência entre validações. Você não pode validar "produto existe" antes de "filial existe" — a ordem importa porque o usuário vê o primeiro erro. Boa prática: validar campos primeiro, depois relacionamentos.

**Desafio:** adicione um endpoint `POST /api/vendas/{id}/estornar` que reverte uma venda (repõe o estoque, muda status para ESTORNADA).

---

### Dia 6 — Recriar Indicadores + serviços (1,5h)

**Objetivo:** separar HTTP da lógica de negócio.

1. Estude `app/services/indicadores.py`. Note que **não tem nada de Flask** — só recebe uma `conn` e retorna dicts.
2. Isso permite testar sem subir a API:
```python
import sqlite3
from app.services.indicadores import kpis_gerais
conn = sqlite3.connect("db/pharma.db")
conn.row_factory = sqlite3.Row
print(kpis_gerais(conn))
```
3. Refaça `services/indicadores.py` implementando pelo menos 3 dos 6 indicadores (KPIs gerais, top produtos, top filiais).
4. Depois crie o blueprint `routes/indicadores.py` que só chama os serviços.

**Ponto a estudar:** por que separar? Porque a mesma função `kpis_gerais(conn)` pode ser usada:
- Pela API (rota HTTP)
- Por um relatório PDF gerado por um script
- Por um job noturno que salva num cache
- Por um teste unitário

Se ela fosse acoplada ao Flask, cada caso precisaria de código duplicado.

---

### Dia 7 — Recriar OpenAPI + Swagger UI + publicar (1,5h)

**Objetivo:** documentar profissionalmente.

1. Estude `app/openapi_spec.py` — como o dict OpenAPI é construído.
2. Estude `app/routes/docs.py` — como a spec é servida e como o Swagger UI é embutido via CDN.
3. Refaça o `openapi_spec.py` para pelo menos 2 recursos (Filiais e Produtos). Você não precisa cobrir tudo — só entender a estrutura.
4. Verifique no navegador que o Swagger UI renderiza sua versão.

**Ponto a estudar:** OpenAPI 3.0 é um **contrato** entre API e cliente. Frontends podem gerar código automaticamente a partir dele. Mobile apps também. Ter uma spec correta é o padrão profissional.

**Publicação (30 min):**
- Crie `.gitignore` (copie do meu)
- `git init && git add . && git commit -m "Módulo 05 - API REST"`
- Push no GitHub em `pharma-system/modulo-05-api-rest/`
- Post no LinkedIn com prints do Swagger UI + resultado do smoke test

---

## Checklist final

- [ ] API rodando localmente com `executar_api.py`
- [ ] Swagger UI acessível em `/api/docs`
- [ ] Consigo criar/atualizar/deletar filiais via Postman
- [ ] Consigo criar uma venda com itens
- [ ] Entendo por que CPF nulo virou `SEM_CPF` (herança do Módulo 04)
- [ ] Entendo a diferença entre 400, 404, 405, 409
- [ ] Consigo explicar o padrão factory (`create_app()`)
- [ ] Consigo explicar por que services e routes são separados
- [ ] Meu smoke test próprio (versão reduzida) rodando
- [ ] Push no GitHub feito
- [ ] Post no LinkedIn publicado

---

## Armadilhas comuns

**"Meu POST retorna 200 mas devia ser 201"** → esqueceu de retornar tupla `(jsonify(...), 201)`. Sem o segundo elemento, Flask assume 200.

**"Meu handler de erro nunca é chamado"** → verifique se registrou com `@app.errorhandler(MeuErro)` **antes** de rodar a app. E se está fazendo `raise MeuErro(...)`, não `return jsonify(...), 400` (que curto-circuita o handler).

**"Meu Swagger UI abre mas não mostra endpoints"** → a URL do `openapi.json` no HTML está errada, ou o JSON está com erro de sintaxe. Abra o Console do navegador (F12) para ver.

**"CPF válido vira inválido"** → sua função de dígito verificador tem bug. Teste com o clássico "111.444.777-35" (é válido). Ou com o gerador do https://www.4devs.com.br/gerador_de_cpf.

**"Meu SQLite dá error 'database is locked'"** → você abriu uma conexão em outra parte do código e não fechou. Ou está usando threading errado. Confira o `teardown_appcontext`.

**"Passei json_body no POST mas request.get_json() retorna None"** → esqueceu do header `Content-Type: application/json` na request. Ou usou `json.dumps()` como `data=` em vez de `json=` no client.

---

## Recursos gratuitos

- **[Flask Docs](https://flask.palletsprojects.com/)** — canônico, especialmente Blueprints e error handlers
- **[Miguel Grinberg — Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)** — 20 partes, referência completa
- **[Real Python — Flask REST API](https://realpython.com/flask-connexion-rest-api/)** — tutorial passo-a-passo
- **[Swagger Editor](https://editor.swagger.io/)** — cole um YAML/JSON OpenAPI e veja renderizado ao vivo
- **[HTTP Cats](https://http.cat/)** — status codes em gatos (útil pra fixar)
- **[REST API Design Rulebook (livro gratuito online)](https://www.oreilly.com/library/view/rest-api-design/9781449317904/)**

---

## O que você vai saber ao final

- **REST na prática:** recursos, verbos HTTP, status codes, JSON como contrato
- **Flask avançado:** factory pattern, blueprints, `flask.g`, error handlers globais
- **SQL sem ORM:** SELECT com filtros dinâmicos, INSERT com transação, UPSERT
- **Validação:** por campo, cruzada, com mensagens estruturadas
- **Paginação:** offset + limit, contagem total, metadata na resposta
- **OpenAPI 3.0:** components, schemas, refs, tags, examples
- **Swagger UI:** como carregar via CDN, como servir a spec
- **Testes com test_client:** happy path + edge cases + status codes
- **Separação de camadas:** routes vs services vs schemas vs database

**Habilidades diretamente aplicáveis** em qualquer processo seletivo backend júnior/pleno, e em qualquer projeto pessoal futuro que precise expor dados.

**Bons estudos!**
