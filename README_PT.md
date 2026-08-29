---

# Versão em Português

# Apostila — Portfólio de Engenharia de Sistemas em 12 Semanas

**Projeto Guarda-Chuva: PharmaSystem — Sistema de Gestão para Rede de Farmácias**

> Cada semana é um módulo do mesmo ecossistema. Ao final, o recrutador verá no seu GitHub uma evolução coerente: modelagem → API → dashboard → arquitetura → integração total.

---

## Como Usar Esta Apostila

Cada módulo segue a mesma estrutura:

- **Contexto:** onde este módulo se encaixa no PharmaSystem.
- **O que estudar:** conteúdos teóricos com fontes gratuitas.
- **Roteiro diário:** divisão prática de segunda a domingo.
- **Entregáveis:** o que precisa estar pronto no domingo à noite.
- **Checklist de publicação:** GitHub + LinkedIn.

**Regra de ouro:** estude de segunda a quarta, construa de quinta a sábado, publique no domingo.

---

## Visão Geral do PharmaSystem

O PharmaSystem é um sistema fictício (mas realista) para uma rede de farmácias com 100 filiais. Ao longo das 12 semanas, você vai construir camada por camada:

```
Semana 1   → Banco de dados (vendas)
Semana 2   → Dashboard executivo (Power BI)
Semana 3   → Análise com Python/Pandas
Semana 4   → Pipeline ETL automatizado
Semana 5   → API REST
Semana 6   → Sistema Web (Help Desk interno)
Semana 7   → Documentação de Engenharia de Requisitos
Semana 8   → Projeto de Arquitetura do sistema completo
Semana 9   → Pipeline de Engenharia de Dados
Semana 10  → Modelagem MBSE
Semana 11  → Integração de todos os módulos
Semana 12  → Projeto final completo + README profissional
```

**Repositório GitHub:** crie um repositório chamado `pharma-system` com uma pasta por módulo:

```
pharma-system/
├── README.md                  ← visão geral do projeto
├── modulo-01-sql/
├── modulo-02-powerbi/
├── modulo-03-python-pandas/
├── modulo-04-etl/
├── modulo-05-api-rest/
├── modulo-06-sistema-web/
├── modulo-07-requisitos/
├── modulo-08-arquitetura/
├── modulo-09-engenharia-dados/
├── modulo-10-mbse/
├── modulo-11-integracao/
└── modulo-12-projeto-final/
```

---

---

# MÓDULO 01 — SQL para Análise de Dados

## Contexto no PharmaSystem

Toda rede de farmácias precisa de um banco de dados de vendas robusto. Neste módulo, você cria a fundação de dados sobre a qual todo o restante do portfólio será construído. Sem este banco, não há dashboard, não há ETL, não há API.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Modelo Relacional:** entidades, atributos, chaves primárias, chaves estrangeiras, normalização (1FN, 2FN, 3FN).
2. **DDL:** CREATE TABLE, ALTER TABLE, DROP TABLE, tipos de dados (INT, VARCHAR, DECIMAL, DATE, TIMESTAMP).
3. **DML:** INSERT, UPDATE, DELETE.
4. **Consultas:** SELECT, WHERE, ORDER BY, GROUP BY, HAVING, LIMIT.
5. **Junções:** INNER JOIN, LEFT JOIN, RIGHT JOIN.
6. **Funções de agregação:** COUNT, SUM, AVG, MIN, MAX.
7. **Subconsultas e CTEs (WITH).**

### Fontes de estudo gratuitas

- **W3Schools SQL Tutorial** — referência rápida para sintaxe.
- **SQLBolt** (sqlbolt.com) — exercícios interativos progressivos.
- **Mode Analytics SQL Tutorial** — foco em análise de dados com SQL.
- **Documentação oficial do PostgreSQL** — para consulta de funções específicas.

### Tempo estimado de estudo teórico

Cerca de 6 a 8 horas distribuídas em dois dias (segunda e terça). Se você já tem familiaridade com SQL, pode reduzir para 3 a 4 horas e adiantar a construção.

## Roteiro Diário

### Segunda-feira — Fundamentos e Modelagem

**Manhã/Tarde (estudo):**

- Estude modelo relacional e normalização.
- Assista a um vídeo ou leia um tutorial sobre modelagem de banco de dados.

**Noite (prática inicial):**

- Instale o PostgreSQL e o DBeaver (se ainda não tiver).
- Crie o banco `pharma_system`.
- Projete o diagrama ER no papel ou no draw.io com estas entidades:

```
filiais (id, nome, cidade, estado, data_abertura)
categorias (id, nome)
produtos (id, nome, categoria_id, preco_custo, preco_venda, estoque_minimo)
clientes (id, nome, cpf, email, telefone, data_cadastro)
vendas (id, filial_id, cliente_id, data_venda, valor_total, forma_pagamento)
itens_venda (id, venda_id, produto_id, quantidade, preco_unitario, subtotal)
```

### Terça-feira — DDL e Inserção de Dados

**Manhã (estudo):**

- Estude DDL, tipos de dados, constraints (NOT NULL, UNIQUE, CHECK, FOREIGN KEY).

**Tarde/Noite (construção):**

- Escreva os scripts `CREATE TABLE` com todas as constraints.
- Insira dados realistas: pelo menos 10 filiais, 50 produtos, 100 clientes e 500 vendas.
- Dica: use ChatGPT ou um script Python para gerar INSERTs em massa com dados que façam sentido para farmácias (medicamentos, cosméticos, higiene).

### Quarta-feira — Consultas Básicas e Intermediárias

**Dia inteiro (construção):**

Crie pelo menos 20 consultas SQL organizadas por categoria. Exemplos:

**Vendas gerais:**

1. Faturamento total da rede.
2. Faturamento por filial.
3. Faturamento por mês.
4. Ticket médio geral.
5. Ticket médio por filial.

**Produtos:**

6. Top 10 produtos mais vendidos (quantidade).
7. Top 10 produtos com maior faturamento.
8. Produtos que nunca foram vendidos.
9. Média de preço por categoria.
10. Margem de lucro por produto (preco_venda - preco_custo).

**Clientes:**

11. Clientes que mais compraram (valor).
12. Clientes que mais compraram (frequência).
13. Clientes sem compra nos últimos 90 dias.
14. Distribuição de clientes por filial.

**Temporal:**

15. Vendas por dia da semana.
16. Comparativo mês a mês.
17. Melhor e pior mês de vendas.

**Avançadas:**

18. Ranking de filiais usando Window Function (RANK, ROW_NUMBER).
19. Média móvel de vendas por mês (Window Function).
20. CTE para calcular o crescimento percentual mês a mês.

### Quinta-feira — Consultas Avançadas e Refinamento

**Dia inteiro:**

- Revise e otimize as consultas.
- Adicione índices nas colunas mais consultadas.
- Crie pelo menos 2 Views para consultas frequentes (ex.: `vw_faturamento_mensal`, `vw_ranking_produtos`).
- Documente cada consulta com comentários no SQL explicando o objetivo.

### Sexta-feira — Organização e Documentação

- Organize os scripts em arquivos separados:
  - `01_schema.sql` — criação das tabelas.
  - `02_inserts.sql` — dados de exemplo.
  - `03_consultas.sql` — todas as 20+ consultas documentadas.
  - `04_views.sql` — views criadas.
- Tire prints dos resultados mais interessantes no DBeaver.
- Escreva o `README.md` do módulo.

### Sábado — Revisão e Polimento

- Releia tudo com olhar crítico: o README está claro? As consultas fazem sentido de negócio?
- Adicione um diagrama ER exportado como imagem ao repositório.
- Teste executar tudo do zero (drop → create → insert → consultas) para garantir que funciona.

### Domingo — Publicação

- Faça o push para o GitHub.
- Publique no LinkedIn.

## Entregáveis

- Diagrama ER em imagem (PNG ou SVG).
- Script de criação do banco (`01_schema.sql`).
- Script de inserção de dados (`02_inserts.sql`).
- No mínimo 20 consultas SQL documentadas (`03_consultas.sql`).
- Pelo menos 2 Views (`04_views.sql`).
- README.md com: descrição do projeto, diagrama ER, como executar, exemplos de consultas e prints dos resultados.

## Checklist de Publicação

**GitHub:**

- [ ] Código limpo e comentado.
- [ ] README com seções: Descrição, Diagrama ER, Tecnologias, Como Executar, Exemplos de Consultas, Prints.
- [ ] Imagens na pasta `docs/` ou `assets/`.

**LinkedIn:**

- [ ] Texto de 3 a 5 parágrafos.
- [ ] Mencionar: o problema de negócio, as tecnologias usadas, o que aprendeu.
- [ ] Incluir 2 a 3 imagens (diagrama ER, resultado de query interessante).
- [ ] Link para o repositório GitHub.
- [ ] Hashtags: #SQL #PostgreSQL #AnáliseDeDados #PortfólioDev #EngenhariaDeSistemas

---

---

# MÓDULO 02 — Power BI

## Contexto no PharmaSystem

Os dados existem no banco, mas a diretoria de uma rede de farmácias precisa de visibilidade rápida. Neste módulo, você transforma os dados brutos do Módulo 01 em um dashboard executivo interativo — exatamente o tipo de entregável que analistas de dados produzem no dia a dia.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Interface do Power BI Desktop:** painéis, abas (Relatório, Dados, Modelo).
2. **Conexão a fontes de dados:** importar de PostgreSQL ou de arquivo CSV.
3. **Power Query (M):** renomear colunas, alterar tipos, remover duplicatas, criar colunas calculadas.
4. **Modelo de dados:** relacionamentos entre tabelas (1:N, N:N), tabela fato vs. dimensão (Star Schema básico).
5. **DAX básico:** CALCULATE, SUM, AVERAGE, COUNTROWS, DIVIDE, FILTER, ALL, DATEADD, SAMEPERIODLASTYEAR.
6. **Visuais:** gráfico de barras, de linhas, de pizza, cartões (KPI), tabelas, segmentadores (slicers), mapas.
7. **Formatação e design:** paleta de cores, alinhamento, contraste, hierarquia visual.

### Fontes de estudo gratuitas

- **Microsoft Learn — Power BI** (learn.microsoft.com) — trilha oficial, gratuita e com certificado.
- **Canal Hashtag Treinamentos** (YouTube, PT-BR) — tutoriais práticos de Power BI.
- **Canal Karine Lago** (YouTube, PT-BR) — foco em dashboards profissionais.
- **DAX Guide** (dax.guide) — referência para funções DAX.

### Tempo estimado

Cerca de 6 horas de estudo teórico. Se já usou Power BI antes, vá direto para a construção.

## Roteiro Diário

### Segunda-feira — Estudo e Preparação dos Dados

**Manhã (estudo):**

- Assista a tutoriais sobre conexão de dados e Power Query.
- Entenda o conceito de Star Schema (tabela fato + dimensões).

**Tarde/Noite (prática):**

- Exporte os dados do banco do Módulo 01 para CSVs (uma tabela por arquivo) ou conecte diretamente ao PostgreSQL.
- Importe no Power BI e configure os relacionamentos no modelo.
- Limpe os dados no Power Query: tipos corretos, nomes claros, remoção de inconsistências.

### Terça-feira — Estudo de DAX e Primeiras Medidas

**Manhã (estudo):**

- Estude as funções DAX mais usadas: SUM, AVERAGE, CALCULATE, COUNTROWS.
- Entenda o conceito de contexto de filtro.

**Tarde/Noite (construção):**

Crie estas medidas DAX:

- `Faturamento Total = SUM(itens_venda[subtotal])`
- `Ticket Médio = DIVIDE([Faturamento Total], COUNTROWS(vendas))`
- `Total de Vendas = COUNTROWS(vendas)`
- `Faturamento Mês Anterior = CALCULATE([Faturamento Total], DATEADD(calendario[Data], -1, MONTH))`
- `Crescimento % = DIVIDE([Faturamento Total] - [Faturamento Mês Anterior], [Faturamento Mês Anterior])`
- Crie uma tabela de calendário (Calendario) com `CALENDAR(MIN(vendas[data_venda]), MAX(vendas[data_venda]))`.

### Quarta-feira — Construção do Dashboard (Página 1: Visão Geral)

**Dia inteiro (construção):**

Crie a primeira página do dashboard com:

- **Cartões (KPIs):** Faturamento Total, Total de Vendas, Ticket Médio, Crescimento %.
- **Gráfico de linhas:** Faturamento mensal (eixo X = mês, eixo Y = faturamento).
- **Gráfico de barras horizontal:** Top 10 filiais por faturamento.
- **Segmentadores:** Período (mês/ano), Estado, Filial.
- Aplique uma paleta de cores consistente (use tons de verde/azul para farmácia).

### Quinta-feira — Dashboard (Página 2: Produtos + Página 3: Clientes)

**Página 2 — Produtos:**

- Gráfico de barras: Top 10 produtos mais vendidos.
- Gráfico de pizza/donut: Faturamento por categoria.
- Tabela: Produtos com margem de lucro (preco_venda - preco_custo).
- Cartão: Produto mais vendido do período selecionado.

**Página 3 — Clientes:**

- Cartões: Total de clientes, Clientes ativos (compraram nos últimos 90 dias).
- Gráfico de barras: Top 10 clientes por valor gasto.
- Gráfico de linhas: Evolução de novos cadastros por mês.
- Segmentador: Filial.

### Sexta-feira — Refinamento Visual e Interatividade

- Adicione tooltips customizados (ao passar o mouse, mostrar detalhes).
- Configure drill-down: ao clicar em uma filial, filtrar tudo para ela.
- Adicione botões de navegação entre páginas.
- Ajuste fontes, cores, alinhamentos — tudo profissional.
- Adicione um título e logotipo fictício "PharmaSystem" no cabeçalho.

### Sábado — Documentação e Prints

- Tire prints de cada página do dashboard (PNG de alta qualidade).
- Exporte o .pbix.
- Escreva o README.md com: descrição do dashboard, prints, medidas DAX criadas, como conectar aos dados, o que cada página mostra.

### Domingo — Publicação

- Push no GitHub (pasta `modulo-02-powerbi/`).
- Publique no LinkedIn com prints do dashboard.

## Entregáveis

- Arquivo `.pbix` do Power BI.
- Pelo menos 3 páginas de dashboard (Visão Geral, Produtos, Clientes).
- Mínimo de 5 medidas DAX.
- Prints de cada página do dashboard.
- README.md completo.

## Checklist de Publicação

**GitHub:**

- [ ] Arquivo .pbix na pasta do módulo.
- [ ] Prints em `docs/`.
- [ ] README com: Descrição, Prints, Medidas DAX, Fonte dos Dados, Como Abrir.

**LinkedIn:**

- [ ] Prints do dashboard (2 a 3 imagens chamativas).
- [ ] Texto explicando: qual problema de negócio o dashboard resolve, KPIs escolhidos, decisão de design.
- [ ] Hashtags: #PowerBI #Dashboard #DataAnalytics #BusinessIntelligence #PortfólioDev

---

---

# MÓDULO 03 — Python + Pandas

## Contexto no PharmaSystem

A equipe de dados da rede de farmácias precisa de análises mais profundas que o SQL puro não entrega facilmente — limpeza de dados sujos, estatísticas descritivas, correlações, e exportação de relatórios automatizados. Neste módulo, você usa Python e Pandas para fazer análise exploratória dos dados de vendas.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Pandas:** DataFrame, Series, leitura de CSV/Excel/SQL, seleção (loc, iloc), filtros, groupby, merge, pivot_table.
2. **Limpeza de dados:** tratar nulos (fillna, dropna), duplicatas, tipos de dados, outliers.
3. **Estatística descritiva:** describe(), mean, median, std, correlação.
4. **Matplotlib/Seaborn:** gráficos de barras, linhas, histograma, boxplot, heatmap de correlação.
5. **Exportação:** to_excel(), to_csv().

### Fontes de estudo gratuitas

- **Pandas oficial** (pandas.pydata.org/docs/getting_started) — tutorials excelentes.
- **Kaggle Learn — Pandas** (kaggle.com/learn/pandas) — curso interativo curto.
- **Real Python — Pandas Tutorials** — artigos aprofundados.
- **Seaborn Gallery** (seaborn.pydata.org/examples) — exemplos visuais de gráficos.

### Tempo estimado

Se já conhece Python, 4 a 5 horas de estudo focado em Pandas. Se é iniciante em Python, reserve 8 a 10 horas incluindo o básico da linguagem.

## Roteiro Diário

### Segunda-feira — Estudo de Pandas

- Faça o curso do Kaggle Learn de Pandas (leva cerca de 4 horas).
- Pratique operações básicas em um notebook Jupyter: ler CSV, filtrar, agrupar.

### Terça-feira — Estudo de Visualização + Conexão ao Banco

- Estude Matplotlib e Seaborn: pelo menos 5 tipos de gráfico.
- Conecte ao banco PostgreSQL usando `psycopg2` ou `sqlalchemy`:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://usuario:senha@localhost:5432/pharma_system')
df_vendas = pd.read_sql('SELECT * FROM vendas', engine)
```

### Quarta-feira — Limpeza e Preparação

- Carregue todas as tabelas do banco em DataFrames.
- Faça a limpeza: verifique nulos, tipos, duplicatas.
- Crie colunas derivadas:
  - `mes_venda` extraído de `data_venda`.
  - `dia_semana` extraído de `data_venda`.
  - `margem_lucro` = preco_venda - preco_custo.
- Faça os merges necessários (vendas + itens + produtos + filiais).

### Quinta-feira — Análise Exploratória

Crie um notebook Jupyter organizado com estas seções:

1. **Resumo geral:** shape, describe(), info().
2. **Análise de vendas:** faturamento por mês, por filial, por categoria.
3. **Análise de produtos:** top 10, distribuição de preços (histograma), boxplot de margem por categoria.
4. **Análise de clientes:** distribuição de frequência de compra, segmentação por valor (quartis).
5. **Correlações:** heatmap de correlação entre variáveis numéricas.
6. **Insights:** escreva em Markdown dentro do notebook pelo menos 5 insights de negócio que os dados revelam.

### Sexta-feira — Exportação e Relatório

- Exporte um relatório em Excel com múltiplas abas:
  - Aba 1: Faturamento mensal.
  - Aba 2: Ranking de produtos.
  - Aba 3: Ranking de filiais.
  - Aba 4: Dados brutos filtrados.
- Use `openpyxl` para formatar o Excel (cabeçalhos em negrito, largura de colunas).
- Salve todos os gráficos como imagens PNG.

### Sábado — Documentação

- Limpe o notebook: remova células de teste, adicione títulos e explicações.
- Escreva o README.md.
- Organize a pasta: `notebooks/`, `exports/`, `graficos/`, `README.md`.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com 2 a 3 gráficos gerados pelo Seaborn/Matplotlib.

## Entregáveis

- Notebook Jupyter completo com análise exploratória.
- Pelo menos 8 gráficos (barras, linhas, histograma, boxplot, heatmap, etc.).
- Relatório exportado em Excel com múltiplas abas.
- README.md completo.

## Checklist de Publicação

**GitHub:**

- [ ] Notebook `.ipynb` limpo e documentado.
- [ ] Gráficos exportados em `graficos/`.
- [ ] Excel em `exports/`.
- [ ] README com: Descrição, Prints/Gráficos, Tecnologias, Como Executar, Insights Encontrados.

**LinkedIn:**

- [ ] 2 a 3 gráficos mais impactantes.
- [ ] Texto focando nos insights de negócio (não na técnica pura).
- [ ] Hashtags: #Python #Pandas #DataAnalysis #AnáliseDeDados #PortfólioDev

---

---

# MÓDULO 04 — ETL (Extract, Transform, Load)

## Contexto no PharmaSystem

No mundo real, os dados de vendas das 100 filiais chegam em arquivos CSV exportados dos caixas. A equipe de dados precisa de um pipeline automatizado que leia esses CSVs, limpe, transforme e carregue no banco de dados — e então o Power BI se atualiza automaticamente. Esse módulo demonstra uma competência muito valorizada no mercado.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **O que é ETL:** Extract (extrair de fontes), Transform (limpar, validar, enriquecer), Load (carregar no destino).
2. **Diferença entre ETL e ELT.**
3. **Logging em Python:** módulo `logging` para registrar cada etapa.
4. **Tratamento de erros:** try/except para arquivos corrompidos ou com formato inesperado.
5. **Agendamento (conceito):** cron, Task Scheduler, ou bibliotecas como `schedule`.
6. **Boas práticas:** idempotência (rodar 2x sem duplicar), validação de schema, pasta de arquivos processados vs. novos.

### Fontes de estudo gratuitas

- **Real Python — ETL Pipeline** — busque "build etl pipeline python" no Real Python.
- **Documentação do módulo logging do Python** — essencial para pipelines.
- **Artigos sobre data pipeline patterns** — Medium e Towards Data Science.

### Tempo estimado

4 a 6 horas de estudo. O foco é mais prática do que teoria.

## Roteiro Diário

### Segunda-feira — Estudo e Planejamento

**Manhã (estudo):**

- Estude conceitos de ETL e boas práticas.
- Estude o módulo `logging` do Python.

**Tarde/Noite:**

- Planeje a arquitetura do pipeline:

```
dados_brutos/           ← CSVs novos chegam aqui
dados_processados/      ← CSVs já processados são movidos para cá
logs/                   ← logs de cada execução
scripts/
  ├── extract.py        ← lê os CSVs
  ├── transform.py      ← limpeza e validação
  ├── load.py           ← carrega no PostgreSQL
  └── pipeline.py       ← orquestra tudo
config/
  └── config.yaml       ← configurações (caminho do banco, etc.)
```

### Terça-feira — Extract

- Gere 5 a 10 arquivos CSV simulando dados das filiais (use Python ou dados do Módulo 01).
- Inclua propositalmente problemas: linhas em branco, datas em formatos diferentes, valores negativos, CPFs duplicados.
- Escreva `extract.py`:
  - Lê todos os CSVs de `dados_brutos/`.
  - Retorna uma lista de DataFrames.
  - Loga quantos arquivos encontrou, quantas linhas cada um tem.

### Quarta-feira — Transform

- Escreva `transform.py`:
  - Padroniza nomes de colunas (snake_case).
  - Converte tipos (datas, decimais).
  - Remove duplicatas.
  - Trata nulos (preencher ou descartar, com justificativa).
  - Valida regras de negócio (ex.: quantidade > 0, preço > 0).
  - Registra em log cada transformação e quantas linhas foram afetadas.
  - Retorna DataFrame limpo.

### Quinta-feira — Load

- Escreva `load.py`:
  - Conecta ao PostgreSQL.
  - Usa `UPSERT` (INSERT ... ON CONFLICT DO UPDATE) para idempotência.
  - Loga quantas linhas foram inseridas/atualizadas.
- Escreva `pipeline.py`:
  - Chama extract → transform → load em sequência.
  - Ao final, move CSVs processados para `dados_processados/`.
  - Gera um log de resumo final (total de arquivos, linhas processadas, erros).

### Sexta-feira — Testes e Robustez

- Teste cenários:
  - CSV vazio.
  - CSV com colunas faltando.
  - CSV com encoding diferente (UTF-8 vs. Latin-1).
  - Rodar o pipeline 2x sem duplicar dados (testar idempotência).
- Adicione tratamento de erros para cada cenário.
- (Opcional) Adicione um envio de e-mail de relatório ao final do pipeline usando `smtplib`.

### Sábado — Documentação e Diagrama

- Crie um diagrama do fluxo ETL (use draw.io ou Mermaid):

```
CSV Filiais → [Extract] → [Transform] → [Load] → PostgreSQL → Power BI
```

- Escreva o README.md com: problema de negócio, arquitetura, como executar, logs de exemplo, tratamento de erros.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com o diagrama de fluxo e um print do log de execução.

## Entregáveis

- Scripts Python separados por responsabilidade (extract, transform, load, pipeline).
- Arquivo de configuração YAML.
- CSVs de exemplo (com e sem erros).
- Diagrama de fluxo do pipeline.
- Logs de execução de exemplo.
- README.md completo.

## Checklist de Publicação

**GitHub:**

- [ ] Código modular e documentado.
- [ ] CSVs de exemplo em `dados_brutos/`.
- [ ] Diagrama de fluxo em `docs/`.
- [ ] README com: Problema, Arquitetura, Como Executar, Exemplos de Log.

**LinkedIn:**

- [ ] Diagrama do fluxo ETL.
- [ ] Print do log de execução com sucesso.
- [ ] Texto explicando: por que ETL é importante, o que o pipeline faz, tratamento de erros.
- [ ] Hashtags: #ETL #Python #DataEngineering #Pipeline #PortfólioDev

---

---

# MÓDULO 05 — API REST

## Contexto no PharmaSystem

O PharmaSystem precisa expor dados para outros sistemas: o app mobile das filiais consulta produtos, o sistema de e-commerce faz pedidos, o dashboard consome indicadores. Uma API REST é a interface que conecta tudo. Este é um dos módulos mais valorizados em processos seletivos.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **REST:** recursos, verbos HTTP (GET, POST, PUT, DELETE), status codes (200, 201, 400, 404, 500).
2. **JSON:** estrutura, serialização, deserialização.
3. **Flask (opção Python)** ou **Spring Boot (opção Java):** rotas, controllers, models, serialização.
4. **ORM:** SQLAlchemy (Flask) ou JPA/Hibernate (Spring Boot) — mapeamento objeto-relacional.
5. **Swagger/OpenAPI:** documentação automática da API.
6. **Testes de API:** Postman ou Insomnia para testar endpoints.

**Recomendação:** como seu portfólio já tem bastante Python, considere fazer em Spring Boot para demonstrar versatilidade. Mas se precisar economizar tempo, Flask é mais rápido de implementar.

### Fontes de estudo gratuitas

**Flask:**
- **Miguel Grinberg — Flask Mega-Tutorial** (blog.miguelgrinberg.com).
- **Real Python — Flask REST API** — busque "flask rest api tutorial".
- **Documentação Flask** (flask.palletsprojects.com).

**Spring Boot:**
- **Baeldung** (baeldung.com) — referência para Spring Boot REST.
- **Spring Initializr** (start.spring.io) — para gerar o projeto base.
- **Canal Michelli Brito** (YouTube, PT-BR) — tutoriais de Spring Boot.

### Tempo estimado

Flask: 6 a 8 horas. Spring Boot: 8 a 12 horas (mais setup, mais conceitos).

## Roteiro Diário

### Segunda-feira — Estudo de REST + Setup

**Manhã (estudo):**

- Estude conceitos REST, verbos HTTP, status codes.
- Assista a um tutorial introdutório do framework escolhido.

**Tarde/Noite:**

- Crie o projeto base.
- Configure a conexão com o banco PostgreSQL do Módulo 01.
- Crie o modelo de `Produto` (entidade/classe mapeada para a tabela `produtos`).

### Terça-feira — CRUD de Produtos

- Implemente os endpoints de Produto:
  - `GET /api/produtos` — listar todos (com paginação).
  - `GET /api/produtos/{id}` — buscar por ID.
  - `POST /api/produtos` — criar novo produto.
  - `PUT /api/produtos/{id}` — atualizar produto.
  - `DELETE /api/produtos/{id}` — deletar produto.
- Teste todos no Postman.

### Quarta-feira — CRUD de Clientes e Filiais

- Repita a mesma estrutura para:
  - `GET/POST/PUT/DELETE /api/clientes`
  - `GET/POST/PUT/DELETE /api/filiais`
- Adicione validações: campos obrigatórios, formato de CPF, e-mail.
- Retorne erros adequados (400 para validação, 404 para não encontrado).

### Quinta-feira — Endpoints de Vendas e Indicadores

- Implemente:
  - `POST /api/vendas` — registrar uma venda (com itens).
  - `GET /api/vendas?filial_id=X&mes=Y` — listar vendas com filtros.
  - `GET /api/indicadores/faturamento-mensal` — retorna faturamento agregado por mês.
  - `GET /api/indicadores/top-produtos?limit=10` — top N produtos.
  - `GET /api/indicadores/top-filiais` — ranking de filiais.

### Sexta-feira — Documentação e Swagger

- Configure Swagger/OpenAPI para documentação automática.
  - Flask: use `flask-smorest` ou `flasgger`.
  - Spring Boot: use `springdoc-openapi`.
- Garanta que todos os endpoints apareçam documentados com exemplos.
- Teste cenários de erro (IDs inexistentes, payloads inválidos).

### Sábado — README e Prints

- Tire prints do Swagger mostrando os endpoints.
- Tire prints do Postman com exemplos de requisições e respostas.
- Escreva o README.md com: descrição da API, endpoints disponíveis, como executar, prints.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com prints do Swagger e do Postman.

## Entregáveis

- Código da API (Flask ou Spring Boot).
- Pelo menos 15 endpoints funcionais.
- Documentação Swagger/OpenAPI.
- Prints do Postman com exemplos de requisições.
- README.md completo.

## Checklist de Publicação

**GitHub:**

- [ ] Código organizado (controllers, models, services, repositories).
- [ ] requirements.txt (Flask) ou pom.xml (Spring Boot).
- [ ] Prints do Swagger e Postman em `docs/`.
- [ ] README com: Descrição, Endpoints, Como Executar, Prints, Tecnologias.

**LinkedIn:**

- [ ] Print do Swagger mostrando a lista de endpoints.
- [ ] Print de uma requisição/resposta no Postman.
- [ ] Texto explicando: o que a API faz, decisões de design, validações.
- [ ] Hashtags: #API #REST #Flask #SpringBoot #Backend #PortfólioDev

---

---

# MÓDULO 06 — Sistema Web

## Contexto no PharmaSystem

Uma rede de 100 filiais gera muitos chamados de TI: impressora parou, sistema caiu, caixa travou. Neste módulo, você constrói o módulo de Help Desk do PharmaSystem — um sistema web para abertura, acompanhamento e resolução de chamados técnicos. Isso conecta diretamente com sua experiência profissional em TI e infraestrutura.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **MVC (Model-View-Controller):** separação de responsabilidades.
2. **Templates HTML:** Jinja2 (Flask) ou Thymeleaf (Spring Boot).
3. **Formulários e validação do lado do servidor.**
4. **Autenticação básica:** login/logout, sessões, roles (admin vs. operador).
5. **CSS básico:** Bootstrap para ter um layout profissional rápido.
6. **CRUD completo via interface web.**

### Fontes de estudo gratuitas

**Flask + Jinja2:**
- **Flask Mega-Tutorial (Miguel Grinberg)** — capítulos sobre templates e login.
- **Real Python — Flask Tutorial.**

**Spring Boot + Thymeleaf:**
- **Baeldung — Spring MVC + Thymeleaf.**
- **Canal Michelli Brito** (YouTube) — projetos Spring MVC.

**Bootstrap:**
- **getbootstrap.com** — documentação e componentes prontos.

### Tempo estimado

8 a 12 horas de estudo + construção. Este módulo é mais denso.

## Roteiro Diário

### Segunda-feira — Estudo e Setup

- Estude MVC, templates e autenticação.
- Crie o projeto e configure o banco (reuse o PostgreSQL existente).
- Crie as tabelas novas:

```sql
usuarios (id, nome, email, senha_hash, role, filial_id)
chamados (id, titulo, descricao, categoria, prioridade, status, 
          filial_id, usuario_abertura_id, usuario_responsavel_id,
          data_abertura, data_fechamento)
comentarios_chamado (id, chamado_id, usuario_id, texto, data)
```

### Terça-feira — Autenticação

- Implemente registro de usuário e login.
- Configure sessões e proteção de rotas.
- Crie dois roles: `admin` (TI central) e `operador` (funcionário da filial).
- Página de login com Bootstrap.

### Quarta-feira — CRUD de Chamados

- Tela de abertura de chamado (formulário com: título, descrição, categoria, prioridade).
- Lista de chamados (tabela com filtros: status, prioridade, filial).
- Tela de detalhes do chamado (ver informações, adicionar comentários).
- Funcionalidade de alterar status (Aberto → Em Andamento → Resolvido → Fechado).

### Quinta-feira — Dashboard Interno + Funcionalidades Extras

- Página de dashboard com contadores:
  - Chamados abertos.
  - Chamados em andamento.
  - Chamados resolvidos este mês.
  - Tempo médio de resolução.
- Adicione filtro por filial e por período.
- Admin pode atribuir chamado a um técnico.
- Operador vê apenas chamados da sua filial.

### Sexta-feira — Polimento Visual e Testes

- Revise todas as telas: alinhamento, responsividade, mensagens de erro claras.
- Teste fluxos completos: registrar → logar → abrir chamado → comentar → resolver → ver no dashboard.
- Adicione feedbacks visuais: toast de sucesso, badge de prioridade (vermelho = urgente), ícones.

### Sábado — Documentação e Prints

- Tire prints de cada tela principal (login, lista, detalhes, dashboard).
- Escreva o README.md.
- Crie um fluxo de navegação visual (diagrama simples mostrando as telas e transições).

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com prints das telas.

## Entregáveis

- Sistema web funcional com autenticação e CRUD.
- Pelo menos 6 telas (login, registro, lista, novo chamado, detalhes, dashboard).
- Dois roles com permissões diferentes.
- Prints de cada tela.
- README.md completo.

## Checklist de Publicação

**GitHub:**

- [ ] Código MVC organizado.
- [ ] requirements.txt ou pom.xml.
- [ ] Prints das telas em `docs/`.
- [ ] README com: Descrição, Funcionalidades, Prints, Como Executar, Tecnologias.

**LinkedIn:**

- [ ] 3 a 4 prints das telas mais bonitas (dashboard, lista de chamados, detalhes).
- [ ] Texto explicando: problema resolvido (gestão de chamados de TI), funcionalidades, decisões de design.
- [ ] Hashtags: #WebDev #Flask #SpringBoot #HelpDesk #FullStack #PortfólioDev

---

---

# MÓDULO 07 — Engenharia de Requisitos

## Contexto no PharmaSystem

Agora você muda de chapéu: em vez de desenvolvedor, você é o engenheiro de sistemas que documenta formalmente o PharmaSystem. Este módulo é o que diferencia um programador de um engenheiro. Você produz um documento de requisitos profissional que poderia ser apresentado a um cliente real.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Tipos de requisitos:** funcionais (RF) vs. não-funcionais (RNF).
2. **Técnicas de elicitação:** entrevistas, brainstorming, análise de documentos.
3. **Especificação de requisitos:** formato IEEE 830 (simplificado).
4. **Casos de uso:** atores, fluxos principal e alternativo, pré/pós-condições.
5. **UML — Diagramas de caso de uso:** atores, elipses, relacionamentos (include, extend).
6. **UML — Diagrama de classes:** classes, atributos, métodos, relacionamentos (associação, agregação, composição, herança).
7. **UML — Diagrama de sequência:** lifelines, mensagens, retornos.
8. **UML — Diagrama de atividade:** fluxo de processos.

### Fontes de estudo gratuitas

- **Lucidchart UML Tutorials** — exemplos visuais de cada diagrama.
- **UML Diagrams (uml-diagrams.org)** — referência completa.
- **draw.io (app.diagrams.net)** — ferramenta gratuita para criar diagramas UML.
- **PlantUML** (plantuml.com) — gera diagramas UML a partir de texto (ideal para versionamento no GitHub).

### Tempo estimado

6 a 8 horas de estudo (conceitos + prática com a ferramenta de diagramas).

## Roteiro Diário

### Segunda-feira — Estudo de Requisitos

- Estude tipos de requisitos e o formato IEEE 830.
- Estude casos de uso: como escrever, exemplos.
- Comece a listar os requisitos do PharmaSystem com base em tudo que você já construiu.

### Terça-feira — Estudo de UML + Levantamento

- Estude diagramas de caso de uso, classes, sequência e atividade.
- Instale o draw.io ou configure o PlantUML.
- Complete a lista de requisitos.

### Quarta-feira — Documento de Requisitos

Escreva o Documento de Requisitos do PharmaSystem com estas seções:

1. **Introdução:** propósito, escopo, definições.
2. **Descrição geral:** perspectiva do produto, funções principais, características dos usuários, restrições.
3. **Requisitos funcionais (RF):**
   - RF01: O sistema deve permitir o cadastro de filiais.
   - RF02: O sistema deve permitir o cadastro de produtos com preço de custo e venda.
   - RF03: O sistema deve registrar vendas com itens e formas de pagamento.
   - RF04: O sistema deve gerar relatórios de faturamento mensal.
   - (Continue até pelo menos RF20.)
4. **Requisitos não-funcionais (RNF):**
   - RNF01: O sistema deve suportar 100 filiais simultâneas.
   - RNF02: O tempo de resposta da API deve ser inferior a 500ms.
   - RNF03: O sistema deve manter logs de auditoria.
   - (Pelo menos 10 RNFs.)
5. **Regras de negócio.**

### Quinta-feira — Casos de Uso e Diagramas UML

**Casos de uso (escreva 5 completos):**

Exemplo de caso de uso:

- **UC01 — Registrar Venda**
  - Ator: Operador de Caixa.
  - Pré-condição: Operador autenticado no sistema.
  - Fluxo principal: (passo a passo).
  - Fluxos alternativos: produto sem estoque, cliente não cadastrado.
  - Pós-condição: venda registrada, estoque atualizado.

**Diagramas:**

- Diagrama de Casos de Uso (geral do sistema).
- Diagrama de Classes (todas as entidades + relacionamentos).

### Sexta-feira — Diagramas de Sequência e Atividade

- Diagrama de Sequência para o caso de uso "Registrar Venda" (mostrando: Operador → Interface → Controller → Service → Database).
- Diagrama de Sequência para "Abrir Chamado de TI".
- Diagrama de Atividade para o fluxo completo de um chamado (Aberto → Triagem → Em Andamento → Resolvido → Fechado).

### Sábado — Revisão e Documentação

- Revise o documento de requisitos: está claro? Um desenvolvedor novo conseguiria implementar o sistema só lendo?
- Exporte todos os diagramas como imagens.
- Escreva o README.md.

### Domingo — Publicação

- Push no GitHub (documento em `.md` ou `.pdf`, diagramas em `diagramas/`).
- Publique no LinkedIn com um ou dois diagramas UML.

## Entregáveis

- Documento de Requisitos completo (20+ RF, 10+ RNF).
- 5 Casos de Uso escritos.
- Diagrama de Casos de Uso.
- Diagrama de Classes.
- 2 Diagramas de Sequência.
- 1 Diagrama de Atividade.
- README.md.

## Checklist de Publicação

**GitHub:**

- [ ] Documento de requisitos em `docs/`.
- [ ] Diagramas em `diagramas/` (PNG + fonte PlantUML ou draw.io).
- [ ] README com: Descrição, Prints dos Diagramas, Metodologia Usada.

**LinkedIn:**

- [ ] Diagrama de classes ou de sequência (visual forte).
- [ ] Texto focando: "além de programar, documentei formalmente a engenharia do sistema".
- [ ] Hashtags: #UML #EngenhariaDeSistemas #Requisitos #SystemsEngineering #PortfólioDev

---

---

# MÓDULO 08 — Arquitetura de Sistemas

## Contexto no PharmaSystem

Agora você é o arquiteto. Neste módulo, você projeta a arquitetura completa do PharmaSystem como se fosse apresentá-la ao CTO de uma empresa. Isso inclui componentes, integrações, bancos de dados, APIs, filas e infraestrutura. Este módulo mostra visão de engenharia de ponta a ponta.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Estilos arquiteturais:** monolítico, microsserviços, serverless, event-driven.
2. **Padrões:** API Gateway, BFF (Backend for Frontend), CQRS, Event Sourcing.
3. **Modelo C4:** Context, Container, Component, Code — níveis de abstração para documentar arquitetura.
4. **Diagramas de infraestrutura:** servidores, load balancers, bancos, caches, filas.
5. **Integrações:** REST, mensageria (RabbitMQ, Kafka conceitual), webhooks.
6. **Decisões arquiteturais (ADR — Architecture Decision Record):** formato de documentar "por que" escolheu algo.

### Fontes de estudo gratuitas

- **C4 Model** (c4model.com) — referência oficial com exemplos.
- **Martin Fowler — Architecture** (martinfowler.com) — artigos sobre padrões.
- **draw.io / Mermaid** — para criar os diagramas.
- **GitHub — ADR Templates** — busque "adr template" para ver exemplos.

### Tempo estimado

6 a 8 horas de estudo. O restante é construção dos diagramas e documentos.

## Roteiro Diário

### Segunda-feira — Estudo

- Estude os estilos arquiteturais e quando usar cada um.
- Estude o Modelo C4 (Context, Container, Component).
- Leia 2 a 3 exemplos de ADRs.

### Terça-feira — Definição da Arquitetura

Defina a arquitetura do PharmaSystem. Sugestão de estrutura:

```
[App Mobile Filiais]  →  [API Gateway]  →  [Serviço de Vendas]     →  [PostgreSQL]
[Portal Web Admin]    →  [API Gateway]  →  [Serviço de Estoque]    →  [PostgreSQL]
[Dashboard BI]        →                    [Serviço de Relatórios]  →  [PostgreSQL]
                                           [Serviço de Help Desk]  →  [PostgreSQL]
                                           [Pipeline ETL]          →  [PostgreSQL]
                           [Fila de Mensagens (RabbitMQ)]
                              ↑ eventos de venda, chamados
```

### Quarta-feira — Diagramas C4

Crie os 3 primeiros níveis do C4:

**Nível 1 — Context:** PharmaSystem e seus atores externos (operadores, gestores, técnicos TI, sistemas externos como SEFAZ, fornecedores).

**Nível 2 — Container:** API Gateway, cada microsserviço, banco de dados, fila, dashboard.

**Nível 3 — Component:** detalhe interno de 1 microsserviço (ex.: Serviço de Vendas → Controller, Service, Repository, Validador).

### Quinta-feira — Diagrama de Infraestrutura + Fluxos

- Diagrama de infraestrutura: onde cada componente roda (servidores, cloud, containers).
- Diagrama de fluxo: como uma venda percorre o sistema (caixa → API → validação → banco → evento → atualização de estoque → notificação).
- Diagrama de integração: como o PharmaSystem se integraria a sistemas externos (SEFAZ para NF-e, fornecedores para reposição).

### Sexta-feira — ADRs (Architecture Decision Records)

Escreva pelo menos 3 ADRs:

- **ADR-001:** Por que escolhemos arquitetura de microsserviços em vez de monolito.
- **ADR-002:** Por que PostgreSQL como banco de dados principal.
- **ADR-003:** Por que API REST em vez de GraphQL.

Formato de cada ADR:

```
# ADR-001: Arquitetura de Microsserviços

## Status
Aceita

## Contexto
O PharmaSystem atende 100 filiais com módulos de vendas, estoque, 
help desk e relatórios. Cada módulo tem ciclos de atualização diferentes.

## Decisão
Adotar arquitetura de microsserviços com API Gateway.

## Consequências
Positivas: deploy independente, escalabilidade por módulo.
Negativas: complexidade operacional, necessidade de orquestração.
```

### Sábado — Documentação Final

- Compile tudo em um documento de arquitetura coeso.
- Organize: Visão Geral → C4 (Context, Container, Component) → Infraestrutura → Fluxos → ADRs.
- Escreva o README.md.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com o diagrama C4 de Container (o mais visual e impactante).

## Entregáveis

- Diagrama C4 — Nível 1 (Context).
- Diagrama C4 — Nível 2 (Container).
- Diagrama C4 — Nível 3 (Component) de 1 serviço.
- Diagrama de infraestrutura.
- Diagrama de fluxo de venda.
- 3 ADRs.
- README.md.

## Checklist de Publicação

**GitHub:**

- [ ] Diagramas em `diagramas/`.
- [ ] ADRs em `docs/adrs/`.
- [ ] Documento de arquitetura em `docs/`.
- [ ] README com: Visão Geral, Diagramas, ADRs, Tecnologias.

**LinkedIn:**

- [ ] Diagrama C4 Container (o mais visual).
- [ ] Texto explicando: visão sistêmica, decisões tomadas e seus trade-offs.
- [ ] Hashtags: #Arquitetura #SystemDesign #C4Model #Microsserviços #PortfólioDev

---

---

# MÓDULO 09 — Engenharia de Dados

## Contexto no PharmaSystem

A rede de farmácias não quer depender de CSVs manuais. Neste módulo, você constrói um pipeline de engenharia de dados que consome uma API externa (simulada), processa os dados e alimenta um dashboard automatizado. Isso complementa o ETL do Módulo 04 com uma abordagem mais moderna e orientada a API.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Diferença entre ETL e ELT moderno.**
2. **Consumo de APIs com Python:** `requests`, paginação, autenticação.
3. **Data Lake vs. Data Warehouse (conceitual).**
4. **Airflow (conceitual):** DAGs, tasks, scheduling — entender o conceito mesmo sem instalar.
5. **Qualidade de dados:** validações, testes de schema, Great Expectations (conceitual).

### Fontes de estudo gratuitas

- **Real Python — Working with APIs** — tutorial de consumo de APIs.
- **Documentação do requests** (docs.python-requests.org).
- **Airflow official docs** — leia a seção "Concepts" para entender DAGs.
- **Artigos sobre Modern Data Stack** — Towards Data Science, Data Engineering Weekly.

### Tempo estimado

5 a 7 horas de estudo.

## Roteiro Diário

### Segunda-feira — Estudo e Planejamento

- Estude os conceitos e a diferença entre ETL tradicional e data pipelines modernos.
- Planeje o pipeline:

```
[API PharmaSystem (Módulo 05)] → [Ingestão Python] → [Staging SQL] → [Transformação] → [Tabelas Analíticas] → [Dashboard]
```

### Terça-feira — API Mock (se necessário) + Ingestão

- Se a API do Módulo 05 não estiver rodando, crie uma versão mock com Flask que retorna JSONs de vendas, produtos e filiais.
- Escreva o script de ingestão:
  - Consome todos os endpoints da API.
  - Salva os dados brutos em tabelas `staging_*` no banco.
  - Loga tudo.

### Quarta-feira — Transformação

- Escreva scripts de transformação que leem de `staging_*` e criam tabelas analíticas:
  - `fato_vendas` — tabela fato desnormalizada com todas as informações de venda.
  - `dim_tempo` — dimensão temporal (ano, mês, trimestre, dia da semana).
  - `dim_filial` — dimensão de filiais.
  - `dim_produto` — dimensão de produtos com categoria.
- Aplique o conceito de Star Schema.

### Quinta-feira — Qualidade de Dados + Dashboard

- Adicione validações: contagem de registros (staging vs. analítico), verificação de nulos, verificação de chaves duplicadas.
- Crie um dashboard simples (pode ser com Streamlit para ser diferente do Módulo 02):
  - Faturamento por período.
  - Top produtos.
  - Comparativo entre filiais.
  - Alimentado diretamente das tabelas analíticas.

### Sexta-feira — Orquestração (Conceitual) + Script Mestre

- Crie um script `orquestrador.py` que executa o pipeline completo em ordem:
  1. Ingestão.
  2. Transformação.
  3. Validação.
  4. (Opcional) Atualização do dashboard.
- Escreva um documento explicando como isso seria orquestrado com Airflow em produção (DAG conceitual, schedule, dependências).

### Sábado — Documentação

- Crie diagrama do pipeline completo.
- Documente o Star Schema com diagrama ER das tabelas analíticas.
- Escreva o README.md.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com o diagrama do pipeline e um print do dashboard.

## Entregáveis

- Scripts de ingestão, transformação, validação e orquestração.
- Tabelas analíticas com Star Schema implementado.
- Dashboard (Streamlit ou outro).
- Diagrama do pipeline.
- Diagrama do Star Schema.
- Documento conceitual de orquestração com Airflow.
- README.md.

## Checklist de Publicação

**GitHub:**

- [ ] Scripts organizados em `ingestao/`, `transformacao/`, `validacao/`.
- [ ] Diagramas em `docs/`.
- [ ] README com: Pipeline, Star Schema, Como Executar, Dashboard.

**LinkedIn:**

- [ ] Diagrama do pipeline.
- [ ] Print do dashboard Streamlit.
- [ ] Texto: diferença entre ETL simples e data pipeline, decisões de modelagem.
- [ ] Hashtags: #DataEngineering #Pipeline #StarSchema #Streamlit #PortfólioDev

---

---

# MÓDULO 10 — MBSE (Model-Based Systems Engineering)

## Contexto no PharmaSystem

MBSE é o que transforma um desenvolvedor em engenheiro de sistemas. Neste módulo, você aplica modelagem baseada em modelos ao PharmaSystem, tratando-o como um sistema completo com requisitos, blocos, interfaces e fluxos — usando a mesma abordagem que seria usada para projetar um drone, um satélite ou uma planta industrial.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **O que é MBSE:** modelagem como fonte de verdade (vs. documentação textual tradicional).
2. **SysML (resumo):** diferença entre UML e SysML, principais diagramas.
3. **Diagrama de Requisitos (SysML):** representar requisitos como blocos com rastreabilidade.
4. **Diagrama de Blocos (BDD — Block Definition Diagram):** estrutura do sistema.
5. **Diagrama de Blocos Internos (IBD — Internal Block Diagram):** interfaces e fluxos entre blocos.
6. **Diagrama de Atividade (já estudado no Módulo 07, agora com fluxos de dados entre subsistemas).**
7. **Rastreabilidade de requisitos:** como ligar cada requisito a um bloco, teste e caso de uso.

### Fontes de estudo gratuitas

- **INCOSE Systems Engineering Handbook** — resumos disponíveis online.
- **SysML Distilled (resumos)** — busque "SysML tutorial" no YouTube.
- **Sparx Systems — SysML Tutorial** (sparxsystems.com/resources/tutorials/sysml).
- **PlantUML** — suporta alguns diagramas SysML.
- **draw.io** — templates de BDD e IBD disponíveis.

### Tempo estimado

6 a 10 horas. MBSE é mais conceitual e pode ser novo para você, então reserve tempo extra.

## Roteiro Diário

### Segunda-feira — Estudo de MBSE e SysML

- Assista a 2 a 3 vídeos sobre MBSE e SysML.
- Leia o tutorial da Sparx Systems.
- Entenda a diferença entre UML (foco em software) e SysML (foco em sistema).

### Terça-feira — Diagrama de Requisitos

- Pegue os requisitos do Módulo 07 e represente-os em um Diagrama de Requisitos SysML.
- Mostre:
  - Requisitos de alto nível derivando em sub-requisitos.
  - Relacionamentos: derive, satisfy, verify.
- Exemplo: `REQ-001: Gestão de Vendas` → deriva em `REQ-001.1: Registrar Venda`, `REQ-001.2: Cancelar Venda`, etc.

### Quarta-feira — Diagrama de Blocos (BDD)

- Modele o PharmaSystem como um sistema de blocos:

```
<<system>> PharmaSystem
  ├── <<subsystem>> Módulo de Vendas
  ├── <<subsystem>> Módulo de Estoque
  ├── <<subsystem>> Módulo de Help Desk
  ├── <<subsystem>> Módulo de Relatórios
  ├── <<subsystem>> Pipeline de Dados
  └── <<subsystem>> Gateway de Integração
```

- Mostre composição e associações entre blocos.

### Quinta-feira — Diagrama de Blocos Internos (IBD)

- Escolha um subsistema (ex.: Módulo de Vendas) e detalhe internamente:
  - Portas (ports): entrada de dados do caixa, saída de eventos de venda.
  - Fluxos: dados, sinais, chamadas.
  - Interfaces com outros subsistemas.
- Crie um IBD mostrando como o Módulo de Vendas se conecta ao Módulo de Estoque e ao Pipeline de Dados.

### Sexta-feira — Matriz de Rastreabilidade

- Crie uma matriz de rastreabilidade ligando:
  - Requisito → Bloco que satisfaz → Caso de uso relacionado → Teste que verifica.
- Exemplo em formato de tabela:

| Requisito | Bloco | Caso de Uso | Teste |
|---|---|---|---|
| RF01 | Módulo de Vendas | UC01 — Registrar Venda | TC01 — Venda com sucesso |
| RF05 | Módulo de Estoque | UC03 — Consultar Estoque | TC05 — Estoque atualizado |

- Pelo menos 10 linhas.

### Sábado — Documentação

- Compile os diagramas em um documento MBSE coeso.
- Escreva uma introdução explicando o que é MBSE e por que foi aplicado.
- Escreva o README.md.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com o BDD (diagrama mais visual e diferenciado).

## Entregáveis

- Diagrama de Requisitos SysML.
- Diagrama de Blocos (BDD) do sistema completo.
- Diagrama de Blocos Internos (IBD) de um subsistema.
- Diagrama de Atividade com fluxo entre subsistemas.
- Matriz de Rastreabilidade (10+ linhas).
- Documento MBSE compilado.
- README.md.

## Checklist de Publicação

**GitHub:**

- [ ] Diagramas em `diagramas/`.
- [ ] Documento MBSE em `docs/`.
- [ ] Matriz de rastreabilidade em `docs/`.
- [ ] README com: O que é MBSE, Diagramas, Rastreabilidade.

**LinkedIn:**

- [ ] Diagrama BDD (visual forte e diferenciado).
- [ ] Texto explicando: o que é MBSE, por que você aplicou ao PharmaSystem, como isso agrega valor.
- [ ] Hashtags: #MBSE #SysML #SystemsEngineering #EngenhariaDeSistemas #PortfólioDev

---

---

# MÓDULO 11 — Projeto Integrador

## Contexto no PharmaSystem

Este é o módulo de convergência. Você pega tudo que construiu — banco, API, dashboard, pipeline, sistema web — e integra em um fluxo ponta a ponta que funciona junto. O objetivo é provar que você não só sabe fazer cada peça, mas sabe fazer o sistema inteiro funcionar.

## O Que Estudar

Neste módulo, o estudo é substituído por revisão. Você não aprende nada novo; você faz os módulos anteriores conversarem.

### O que revisar (segunda)

- Revise a API (Módulo 05): ela ainda funciona? Os endpoints estão acessíveis?
- Revise o ETL (Módulo 04): ele carrega dados corretamente?
- Revise o sistema web (Módulo 06): consegue consumir a API?
- Revise o dashboard (Módulo 02/09): está conectado às tabelas analíticas?

## Roteiro Diário

### Segunda-feira — Inventário e Planejamento de Integração

- Liste todos os componentes existentes e seu estado atual.
- Defina o fluxo integrado:

```
[Filial] → Venda registrada via [Sistema Web ou API]
       → Dados persistidos no [PostgreSQL]
       → [Pipeline ETL] processa e alimenta [tabelas analíticas]
       → [Dashboard] mostra indicadores atualizados
       → [Help Desk] permite abertura de chamados
       → Tudo documentado em [Requisitos + Arquitetura + MBSE]
```

- Identifique pontos de integração que estão desconectados.

### Terça-feira — Conectar API ao Sistema Web

- Faça o sistema web do Módulo 06 consumir a API do Módulo 05 para listar produtos e filiais (em vez de consultar diretamente o banco).
- Exemplo: a tela de abertura de chamado carrega a lista de filiais via `GET /api/filiais`.

### Quarta-feira — Conectar Pipeline ao Dashboard

- Garanta que o pipeline do Módulo 09 alimenta as tabelas que o dashboard consome.
- Execute: API → Ingestão → Transformação → Dashboard atualizado.
- Adicione uma funcionalidade de "última atualização" no dashboard.

### Quinta-feira — Fluxo Completo End-to-End

- Demonstre o fluxo completo:
  1. Cadastre um produto via API.
  2. Registre uma venda via API ou sistema web.
  3. Execute o pipeline.
  4. Verifique o indicador atualizado no dashboard.
  5. Abra um chamado no Help Desk.
- Grave prints ou GIFs de cada etapa.

### Sexta-feira — Testes de Integração e Correções

- Execute tudo do zero e anote problemas.
- Corrija bugs de integração.
- Escreva um roteiro de demonstração passo a passo (como um "demo script" para apresentar a um recrutador ou professor).

### Sábado — Documentação do Integrador

- Crie um diagrama de integração mostrando como cada módulo se conecta.
- Escreva o README.md explicando: o que foi integrado, como executar, demo script.
- Atualize o README.md raiz do repositório `pharma-system/` com a visão geral de todos os módulos.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn mostrando o fluxo end-to-end.

## Entregáveis

- Integrações funcionais entre os módulos.
- Demonstração do fluxo end-to-end documentada (prints ou GIFs).
- Demo script (roteiro de apresentação).
- Diagrama de integração.
- README.md do módulo + README.md raiz atualizado.

## Checklist de Publicação

**GitHub:**

- [ ] Código de integração.
- [ ] Prints/GIFs do fluxo end-to-end em `docs/`.
- [ ] Demo script em `docs/`.
- [ ] README raiz atualizado com visão geral de todos os 11 módulos.

**LinkedIn:**

- [ ] Diagrama de integração.
- [ ] GIF ou sequência de prints do fluxo end-to-end.
- [ ] Texto: "integrei todos os módulos do meu portfólio em um sistema funcional".
- [ ] Hashtags: #Integração #FullStack #EndToEnd #EngenhariaDeSistemas #PortfólioDev

---

---

# MÓDULO 12 — Projeto Final

## Contexto no PharmaSystem

Este é o módulo de fechamento. Aqui você não constrói nada novo — você poliu, refina e empacota tudo como um produto profissional. O objetivo é que qualquer recrutador que entre no seu GitHub veja um projeto coeso, bem documentado e impressionante.

## O Que Fazer

### Segunda-feira — Revisão Geral de Código

- Percorra todos os módulos.
- Padronize nomes de variáveis e funções.
- Remova código comentado e debugs esquecidos.
- Garanta que cada módulo tem um `requirements.txt` ou equivalente.
- Verifique que tudo roda a partir do README (se alguém seguir as instruções, funciona?).

### Terça-feira — README Raiz Profissional

Reescreva o README.md raiz do repositório com qualidade profissional:

```markdown
# PharmaSystem — Sistema de Gestão para Rede de Farmácias

## Sobre o Projeto
O PharmaSystem é um ecossistema completo para gestão de uma rede 
de farmácias com 100 filiais, desenvolvido como portfólio acadêmico 
de Engenharia de Sistemas.

## Arquitetura
[Imagem do diagrama C4 Container]

## Módulos
| # | Módulo | Tecnologias | Descrição |
|---|--------|-------------|-----------|
| 01 | SQL | PostgreSQL | Banco de dados de vendas |
| 02 | Power BI | Power BI, DAX | Dashboard executivo |
| ... | ... | ... | ... |

## Stack Tecnológico
Python, Flask/Spring Boot, PostgreSQL, Power BI, Streamlit, 
Pandas, UML, SysML, MBSE

## Como Executar
[Instruções gerais + links para cada módulo]

## Sobre o Autor
[Seu nome, curso, universidade, LinkedIn, contato]
```

### Quarta-feira — Documentação Visual

- Reexporte todos os diagramas em alta resolução.
- Crie uma pasta `docs/apresentacao/` com as melhores imagens de cada módulo.
- Se possível, grave um vídeo de 2 a 3 minutos mostrando o sistema rodando (Loom ou OBS).

### Quinta-feira — Feature Extra (Diferencial)

Adicione uma funcionalidade extra que impressione:

Sugestões:

- **Predição simples:** use scikit-learn para prever vendas do próximo mês com regressão linear (mesmo que simples, mostra que você sabe integrar ML).
- **Notificação:** o pipeline envia um resumo por e-mail quando processa novos dados.
- **Autenticação JWT na API:** substitua sessões por tokens JWT (mais profissional).
- **Docker Compose:** crie um `docker-compose.yml` que sobe banco + API + dashboard com um comando.

Escolha UMA e implemente.

### Sexta-feira — Teste Final + Vídeo

- Execute o sistema inteiro do zero seguindo apenas o README.
- Se algo não funcionar, corrija.
- Grave o vídeo de demonstração (se não fez na quinta).

### Sábado — Publicação Final no GitHub

- Faça o push final.
- Adicione tags/releases no GitHub (v1.0).
- Fixe o repositório no perfil do GitHub.
- Verifique que o README raiz renderiza bonito com imagens e tabelas.

### Domingo — Publicação Final no LinkedIn

- Publique o post final: um retrospecto das 12 semanas.
- Modelo de post:

> Nas últimas 12 semanas, construí o PharmaSystem — um sistema completo 
> de gestão para uma rede de farmácias com 100 filiais.
>
> O que eu aprendi e apliquei:
> - SQL e modelagem de dados
> - Dashboards com Power BI e Streamlit
> - Análise exploratória com Python e Pandas
> - Pipeline ETL automatizado
> - API REST com [Flask/Spring Boot]
> - Sistema web com autenticação
> - Engenharia de requisitos e UML
> - Arquitetura de sistemas (C4 Model)
> - Engenharia de dados com Star Schema
> - MBSE com SysML
> - Integração de ponta a ponta
>
> Tudo documentado, versionado e acessível no GitHub.
>
> [Link para o repositório]

## Entregáveis Finais

- Repositório completo e polido.
- README raiz profissional.
- Feature extra implementada.
- Vídeo de demonstração (opcional, mas muito recomendado).
- Post final no LinkedIn.

---

---

# Resumo Visual do Cronograma

```
Semana  Módulo                    Foco Principal               Entrega Chave
──────  ────────────────────────  ─────────────────────────    ──────────────────────
  01    SQL                       Fundação de dados            20+ consultas SQL
  02    Power BI                  Visualização executiva       Dashboard 3 páginas
  03    Python + Pandas           Análise exploratória         Notebook + gráficos
  04    ETL                       Pipeline automatizado        Scripts modulares
  05    API REST                  Backend                      15+ endpoints
  06    Sistema Web               Full Stack                   Help Desk funcional
  07    Engenharia de Requisitos  Documentação formal          Requisitos + UML
  08    Arquitetura               Visão sistêmica              C4 + ADRs
  09    Engenharia de Dados       Data pipeline moderno        Star Schema + Streamlit
  10    MBSE                      Modelagem de sistemas        BDD + IBD + Rastreio
  11    Integrador                Conectar tudo                Fluxo end-to-end
  12    Projeto Final             Polimento + publicação       README profissional
```

---

# Dicas Gerais Para o Sucesso

**1. Não busque perfeição na primeira versão.** Publique o mínimo funcional no domingo e depois melhore durante a semana seguinte se necessário. Publicar com consistência é mais valioso do que ter um projeto perfeito daqui a 6 meses.

**2. Use o tempo de transporte e espera para estudar.** Os vídeos e artigos de estudo podem ser consumidos no celular. Reserve o computador para a construção.

**3. Se travar em um módulo, simplifique o escopo, não atrase.** Melhor entregar 15 consultas SQL do que não publicar nada porque queria fazer 30. Você pode sempre voltar e melhorar depois.

**4. O README é tão importante quanto o código.** Recrutadores raramente leem o código inteiro. Eles leem o README. Dedique tempo a ele.
