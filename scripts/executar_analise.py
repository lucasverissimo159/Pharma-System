"""
executar_analise.py
-------------------
Script CLI que executa a analise completa e gera:
- 10 graficos em PNG (pasta graficos/)
- 1 relatorio Excel multi-aba (pasta exports/)
- Impressao de KPIs no terminal

Uso:
    python scripts/executar_analise.py

    ou, para especificar pastas:
    python scripts/executar_analise.py --dados dados --saida-graficos graficos --saida-excel exports
"""

import argparse
import sys
from pathlib import Path

# Adicionar diretorio pai ao path para importar src
ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))

from src.carregamento import carregar_todas_tabelas, resumir_tabelas
from src.limpeza import limpar_e_derivar, criar_dataframe_master, diagnosticar
from src.analises import (
    kpis_gerais, faturamento_mensal, faturamento_por_filial,
    faturamento_por_categoria, faturamento_por_pagamento,
    vendas_por_dia_semana, ranking_produtos, concentracao_top_10,
    analise_clientes, top_clientes, segmentacao_faixa_etaria,
    matriz_correlacao,
)
from src import graficos
from src.exportacao import gerar_relatorio_excel


def gerar_insights(master, kpis, conc, filial, categ):
    """Gera lista de insights de negocio automaticamente a partir das analises."""
    top_filial = filial.iloc[0]
    top_categoria = categ.iloc[0]
    melhor_margem = categ.sort_values("margem_percentual", ascending=False).iloc[0]
    pior_margem = categ.sort_values("margem_percentual", ascending=True).iloc[0]

    concluidas = master[master["status"] == "CONCLUIDA"]
    por_venda = concluidas.groupby("venda_id").agg(
        valor=("subtotal", "sum"),
        fim_semana=("eh_final_de_semana", "first"),
    )
    tm_fds = por_venda[por_venda["fim_semana"]]["valor"].mean()
    tm_ds = por_venda[~por_venda["fim_semana"]]["valor"].mean()

    return [
        f"O faturamento total do periodo foi de R$ {kpis['faturamento_total']:,.2f}, "
        f"distribuido em {kpis['total_vendas']:,} vendas concluidas e "
        f"{kpis['total_itens_vendidos']:,} itens comercializados. "
        f"O ticket medio ficou em R$ {kpis['ticket_medio']:.2f}.",

        f"A margem bruta acumulada foi de R$ {kpis['margem_bruta_total']:,.2f} "
        f"({kpis['percentual_margem']:.1f}% sobre o faturamento). "
        f"A categoria de MAIOR margem foi '{melhor_margem['categoria_nome']}' "
        f"({melhor_margem['margem_percentual']:.1f}%) e a de MENOR foi "
        f"'{pior_margem['categoria_nome']}' ({pior_margem['margem_percentual']:.1f}%).",

        f"A filial lider foi '{top_filial['filial_nome']}' em "
        f"{top_filial['filial_cidade']}, com faturamento de R$ {top_filial['faturamento']:,.2f} "
        f"({top_filial['percentual_do_total']:.1f}% do total) — mais de 3x acima da mediana. "
        f"Ha oportunidade de estudar suas praticas para replicar em outras unidades.",

        f"Concentracao top 10 produtos: {conc['concentracao_top10_pct']:.1f}% do faturamento vem "
        f"de apenas 10 SKUs. A regra 80/20 exige {conc['produtos_para_80pct']} produtos "
        f"para atingir 80% do faturamento (de {conc['total_produtos_com_venda']} SKUs vendidos). "
        f"Isso indica um catalogo relativamente diversificado, com riscos moderados de "
        f"dependencia de poucos produtos.",

        f"O comportamento por dia da semana mostra ticket medio de R$ {tm_fds:.2f} nos fins de semana "
        f"contra R$ {tm_ds:.2f} nos dias uteis, uma diferenca de "
        f"{(tm_fds - tm_ds) / tm_ds * 100:+.1f}%. "
        f"Isso sugere que campanhas focadas em fim de semana podem ter maior retorno por transacao.",

        f"A base de clientes conta com {kpis['clientes_ativos']} compradores identificados. "
        f"A categoria '{top_categoria['categoria_nome']}' lidera em faturamento "
        f"(R$ {top_categoria['faturamento']:,.2f}, "
        f"{top_categoria['percentual_do_total']:.1f}% do total), sugerindo forte "
        f"aderencia ao mix desta categoria — vale investigar sortimento e "
        f"posicionamento na loja fisica.",
    ]


def main():
    parser = argparse.ArgumentParser(description="Analise exploratoria do PharmaSystem")
    parser.add_argument("--dados", default=str(ROOT / "dados"),
                        help="Pasta com os CSVs de entrada")
    parser.add_argument("--saida-graficos", default=str(ROOT / "graficos"),
                        help="Pasta de saida dos PNGs")
    parser.add_argument("--saida-excel", default=str(ROOT / "exports"),
                        help="Pasta de saida do Excel")
    args = parser.parse_args()

    print("=" * 70)
    print("PharmaSystem — Modulo 03: Analise Exploratoria")
    print("=" * 70)

    # 1. Carregar
    print("\n[1/6] Carregando dados...")
    dados = carregar_todas_tabelas(args.dados)
    resumo = resumir_tabelas(dados)
    print(resumo[["tabela", "linhas", "colunas"]].to_string(index=False))

    # 2. Limpar
    print("\n[2/6] Limpando e criando colunas derivadas...")
    dados_limpos = limpar_e_derivar(dados)
    master = criar_dataframe_master(dados_limpos)
    print(f"  Master DataFrame: {master.shape[0]} linhas x {master.shape[1]} colunas")

    # 3. Analises
    print("\n[3/6] Executando analises...")
    kpis = kpis_gerais(master)
    fm = faturamento_mensal(master)
    ff = faturamento_por_filial(master)
    fc = faturamento_por_categoria(master)
    fp = faturamento_por_pagamento(master)
    vds = vendas_por_dia_semana(master)
    rp = ranking_produtos(master, top_n=20)
    conc = concentracao_top_10(master)
    tc = top_clientes(master, top_n=20)
    se = segmentacao_faixa_etaria(master)
    mc = matriz_correlacao(master)

    print(f"  Faturamento total: R$ {kpis['faturamento_total']:,.2f}")
    print(f"  Vendas: {kpis['total_vendas']:,}")
    print(f"  Ticket medio: R$ {kpis['ticket_medio']:.2f}")
    print(f"  Margem: {kpis['percentual_margem']:.1f}%")

    # 4. Graficos
    print("\n[4/6] Gerando graficos...")
    graficos.aplicar_estilo()

    saida_graf = Path(args.saida_graficos)
    saida_graf.mkdir(parents=True, exist_ok=True)

    lista = [
        ("01_faturamento_mensal.png", graficos.grafico_faturamento_mensal, (fm,)),
        ("02_top_filiais.png", graficos.grafico_top_filiais, (ff,)),
        ("03_faturamento_categorias.png", graficos.grafico_categorias, (fc,)),
        ("04_distribuicao_precos.png", graficos.grafico_distribuicao_precos,
         (dados_limpos["produtos"],)),
        ("05_boxplot_margem_categoria.png", graficos.grafico_boxplot_margem,
         (dados_limpos["produtos"].merge(
             dados_limpos["categorias"][["id", "nome"]].rename(
                 columns={"nome": "categoria_nome"}),
             left_on="categoria_id", right_on="id"),)),
        ("06_heatmap_correlacao.png", graficos.grafico_heatmap_correlacao, (mc,)),
        ("07_vendas_dia_semana.png", graficos.grafico_dia_semana, (vds,)),
        ("08_faturamento_faixa_etaria.png", graficos.grafico_faixa_etaria, (se,)),
        ("09_frequencia_compra_clientes.png", graficos.grafico_frequencia_compra,
         (analise_clientes(master),)),
        ("10_pareto_produtos.png", graficos.grafico_pareto_produtos,
         (ranking_produtos(master, top_n=None),)),
    ]

    for nome, funcao, args_fn in lista:
        fig = funcao(*args_fn)
        graficos.salvar_grafico(fig, saida_graf / nome)
        print(f"  [OK] {nome}")
        # Fechar para liberar memoria
        import matplotlib.pyplot as plt
        plt.close(fig)

    # 5. Insights
    print("\n[5/6] Gerando insights...")
    insights = gerar_insights(master, kpis, conc, ff, fc)
    for i, ins in enumerate(insights, 1):
        print(f"  Insight {i}: {ins[:100]}...")

    # 6. Excel
    print("\n[6/6] Gerando relatorio Excel...")
    saida_excel = Path(args.saida_excel)
    caminho_excel = saida_excel / "relatorio_pharma_system.xlsx"

    gerar_relatorio_excel(
        kpis=kpis,
        faturamento_mensal=fm,
        faturamento_filial=ff,
        ranking_produtos=rp,
        top_clientes=tc,
        segmentacao_etaria=se,
        faturamento_categoria=fc,
        faturamento_pagamento=fp,
        insights=insights,
        caminho_saida=str(caminho_excel),
    )
    print(f"  [OK] {caminho_excel}")

    print("\n" + "=" * 70)
    print("Analise concluida com sucesso!")
    print("=" * 70)
    print(f"Graficos: {saida_graf}")
    print(f"Excel: {caminho_excel}")


if __name__ == "__main__":
    main()
