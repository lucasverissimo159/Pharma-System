# Exemplos com `curl`

Todos os exemplos assumem a API rodando em `http://localhost:5000`.

Para começar:
```bash
python scripts/executar_api.py
```

Em outro terminal, cole os comandos abaixo.

---

## Health & Metadados

```bash
# Saúde da API
curl http://localhost:5000/api/health

# Saúde da API + banco
curl http://localhost:5000/api/health/db

# Metadados da versão
curl http://localhost:5000/api/versao
```

---

## Filiais

```bash
# Listar todas
curl http://localhost:5000/api/filiais

# Filtrar por estado + paginação
curl "http://localhost:5000/api/filiais?estado=MG&pagina=1&por_pagina=5"

# Buscar por ID
curl http://localhost:5000/api/filiais/1

# Criar filial (POST + JSON)
curl -X POST http://localhost:5000/api/filiais \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "FIL050",
    "nome": "PharmaMinas Ipatinga",
    "cidade": "Ipatinga",
    "estado": "MG"
  }'

# Atualizar (PUT — parcial ou total)
curl -X PUT http://localhost:5000/api/filiais/16 \
  -H "Content-Type: application/json" \
  -d '{"ativa": false}'

# Deletar
curl -X DELETE http://localhost:5000/api/filiais/16

# 404 - filial que não existe
curl -i http://localhost:5000/api/filiais/999

# 409 - deletar filial com vendas
curl -i -X DELETE http://localhost:5000/api/filiais/1

# 400 - UF inválida
curl -i -X POST http://localhost:5000/api/filiais \
  -H "Content-Type: application/json" \
  -d '{"codigo":"X","nome":"x","cidade":"x","estado":"XX"}'
```

---

## Produtos

```bash
# Buscar por nome
curl "http://localhost:5000/api/produtos?nome=Dipirona"

# Filtros combinados (categoria + faixa de preço + receita)
curl "http://localhost:5000/api/produtos?categoria_id=1&preco_max=50&exige_receita=false"

# Produto com estoque agregado
curl http://localhost:5000/api/produtos/1

# Criar produto
curl -X POST http://localhost:5000/api/produtos \
  -H "Content-Type: application/json" \
  -d '{
    "codigo_barras": "7891111111111",
    "nome": "Vitamina D 2000UI 30cp",
    "categoria_id": 8,
    "fabricante": "Vitaminex",
    "preco_custo": 25.00,
    "preco_venda": 55.90
  }'

# Validação: preco_venda < preco_custo
curl -i -X POST http://localhost:5000/api/produtos \
  -H "Content-Type: application/json" \
  -d '{"codigo_barras":"999","nome":"x","categoria_id":1,"preco_custo":100,"preco_venda":50}'
```

---

## Clientes

```bash
# Buscar por nome (LIKE)
curl "http://localhost:5000/api/clientes?nome=Silva"

# Buscar por CPF (aceita com ou sem pontuação)
curl "http://localhost:5000/api/clientes?cpf=123.456.789-01"
curl "http://localhost:5000/api/clientes?cpf=12345678901"

# Cliente por ID (com resumo de compras)
curl http://localhost:5000/api/clientes/1

# Criar cliente
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Maria Fernanda Silva",
    "cpf": "111.444.777-35",
    "email": "maria@example.com",
    "cidade": "Montes Claros",
    "estado": "MG"
  }'

# Validação: CPF inválido (dígito verificador errado)
curl -i -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome":"x","cpf":"111.111.111-11"}'
```

---

## Vendas

```bash
# Vendas de uma filial num período
curl "http://localhost:5000/api/vendas?filial_id=1&data_inicio=2026-06-01&data_fim=2026-06-30"

# Buscar venda (com itens aninhados)
curl http://localhost:5000/api/vendas/1

# Criar venda com múltiplos itens
curl -X POST http://localhost:5000/api/vendas \
  -H "Content-Type: application/json" \
  -d '{
    "filial_id": 1,
    "cliente_id": 5,
    "forma_pagamento": "PIX",
    "desconto": 0,
    "itens": [
      {"produto_id": 1, "quantidade": 2},
      {"produto_id": 5, "quantidade": 1, "preco_unitario": 25.90}
    ]
  }'

# Cancelar venda
curl -X POST http://localhost:5000/api/vendas/1501/cancelar

# Erro: forma de pagamento inválida
curl -i -X POST http://localhost:5000/api/vendas \
  -H "Content-Type: application/json" \
  -d '{"filial_id":1,"forma_pagamento":"BOLETO","itens":[{"produto_id":1,"quantidade":1}]}'
```

---

## Indicadores

```bash
# KPIs gerais (snapshot da rede)
curl http://localhost:5000/api/indicadores/kpis-gerais | python3 -m json.tool

# Faturamento mensal (todos os meses)
curl http://localhost:5000/api/indicadores/faturamento-mensal | python3 -m json.tool

# Faturamento de um ano específico
curl "http://localhost:5000/api/indicadores/faturamento-mensal?ano=2026"

# Top 5 produtos por faturamento
curl "http://localhost:5000/api/indicadores/top-produtos?limite=5"

# Top 5 produtos por unidades vendidas
curl "http://localhost:5000/api/indicadores/top-produtos?limite=5&ordem=quantidade"

# Top 10 filiais
curl "http://localhost:5000/api/indicadores/top-filiais?limite=10"

# Faturamento por categoria
curl http://localhost:5000/api/indicadores/faturamento-por-categoria

# Distribuição por forma de pagamento
curl http://localhost:5000/api/indicadores/formas-pagamento
```

---

## Documentação Interativa

O Swagger UI serve como documentação **e** interface de teste:

- **Swagger UI:** http://localhost:5000/api/docs
- **Spec OpenAPI:** http://localhost:5000/api/openapi.json

Clique em qualquer endpoint no Swagger UI, "Try it out", preencha os parâmetros e "Execute" — funciona sem sair do navegador.
