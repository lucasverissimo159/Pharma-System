# Como Estudar Este Módulo — Roteiro de Engenharia Reversa

Este pacote entrega uma análise pronta e executável. Mas o objetivo do estudo NÃO é rodar o script — é **reconstruir tudo do zero olhando o resultado final** para entender cada decisão.

**Carga total:** 8 a 10 horas em 7 dias (~1-1,5h por dia).

---

## Filosofia

O truque da reversa aqui é: você tem o gabarito visível. Isso liberta você para tentar sozinho — se travar, olha o gabarito, entende, apaga, tenta de novo até fazer sem consultar.

O que você recebe:
- Notebook `01_analise_exploratoria.ipynb` já executado (com gráficos)
- 10 PNGs prontos como referência visual
- Excel pronto como referência de estrutura final
- Pacote Python `src/` com código modular como implementação de referência
- `docs/insights.md` com os 6 insights de negócio já extraídos

O que você vai construir:
- Seu próprio notebook do zero, replicando cada análise
- Sua própria versão modular em `src/`
- Seus próprios insights (que podem ser diferentes/adicionais aos meus)

---

## Pré-requisitos

- Python 3.10+ instalado
- Editor com suporte a Jupyter: **VS Code** (extensão Jupyter) ou **Jupyter Lab** ou **Google Colab**
- Familiaridade básica com Python (funções, listas, dicionários)

Se Pandas for novo pra você, faça primeiro o [Kaggle Learn - Pandas](https://www.kaggle.com/learn/pandas) — leva 4h e é suficiente.

---

## Setup (30 min)

```bash
# Clone/extraia o pacote
cd modulo-03-python-pandas-pharma-system

# Crie ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instale dependências
pip install -r requirements.txt

# Teste que tudo funciona
python scripts/executar_analise.py
```

Se rodou sem erro, os arquivos em `graficos/` e `exports/` foram regerados. Pronto para estudar.

---

## Roteiro de 7 Dias

### Dia 1 — Explorar o resultado (1h)

**Sem escrever código.**

1. Abra `notebooks/01_analise_exploratoria.ipynb` no VS Code (ou GitHub) e leia do início ao fim (15 min).
2. Abra `exports/relatorio_pharma_system.xlsx` e navegue pelas 9 abas (15 min).
3. Olhe os 10 PNGs em `graficos/` e tente responder: por que cada gráfico foi escolhido? Que pergunta cada um responde? (15 min)
4. Leia `docs/insights.md` (15 min). Você concorda com os insights? Faria outros?

**Entregável:** anotações no seu caderno com 3 perguntas que você teria feito diferente.

---

### Dia 2 — Carregamento de dados (1,5h)

**Objetivo:** dominar `pd.read_csv` e tipos.

1. Crie um notebook novo em branco: `meus_estudos/01_carregamento.ipynb`.
2. **Sem consultar** `src/carregamento.py`, tente carregar cada CSV em um DataFrame separado.
3. Explore com `df.info()`, `df.dtypes`, `df.head()`, `df.describe()`.
4. Consulte `src/carregamento.py` e compare:
   - Por que ele usa `dtype` explícito?
   - Por que `parse_dates` separado?
   - Por que encoding `utf-8-sig`?
5. Refaça seu notebook aplicando os aprendizados.

**Desafio:** modifique a função para carregar apenas linhas dos últimos 6 meses (`nrows` ou filtro pós-carregamento?).

---

### Dia 3 — Limpeza e colunas derivadas (1,5h)

**Objetivo:** transformações com Pandas.

1. Em `meus_estudos/02_limpeza.ipynb`, tente sozinho:
   - Criar coluna `valor_liquido` em `vendas`
   - Extrair `ano_mes` e `dia_semana_nome` de `data_venda`
   - Calcular `margem_lucro` em `produtos`
   - Calcular `idade` em `clientes` (dica: `(hoje - data_nascimento).dt.days / 365.25`)
2. Consulte `src/limpeza.py` e compare técnicas.
3. **Ponto de atenção:** o cast `float → Int64` no cálculo de idade é traiçoeiro. Veja como está resolvido no código de referência.
4. Depois de limpezas simples, reproduza o **`criar_dataframe_master`**: entenda cada `merge` e por que a ordem importa.

**Desafio:** faça uma versão alternativa do master usando `pd.concat` com `axis=1` em vez de `merge`. Funciona? Quando cada abordagem é melhor?

---

### Dia 4 — Análises e agregações (2h)

**Objetivo:** dominar `groupby`, `agg`, `pivot_table`.

1. Em `meus_estudos/03_analises.ipynb`, tente reproduzir sem consultar:
   - Faturamento por mês (`groupby('ano_mes').agg({'subtotal': 'sum'})`)
   - Ranking de filiais (agrupar, ordenar, adicionar `%`)
   - Top 10 produtos por faturamento
2. **Erro comum:** somar `subtotal` sem filtrar `status == 'CONCLUIDA'` infla o faturamento. Detecte isso no seu código antes de olhar o gabarito.
3. Consulte `src/analises.py` e compare:
   - Padronização de `apenas_concluidas`
   - Uso de `nunique` para contar vendas distintas quando o master tem múltiplos itens por venda
   - Ranking com `range(1, len+1)`

**Desafio avançado:** implemente `concentracao_top_10` com uma lambda. Depois compare com a versão do código.

---

### Dia 5 — Gráficos com Matplotlib + Seaborn (2h)

**Objetivo:** visualização com estilo consistente.

1. Em `meus_estudos/04_graficos.ipynb`, tente reproduzir olhando **só o PNG**:
   - `01_faturamento_mensal.png` (linha com média móvel)
   - `02_top_filiais.png` (barras horizontais coloridas)
   - `06_heatmap_correlacao.png` (seaborn heatmap com máscara triangular)
2. Consulte `src/graficos.py` e observe:
   - Como `aplicar_estilo()` centraliza a configuração
   - O uso de `FuncFormatter` para "R$ 42k" no eixo
   - Como o Pareto usa `fill_between` para sombreamento
3. **Padrão profissional:** todo gráfico retorna `fig` (Figure), o caller decide se salva ou mostra.

**Desafio:** crie um 11º gráfico — dispersão de `preco_venda` vs `unidades_vendidas` por produto, para identificar outliers de demanda.

---

### Dia 6 — Análise de clientes RFM + Insights (1,5h)

**Objetivo:** análise de negócio, não só cálculo.

1. Em `meus_estudos/05_clientes.ipynb`, implemente do zero:
   - `analise_clientes` com `n_compras`, `ltv`, `ticket_medio`, `dias_desde_ultima`
   - Classificação de `status` (Ativo/Em risco/Inativo) por dias desde última compra
   - Quartis de LTV (`pd.qcut`)
2. Escreva **seus próprios 6 insights** baseados nas análises. Não copie os meus.
3. Compare com `docs/insights.md` — o quê está igual? O quê ficou diferente?

**Ponto-chave da carreira:** um analista júnior gera gráficos. Um analista sênior gera **insights**. Este dia é sobre isso.

---

### Dia 7 — Exportação, empacotamento e publicação (1,5h)

**Objetivo:** entregável profissional.

1. Estude `src/exportacao.py`. Foco em:
   - Uso do `openpyxl` para formatação (fonte, cor, borda)
   - `ColorScaleRule` para formatação condicional na aba filiais
   - Reuso de estilos com constantes (`FONT_HEADER`, `FILL_HEADER`)
2. Consolide seu notebook: limpe células de teste, adicione títulos hierárquicos, coloque a fonte no primeiro parágrafo de cada seção.
3. **Publicação:**
   - `git init && git add . && git commit`
   - Suba para o GitHub em `pharma-system/modulo-03-python-pandas/`
   - Verifique que o `.ipynb` renderiza corretamente no GitHub
   - Escreva o post do LinkedIn (rascunho no README)

**Entregável final:** seu repositório público + post publicado.

---

## Checklist final

- [ ] Notebook próprio criado replicando as análises
- [ ] Pacote `src/` próprio (mesmo que copiado do original, mas você lê e entende cada linha)
- [ ] Excel gerado programaticamente
- [ ] 10 gráficos (ou mais) no seu `graficos/`
- [ ] Insights próprios em `docs/insights.md`
- [ ] README completo
- [ ] `requirements.txt` com versões exatas do seu ambiente
- [ ] Push no GitHub
- [ ] Post no LinkedIn

---

## Erros comuns e como evitar

**"Meu faturamento total deu diferente"** → provavelmente não filtrou `status == 'CONCLUIDA'`, ou está somando `valor_total` (que é por venda) em vez de `subtotal` (por item) no master.

**"Meu master tem linhas duplicadas"** → algum merge deu `many-to-many`. Verifique se as chaves são únicas do lado "1" da relação.

**"Meu heatmap está horrível"** → não aplicou máscara triangular (`np.triu`) e não escolheu paleta divergente centrada em zero (`cmap="RdYlGn", center=0`).

**"Meu Excel abre sem formatação"** → esqueceu de definir `cell.font`, `cell.fill`, `cell.alignment`. `openpyxl` só formata o que você mandar.

**"Meu notebook está com 40MB"** → algum gráfico foi renderizado em resolução altíssima. Use `dpi=100`, não `dpi=300`.

---

## Recursos gratuitos recomendados

- **[Pandas Docs](https://pandas.pydata.org/docs/getting_started/)** — canônico.
- **[Kaggle Learn - Pandas](https://www.kaggle.com/learn/pandas)** — 4h interativo.
- **[Seaborn Gallery](https://seaborn.pydata.org/examples/)** — inspiração visual.
- **[Real Python - Pandas Tutorials](https://realpython.com/learning-paths/pandas-data-science/)** — profundo.
- **[Karine Lago (YouTube, PT-BR)](https://www.youtube.com/c/KarineLago)** — Pandas prático.

---

## O que você vai saber ao final

- **Pandas core:** DataFrame, Series, `loc/iloc`, `groupby`, `agg`, `merge`, `pivot_table`, `qcut`, `cut`, funções de string e data.
- **Limpeza:** tratamento de nulos, tipos, duplicatas, cast seguro entre tipos.
- **Visualização:** Matplotlib (Figure/Axes, ticks, formatters, layout) + Seaborn (histplot, boxplot, heatmap, temas).
- **Análise:** KPIs, agregações complexas, rankings, RFM, curva de Pareto, correlações.
- **Exportação:** Excel multi-aba com openpyxl, formatação condicional, estilos.
- **Engenharia de código:** separação de responsabilidades em módulos, funções puras que retornam DataFrames, docstrings.

Habilidades diretamente aplicáveis em **qualquer projeto de análise de dados** — no trabalho, em portfólio ou em freelance.

**Bons estudos!**
