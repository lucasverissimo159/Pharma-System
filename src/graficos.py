"""
graficos.py
-----------
Funcoes para gerar cada grafico do relatorio.

Cada funcao gera um `Figure` matplotlib e retorna. Use `salvar_grafico(fig, "path")`
para persistir em PNG.

Estilo:
    - Paleta PharmaSystem (verde-farmacia + acentos)
    - Fonte sans-serif
    - Tamanho consistente (12x6 padrao, 10x6 para donuts)
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Estilo global
# ---------------------------------------------------------------------------

CORES = {
    "primaria": "#00695C",
    "secundaria": "#26A69A",
    "azul": "#1976D2",
    "ambar": "#FFA000",
    "roxo": "#7B1FA2",
    "verde_ok": "#4CAF50",
    "vermelho": "#EF5350",
    "cinza_claro": "#F5F5F5",
    "cinza_texto": "#424242",
    "cinza_grid": "#F0F0F0",
}

PALETA_SEQUENCIAL = [
    "#00695C", "#00796B", "#00897B", "#009688",
    "#26A69A", "#4DB6AC", "#80CBC4", "#B2DFDB",
]


def aplicar_estilo():
    """Configura estilo global padrao dos graficos."""
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#BDBDBD",
        "axes.labelcolor": CORES["cinza_texto"],
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlecolor": CORES["cinza_texto"],
        "axes.labelsize": 11,
        "xtick.color": CORES["cinza_texto"],
        "ytick.color": CORES["cinza_texto"],
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "grid.color": CORES["cinza_grid"],
        "grid.linestyle": "--",
        "grid.linewidth": 0.6,
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "legend.frameon": False,
    })


def salvar_grafico(fig, caminho: str):
    """Salva figura em PNG com fundo branco e boa resolucao."""
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho, dpi=120, bbox_inches="tight", facecolor="white")


def _fmt_brl(valor, _=None):
    """Formata numero como R$ para uso em ticks."""
    if abs(valor) >= 1_000_000:
        return f"R$ {valor/1_000_000:.1f}M"
    if abs(valor) >= 1_000:
        return f"R$ {valor/1_000:.0f}k"
    return f"R$ {valor:.0f}"


# ---------------------------------------------------------------------------
# Grafico 1: Faturamento mensal (linha)
# ---------------------------------------------------------------------------

def grafico_faturamento_mensal(faturamento_mensal_df: pd.DataFrame):
    """Linha do faturamento mensal + tendencia."""
    fig, ax = plt.subplots(figsize=(12, 5.5))

    x = faturamento_mensal_df["ano_mes"]
    y = faturamento_mensal_df["faturamento"]

    ax.plot(x, y, color=CORES["primaria"], linewidth=2.5, marker="o",
            markersize=6, label="Faturamento mensal")

    # Media movel de 3 meses (se houver dados suficientes)
    if len(y) >= 3:
        mm = y.rolling(window=3, min_periods=1).mean()
        ax.plot(x, mm, color=CORES["secundaria"], linewidth=1.8,
                linestyle="--", label="Media movel 3M")

    ax.set_title("Evolucao do Faturamento Mensal — PharmaMinas")
    ax.set_xlabel("")
    ax.set_ylabel("Faturamento")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(_fmt_brl))
    ax.tick_params(axis="x", rotation=45)
    ax.legend(loc="upper left")
    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.grid(False, axis="x")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Grafico 2: Top filiais (barras horizontais)
# ---------------------------------------------------------------------------

def grafico_top_filiais(fat_filial_df: pd.DataFrame, top_n: int = 10):
    """Barras horizontais das top N filiais."""
    df = fat_filial_df.head(top_n).sort_values("faturamento")

    fig, ax = plt.subplots(figsize=(11, 6))

    cores = [PALETA_SEQUENCIAL[i % len(PALETA_SEQUENCIAL)]
             for i in range(len(df) - 1, -1, -1)]

    bars = ax.barh(df["filial_nome"], df["faturamento"], color=cores, edgecolor="none")

    for bar, valor in zip(bars, df["faturamento"]):
        ax.text(bar.get_width() + df["faturamento"].max() * 0.01,
                bar.get_y() + bar.get_height() / 2,
                _fmt_brl(valor), va="center", fontsize=9,
                color=CORES["cinza_texto"])

    ax.set_title(f"Top {top_n} Filiais por Faturamento")
    ax.set_xlabel("Faturamento")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(_fmt_brl))
    ax.grid(True, axis="x", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.grid(False, axis="y")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Grafico 3: Faturamento por categoria (barras verticais)
# ---------------------------------------------------------------------------

def grafico_categorias(fat_categoria_df: pd.DataFrame):
    """Barras verticais de categorias com margem % em label."""
    df = fat_categoria_df.copy()

    fig, ax = plt.subplots(figsize=(12, 6))

    bars = ax.bar(df["categoria_nome"], df["faturamento"],
                  color=CORES["primaria"], edgecolor="none")

    for bar, fat, marg in zip(bars, df["faturamento"], df["margem_percentual"]):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + df["faturamento"].max() * 0.01,
                f"{_fmt_brl(fat)}\n(margem {marg:.0f}%)",
                ha="center", va="bottom", fontsize=9,
                color=CORES["cinza_texto"])

    ax.set_title("Faturamento por Categoria de Produto")
    ax.set_xlabel("")
    ax.set_ylabel("Faturamento")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(_fmt_brl))
    ax.tick_params(axis="x", rotation=30)

    for label in ax.get_xticklabels():
        label.set_ha("right")

    # Espaco superior para os labels
    ax.set_ylim(0, df["faturamento"].max() * 1.20)
    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.grid(False, axis="x")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Grafico 4: Distribuicao de precos (histograma)
# ---------------------------------------------------------------------------

def grafico_distribuicao_precos(df_produtos: pd.DataFrame):
    """Histograma de precos de venda."""
    fig, ax = plt.subplots(figsize=(11, 5.5))

    sns.histplot(data=df_produtos, x="preco_venda", bins=20,
                 color=CORES["primaria"], edgecolor="white", ax=ax)

    mediana = df_produtos["preco_venda"].median()
    media = df_produtos["preco_venda"].mean()

    ax.axvline(mediana, color=CORES["vermelho"], linestyle="--", linewidth=1.5,
               label=f"Mediana: R$ {mediana:.2f}")
    ax.axvline(media, color=CORES["ambar"], linestyle="--", linewidth=1.5,
               label=f"Media: R$ {media:.2f}")

    ax.set_title("Distribuicao dos Precos de Venda dos Produtos")
    ax.set_xlabel("Preco de venda (R$)")
    ax.set_ylabel("Numero de produtos")
    ax.legend(loc="upper right")
    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.grid(False, axis="x")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Grafico 5: Boxplot de margem por categoria
# ---------------------------------------------------------------------------

def grafico_boxplot_margem(df_produtos_com_categoria: pd.DataFrame):
    """Boxplot de margem_percentual por categoria."""
    fig, ax = plt.subplots(figsize=(12, 6))

    # Ordenar categorias pela mediana de margem
    ordem = (df_produtos_com_categoria.groupby("categoria_nome")["margem_percentual"]
             .median().sort_values(ascending=False).index.tolist())

    sns.boxplot(
        data=df_produtos_com_categoria,
        y="categoria_nome",
        x="margem_percentual",
        order=ordem,
        color=CORES["primaria"],
        ax=ax,
    )

    # Suavizar cor por transparencia dos patches
    for patch in ax.patches:
        r, g, b, _ = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0.6))
        patch.set_edgecolor(CORES["primaria"])

    ax.set_title("Distribuicao da Margem % por Categoria")
    ax.set_xlabel("Margem percentual (%)")
    ax.set_ylabel("")
    ax.grid(True, axis="x", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.grid(False, axis="y")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Grafico 6: Heatmap de correlacao
# ---------------------------------------------------------------------------

def grafico_heatmap_correlacao(matriz_corr: pd.DataFrame):
    """Heatmap de correlacao entre variaveis numericas."""
    fig, ax = plt.subplots(figsize=(10, 8))

    mask = np.triu(np.ones_like(matriz_corr, dtype=bool), k=1)

    sns.heatmap(
        matriz_corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.7},
        ax=ax,
    )

    ax.set_title("Correlacao entre Variaveis Numericas de Vendas")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Grafico 7: Vendas por dia da semana
# ---------------------------------------------------------------------------

def grafico_dia_semana(vendas_dia_df: pd.DataFrame):
    """Barras verticais de vendas por dia da semana."""
    fig, ax = plt.subplots(figsize=(11, 5.5))

    # Cores: destacar fim de semana
    cores_barra = [
        CORES["primaria"] if d not in ["Sabado", "Domingo"]
        else CORES["ambar"] if d == "Sabado"
        else CORES["cinza_claro"]
        for d in vendas_dia_df["dia_semana_nome"].astype(str)
    ]

    bars = ax.bar(vendas_dia_df["dia_semana_nome"].astype(str),
                  vendas_dia_df["n_vendas"],
                  color=cores_barra, edgecolor="none")

    for bar, valor in zip(bars, vendas_dia_df["n_vendas"]):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + vendas_dia_df["n_vendas"].max() * 0.02,
                f"{valor:,}", ha="center", va="bottom", fontsize=10,
                color=CORES["cinza_texto"], fontweight="bold")

    ax.set_title("Distribuicao de Vendas por Dia da Semana")
    ax.set_xlabel("")
    ax.set_ylabel("Numero de vendas")
    ax.set_ylim(0, vendas_dia_df["n_vendas"].max() * 1.15)
    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.grid(False, axis="x")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Grafico 8: Segmentacao por faixa etaria
# ---------------------------------------------------------------------------

def grafico_faixa_etaria(seg_etaria_df: pd.DataFrame):
    """Barras horizontais de faturamento por faixa etaria."""
    df = seg_etaria_df.sort_values("faixa_etaria")

    fig, ax = plt.subplots(figsize=(11, 5.5))

    bars = ax.barh(df["faixa_etaria"], df["faturamento"],
                   color=CORES["roxo"], edgecolor="none")

    for bar, fat, n in zip(bars, df["faturamento"], df["n_clientes"]):
        ax.text(bar.get_width() + df["faturamento"].max() * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{_fmt_brl(fat)}  ({n} clientes)",
                va="center", fontsize=10, color=CORES["cinza_texto"])

    ax.set_title("Faturamento por Faixa Etaria dos Clientes")
    ax.set_xlabel("Faturamento")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(_fmt_brl))
    ax.grid(True, axis="x", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.grid(False, axis="y")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Grafico 9: Distribuicao de frequencia de compra (histograma)
# ---------------------------------------------------------------------------

def grafico_frequencia_compra(clientes_df: pd.DataFrame):
    """Histograma da frequencia de compras dos clientes."""
    fig, ax = plt.subplots(figsize=(11, 5.5))

    sns.histplot(data=clientes_df, x="n_compras", bins=15,
                 color=CORES["azul"], edgecolor="white", ax=ax)

    mediana = clientes_df["n_compras"].median()
    ax.axvline(mediana, color=CORES["vermelho"], linestyle="--", linewidth=1.5,
               label=f"Mediana: {mediana:.0f} compras")

    ax.set_title("Distribuicao da Frequencia de Compras por Cliente")
    ax.set_xlabel("Numero de compras")
    ax.set_ylabel("Numero de clientes")
    ax.legend(loc="upper right")
    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.grid(False, axis="x")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Grafico 10: Curva de concentracao (Pareto)
# ---------------------------------------------------------------------------

def grafico_pareto_produtos(ranking_df: pd.DataFrame):
    """Curva de Pareto — % acumulada de faturamento por produto."""
    df = ranking_df.sort_values("faturamento", ascending=False).reset_index(drop=True)
    df["acumulado"] = df["faturamento"].cumsum()
    df["acumulado_pct"] = df["acumulado"] / df["faturamento"].sum() * 100
    df["posicao_pct"] = (df.index + 1) / len(df) * 100

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.fill_between(df["posicao_pct"], df["acumulado_pct"], 0,
                    color=CORES["primaria"], alpha=0.15)
    ax.plot(df["posicao_pct"], df["acumulado_pct"],
            color=CORES["primaria"], linewidth=2.5, label="Concentracao acumulada")

    # Linha 80/20
    ax.axhline(80, color=CORES["vermelho"], linestyle=":", linewidth=1)
    ax.axvline(20, color=CORES["vermelho"], linestyle=":", linewidth=1,
               label="Referencia 80/20")

    ax.set_title("Curva de Pareto — Concentracao do Faturamento por Produto")
    ax.set_xlabel("% de produtos (ordenados pelo maior faturamento)")
    ax.set_ylabel("% acumulada do faturamento")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 105)
    ax.legend(loc="lower right")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
    fig.tight_layout()
    return fig
