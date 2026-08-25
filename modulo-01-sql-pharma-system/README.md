# Módulo 01 — SQL para Análise de Dados
## PharmaSystem: Sistema de Gestão para Rede de Farmácias

> **Portfólio Lucas Veríssimo — Engenharia de Sistemas / UNIMONTES**
> Semana 1 de 12 do plano de portfólio.

---

## 📋 Sobre este módulo

Este é o **Módulo 01** do sistema PharmaSystem — um sistema fictício de gestão para uma rede de farmácias com 15 filiais espalhadas por Minas Gerais. Ele serve como fundação para todos os outros módulos (Power BI, Python, ETL, API, etc).

O foco desta semana é **modelagem relacional em PostgreSQL** e **consultas SQL analíticas**.

Este pacote está estruturado para **estudo por engenharia reversa**: leia os arquivos, tente entender antes de reproduzir, e depois reescreva do zero.

---

## 🗂️ Estrutura do projeto

```
modulo-01-sql-pharma-system/
│
├── README.md                    ← Você está aqui
├── COMO_ESTUDAR.md              ← Roteiro sugerido de engenharia reversa
│
├── 01_schema.sql                ← Criação de tabelas, constraints e índices
├── 02_inserts.sql               ← Dados sintéticos (15 filiais, 71 produtos, 1500 vendas)
├── 03_consultas.sql             ← 25 consultas analíticas documentadas
├── 04_views.sql                 ← 5 views para consultas frequentes
│
├── docs/
│   ├── diagrama_er.png          ← Diagrama Entidade-Relacionamento (imagem)
│   ├── diagrama_er.svg          ← Mesmo diagrama em formato vetorial
│   ├── diagrama_er.dot          ← Fonte do diagrama (Graphviz DOT)
│   └── dicionario_dados.md      ← Documentação completa das tabelas
│
├── scripts/
│   └── gerar_dados.py           ← Script Python que gerou os inserts
│
└── exemplos_resultados/
    └── resultados_consultas.md  ← Resultado esperado de cada consulta
```

---

## 🎯 Contexto de negócio

O PharmaSystem é a espinha dorsal de uma rede fictícia chamada **PharmaMinas**, com filiais em cidades reais de Minas Gerais:

- **Norte de Minas:** Montes Claros (4 filiais), Bocaiúva, Janaúba, Salinas, Pirapora, Grão Mogol, Buritizeiro, Corinto, Curvelo
- **Central:** Diamantina
- **Capital:** Belo Horizonte (Savassi)
- **Triângulo:** Uberlândia

O sistema precisa responder perguntas como:

- Quanto faturamos por mês? Estamos crescendo?
- Qual filial vende mais? E qual tem maior ticket médio?
- Quais produtos giram mais? Quais estão encalhados?
- Quem são meus melhores clientes? Quem parou de comprar?
- Onde meu estoque está crítico?
- Que produtos são vendidos juntos? (cross-sell)

Essas perguntas viram consultas SQL neste módulo, dashboards Power BI na Semana 2 e uma API REST na Semana 5.

---

## 🚀 Como executar

### Pré-requisitos

- **PostgreSQL 13+** instalado
- Cliente SQL (psql, DBeaver, pgAdmin, DataGrip)

### Passo a passo

```bash
# 1. Criar o banco
psql -U postgres -c "CREATE DATABASE pharma_system;"

# 2. Executar os scripts na ordem
psql -U postgres -d pharma_system -f 01_schema.sql
psql -U postgres -d pharma_system -f 02_inserts.sql
psql -U postgres -d pharma_system -f 04_views.sql

# 3. Testar uma consulta
psql -U postgres -d pharma_system -c "SELECT * FROM vw_ranking_filiais LIMIT 5;"
```

### Rodando as consultas

Abra `03_consultas.sql` no seu cliente SQL e execute consulta por consulta. Cada uma tem um cabeçalho explicando o objetivo de negócio, a técnica SQL usada e o resultado esperado.

---

## 🧩 Diagrama Entidade-Relacionamento

Ver arquivo `docs/diagrama_er.png` para o diagrama visual completo.

**Modelo resumido:**

```
CATEGORIAS ──1:N──> PRODUTOS ──1:N──> ITENS_VENDA <──N:1── VENDAS ──N:1──> FILIAIS
                       │                                       │
                       └────1:N────> ESTOQUE <──N:1───────────┤
                                                              │
                                                     CLIENTES ─┘ (0:N)
```

**7 tabelas:**

- **Cadastrais:** `filiais`, `categorias`, `produtos`, `clientes`
- **Operacionais:** `estoque`, `vendas`, `itens_venda`

---

## 📊 Volumetria do dataset

| Entidade | Quantidade |
|---|---:|
| Filiais | 15 |
| Categorias | 10 |
| Produtos | 71 |
| Registros de Estoque (produto × filial) | 1.065 |
| Clientes | 200 |
| Vendas | 1.500 |
| Itens de Venda | 3.253 |

**Período coberto:** Jan/2024 a Jun/2026 (com viés de 60% no último ano para simular crescimento).

**Faturamento total do dataset:** ~R$ 224 mil (1458 vendas concluídas + 42 canceladas ≈ 3% de cancelamento).

---

## 📚 Consultas incluídas (25 no total)

Organizadas em 5 seções progressivas, do básico ao avançado.

### Seção 1 — Vendas (Q01–Q07)
- Q01. Faturamento total da rede
- Q02. Faturamento por filial
- Q03. Faturamento mensal (série temporal)
- Q04. Ticket médio por filial
- Q05. Distribuição por forma de pagamento
- Q06. Vendas por dia da semana
- Q07. Taxa de cancelamento por filial

### Seção 2 — Produtos (Q08–Q14)
- Q08. Top 10 mais vendidos (unidades)
- Q09. Top 10 maior faturamento
- Q10. Produtos que nunca foram vendidos (anti-join)
- Q11. Margem por categoria
- Q12. Vendas de produtos com receita médica
- Q13. Ranking de fabricantes
- Q14. Estatísticas de preço por categoria (AVG, STDDEV, MIN, MAX)

### Seção 3 — Clientes (Q15–Q18)
- Q15. Top 10 clientes por LTV
- Q16. Clientes inativos há +90 dias
- Q17. Distribuição geográfica
- Q18. Segmentação por faixa etária

### Seção 4 — Estoque (Q19–Q21)
- Q19. Produtos com estoque crítico
- Q20. Valor imobilizado por filial
- Q21. Cobertura de estoque em dias (CTE)

### Seção 5 — Análises Avançadas (Q22–Q25)
- Q22. Ranking mensal com `RANK() OVER (PARTITION BY ...)`
- Q23. Crescimento MoM com `LAG()`
- Q24. Média móvel 3M com `ROWS BETWEEN`
- Q25. Análise de cesta (produtos vendidos juntos — self-join)

**Técnicas SQL cobertas:**
JOINs (INNER, LEFT), GROUP BY, HAVING, subconsultas, CTEs, Window Functions (RANK, LAG, AVG com frames), funções de data (EXTRACT, DATE_TRUNC, TO_CHAR, AGE), agregações estatísticas (STDDEV), CASE WHEN, anti-join, FILTER, self-join, NULLIF.

---

## 🗄️ Views criadas

| View | Uso principal |
|---|---|
| `vw_faturamento_mensal` | Série temporal para dashboards |
| `vw_ranking_produtos` | Ranking de produtos por múltiplos critérios |
| `vw_ranking_filiais` | KPIs consolidados por filial |
| `vw_clientes_top` | Base para CRM e campanhas |
| `vw_estoque_critico` | Alertas operacionais de reposição |

Todas vão ser reaproveitadas no Módulo 02 (Power BI) e Módulo 04 (ETL).

---

## 🔍 Amostras de resultados

O arquivo `exemplos_resultados/resultados_consultas.md` contém o resultado esperado de cada consulta contra o dataset gerado.

**Exemplo — Q02: Faturamento por filial (top 5):**

| Filial | Cidade | Vendas | Faturamento |
|---|---|---:|---:|
| PharmaMinas BH Savassi | Belo Horizonte | 234 | R$ 42.442,11 |
| PharmaMinas Centro Montes Claros | Montes Claros | 184 | R$ 27.420,02 |
| PharmaMinas Uberlândia Centro | Uberlândia | 184 | R$ 27.362,96 |
| PharmaMinas Todos os Santos | Montes Claros | 166 | R$ 26.056,73 |
| PharmaMinas Ibituruna | Montes Claros | 102 | R$ 13.926,56 |

---

## 🔄 Regenerar os dados

Se quiser gerar variações do dataset (mais vendas, mais clientes, etc), edite as constantes no topo de `scripts/gerar_dados.py` e execute:

```bash
python scripts/gerar_dados.py
```

O arquivo `02_inserts.sql` será reescrito. A semente `random.seed(42)` garante reprodutibilidade.

---

## 🔗 Publicação sugerida

### GitHub
Nome do repo: `pharma-system`
Este módulo vai em: `pharma-system/modulo-01-sql-pharma-system/`

### LinkedIn
Post sugerido:

> 🗄️ Semana 1 do meu portfólio em Engenharia de Sistemas concluída!
>
> Modelei do zero o banco de dados do PharmaSystem — sistema de gestão para uma rede fictícia de farmácias com 15 filiais. 7 tabelas, 25 consultas SQL analíticas cobrindo Window Functions, CTEs, self-joins e análises de RFM.
>
> Nas próximas semanas, esse mesmo modelo vai virar dashboards em Power BI, uma API REST em Flask e um pipeline de ETL. Tudo público no GitHub.
>
> #SQL #PostgreSQL #DataAnalytics #EngenhariaDeSistemas

Hashtags: `#SQL #PostgreSQL #DataAnalytics #EngenhariaDeSistemas #Portfolio`

---

## ⏭️ Próximo módulo

**Semana 2 — Business Intelligence com Power BI:**
Vai usar exatamente essas views (`vw_faturamento_mensal`, `vw_ranking_produtos`, etc) como fonte de dados para dashboards executivos.

---

## 📝 Licença

Este é um projeto de estudo/portfólio. Dados sintéticos, empresa e clientes fictícios.
