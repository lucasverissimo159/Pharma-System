# Especificação de Visuais — Dashboard PharmaSystem

Este documento descreve **cada visual** do dashboard: tipo, campos, formatação e configurações. Use como referência ao construir cada página no Power BI.

**Referências visuais:**
- `mockup_pagina1_visao_geral.png` / `.svg`
- `mockup_pagina2_produtos.png` / `.svg`
- `mockup_pagina3_clientes.png` / `.svg`

---

## Paleta de Cores (aplicar via tema)

| Uso | Hex | Nome |
|---|---|---|
| Primária | `#00695C` | Verde farmácia escuro |
| Secundária | `#26A69A` | Verde farmácia claro |
| Acento 1 | `#1976D2` | Azul confiança |
| Acento 2 | `#FFA000` | Âmbar destaque |
| Acento 3 | `#7B1FA2` | Roxo clientes |
| Alerta positivo | `#4CAF50` | Verde OK |
| Alerta negativo | `#EF5350` | Vermelho warning |
| Fundo | `#F5F5F5` | Cinza claro |
| Texto principal | `#424242` | Cinza escuro |
| Texto secundário | `#9E9E9E` | Cinza médio |

O arquivo `tema/tema_pharmasystem.json` já traz tudo isso — importe em **Exibição → Temas → Procurar temas**.

---

## Elementos globais (todas as páginas)

### Cabeçalho superior
- **Tipo:** Retângulo + Caixa de texto
- **Altura:** 80 px
- **Preenchimento:** gradiente vertical `#00695C → #004D40`
- **Conteúdo:**
  - Título "PharmaSystem" (branco, 20pt, bold)
  - Subtítulo "Dashboard Executivo — [nome da página]" (verde-água claro, 13pt)

### Botões de navegação
- **Tipo:** Botões (Inserir → Botão → Em branco)
- **Ação:** *Navegação de página*
- 3 botões: "Visão Geral", "Produtos", "Clientes"
- **Formato ativo:** fundo `#00695C`, texto branco bold
- **Formato inativo:** fundo branco, borda `#00695C`, texto `#00695C`

### Painel de filtros (esquerda)
Bloco branco, 220 px de largura, sombra sutil.

Segmentadores comuns:
| Página | Segmentadores |
|---|---|
| Todas | Ano, Filial |
| Página 1 | + Estado, Categoria, Forma de Pagamento |
| Página 2 | + Categoria, Exige Receita, Fabricante, Faixa de Preço |
| Página 3 | + Cidade, Faixa Etária, Status Cliente, Período |

Configuração dos segmentadores:
- **Formato:** Título em maiúsculas, 12pt, `#616161`
- **Cor de seleção:** `#00695C`
- **Fonte dos itens:** 11pt, `#424242`

---

# PÁGINA 1 — VISÃO GERAL

## KPI 1: Faturamento Total
| Propriedade | Valor |
|---|---|
| Tipo | Cartão |
| Campo | Medida `Faturamento Total` |
| Fonte principal | 32pt bold, `#00695C` |
| Formato | Moeda BRL, casas decimais dinâmicas |
| Detalhe | Cartão pequeno com `Crescimento Mensal %` abaixo |
| Ícone lateral | Faixa vertical `#00695C` de 6px |

## KPI 2: Total de Vendas
| Propriedade | Valor |
|---|---|
| Tipo | Cartão |
| Campo | Medida `Total Vendas` |
| Fonte principal | 32pt bold, `#1976D2` |
| Formato | Número inteiro |
| Detalhe adicional | "X canceladas (Y%)" com `Total Vendas Canceladas` e `Taxa Cancelamento` |

## KPI 3: Ticket Médio
| Propriedade | Valor |
|---|---|
| Tipo | Cartão |
| Campo | Medida `Ticket Medio` |
| Fonte | 32pt bold, `#FFA000` |
| Formato | Moeda BRL, 2 decimais |

## KPI 4: Margem Bruta
| Propriedade | Valor |
|---|---|
| Tipo | Cartão |
| Campo | Medida `Margem Bruta` |
| Fonte | 32pt bold, `#26A69A` |
| Detalhe | "X% de margem" via `Percentual de Margem` |

## KPI 5: Clientes Ativos
| Propriedade | Valor |
|---|---|
| Tipo | Cartão |
| Campo | Medida `Clientes Ativos 90d` |
| Fonte | 32pt bold, `#7B1FA2` |
| Detalhe | "de X cadastrados" via `Total Clientes` |

## Visual 6: Evolução do Faturamento Mensal
| Propriedade | Valor |
|---|---|
| Tipo | Gráfico de Linhas |
| Eixo X | `calendario[ano_mes]` (ordenado por `ano_mes`) |
| Valor 1 | `Faturamento Total` (linha grossa `#00695C`) |
| Valor 2 | `Media Movel 3M` (linha tracejada `#26A69A`) |
| Rótulos | Ativados, formato R$ mil |
| Zoom | Slider desativado para não poluir |

## Visual 7: Top 10 Filiais por Faturamento
| Propriedade | Valor |
|---|---|
| Tipo | Gráfico de Barras (horizontal) |
| Eixo Y | `filiais[nome]` |
| Eixo X | `Faturamento Total` |
| Ordenação | Decrescente por Faturamento |
| Filtro do visual | `TopN = 10` |
| Rótulos de dados | Ativados, formato "R$ #,##0 K" |
| Cor | Gradiente `#00695C → #B2DFDB` (mais escuro = maior) |

## Visual 8: Forma de Pagamento
| Propriedade | Valor |
|---|---|
| Tipo | Rosca (Donut) |
| Legenda | `vendas[forma_pagamento]` |
| Valores | `Faturamento Total` |
| Rótulos | Categoria + % |
| Cores | Paleta de verde-água (`#00695C`, `#26A69A`, `#80CBC4`, `#1976D2`, `#B2DFDB`) |

## Visual 9: Vendas por Dia da Semana
| Propriedade | Valor |
|---|---|
| Tipo | Gráfico de Colunas (vertical) |
| Eixo X | `calendario[dia_semana_nome]` |
| Eixo Y | `Total Vendas` |
| Ordenação | Manual: Seg, Ter, Qua, Qui, Sex, Sab, Dom |
| Cor destaque | Sexta e Sábado em `#00695C`, resto `#26A69A`, Domingo `#B2DFDB` |

**Truque para ordenar dia da semana:** na tabela `calendario`, use `dia_semana_num` como coluna de ordenação para `dia_semana_nome`.

## Visual 10: Resumo por Filial (top 5)
| Propriedade | Valor |
|---|---|
| Tipo | Tabela |
| Colunas | `filiais[nome]`, `Total Vendas`, `Faturamento Total`, `Ticket Medio`, `Percentual do Total` |
| Filtro | Top 5 por Faturamento |
| Formatação condicional | Faturamento com barra de dados verde |

---

# PÁGINA 2 — PRODUTOS

## KPI 1: Produto Campeão do Período
| Propriedade | Valor |
|---|---|
| Tipo | Cartão de várias linhas (Multi-row card) |
| Campo | Medida `Produto Mais Vendido` |
| Fonte | 16pt bold, `#2E7D32` |
| Extras | Total de unidades vendidas do líder, categoria, fabricante |

## KPI 2: Produtos Ativos
Medida `Total Produtos Ativos` — número inteiro.

## KPI 3: Unidades Vendidas
Medida `Total Itens Vendidos` — número inteiro com separador de milhar.

## KPI 4: Margem Média
Medida `Percentual de Margem` — formato %, 1 decimal.

## KPI 5: Concentração Top 10
Medida `Concentracao Top 10 %` — formato %, 1 decimal.
Cor: verde se ≤ 40%, âmbar se 40–60%, vermelho se ≥ 60% (formatação condicional).

## Visual 6: Top 10 Produtos por Unidades
Barras horizontais, ordenação decrescente. TopN filter = 10.

## Visual 7: Faturamento por Categoria
Rosca (Donut). Fatias com percentual visível.

## Visual 8: Margem % por Categoria
Barras horizontais. Alerta: margens baixas em vermelho, altas em verde.

## Visual 9: Tabela Top 10 Produtos por Faturamento
Colunas: Produto, Categoria, Unidades, Faturamento, `Percentual do Total`.
Barra de dados na coluna Faturamento.

## Visual 10: Painel de Alertas
Cartão de texto customizado com 3 alertas visuais coloridos:
- **Âmbar:** Produtos sem venda no período (usar Q10 do módulo 01 como base)
- **Azul:** Total de medicamentos com receita (contagem + relatório SNGPC)
- **Verde:** Concentração top 10 saudável (< 40%)

---

# PÁGINA 3 — CLIENTES

## KPI 1: Total de Clientes
Medida `Total Clientes`.

## KPI 2: Clientes Ativos 90d
Medida `Clientes Ativos 90d`. Cor: `#4CAF50`.

## KPI 3: Clientes Inativos
Medida customizada: `Total Clientes - Clientes Ativos 90d`.
Cor: `#EF6C00`.

## KPI 4: LTV Médio
Medida customizada:
```dax
LTV Medio =
DIVIDE(
    [Faturamento Total],
    [Clientes com Compra],
    0
)
```
Formato: Moeda BRL.

## KPI 5: Novos Clientes (mês)
Medida `Novos Clientes` com filtro do mês atual.

## Visual 6: Top 10 Clientes por LTV
Tabela com: Nome, Cidade, Nº Compras, Ticket Médio, LTV.
Ordenar decrescente por LTV, TopN=10.

## Visual 7: Segmentação por Faixa Etária
Barras horizontais.

Criar coluna calculada em `clientes`:
```dax
Faixa Etaria =
VAR Idade = DATEDIFF(clientes[data_nascimento], TODAY(), YEAR)
RETURN
    SWITCH(
        TRUE(),
        Idade < 25, "1. Ate 24 anos",
        Idade < 35, "2. 25 a 34",
        Idade < 45, "3. 35 a 44",
        Idade < 60, "4. 45 a 59",
        "5. 60+ anos"
    )
```

Usar essa coluna no eixo Y.

## Visual 8: Evolução de Novos Cadastros por Mês
Gráfico de colunas. Eixo X: `calendario[ano_mes]` (via USERELATIONSHIP com data_cadastro).
Eixo Y: `Novos Clientes`.

**Alternativa mais simples (sem relacionamento inativo):**
```dax
Novos Clientes Simple =
CALCULATE (
    DISTINCTCOUNT ( clientes[id] ),
    USERELATIONSHIP ( clientes[data_cadastro], calendario[data] )
)
```

## Visual 9: Distribuição Geográfica
Barras horizontais. Top 6 cidades + "Outras (N)" agrupadas.

---

## Configurações Gerais dos Visuais

### Cartões (KPIs)
- **Preenchimento:** branco com sombra sutil
- **Borda esquerda colorida** de 6px (linha vertical dentro do cartão) na cor do KPI
- **Cantos:** arredondados 6px
- **Espaçamento entre cartões:** 20px

### Gráficos
- **Preenchimento fundo:** branco
- **Grade:** apenas horizontal, cor `#F0F0F0`, estilo tracejado
- **Eixos:** cor `#9E9E9E`, fonte 10pt
- **Rótulos de dados:** ativados sempre que couber sem poluir

### Tabelas
- **Cabeçalho:** fundo cinza claro `#F5F5F5`, texto `#757575` bold 10pt
- **Linhas alternadas:** desativadas (limpo)
- **Divisórias entre linhas:** cor `#F5F5F5`, 1px
- **Fonte das linhas:** 11pt, `#424242`

### Interações entre visuais
- **Padrão:** ao clicar em um visual, filtra todos os outros da página (comportamento padrão do Power BI).
- **Exceção:** cartões KPI não devem ser afetados por clique em outros visuais (usar *Editar interações*).

---

## Tooltips customizados (opcional, avançado)

Crie uma página oculta chamada "Tooltip Filial":
- Nome da filial (grande)
- Faturamento, Ticket, Ranking
- Mini-gráfico de evolução

Aplique como tooltip nos visuais da página 1 que envolvam filial.

Mesmo procedimento para "Tooltip Produto" e "Tooltip Cliente".
