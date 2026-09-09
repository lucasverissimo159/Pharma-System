# Insights de Negócio — Análise Exploratória PharmaMinas

**Módulo 03 — Python + Pandas**
**Período analisado:** Jan/2024 a Jun/2026 (dataset sintético)
**Universo:** 1.500 vendas em 15 filiais, 71 SKUs ativos, 200 clientes

---

## Insight 1 — Volume e ticket

O faturamento total do período foi de **R$ 226.548,60**, distribuído em **1.458 vendas concluídas** e **4.247 itens comercializados**. O ticket médio ficou em **R$ 155,38**.

**Implicação:** o dado por si só é baixo (R$ 155 por venda), consistente com o público de farmácia (compras pequenas e frequentes). O foco de crescimento deve ser em **frequência**, não em ticket.

---

## Insight 2 — Margem e categoria mais rentável

A margem bruta acumulada foi de **R$ 123.224,20 (54,4%** sobre o faturamento). A categoria de **MAIOR margem** foi *Cosméticos* (**56,9%**) e a de **MENOR** foi *Dermocosméticos* (**53,9%**).

**Implicação:** o mix está bem balanceado — a diferença entre a melhor e a pior margem é de apenas 3 pontos percentuais. Isso indica precificação disciplinada em toda a rede, sem categorias "queimadas".

---

## Insight 3 — Concentração geográfica em BH

A filial líder foi **PharmaMinas Belo Horizonte Savassi**, com faturamento de **R$ 42.822,90** — **18,9% do total** e **mais de 3x acima da mediana** das outras unidades.

**Implicação:** oportunidade clara de **estudar as práticas** dessa unidade (mix, layout, equipe, campanhas locais) para replicar. Também é sinal de alerta: uma única loja concentrando quase 1/5 do faturamento aumenta o risco operacional.

---

## Insight 4 — Concentração de SKUs saudável

**54,1%** do faturamento vem dos **10 produtos mais vendidos**. A regra 80/20 exige **30 produtos** para atingir 80% (de 71 SKUs vendidos ao todo).

**Implicação:** o catálogo é **relativamente diversificado** — não há dependência crítica de poucos SKUs. Isso reduz risco de ruptura, mas também sugere que o giro por SKU é mais espalhado (menor economia de escala em negociação com fornecedores).

---

## Insight 5 — Ticket fim de semana ≈ dia útil

Ticket médio no **fim de semana: R$ 153,83** vs **dia útil: R$ 155,98** — diferença de apenas **-1,4%**.

**Implicação:** ao contrário do senso comum ("fim de semana vende mais"), o cliente do PharmaMinas gasta praticamente o mesmo. **Campanhas de fim de semana** para elevar ticket (kits, combos, brindes acima de X) têm potencial, já que o comportamento é homogêneo. Vale testar A/B.

---

## Insight 6 — Perfumaria lidera

A categoria **Perfumaria** lidera em faturamento (**R$ 44.906,20, 19,8% do total**), à frente de categorias mais "esperadas" como medicamentos.

**Implicação:** sugere forte aderência do mix de perfumaria — vale investigar **sortimento**, **posicionamento na loja física** (área nobre?) e se esse padrão vem da localização das filiais (bairros de classe A/B/C podem mudar o resultado). Também vale um plano de expansão de linhas complementares (banho, dermocosméticos premium).

---

## Como reproduzir esta análise

```bash
python scripts/executar_analise.py
```

Todos os cálculos estão em `src/analises.py`. Gráficos em `graficos/`. Relatório executivo em `exports/relatorio_pharma_system.xlsx`.

---

## Limitações

- Dataset **sintético** (seed=42) — insights são válidos como *exercício de análise*, mas não refletem uma rede real.
- Período de 30 meses (2024-01 a 2026-06) pode ter viés sazonal.
- Vendas sem cliente identificado (chapa branca) não entram na análise de LTV — pode subestimar a base ativa.
