# Como Estudar Este Módulo por Engenharia Reversa

> Este arquivo é o **guia de estudo** para quem recebeu este pacote pronto e quer fazer engenharia reversa: entender profundamente cada decisão de modelagem, cada consulta SQL, e depois **reproduzir tudo do zero sem olhar**.

---

## 🎯 A ideia

Engenharia reversa aqui significa: você tem uma solução pronta e boa. Sua missão é entender **por quê** cada coisa é do jeito que é, e depois construir você mesmo. No final, você deve conseguir:

1. Explicar cada decisão de modelagem em voz alta.
2. Escrever qualquer uma das 25 consultas sem consultar o arquivo.
3. Estender o sistema (adicionar novas tabelas, novas consultas).

---

## 📅 Roteiro sugerido — 5 dias

### Dia 1 — Modelo Conceitual (2h)

**O quê:** Entender **o que** o sistema modela, sem olhar SQL ainda.

**Como:**
1. Abra `README.md` e leia a seção "Contexto de negócio".
2. Abra `docs/diagrama_er.png` e olhe o diagrama. **Não olhe o SQL ainda.**
3. Responda **por escrito** (num caderno ou markdown):
   - Quantas entidades existem?
   - Quais são as relações principais?
   - Por que `estoque` é uma tabela separada de `produtos`?
   - Por que `itens_venda` é separado de `vendas`?
   - Por que `cliente_id` em vendas é opcional (0:N)?
4. Só depois abra `docs/dicionario_dados.md` e confira suas respostas.

**Entregável mental:** Você deve conseguir desenhar o diagrama ER de memória.

---

### Dia 2 — Schema Físico (3h)

**O quê:** Entender **como** o modelo vira SQL DDL.

**Como:**
1. Abra `01_schema.sql`. Leia do início ao fim, prestando atenção a:
   - Ordem em que as tabelas são criadas (por quê nessa ordem?).
   - Tipos de dados escolhidos (`SERIAL` vs `INTEGER`, `VARCHAR(N)` vs `TEXT`, `DECIMAL(10,2)` para dinheiro).
   - Constraints:
     - `CHECK` para regras de negócio (`preco_venda >= preco_custo`).
     - `CHECK` com regex (`estado ~ '^[A-Z]{2}$'`).
     - `FK` com diferentes `ON DELETE` (CASCADE, RESTRICT, SET NULL) — por que cada uma?
     - `UNIQUE` composto em `estoque(produto_id, filial_id)`.
   - Índices criados: por que essas colunas?

2. Feche o arquivo. **Reescreva o schema do zero num arquivo novo.** Compare depois.

3. Perguntas de reflexão:
   - Por que `ON DELETE CASCADE` em `itens_venda → vendas` mas `ON DELETE RESTRICT` em `itens_venda → produtos`?
   - Por que `ON DELETE SET NULL` em `vendas → clientes`?
   - Por que `preco_unitario` está em `itens_venda` e não usamos o `produto.preco_venda`?

**Entregável físico:** Seu próprio `01_schema.sql` reescrito de memória.

---

### Dia 3 — População de Dados (2h)

**O quê:** Entender como gerar dados sintéticos realistas.

**Como:**
1. Abra `scripts/gerar_dados.py`.
2. Estude:
   - Como as filiais foram distribuídas geograficamente.
   - Como os produtos foram criados com códigos de barras, categorias, preços.
   - Como as vendas foram distribuídas no tempo com viés (60% no último ano).
   - Como a forma de pagamento é escolhida por probabilidade.
   - Por que existe `random.seed(42)` no início.
3. Rode o script você mesmo. Confirme que ele gera o mesmo arquivo `02_inserts.sql`.
4. **Modifique** o script: aumente para 5000 vendas, adicione uma nova categoria, mude os pesos das filiais.
5. Confira que a estrutura dos INSERTs em `02_inserts.sql` respeita a ordem: filiais → categorias → produtos → estoque → clientes → vendas → itens_venda (por quê?).

**Entregável físico:** Uma variação sua do script gerando 3000 vendas.

---

### Dia 4 — Consultas SQL (4h — o cerne)

**O quê:** Dominar as 25 consultas.

**Como:**
1. Abra `03_consultas.sql`.
2. Para **cada consulta** (Q01 a Q25):
   - Leia o cabeçalho (objetivo).
   - **Antes de olhar o SQL**, escreva sua tentativa num arquivo separado.
   - Compare com a resposta oficial. Identifique diferenças.
   - Rode a consulta no banco. Confira contra `exemplos_resultados/resultados_consultas.md`.

3. Marque as consultas em três níveis:
   - 🟢 **Fácil** (Q01, Q02, Q04, Q17, Q19, Q20)
   - 🟡 **Média** (Q03, Q05, Q07, Q08–Q14, Q15, Q16)
   - 🔴 **Difícil** (Q11 com margem, Q21 com CTE, Q22–Q25 com Window Functions e self-join)

4. Nas difíceis, gaste tempo extra entendendo:
   - **Q22 (RANK):** por que `PARTITION BY mes_ano`? O que aconteceria sem?
   - **Q23 (LAG):** o que `LAG(faturamento) OVER (ORDER BY mes)` retorna para a primeira linha? Como o `NULLIF` evita divisão por zero?
   - **Q24 (média móvel):** o que `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` significa? Como muda se for 4 PRECEDING?
   - **Q25 (self-join):** por que `iv1.produto_id < iv2.produto_id`? (Sem isso, cada par apareceria duas vezes.)

**Entregável físico:** Um arquivo `minhas_consultas.sql` com todas as 25 refeitas do zero. Bônus: crie 5 novas suas.

---

### Dia 5 — Views e Publicação (2h)

**O quê:** Entender views e preparar o repositório para publicação.

**Como:**
1. Abra `04_views.sql`. Cada view é uma consulta encapsulada. Entenda:
   - Por que essas 5 views foram escolhidas? (Reutilização.)
   - Como `vw_ranking_filiais` usa `FILTER (WHERE ...)` para separar concluídas de canceladas.
   - Como `vw_ranking_produtos` usa `RANK() OVER (...)` para gerar dois rankings simultâneos.
   - Como `vw_clientes_top` calcula RFM básico (Recência, Frequência, Monetary).

2. Rode `SELECT * FROM vw_XXX LIMIT 10;` para cada view.

3. Prepare seu **post do LinkedIn** e seu **README do GitHub**. Use o modelo em `README.md` como base.

4. Crie o repositório `pharma-system` no GitHub, coloque tudo em `modulo-01-sql-pharma-system/`, commit e push.

**Entregável físico:** Post publicado + repositório público no GitHub.

---

## 🧠 Exercícios extras (opcionais)

Se sobrar tempo, tente estes desafios:

1. **Materialized View:** Transforme `vw_faturamento_mensal` em uma `MATERIALIZED VIEW`. Quais os prós e contras?

2. **Trigger:** Crie um trigger que atualiza `estoque.quantidade` automaticamente quando uma venda é finalizada.

3. **Função:** Crie uma função `fn_faturamento_periodo(data_inicio DATE, data_fim DATE)` que recebe duas datas e retorna o faturamento no intervalo.

4. **Auditoria:** Adicione uma tabela `vendas_auditoria` que armazena o histórico de mudanças (via trigger).

5. **Particionamento:** Estude como particionar `vendas` por ano — quando isso vale a pena?

6. **Explain Analyze:** Rode `EXPLAIN ANALYZE` em Q22 (Window Function). Entenda o plano de execução. Adicione índices se necessário.

7. **Full Text Search:** Crie um índice GIN para busca full-text no nome dos produtos.

---

## ⚠️ Erros comuns a evitar

- **Esquecer o WHERE status = 'CONCLUIDA'** ao somar faturamento (contaria canceladas).
- **Confundir `valor_total` com `valor_total - desconto`** (líquido é sempre depois do desconto).
- **`GROUP BY` mal formado**: toda coluna do SELECT que não é agregação precisa estar no GROUP BY.
- **Divisão por zero**: sempre `NULLIF(x, 0)` em denominadores.
- **`COUNT(*)` vs `COUNT(coluna)`**: o segundo ignora NULLs.

---

## 📖 Referências gratuitas

Se travar em algum conceito, consulte:

- **SQL básico:** [SQLBolt](https://sqlbolt.com/) — interativo, 15 lições.
- **Window Functions:** [Mode SQL Analytics Training](https://mode.com/sql-tutorial/sql-window-functions/)
- **PostgreSQL:** [Documentação oficial em PT-BR](https://www.postgresql.org/docs/current/index.html)
- **Kaggle Learn — Advanced SQL:** [Kaggle Learn](https://www.kaggle.com/learn/advanced-sql)
- **Livro grátis:** [SQL Antipatterns](https://pragprog.com/titles/bksqla/sql-antipatterns/) (Bill Karwin — algumas amostras livres)

---

## ✅ Checklist final

Antes de considerar a semana concluída, garanta:

- [ ] Consigo desenhar o ER de memória.
- [ ] Executei `01_schema.sql`, `02_inserts.sql` e `04_views.sql` no meu PostgreSQL local.
- [ ] Rodei todas as 25 consultas e confirmei os resultados.
- [ ] Escrevi minha própria versão do `01_schema.sql` sem olhar o original.
- [ ] Refiz pelo menos 15 das 25 consultas de memória.
- [ ] Entendo (em voz alta) por que `Q22`, `Q23`, `Q24` e `Q25` funcionam.
- [ ] Repositório `pharma-system` está no GitHub com este módulo.
- [ ] Post no LinkedIn publicado.

**Se todos os itens acima estão marcados, você dominou o Módulo 01. Próxima parada: Semana 2 (Power BI).** 🚀
