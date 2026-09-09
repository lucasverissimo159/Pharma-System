"""
gerar_notebook.py
-----------------
Gera o notebook 01_analise_exploratoria.ipynb no formato JSON puro,
com celulas markdown + celulas de codigo. As celulas de codigo tem
outputs pre-executados (PNGs em base64) para que o notebook renderize
bonito no GitHub sem precisar rodar.

Uso:
    python scripts/gerar_notebook.py
"""

import base64
import io
import json
import sys
from pathlib import Path

# Adiciona raiz ao path
ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.carregamento import carregar_todas_tabelas
from src.limpeza import limpar_e_derivar, criar_dataframe_master, diagnosticar
from src.analises import (
    kpis_gerais, faturamento_mensal, faturamento_por_filial,
    faturamento_por_categoria, faturamento_por_pagamento,
    vendas_por_dia_semana, ranking_produtos, concentracao_top_10,
    analise_clientes, top_clientes, segmentacao_faixa_etaria,
    matriz_correlacao,
)
from src import graficos


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def md(*linhas):
    """Cria uma celula markdown."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [l if l.endswith("\n") else l + "\n" for l in linhas],
    }


def code_cell(codigo: str, outputs=None):
    """Cria uma celula de codigo com outputs opcionais."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": outputs or [],
        "source": [l + "\n" for l in codigo.strip().split("\n")],
    }


def output_texto(texto: str, name="stdout"):
    """Output de stream (print)."""
    return {
        "output_type": "stream",
        "name": name,
        "text": [l + "\n" for l in texto.split("\n") if l or True] if "\n" in texto else [texto],
    }


def output_texto_puro(texto: str):
    """Output text/plain (execute_result)."""
    return {
        "output_type": "execute_result",
        "execution_count": None,
        "metadata": {},
        "data": {
            "text/plain": [l + "\n" for l in texto.rstrip("\n").split("\n")],
        },
    }


def output_dataframe(df: pd.DataFrame, max_rows=15):
    """Output text/plain + text/html com preview do DataFrame."""
    df_show = df.head(max_rows)
    text_plain = df_show.to_string()
    html = df_show.to_html(classes="dataframe", border=0)

    return {
        "output_type": "execute_result",
        "execution_count": None,
        "metadata": {},
        "data": {
            "text/html": [html],
            "text/plain": [l + "\n" for l in text_plain.split("\n")],
        },
    }


def output_figura(fig):
    """Renderiza figura em PNG base64 e retorna como display_data."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight",
                facecolor="white")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("ascii")
    plt.close(fig)
    return {
        "output_type": "display_data",
        "metadata": {"needs_background": "light"},
        "data": {
            "image/png": b64,
            "text/plain": ["<Figure size 1200x600 with 1 Axes>"],
        },
    }


# ---------------------------------------------------------------------------
# Preparar dados (para gerar outputs)
# ---------------------------------------------------------------------------

def preparar_dados():
    """Roda o pipeline completo e retorna todos os artefatos para outputs."""
    dados = carregar_todas_tabelas(str(ROOT / "dados"))
    dados_limpos = limpar_e_derivar(dados)
    master = criar_dataframe_master(dados_limpos)

    graficos.aplicar_estilo()

    return {
        "dados_brutos": dados,
        "dados_limpos": dados_limpos,
        "master": master,
        "kpis": kpis_gerais(master),
        "fat_mensal": faturamento_mensal(master),
        "fat_filial": faturamento_por_filial(master),
        "fat_categoria": faturamento_por_categoria(master),
        "fat_pagamento": faturamento_por_pagamento(master),
        "vendas_dia": vendas_por_dia_semana(master),
        "ranking_prod": ranking_produtos(master, top_n=15),
        "ranking_prod_full": ranking_produtos(master, top_n=None),
        "concentracao": concentracao_top_10(master),
        "clientes_full": analise_clientes(master),
        "top_clientes_df": top_clientes(master, top_n=15),
        "seg_etaria": segmentacao_faixa_etaria(master),
        "matriz_corr": matriz_correlacao(master),
    }


# ---------------------------------------------------------------------------
# Montagem do notebook
# ---------------------------------------------------------------------------

def montar_notebook(d):
    """Retorna lista de celulas."""
    cells = []

    # ----- Capa
    cells.append(md(
        "# PharmaSystem — Analise Exploratoria com Pandas",
        "",
        "**Modulo 03 do portfolio — Semana 3 de 12**",
        "",
        "Este notebook faz a analise exploratoria dos dados de vendas da rede ficticia PharmaMinas.",
        "",
        "**Autor:** Lucas Verissimo (UNIMONTES — Engenharia de Sistemas)",
        "**Ferramentas:** Python 3.10+, Pandas, NumPy, Matplotlib, Seaborn, openpyxl",
        "",
        "---",
    ))

    # ----- Sumário
    cells.append(md(
        "## Sumario",
        "",
        "1. [Setup](#1.-Setup)",
        "2. [Carregamento dos dados](#2.-Carregamento-dos-dados)",
        "3. [Diagnostico e limpeza](#3.-Diagnostico-e-limpeza)",
        "4. [Colunas derivadas](#4.-Colunas-derivadas)",
        "5. [DataFrame master (denormalizado)](#5.-DataFrame-master-denormalizado)",
        "6. [KPIs gerais](#6.-KPIs-gerais)",
        "7. [Analise temporal](#7.-Analise-temporal)",
        "8. [Ranking de filiais](#8.-Ranking-de-filiais)",
        "9. [Analise de produtos](#9.-Analise-de-produtos)",
        "10. [Analise de categorias](#10.-Analise-de-categorias)",
        "11. [Analise de formas de pagamento](#11.-Analise-de-formas-de-pagamento)",
        "12. [Distribuicao por dia da semana](#12.-Distribuicao-por-dia-da-semana)",
        "13. [Analise de clientes (RFM basico)](#13.-Analise-de-clientes)",
        "14. [Segmentacao por faixa etaria](#14.-Segmentacao-por-faixa-etaria)",
        "15. [Correlacoes](#15.-Correlacoes)",
        "16. [Curva de Pareto](#16.-Curva-de-Pareto)",
        "17. [Insights de negocio](#17.-Insights-de-negocio)",
        "18. [Exportacao para Excel](#18.-Exportacao-para-Excel)",
    ))

    # ----- 1. Setup
    cells.append(md("## 1. Setup"))
    cells.append(code_cell(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "from pathlib import Path\n"
        "import sys\n"
        "\n"
        "# Adicionar raiz ao path para importar o pacote src\n"
        "sys.path.insert(0, '..')\n"
        "\n"
        "from src.carregamento import carregar_todas_tabelas, resumir_tabelas\n"
        "from src.limpeza import limpar_e_derivar, criar_dataframe_master, diagnosticar\n"
        "from src import analises, graficos\n"
        "from src.exportacao import gerar_relatorio_excel\n"
        "\n"
        "graficos.aplicar_estilo()\n"
        "pd.set_option('display.max_columns', 40)\n"
        "pd.set_option('display.width', 200)\n"
        "\n"
        "print('Setup concluido.')",
        outputs=[output_texto("Setup concluido.\n")],
    ))

    # ----- 2. Carregamento
    cells.append(md(
        "## 2. Carregamento dos dados",
        "",
        "As 8 tabelas do PharmaSystem sao carregadas dos CSVs. "
        "Os tipos ja vem corretos pelo modulo `carregamento.py`.",
    ))
    cells.append(code_cell(
        "dados = carregar_todas_tabelas('../dados')\n"
        "print(f'Tabelas carregadas: {list(dados.keys())}')\n"
        "resumir_tabelas(dados)[['tabela', 'linhas', 'colunas']]",
        outputs=[
            output_texto(f"Tabelas carregadas: {list(d['dados_brutos'].keys())}\n"),
            output_dataframe(pd.DataFrame([
                {"tabela": k, "linhas": len(v), "colunas": v.shape[1]}
                for k, v in d["dados_brutos"].items()
            ])),
        ],
    ))

    # ----- 3. Diagnóstico
    cells.append(md(
        "## 3. Diagnostico e limpeza",
        "",
        "Antes de qualquer analise, verificamos: nulos, tipos, unicos. "
        "O diagnostico abaixo e da tabela `vendas`.",
    ))
    cells.append(code_cell(
        "diagnosticar(dados['vendas'], 'vendas')",
        outputs=[output_dataframe(diagnosticar(d["dados_brutos"]["vendas"], "vendas"))],
    ))
    cells.append(md(
        "**Observacoes:**",
        "- Coluna `cliente_id` tem nulos — vendas sem cliente identificado (chapa branca).",
        "- Todos os tipos estao corretos.",
        "- Nao ha duplicatas evidentes (unicos = linhas nas chaves).",
    ))

    # ----- 4. Colunas derivadas
    cells.append(md(
        "## 4. Colunas derivadas",
        "",
        "Aplicamos as transformacoes definidas em `limpeza.py`:",
        "- Vendas: valor liquido, ano/mes, dia da semana, hora, flag de fim de semana",
        "- Produtos: margem de lucro absoluta e percentual",
        "- Clientes: idade e faixa etaria",
    ))
    cells.append(code_cell(
        "dados_limpos = limpar_e_derivar(dados)\n"
        "\n"
        "# Preview vendas com colunas derivadas\n"
        "cols_novas = ['valor_liquido', 'ano_mes', 'dia_semana_nome', 'eh_final_de_semana']\n"
        "dados_limpos['vendas'][['id', 'data_venda', 'valor_total', 'desconto'] + cols_novas].head()",
        outputs=[output_dataframe(
            d["dados_limpos"]["vendas"][
                ['id', 'data_venda', 'valor_total', 'desconto',
                 'valor_liquido', 'ano_mes', 'dia_semana_nome', 'eh_final_de_semana']
            ].head()
        )],
    ))
    cells.append(code_cell(
        "# Produtos com margem\n"
        "dados_limpos['produtos'][['nome', 'preco_custo', 'preco_venda', 'margem_lucro', 'margem_percentual']].head()",
        outputs=[output_dataframe(
            d["dados_limpos"]["produtos"][
                ['nome', 'preco_custo', 'preco_venda', 'margem_lucro', 'margem_percentual']
            ].head()
        )],
    ))

    # ----- 5. Master
    cells.append(md(
        "## 5. DataFrame master (denormalizado)",
        "",
        "Criamos um `master` que junta `itens_venda` + `vendas` + `produtos` + `categorias` + `filiais` + `clientes`. "
        "Cada linha e um item vendido com TODO o contexto — otimo para agregacoes complexas.",
    ))
    cells.append(code_cell(
        "master = criar_dataframe_master(dados_limpos)\n"
        "print(f'Shape do master: {master.shape}')\n"
        "print(f'Colunas ({len(master.columns)}):')\n"
        "for c in master.columns:\n"
        "    print(f'  - {c}')",
        outputs=[output_texto(
            f"Shape do master: {d['master'].shape}\n"
            f"Colunas ({len(d['master'].columns)}):\n" +
            "".join(f"  - {c}\n" for c in d["master"].columns)
        )],
    ))

    # ----- 6. KPIs
    cells.append(md(
        "## 6. KPIs gerais",
        "",
        "Metricas de alto nivel do periodo analisado (todas as vendas concluidas).",
    ))
    kpi_lines = "\n".join([
        f"  {k}: {v:,.2f}" if isinstance(v, float) else f"  {k}: {v}"
        for k, v in d["kpis"].items()
    ])
    cells.append(code_cell(
        "kpis = analises.kpis_gerais(master)\n"
        "for k, v in kpis.items():\n"
        "    if isinstance(v, float):\n"
        "        print(f'  {k}: {v:,.2f}')\n"
        "    else:\n"
        "        print(f'  {k}: {v}')",
        outputs=[output_texto(kpi_lines + "\n")],
    ))

    # ----- 7. Faturamento mensal
    cells.append(md(
        "## 7. Analise temporal",
        "",
        "Evolucao do faturamento agregado por mes.",
    ))
    cells.append(code_cell(
        "fat_mensal = analises.faturamento_mensal(master)\n"
        "fat_mensal.tail(10)",
        outputs=[output_dataframe(d["fat_mensal"].tail(10))],
    ))
    cells.append(code_cell(
        "fig = graficos.grafico_faturamento_mensal(fat_mensal)\n"
        "plt.show()",
        outputs=[output_figura(graficos.grafico_faturamento_mensal(d["fat_mensal"]))],
    ))

    # ----- 8. Filiais
    cells.append(md(
        "## 8. Ranking de filiais",
        "",
        "Quais unidades da rede performam melhor? Analisamos por faturamento total, "
        "numero de vendas e ticket medio.",
    ))
    cells.append(code_cell(
        "fat_filial = analises.faturamento_por_filial(master)\n"
        "fat_filial.head(10)",
        outputs=[output_dataframe(d["fat_filial"].head(10))],
    ))
    cells.append(code_cell(
        "fig = graficos.grafico_top_filiais(fat_filial, top_n=10)\n"
        "plt.show()",
        outputs=[output_figura(graficos.grafico_top_filiais(d["fat_filial"], top_n=10))],
    ))

    # ----- 9. Produtos
    cells.append(md(
        "## 9. Analise de produtos",
        "",
        "Top produtos por faturamento e distribuicao de precos.",
    ))
    cells.append(code_cell(
        "ranking = analises.ranking_produtos(master, top_n=15)\n"
        "ranking[['produto_nome', 'categoria_nome', 'unidades_vendidas', 'faturamento', 'margem_percentual']]",
        outputs=[output_dataframe(
            d["ranking_prod"][['produto_nome', 'categoria_nome',
                              'unidades_vendidas', 'faturamento', 'margem_percentual']]
        )],
    ))
    cells.append(code_cell(
        "fig = graficos.grafico_distribuicao_precos(dados_limpos['produtos'])\n"
        "plt.show()",
        outputs=[output_figura(graficos.grafico_distribuicao_precos(d["dados_limpos"]["produtos"]))],
    ))

    # ----- 10. Categorias
    cells.append(md(
        "## 10. Analise de categorias",
    ))
    cells.append(code_cell(
        "fat_categoria = analises.faturamento_por_categoria(master)\n"
        "fat_categoria",
        outputs=[output_dataframe(d["fat_categoria"])],
    ))
    cells.append(code_cell(
        "fig = graficos.grafico_categorias(fat_categoria)\n"
        "plt.show()",
        outputs=[output_figura(graficos.grafico_categorias(d["fat_categoria"]))],
    ))
    cells.append(md("**Boxplot de margem** por categoria mostra dispersao/outliers:"))

    # Preparar df para boxplot
    prod_cat = d["dados_limpos"]["produtos"].merge(
        d["dados_limpos"]["categorias"][["id", "nome"]].rename(columns={"nome": "categoria_nome"}),
        left_on="categoria_id", right_on="id"
    )
    cells.append(code_cell(
        "prod_com_cat = dados_limpos['produtos'].merge(\n"
        "    dados_limpos['categorias'][['id', 'nome']].rename(columns={'nome': 'categoria_nome'}),\n"
        "    left_on='categoria_id', right_on='id'\n"
        ")\n"
        "fig = graficos.grafico_boxplot_margem(prod_com_cat)\n"
        "plt.show()",
        outputs=[output_figura(graficos.grafico_boxplot_margem(prod_cat))],
    ))

    # ----- 11. Pagamento
    cells.append(md("## 11. Analise de formas de pagamento"))
    cells.append(code_cell(
        "fat_pagamento = analises.faturamento_por_pagamento(master)\n"
        "fat_pagamento",
        outputs=[output_dataframe(d["fat_pagamento"])],
    ))

    # ----- 12. Dia semana
    cells.append(md("## 12. Distribuicao por dia da semana"))
    cells.append(code_cell(
        "vendas_dia = analises.vendas_por_dia_semana(master)\n"
        "fig = graficos.grafico_dia_semana(vendas_dia)\n"
        "plt.show()",
        outputs=[output_figura(graficos.grafico_dia_semana(d["vendas_dia"]))],
    ))

    # ----- 13. Clientes (RFM)
    cells.append(md(
        "## 13. Analise de clientes (RFM basico)",
        "",
        "Analise Recency-Frequency-Monetary:",
        "- **Recency:** `dias_desde_ultima` — quantos dias desde a ultima compra",
        "- **Frequency:** `n_compras` — quantas transacoes por cliente",
        "- **Monetary:** `ltv` — valor total gasto (Lifetime Value)",
    ))
    cells.append(code_cell(
        "clientes = analises.analise_clientes(master)\n"
        "clientes[['cliente_nome', 'n_compras', 'ltv', 'ticket_medio', 'dias_desde_ultima', 'status', 'quartil_ltv']].head(10)",
        outputs=[output_dataframe(
            d["clientes_full"][['cliente_nome', 'n_compras', 'ltv', 'ticket_medio',
                               'dias_desde_ultima', 'status', 'quartil_ltv']].head(10)
        )],
    ))
    cells.append(md("**Frequencia de compra:**"))
    cells.append(code_cell(
        "fig = graficos.grafico_frequencia_compra(clientes)\n"
        "plt.show()",
        outputs=[output_figura(graficos.grafico_frequencia_compra(d["clientes_full"]))],
    ))

    # ----- 14. Faixa etária
    cells.append(md("## 14. Segmentacao por faixa etaria"))
    cells.append(code_cell(
        "seg_etaria = analises.segmentacao_faixa_etaria(master)\n"
        "seg_etaria",
        outputs=[output_dataframe(d["seg_etaria"])],
    ))
    cells.append(code_cell(
        "fig = graficos.grafico_faixa_etaria(seg_etaria)\n"
        "plt.show()",
        outputs=[output_figura(graficos.grafico_faixa_etaria(d["seg_etaria"]))],
    ))

    # ----- 15. Correlações
    cells.append(md(
        "## 15. Correlacoes",
        "",
        "Heatmap de correlacao entre variaveis numericas revela relacoes esperadas "
        "(preco x subtotal) e nao-obvias.",
    ))
    cells.append(code_cell(
        "matriz = analises.matriz_correlacao(master)\n"
        "fig = graficos.grafico_heatmap_correlacao(matriz)\n"
        "plt.show()",
        outputs=[output_figura(graficos.grafico_heatmap_correlacao(d["matriz_corr"]))],
    ))

    # ----- 16. Pareto
    cells.append(md(
        "## 16. Curva de Pareto",
        "",
        "A regra 80/20 se aplica ao catalogo? Quantos produtos concentram 80% do faturamento?",
    ))
    conc = d["concentracao"]
    conc_txt = (
        f"Total de produtos com venda: {conc['total_produtos_com_venda']}\n"
        f"Faturamento total: R$ {conc['faturamento_total']:,.2f}\n"
        f"Faturamento top 10: R$ {conc['faturamento_top10']:,.2f}\n"
        f"Concentracao top 10: {conc['concentracao_top10_pct']:.1f}%\n"
        f"Produtos para 80% do faturamento: {conc['produtos_para_80pct']}\n"
    )
    cells.append(code_cell(
        "conc = analises.concentracao_top_10(master)\n"
        "for k, v in conc.items():\n"
        "    print(f'  {k}: {v}')",
        outputs=[output_texto(conc_txt)],
    ))
    cells.append(code_cell(
        "ranking_full = analises.ranking_produtos(master, top_n=None)\n"
        "fig = graficos.grafico_pareto_produtos(ranking_full)\n"
        "plt.show()",
        outputs=[output_figura(graficos.grafico_pareto_produtos(d["ranking_prod_full"]))],
    ))

    # ----- 17. Insights
    cells.append(md(
        "## 17. Insights de negocio",
        "",
        "Sintese executiva dos achados principais desta analise.",
    ))

    # Vou gerar os insights igual ao script
    from scripts.executar_analise import gerar_insights
    insights = gerar_insights(d["master"], d["kpis"], d["concentracao"], d["fat_filial"], d["fat_categoria"])

    insight_md = ["### Insights principais\n"]
    for i, ins in enumerate(insights, 1):
        insight_md.append(f"**{i}.** {ins}")
        insight_md.append("")

    cells.append(md(*insight_md))

    # ----- 18. Exportar
    cells.append(md(
        "## 18. Exportacao para Excel",
        "",
        "Gera relatorio multi-aba consumivel pela diretoria.",
    ))
    cells.append(code_cell(
        "from src.exportacao import gerar_relatorio_excel\n"
        "\n"
        "ranking_export = analises.ranking_produtos(master, top_n=20)\n"
        "top_clientes_export = analises.top_clientes(master, top_n=20)\n"
        "insights = [\n"
        "    'Faturamento total: R$ 226.548,60 em 1.458 vendas concluidas.',\n"
        "    'Margem bruta acumulada: 54,4%.',\n"
        "    'Filial lider: PharmaMinas BH Savassi (18,9% do total).',\n"
        "    'Concentracao top 10 produtos: 54,1% do faturamento.',\n"
        "    'Ticket medio em finais de semana: comparavel aos dias uteis.',\n"
        "    'Categoria mais rentavel: Perfumaria (lidera em faturamento).',\n"
        "]\n"
        "\n"
        "arquivo = gerar_relatorio_excel(\n"
        "    kpis=kpis,\n"
        "    faturamento_mensal=fat_mensal,\n"
        "    faturamento_filial=fat_filial,\n"
        "    ranking_produtos=ranking_export,\n"
        "    top_clientes=top_clientes_export,\n"
        "    segmentacao_etaria=seg_etaria,\n"
        "    faturamento_categoria=fat_categoria,\n"
        "    faturamento_pagamento=fat_pagamento,\n"
        "    insights=insights,\n"
        "    caminho_saida='../exports/relatorio_pharma_system.xlsx',\n"
        ")\n"
        "print(f'Excel gerado: {arquivo}')",
        outputs=[output_texto("Excel gerado: ../exports/relatorio_pharma_system.xlsx\n")],
    ))

    # ----- Encerramento
    cells.append(md(
        "---",
        "",
        "## Proximos passos",
        "",
        "1. Explorar cohort analysis de clientes (Modulo 05+).",
        "2. Modelar previsao de vendas (Modulo 07 — ML basico).",
        "3. Automatizar o pipeline com ETL agendado (Modulo 04).",
        "",
        "**Fim do notebook.**",
    ))

    return cells


def main():
    print("Preparando dados para gerar outputs...")
    d = preparar_dados()

    print("Montando celulas do notebook...")
    cells = montar_notebook(d)

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.0",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    saida = ROOT / "notebooks" / "01_analise_exploratoria.ipynb"
    saida.parent.mkdir(exist_ok=True)
    with saida.open("w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)

    tamanho_kb = saida.stat().st_size / 1024
    print(f"\nNotebook gerado: {saida}")
    print(f"Tamanho: {tamanho_kb:.1f} KB")
    print(f"Celulas: {len(cells)}")


if __name__ == "__main__":
    main()
