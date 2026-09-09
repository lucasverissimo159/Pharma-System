# Módulo 03 — Análise Exploratória com Python + Pandas

**PharmaSystem — Semana 3 de 12 do portfólio**

Análise exploratória de dados (EDA) sobre os dados de vendas da rede fictícia PharmaMinas, com Pandas, Matplotlib e Seaborn. O entregável é um notebook Jupyter com 51 células, 10 gráficos, um relatório Excel multi-aba e um pacote Python modular reutilizável.

---

## Prévia dos resultados

| Métrica | Valor |
|---|---|
| Faturamento total | R$ 226.548,60 |
| Vendas concluídas | 1.458 |
| Ticket médio | R$ 155,38 |
| Margem bruta | 54,4% |
| Clientes distintos | 200 |
| Filial líder | BH Savassi (18,9% do total) |
| Concentração top 10 SKUs | 54,1% do faturamento |

**6 insights de negócio** completos em `docs/insights.md`.

---

## Diferencial deste módulo

Ao contrário do Módulo 02 (que entregava blueprint para você construir o Power BI), aqui **tudo já foi executado**:

- Notebook Jupyter com todos os outputs pré-renderizados (10 gráficos embutidos como base64)
- 10 PNGs de alta qualidade na pasta `graficos/`
- Relatório Excel de 9 abas pronto em `exports/`
- Pacote Python `src/` modular e testado

Você pode **abrir o notebook no GitHub e ver tudo funcionando** sem rodar uma linha. Depois, para estudar por engenharia reversa, você limpa os outputs e reexecuta célula por célula.

---

## Estrutura do pacote

```
modulo-03-python-pandas-pharma-system/
├── README.md                            (este arquivo)
├── COMO_ESTUDAR.md                      Roteiro de reversa (7 dias)
├── requirements.txt                     Dependencias Python
│
├── dados/                               8 CSVs (herdados do Módulo 02)
│   ├── filiais.csv, categorias.csv, produtos.csv, estoque.csv
│   ├── clientes.csv, vendas.csv, itens_venda.csv, calendario.csv
│
├── notebooks/
│   └── 01_analise_exploratoria.ipynb    Notebook principal (51 células)
│
├── src/                                 Pacote Python modular
│   ├── __init__.py
│   ├── carregamento.py                  Leitura de CSVs com tipos corretos
│   ├── limpeza.py                       Limpeza + colunas derivadas + master DF
│   ├── analises.py                      Funções de agregação e KPIs
│   ├── graficos.py                      Estilos + 10 gráficos
│   └── exportacao.py                    Excel multi-aba com openpyxl
│
├── graficos/                            10 PNGs (~600 KB total)
│   ├── 01_faturamento_mensal.png
│   ├── 02_top_filiais.png
│   ├── 03_faturamento_categorias.png
│   ├── 04_distribuicao_precos.png
│   ├── 05_boxplot_margem_categoria.png
│   ├── 06_heatmap_correlacao.png
│   ├── 07_vendas_dia_semana.png
│   ├── 08_faturamento_faixa_etaria.png
│   ├── 09_frequencia_compra_clientes.png
│   └── 10_pareto_produtos.png
│
├── exports/
│   └── relatorio_pharma_system.xlsx     Relatório executivo (9 abas)
│
├── scripts/
│   ├── executar_analise.py              Reexecuta tudo do zero
│   └── gerar_notebook.py                Regera o .ipynb com outputs
│
└── docs/
    └── insights.md                       6 insights de negócio explicados
```

---

## Como usar

### Opção A — Só olhar o resultado

Basta abrir os arquivos:
- **`notebooks/01_analise_exploratoria.ipynb`** no VS Code ou Jupyter (ou clique no arquivo direto no GitHub)
- **`exports/relatorio_pharma_system.xlsx`** no Excel
- **`graficos/*.png`** em qualquer visualizador

Nenhum código precisa ser executado.

### Opção B — Reexecutar tudo

Instale as dependências e rode:

```bash
pip install -r requirements.txt
python scripts/executar_analise.py
```

Gera todos os PNGs (`graficos/`) e o Excel (`exports/`) do zero em ~5 segundos.

### Opção C — Estudar por engenharia reversa (RECOMENDADO)

Ver `COMO_ESTUDAR.md` para o roteiro de 7 dias. A ideia é limpar os outputs do notebook e reconstruir célula por célula entendendo cada linha.

---

## O que o notebook cobre

1. **Setup** e importação do pacote `src/`
2. **Carregamento** de 8 CSVs em DataFrames com tipos corretos
3. **Diagnóstico** de nulos, tipos e duplicatas (`diagnosticar`)
4. **Limpeza + colunas derivadas:** valor líquido, ano/mês, dia da semana, hora, margem de lucro, idade, faixa etária
5. **DataFrame master** (denormalizado, 3.253 linhas × 34 colunas)
6. **KPIs gerais** (9 métricas)
7. **Análise temporal** (evolução mensal + média móvel)
8. **Ranking de filiais** (barras horizontais + % do total)
9. **Análise de produtos** (top 15 + distribuição de preços)
10. **Análise de categorias** (barras + boxplot de margem)
11. **Formas de pagamento** (tabela + %)
12. **Distribuição por dia da semana** (barras)
13. **Análise de clientes RFM básico** (Recency, Frequency, Monetary + quartis)
14. **Segmentação por faixa etária** (barras horizontais)
15. **Correlações** (heatmap)
16. **Curva de Pareto** (concentração 80/20)
17. **Insights de negócio** (6 achados executivos)
18. **Exportação** para Excel multi-aba

---

## As 5 dependências principais

| Biblioteca | Versão mínima | Uso |
|---|---|---|
| pandas | 2.0+ | DataFrames, merges, agregações |
| numpy | 1.24+ | Operações numéricas |
| matplotlib | 3.7+ | Gráficos base |
| seaborn | 0.12+ | Boxplot, heatmap, temas |
| openpyxl | 3.1+ | Excel multi-aba com formatação |

Ver `requirements.txt` para versões testadas.

---

## Modelo modular (`src/`)

O código está organizado em módulos, com responsabilidade única:

- **`carregamento.py`** — só lê arquivos. Nenhuma transformação.
- **`limpeza.py`** — só transforma. Não lê nem plota.
- **`analises.py`** — só agrega/calcula. Não plota nem exporta.
- **`graficos.py`** — só desenha. Recebe DataFrames prontos.
- **`exportacao.py`** — só escreve Excel. Recebe DataFrames prontos.

Essa separação facilita testes, manutenção e reuso em outros projetos. É o mesmo padrão que qualquer engenharia de dados séria usa.

---

## Reprodutibilidade

- Dataset sintético com **seed=42** (idêntico ao Módulo 01 e 02).
- Sem chamadas de rede, sem dependência de banco de dados.
- Executa em qualquer máquina com Python 3.10+ e as bibliotecas do `requirements.txt`.

Após rodar `python scripts/executar_analise.py`, os arquivos em `graficos/` e `exports/` são bit-exatos do que está commitado.

---

## Publicação no GitHub

Estrutura sugerida no repositório `pharma-system`:

```
pharma-system/
├── modulo-01-sql/
├── modulo-02-powerbi/
└── modulo-03-python-pandas/    ← este módulo
    ├── notebooks/*.ipynb        (GitHub renderiza automaticamente!)
    ├── graficos/*.png
    ├── exports/*.xlsx
    ├── src/
    ├── scripts/
    ├── docs/
    ├── README.md
    └── requirements.txt
```

Ao subir para o GitHub, o notebook renderiza como página completa direto no navegador — os gráficos já estão embutidos como base64 no arquivo.

---

## Post do LinkedIn — Rascunho

> 📊 Semana 3 do meu portfólio de Engenharia de Sistemas concluída!
>
> Análise exploratória completa de vendas da rede fictícia PharmaMinas em Python + Pandas.
>
> Highlights:
> ✅ Notebook Jupyter com 51 células (25 markdown + 26 código)
> ✅ Pacote Python modular (carregamento, limpeza, análises, gráficos, exportação)
> ✅ 10 visualizações com Matplotlib + Seaborn
> ✅ Relatório Excel de 9 abas gerado programaticamente
> ✅ RFM básico de clientes (Recency, Frequency, Monetary)
> ✅ Curva de Pareto do catálogo
>
> Alguns achados:
> 🔍 Filial líder concentra 18,9% do faturamento (3x acima da mediana)
> 🔍 Ticket médio de FdS ≈ dia útil (-1,4%)
> 🔍 Regra 80/20 mais fraca — precisa de 30 SKUs (de 71) para 80%
>
> #Python #Pandas #DataAnalysis #EDA #Portfolio #EngenhariaDeSistemas

Anexe 2-3 dos gráficos gerados (recomendo: `01_faturamento_mensal.png`, `06_heatmap_correlacao.png`, `10_pareto_produtos.png`).

---

## Próximo módulo

**Módulo 04 — ETL (Extract, Transform, Load):** automatização do pipeline que leva os dados da fonte ao dashboard. Usaremos Python + agendamento + tratamento de erros.

---

## Créditos

- **Autor:** Lucas Veríssimo (UNIMONTES — Engenharia de Sistemas)
- **Dataset:** PharmaSystem (Módulo 01), gerado sinteticamente com seed=42
- **Assistência técnica:** Claude (Anthropic)
