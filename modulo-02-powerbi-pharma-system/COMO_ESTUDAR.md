# Como Estudar Este Módulo — Roteiro de Engenharia Reversa

Este módulo foi construído para **estudo por engenharia reversa**. Você não recebe o `.pbix` pronto — recebe os ingredientes e um mapa. O objetivo é que ao final da semana **você tenha construído o dashboard sozinho**, entendendo cada decisão.

**Carga total:** ~10 horas divididas em 7 dias (1-2h por dia).

---

## Filosofia

A engenharia reversa aqui funciona assim:

1. **Olhe o resultado final** (mockups) antes de escrever qualquer código.
2. **Estude os artefatos isolados** (medidas DAX, tema, modelo) sem contexto.
3. **Reconstrua** conectando as peças, tirando dúvidas nos docs.
4. **Compare** seu resultado com a referência ao final.

O ganho não é chegar num `.pbix` bonito — é entender **por que** cada peça existe e como decidir por si próprio em projetos futuros.

---

## Roteiro de 7 Dias

### Dia 1 — Modelo Conceitual (1h) — SEM abrir Power BI ainda

**Objetivo:** entender o *quê* antes do *como*.

1. Abra os 3 mockups em `docs/mockup_pagina*.png`. Observe por 15 minutos:
   - Que perguntas de negócio cada página responde?
   - Quantos KPIs existem? Qual a hierarquia visual?
   - Onde a atenção vai primeiro? Por quê?
2. Abra `docs/especificacao_visuais.md` e leia até o final da Página 1.
3. Faça um **desenho seu à mão** (papel ou tablet) de uma quarta página fictícia (por exemplo: "Estoque"). Que KPIs colocaria? Que gráficos?
4. Abra `docs/modelo_dados.png` e responda por escrito:
   - Por que `calendario` está no topo?
   - Por que existem duas linhas ligando `calendario` (uma sólida, outra tracejada)?
   - Por que `vendas` está separada de `itens_venda`?
   - O que aconteceria se `filiais` fosse ligada direto em `itens_venda`?

**Entregável:** anotações à mão respondendo as 4 perguntas acima.

---

### Dia 2 — Importação e Power Query (1,5h)

**Objetivo:** dominar carga de dados e configuração inicial.

1. **Estudo prévio (30 min):** assista a um vídeo sobre importação de CSV no Power BI. Sugestões PT-BR gratuitas:
   - Karine Lago — "Importando dados no Power BI"
   - Hashtag Treinamentos — "Power BI para Iniciantes"
2. **Prática (60 min):** abra o Power BI Desktop e siga a **FASE 1** de `docs/guia_construcao.md`. Importe todos os 8 CSVs.
3. **Reflexão:** por que colocamos BOM UTF-8 nos arquivos? O que acontece se remover?

**Entregável:** `.pbix` salvo com dados carregados e tipos corrigidos.

**Se travar:** confira que os arquivos CSV têm delimitador **vírgula** (não ponto e vírgula). Se aparecerem caracteres estranhos (ç → �), a origem provavelmente foi detectada errada — force **65001 UTF-8**.

---

### Dia 3 — Modelo de Dados (1h)

**Objetivo:** entender Star Schema na prática.

1. **Estudo prévio (20 min):** leia sobre Star Schema. O DAX Guide (dax.guide) tem uma introdução conceitual excelente.
2. **Prática (40 min):** siga a **FASE 2** de `docs/guia_construcao.md`. Configure os 9 relacionamentos.
3. **Reflexão:** teste — arraste `filiais[nome]` numa tabela e adicione `SUM(itens_venda[subtotal])`. Funciona? Por que sim/não?

**Entregável:** modelo com todos os relacionamentos corretos + tabela calendário marcada.

**Teste rápido:** crie uma tabela na página em branco com `filiais[nome]` e `SUM(vendas[valor_total])`. Deve mostrar valores por filial. Se der 0 ou em branco, revisite os relacionamentos.

---

### Dia 4 — Medidas DAX Base + Time Intelligence (2h)

**Objetivo:** entender contexto de filtro e CALCULATE.

1. **Estudo prévio (30 min):** o conceito de **contexto de filtro** é a chave de tudo em DAX. Assista a "SQLBI - Introduction to filter context" (YouTube, EN com legendas) ou o equivalente na Karine Lago em PT-BR.
2. **Prática A (45 min):** abra `dax/01_medidas_base.dax`. Crie **uma medida por vez** e a teste imediatamente em uma tabela ao lado. Depois de cada medida, tente **descrevê-la em português** antes de olhar o comentário. Se você conseguir explicar, entendeu.
3. **Prática B (45 min):** faça o mesmo com `dax/02_medidas_temporais.dax`. Aqui é fundamental testar — por exemplo, `Faturamento Mês Anterior` só faz sentido se você tiver o mês no contexto.

**Entregável:** 21 medidas criadas, formatadas e testadas em uma tabela de conferência.

**Desafio extra:** você consegue criar `Faturamento Trimestre Anterior` sem olhar? (Dica: `DATEADD(-1, QUARTER)`)

---

### Dia 5 — Medidas Avançadas + Página 1 (2h)

**Objetivo:** medidas com RANKX/TOPN e primeira página completa.

1. **Prática A (30 min):** crie as 11 medidas de `dax/03_medidas_avancadas.dax`. `RANKX` merece atenção — teste colocando `filiais[nome]` numa tabela com `Ranking Filial` e veja como muda.
2. **Prática B (30 min):** aplique o tema. Vá em `docs/guia_construcao.md` **FASE 4**. Nada deve mudar visualmente ainda, mas as cores padrões passam a ser as da PharmaSystem.
3. **Prática C (60 min):** construa a **Página 1 completa** (FASE 5 do guia). Não tente decorar — abra o mockup ao lado e reconstrua elemento por elemento.

**Entregável:** Página 1 pronta, com KPIs, gráfico de linhas, top filiais, donut, colunas de dia da semana e tabela.

**Reflexão:** compare sua página 1 com o mockup. O que ficou diferente? Foi intencional ou por não conseguir replicar?

---

### Dia 6 — Páginas 2 e 3 (2h)

**Objetivo:** replicar o padrão para produtos e clientes.

1. **Prática A (60 min):** duplique a Página 1 e adapte para **Produtos** (FASE 6). Foco: cartão do produto campeão (que usa `Produto Mais Vendido`) e painel de alertas coloridos (esse é 100% criativo — não tem no Power BI nativo, você monta com formas e caixas de texto).
2. **Prática B (60 min):** duplique novamente para **Clientes** (FASE 7). Foco: criar a coluna calculada `Faixa Etaria` e usar `USERELATIONSHIP` na medida `Novos Clientes` (relacionamento inativo entra em cena aqui).

**Entregável:** 3 páginas prontas, todos os botões de navegação funcionando.

---

### Dia 7 — Refinamento e Publicação (1,5h)

**Objetivo:** deixar profissional.

1. **Refinamento (60 min):** siga a **FASE 8**:
   - Padronize fontes.
   - Adicione sombras nos containers.
   - Configure tooltips ao menos nos gráficos principais.
   - Teste os segmentadores — todos filtram tudo?
   - Ajuste alinhamentos com `Formato → Alinhar`.
2. **Publicação (30 min):** siga a **FASE 9**:
   - Exporte 3 PNGs (um por página) usando a Ferramenta de Captura do Windows.
   - Commit no GitHub em `pharma-system/modulo-02-powerbi/`.
   - Escreva o post do LinkedIn (rascunho está no `README.md`).

**Entregável final:** `.pbix` no GitHub + post no LinkedIn.

---

## Checklist final

Ao terminar o Dia 7, você deve ter:

- [ ] Todos os 8 CSVs carregados no Power BI.
- [ ] Modelo Star Schema com 8 relacionamentos ativos e 1 inativo.
- [ ] Tabela `calendario` marcada como Tabela de Data.
- [ ] 32 medidas DAX criadas, formatadas e organizadas em pastas.
- [ ] Tema `tema_pharmasystem.json` aplicado.
- [ ] 3 páginas construídas seguindo os mockups.
- [ ] Botões de navegação funcionando entre as páginas.
- [ ] Segmentadores filtrando todos os visuais corretamente.
- [ ] Prints das 3 páginas em `docs/prints/`.
- [ ] `.pbix` comitado no GitHub.
- [ ] Post do LinkedIn publicado.

---

## Como aprender melhor

**Faça sem consultar sempre que possível.** O guia está lá para desbloquear, não para copiar. Se você conseguir construir a Página 1 olhando só o mockup e a especificação de visuais, aprendeu de verdade.

**Erre e revise.** Se uma medida não funciona, tente descobrir sozinho por 10 minutos antes de olhar. Erros são o momento onde o aprendizado acontece.

**Explique em voz alta.** Depois de criar uma medida DAX, explique o que ela faz como se ensinasse alguém. Se não conseguir, ainda não entendeu.

**Documente para você mesmo.** Ao final do dia, escreva 2-3 linhas sobre o que aprendeu e o que ficou confuso. Isso vira sua "cola" pessoal.

---

## Recursos gratuitos

- **Microsoft Learn — Power BI:** trilha oficial com certificado.
- **DAX Guide** (dax.guide): referência canônica de funções DAX.
- **SQLBI** (sqlbi.com): artigos técnicos de altíssimo nível.
- **Karine Lago** (YouTube, PT-BR): tutoriais práticos de dashboards.
- **Hashtag Treinamentos** (YouTube, PT-BR): fundamentos Power BI.

---

## O que você vai saber ao final

- **Modelagem dimensional (Star Schema):** dimensão vs. fato, tabela calendário, marca de tabela de datas.
- **Relacionamentos:** ativos, inativos, cardinalidade, direção de filtro.
- **Power Query:** importação, tipos, colunas calculadas.
- **DAX:** contexto de filtro, `CALCULATE`, `FILTER`, `ALL`, `RANKX`, `TOPN`, `SUMX`, time intelligence (`DATEADD`, `SAMEPERIODLASTYEAR`, `DATESYTD`, `DATESINPERIOD`), `USERELATIONSHIP`, `VAR`, `SWITCH`, `CONCATENATEX`, `FORMAT`.
- **Design de dashboard:** paleta consistente, hierarquia visual, KPIs, formatação condicional.
- **Interatividade:** slicers, botões de navegação, editar interações, tooltips customizados.

Habilidades que vão para o Módulo 03 (Python/Pandas — dashboards em Streamlit) e para qualquer projeto de BI que você for tocar no trabalho ou em outros portfolios.

**Bons estudos!**
