"""
PharmaSystem — Modulo 03: Analise Exploratoria com Pandas
==========================================================

Pacote com utilitarios de carregamento, limpeza, analise, visualizacao e
exportacao dos dados de vendas da rede fictícia PharmaMinas.

Uso rapido:

    from src import carregamento, limpeza, analises, graficos, exportacao

    dados = carregamento.carregar_todas_tabelas("dados")
    dados_limpos = limpeza.limpar_e_derivar(dados)
    master = limpeza.criar_dataframe_master(dados_limpos)

    kpis = analises.kpis_gerais(master)
    fig = graficos.grafico_faturamento_mensal(analises.faturamento_mensal(master))
"""

__version__ = "1.0.0"
__author__ = "Lucas Verissimo"
