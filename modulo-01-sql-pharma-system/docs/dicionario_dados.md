# Dicionário de Dados — PharmaSystem

Documentação completa das tabelas do banco de dados do PharmaSystem, incluindo tipos, constraints e regras de negócio.

---

## Convenções

- **PK** = Primary Key (chave primária)
- **FK** = Foreign Key (chave estrangeira)
- **UK** = Unique Key (chave única)
- **NN** = Not Null (obrigatório)
- **DEF** = Valor default
- **CHK** = Check constraint (regra de validação)

---

## 1. Tabela `filiais`

Cadastro das lojas físicas da rede.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | SERIAL | PK | Identificador único |
| codigo | VARCHAR(10) | NN, UK | Código interno (ex: FIL001) |
| nome | VARCHAR(100) | NN | Nome fantasia da filial |
| cidade | VARCHAR(80) | NN | Cidade de localização |
| estado | CHAR(2) | NN, CHK regex `^[A-Z]{2}$` | UF em maiúsculas |
| endereco | VARCHAR(200) |  | Endereço completo |
| telefone | VARCHAR(20) |  | Telefone comercial |
| data_abertura | DATE | NN | Data de inauguração |
| ativa | BOOLEAN | NN, DEF TRUE | Filial em operação? |
| data_criacao | TIMESTAMP | NN, DEF NOW | Data de registro no sistema |

**Regras de negócio:**
- Uma filial inativa não deve receber novas vendas (aplicação valida).
- Código deve seguir padrão `FIL###`.

---

## 2. Tabela `categorias`

Classificação de produtos (medicamentos, higiene, cosméticos, etc).

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | SERIAL | PK | Identificador único |
| nome | VARCHAR(80) | NN, UK | Nome da categoria |
| descricao | TEXT |  | Descrição detalhada |
| data_criacao | TIMESTAMP | NN, DEF NOW | Data de criação |

---

## 3. Tabela `produtos`

Catálogo mestre de produtos comercializados.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | SERIAL | PK | Identificador único |
| codigo_barras | VARCHAR(20) | UK | EAN-13 do produto |
| nome | VARCHAR(150) | NN | Nome comercial |
| categoria_id | INTEGER | NN, FK → categorias(id) | Categoria do produto |
| fabricante | VARCHAR(100) |  | Nome do fabricante |
| preco_custo | DECIMAL(10,2) | NN, CHK ≥ 0 | Preço de custo |
| preco_venda | DECIMAL(10,2) | NN, CHK ≥ preco_custo | Preço de venda ao público |
| estoque_minimo | INTEGER | NN, DEF 10, CHK ≥ 0 | Estoque mínimo antes de repor |
| exige_receita | BOOLEAN | NN, DEF FALSE | Precisa de receita médica? |
| ativo | BOOLEAN | NN, DEF TRUE | Produto disponível para venda? |
| data_cadastro | TIMESTAMP | NN, DEF NOW | Data de cadastro |

**Regras de negócio:**
- `preco_venda` deve ser sempre ≥ `preco_custo` (margem não-negativa).
- Produtos que exigem receita têm controle regulatório (SNGPC — Sistema Nacional de Gerenciamento de Produtos Controlados).
- Ao definir produto como inativo, ele não aparece em novas vendas mas mantém histórico.

---

## 4. Tabela `estoque`

Controle de estoque por produto e filial (relação N:N materializada).

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | SERIAL | PK | Identificador único |
| produto_id | INTEGER | NN, FK → produtos(id) | Produto |
| filial_id | INTEGER | NN, FK → filiais(id) | Filial |
| quantidade | INTEGER | NN, DEF 0, CHK ≥ 0 | Quantidade em estoque |
| data_atualizacao | TIMESTAMP | NN, DEF NOW | Última atualização |

**Restrições adicionais:**
- UK composta: (produto_id, filial_id) — cada produto tem apenas 1 registro por filial.

---

## 5. Tabela `clientes`

Cadastro de clientes da rede.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | SERIAL | PK | Identificador único |
| nome | VARCHAR(150) | NN | Nome completo |
| cpf | VARCHAR(14) | UK, CHK regex CPF | CPF formatado (`999.999.999-99`) |
| email | VARCHAR(120) |  | E-mail para comunicação |
| telefone | VARCHAR(20) |  | Telefone celular |
| data_nascimento | DATE |  | Para segmentação etária |
| cidade | VARCHAR(80) |  | Cidade do cliente |
| estado | CHAR(2) | CHK regex `^[A-Z]{2}$` | UF |
| data_cadastro | TIMESTAMP | NN, DEF NOW | Data de cadastro |

**Regras de negócio:**
- CPF opcional (venda pode ser anônima) mas se preenchido deve ser único.
- Cadastro completo permite campanhas de fidelidade e RFM.

---

## 6. Tabela `vendas`

Cabeçalho de cada transação de venda.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | SERIAL | PK | Identificador único |
| filial_id | INTEGER | NN, FK → filiais(id) | Filial onde ocorreu |
| cliente_id | INTEGER | FK → clientes(id) | Cliente identificado (NULL = anônima) |
| data_venda | TIMESTAMP | NN | Data/hora da venda |
| valor_total | DECIMAL(10,2) | NN, CHK ≥ 0 | Soma dos subtotais dos itens |
| desconto | DECIMAL(10,2) | NN, DEF 0, CHK ≥ 0 | Desconto aplicado |
| forma_pagamento | VARCHAR(20) | NN, CHK IN (...) | Forma de pagamento |
| status | VARCHAR(20) | NN, DEF 'CONCLUIDA' | Status da venda |
| data_criacao | TIMESTAMP | NN, DEF NOW | Data de registro |

**Formas de pagamento válidas:**
- `DINHEIRO`
- `CARTAO_CREDITO`
- `CARTAO_DEBITO`
- `PIX`
- `CONVENIO`

**Status válidos:**
- `CONCLUIDA` — Venda finalizada (contabiliza no faturamento)
- `CANCELADA` — Venda cancelada (não contabiliza)
- `PENDENTE` — Venda em processamento

**Regras de negócio:**
- Cancelar uma venda deve manter o registro (auditoria); nunca deletar.
- Valor líquido = `valor_total - desconto`.

---

## 7. Tabela `itens_venda`

Detalhamento dos produtos de cada venda (relação N:N materializada).

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | SERIAL | PK | Identificador único |
| venda_id | INTEGER | NN, FK → vendas(id) | Venda pai |
| produto_id | INTEGER | NN, FK → produtos(id) | Produto vendido |
| quantidade | INTEGER | NN, CHK > 0 | Quantidade vendida |
| preco_unitario | DECIMAL(10,2) | NN, CHK ≥ 0 | Preço no momento da venda |
| subtotal | DECIMAL(10,2) | NN, CHK ≥ 0 | quantidade × preco_unitario |

**Regras de negócio:**
- `preco_unitario` é gravado no momento da venda (histórico de preços é preservado mesmo que o produto mude de preço depois).
- `subtotal` deve sempre ser igual a `quantidade × preco_unitario` (validação no domínio de aplicação).

---

## Cardinalidades entre Tabelas

| Origem | Destino | Cardinalidade | Descrição |
|---|---|---|---|
| categorias | produtos | 1 : N | Uma categoria classifica vários produtos |
| produtos | itens_venda | 1 : N | Um produto pode aparecer em várias vendas |
| produtos | estoque | 1 : N | Um produto tem estoque em várias filiais |
| filiais | estoque | 1 : N | Uma filial armazena vários produtos |
| filiais | vendas | 1 : N | Uma filial realiza várias vendas |
| clientes | vendas | 0 : N | Um cliente faz várias vendas (venda pode ser sem cliente) |
| vendas | itens_venda | 1 : N | Uma venda tem vários itens |

---

## Índices Criados

| Índice | Tabela | Coluna(s) | Motivo |
|---|---|---|---|
| idx_vendas_data | vendas | data_venda | Consultas temporais frequentes |
| idx_vendas_filial | vendas | filial_id | Filtros por filial |
| idx_vendas_cliente | vendas | cliente_id | Histórico de compras do cliente |
| idx_vendas_status | vendas | status | Filtro de vendas concluídas |
| idx_itens_venda_produto | itens_venda | produto_id | Análise de produtos |
| idx_itens_venda_venda | itens_venda | venda_id | JOIN principal com vendas |
| idx_produtos_categoria | produtos | categoria_id | Filtros por categoria |
| idx_produtos_ativo | produtos | ativo | Excluir inativos |
| idx_estoque_filial | estoque | filial_id | Consulta de estoque por filial |
| idx_clientes_cidade | clientes | cidade | Segmentação geográfica |

---

## Views Criadas

Ver arquivo `04_views.sql` para o SQL completo.

| View | Uso |
|---|---|
| `vw_faturamento_mensal` | Série temporal de faturamento |
| `vw_ranking_produtos` | Ranking de produtos por faturamento e quantidade |
| `vw_ranking_filiais` | Ranking de filiais com KPIs |
| `vw_clientes_top` | Clientes com métricas de LTV e recência |
| `vw_estoque_critico` | Alertas de reposição |
