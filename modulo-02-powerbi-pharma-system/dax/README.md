# Medidas DAX — PharmaSystem

Este diretório contém as **32 medidas DAX** que alimentam o dashboard do PharmaSystem, organizadas em 3 arquivos por nível de complexidade.

---

## Como usar

Cada arquivo `.dax` é uma **coleção de medidas** para copiar e colar no Power BI Desktop. **Não é um arquivo executável** — é referência de código, como um `.sql` seria para um SGBD.

### Passo a passo no Power BI

1. Importe os CSVs da pasta `dados/` (ver `docs/guia_construcao.md`).
2. Configure relacionamentos e marque `calendario` como Tabela de Data.
3. Abra o arquivo `.dax` desejado no seu editor de texto.
4. Para cada medida:
   - No Power BI, vá em **Modelo de dados** → clique com botão direito na tabela → **Nova medida**.
   - Cole o código a partir do nome (linha `Nome Medida =`).
   - Confirme com **Enter**.
   - Formate na guia **Ferramentas de medida** (Moeda, %, Nº inteiro, etc).

### Ordem recomendada de criação

Siga a numeração — as medidas dependem umas das outras.

| Arquivo | Medidas | Depende de |
|---|---|---|
| `01_medidas_base.dax` | M01–M13 | Nada (base) |
| `02_medidas_temporais.dax` | M14–M21 | M01 + calendário configurado |
| `03_medidas_avancadas.dax` | M22–M32 | M01, M06 |

---

## Índice das 32 medidas

### Base (13)

| # | Nome | Retorna | Uso principal |
|---|---|---|---|
| M01 | Faturamento Total | R$ | KPI principal |
| M02 | Faturamento Bruto | R$ | Análise de desconto |
| M03 | Total Descontos | R$ | Análise de desconto |
| M04 | Total Vendas | nº | KPI |
| M05 | Total Vendas Canceladas | nº | Auditoria |
| M06 | Ticket Medio | R$ | KPI |
| M07 | Total Itens Vendidos | nº | Volume |
| M08 | Total Clientes | nº | Base de cadastro |
| M09 | Clientes com Compra | nº | Conversão |
| M10 | Total Produtos Ativos | nº | Catálogo |
| M11 | Taxa Cancelamento | % | Qualidade |
| M12 | Margem Bruta | R$ | Lucratividade |
| M13 | Percentual de Margem | % | Lucratividade |

### Time Intelligence (8)

| # | Nome | Retorna | Uso principal |
|---|---|---|---|
| M14 | Faturamento Mes Anterior | R$ | Comparativo MoM |
| M15 | Faturamento Ano Anterior | R$ | Comparativo YoY |
| M16 | Crescimento Mensal % | % | KPI de tendência |
| M17 | Crescimento Anual % | % | KPI de tendência |
| M18 | Faturamento YTD | R$ | Acumulado do ano |
| M19 | Faturamento YTD Ano Anterior | R$ | Comparativo YTD |
| M20 | Media Movel 3M | R$ | Suavização de série |
| M21 | Clientes Ativos 90d | nº | Retenção |

### Avançadas (11)

| # | Nome | Retorna | Uso principal |
|---|---|---|---|
| M22 | Ranking Filial | nº | Cartão contextual |
| M23 | Ranking Produto | nº | Cartão contextual |
| M24 | Percentual do Total | % | Participação em tabelas |
| M25 | Faturamento Top 10 Produtos | R$ | Concentração |
| M26 | Concentracao Top 10 % | % | Alerta 80/20 |
| M27 | Produto Mais Vendido | texto | Cartão dinâmico |
| M28 | Filial Mais Vendedora | texto | Cartão dinâmico |
| M29 | Ticket Medio da Rede | R$ | Referência |
| M30 | Ticket Medio vs Rede % | % | Benchmark |
| M31 | Novos Clientes | nº | Aquisição |
| M32 | Rotulo Faturamento | texto | KPI formatado |

---

## Requisitos do modelo de dados

Antes de criar as medidas, o modelo precisa ter:

1. **Relacionamentos** (ver `docs/modelo_dados.png`):
   - `calendario[data]` → `vendas[data_venda]` (1:N, ativo)
   - `filiais[id]` → `vendas[filial_id]` (1:N)
   - `clientes[id]` → `vendas[cliente_id]` (1:N)
   - `vendas[id]` → `itens_venda[venda_id]` (1:N)
   - `produtos[id]` → `itens_venda[produto_id]` (1:N)
   - `produtos[id]` → `estoque[produto_id]` (1:N)
   - `filiais[id]` → `estoque[filial_id]` (1:N)
   - `categorias[id]` → `produtos[categoria_id]` (1:N)
   - `clientes[data_cadastro]` → `calendario[data]` (1:N, **INATIVO** — só para M31)

2. **Marcar `calendario` como Tabela de Data:**
   - Aba Modelagem → clique em `calendario` → *Marcar como tabela de datas* → coluna `data`.

3. **Formatação de coluna:**
   - `vendas[valor_total]`, `vendas[desconto]`, `itens_venda[subtotal]`, `itens_venda[preco_unitario]`, `produtos[preco_custo]`, `produtos[preco_venda]`: **Moeda BRL**.
   - `vendas[data_venda]`, `clientes[data_cadastro]`, `calendario[data]`, `filiais[data_abertura]`, `clientes[data_nascimento]`: **Data**.

---

## Organização das medidas em pastas (opcional mas recomendado)

No Power BI, botão direito na medida → *Nova pasta de exibição*. Sugestão de estrutura:

```
📁 vendas
├── 📁 KPIs Principais
│   ├── Faturamento Total
│   ├── Ticket Medio
│   ├── Total Vendas
│   └── ...
├── 📁 Time Intelligence
│   ├── Faturamento Mes Anterior
│   ├── Crescimento Mensal %
│   └── ...
├── 📁 Rankings
│   ├── Ranking Filial
│   ├── Ranking Produto
│   └── Filial Mais Vendedora
└── 📁 Auxiliares
    ├── Rotulo Faturamento
    └── Ticket Medio da Rede
```

Isso deixa o painel de campos limpo e profissional.

---

## Dica: usando `VAR` para clareza

Muitas medidas avançadas usam `VAR` (variáveis) para melhorar legibilidade e performance. Exemplo:

```dax
Crescimento Mensal % =
VAR FaturamentoAtual = [Faturamento Total]        -- calculado 1x
VAR FaturamentoAnterior = [Faturamento Mes Anterior]  -- calculado 1x
RETURN
    DIVIDE (
        FaturamentoAtual - FaturamentoAnterior,
        FaturamentoAnterior,
        0
    )
```

Sem `VAR`, `[Faturamento Total]` seria calculado duas vezes. Com `VAR`, é calculado uma vez e reutilizado.

---

## Debugando medidas

Se uma medida retornar em branco ou dar erro:

1. Coloque-a numa **tabela** com uma coluna de contexto (ex: filial ou mês).
2. Use **Card** para ver o valor total.
3. Use **DAX Studio** (ferramenta externa gratuita) para inspecionar o plano de execução em medidas complexas.
