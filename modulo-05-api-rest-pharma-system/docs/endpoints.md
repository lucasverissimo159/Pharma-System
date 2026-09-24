# Endpoints da API

Total: **37 endpoints** (mais que os 15 pedidos pela apostila).

## Convenções

- **URL base:** `http://localhost:5000/api`
- **Content-Type:** `application/json` para POST/PUT
- **Códigos HTTP:**
  - `200 OK` — sucesso em GET/PUT
  - `201 Created` — sucesso em POST
  - `204 No Content` — sucesso em DELETE
  - `400 Bad Request` — payload inválido
  - `404 Not Found` — recurso não encontrado
  - `405 Method Not Allowed` — método inválido para a rota
  - `409 Conflict` — violação de unicidade ou integridade referencial
  - `500 Internal Server Error` — erro não previsto

## Formato de erro

Todo erro retorna no formato:
```json
{
  "erro": "requisicao_invalida",
  "mensagem": "Dados invalidos",
  "status": 400,
  "detalhes": {
    "campos": {
      "cpf": "CPF invalido (digito verificador incorreto)"
    }
  }
}
```

## Formato de listagem paginada

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

---

## Endpoints

### 🩺 Health (3)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/health` | Healthcheck simples |
| GET | `/api/health/db` | Healthcheck com conexão ao banco |
| GET | `/api/versao` | Metadados da API |

### 🏢 Filiais (5)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/filiais` | Listar (com filtros: cidade, estado, ativa) |
| GET | `/api/filiais/{id}` | Buscar por ID |
| POST | `/api/filiais` | Criar |
| PUT | `/api/filiais/{id}` | Atualizar |
| DELETE | `/api/filiais/{id}` | Deletar (bloqueado se tiver vendas) |

### 🏷️ Categorias (5)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/categorias` | Listar todas |
| GET | `/api/categorias/{id}` | Buscar (com contagem de produtos) |
| POST | `/api/categorias` | Criar |
| PUT | `/api/categorias/{id}` | Atualizar |
| DELETE | `/api/categorias/{id}` | Deletar (bloqueado se tiver produtos) |

### 💊 Produtos (5)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/produtos` | Listar (filtros: categoria_id, fabricante, nome, preco_min, preco_max, exige_receita, ativo) |
| GET | `/api/produtos/{id}` | Buscar (com estoque agregado) |
| POST | `/api/produtos` | Criar (valida preco_venda >= preco_custo) |
| PUT | `/api/produtos/{id}` | Atualizar |
| DELETE | `/api/produtos/{id}` | Deletar (bloqueado se tiver vendas) |

### 👥 Clientes (5)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/clientes` | Listar (filtros: cidade, estado, nome, cpf) |
| GET | `/api/clientes/{id}` | Buscar (com resumo de compras) |
| POST | `/api/clientes` | Criar (valida CPF + email) |
| PUT | `/api/clientes/{id}` | Atualizar |
| DELETE | `/api/clientes/{id}` | Deletar (bloqueado se tiver compras) |

### 💰 Vendas (4)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/vendas` | Listar (filtros: filial_id, cliente_id, status, data_inicio, data_fim) |
| GET | `/api/vendas/{id}` | Buscar (com itens aninhados) |
| POST | `/api/vendas` | Criar (transação atômica com itens) |
| POST | `/api/vendas/{id}/cancelar` | Cancelar (soft cancel) |

### 📊 Indicadores (6)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/indicadores/kpis-gerais` | 11 KPIs de alto nível |
| GET | `/api/indicadores/faturamento-mensal` | Série temporal por mês |
| GET | `/api/indicadores/top-produtos` | Ranking de produtos |
| GET | `/api/indicadores/top-filiais` | Ranking de filiais |
| GET | `/api/indicadores/faturamento-por-categoria` | Agregação por categoria |
| GET | `/api/indicadores/formas-pagamento` | Distribuição por pagamento |

### 📖 Documentação (3)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/` | Índice de recursos |
| GET | `/api/docs` | Swagger UI interativa |
| GET | `/api/openapi.json` | Especificação OpenAPI 3.0 |

---

## Query Params comuns

### Paginação (todos os `GET` de listagem)
- `pagina` — página atual (default: 1)
- `por_pagina` — itens por página (default: 20, max: 100)

### Filtros por texto
- `nome`, `fabricante` — busca com `LIKE %valor%` (case-sensitive no SQLite)

### Filtros por valor
- `preco_min`, `preco_max` — inclusivos
- `data_inicio`, `data_fim` — formato YYYY-MM-DD (data_fim inclusiva)

---

## Validações destacadas

### CPF
Valida formato **e** dígitos verificadores. Rejeita CPFs com todos os dígitos iguais.
```
✓ 111.444.777-35    (dígitos verificadores corretos)
✗ 111.111.111-11    (todos iguais)
✗ 123.456.789-01    (dígitos verificadores errados)
```

### Email
Regex simples: `[^@\s]+@[^@\s]+\.[^@\s]+`

### UF
Apenas as 27 UFs brasileiras. Case-insensitive na entrada, maiúsculas na saída.

### Forma de pagamento
Whitelist: `PIX`, `DINHEIRO`, `DEBITO`, `CREDITO`, `CONVENIO`.

### Status de venda
Whitelist: `CONCLUIDA`, `CANCELADA`, `PENDENTE`.
