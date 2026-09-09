# Guia de Construção do Dashboard — Passo a Passo

Este é o **manual operacional** para construir o `.pbix` do zero. Cada etapa é uma sessão de 30 a 90 minutos. Se seguir na ordem, você terá o dashboard completo em cerca de 8 a 10 horas de trabalho efetivo.

**Pré-requisitos:**
- Power BI Desktop instalado (baixe grátis em [powerbi.microsoft.com](https://powerbi.microsoft.com/pt-br/desktop/))
- Todos os arquivos deste pacote extraídos em uma pasta
- Windows (Power BI Desktop não roda em Linux/Mac nativamente)

---

## FASE 1 — Importação dos Dados (45 min)

### 1.1 Novo projeto
1. Abra o Power BI Desktop.
2. Feche a tela inicial ("Começar" ou "Get started").
3. Salve o arquivo desde já: `Arquivo → Salvar como → PharmaSystem.pbix`.

### 1.2 Importar CSVs
1. **Página inicial → Obter dados → Texto/CSV**.
2. Selecione `dados/filiais.csv`. Preview aparece.
3. Confirme:
   - **Origem do arquivo:** UTF-8 (65001)
   - **Delimitador:** Vírgula
   - **Detecção de tipo:** Baseada nas primeiras 200 linhas
4. Clique em **Transformar dados** (NÃO em "Carregar" ainda).

### 1.3 Ajustes no Power Query (Editor)
Ainda em Filiais, no Power Query Editor:
- Verifique tipos:
  - `id` → **Número inteiro**
  - `data_abertura` → **Data**
  - `ativa` → **Texto**
- Rename da consulta (canto direito) para `filiais` (minúsculo).

Repita esse fluxo para cada CSV. Configurações-chave por tabela:

| Tabela | Coluna | Tipo |
|---|---|---|
| `categorias` | id | Nº inteiro |
| `produtos` | id, categoria_id, estoque_minimo | Nº inteiro |
| `produtos` | preco_custo, preco_venda | Número decimal fixo |
| `estoque` | id, produto_id, filial_id, quantidade | Nº inteiro |
| `clientes` | id | Nº inteiro |
| `clientes` | data_nascimento, data_cadastro | Data |
| `vendas` | id, filial_id, cliente_id | Nº inteiro |
| `vendas` | data_venda | Data/Hora |
| `vendas` | valor_total, desconto | Número decimal fixo |
| `itens_venda` | id, venda_id, produto_id, quantidade | Nº inteiro |
| `itens_venda` | preco_unitario, subtotal | Número decimal fixo |
| `calendario` | data | Data |
| `calendario` | ano, trimestre, mes_num, dia, dia_semana_num | Nº inteiro |

### 1.4 Coluna computada em `vendas`: valor líquido
Ainda no Power Query, na tabela `vendas`:
- **Adicionar coluna → Coluna personalizada**
- Nome: `valor_liquido`
- Fórmula: `[valor_total] - [desconto]`
- Tipo: Número decimal fixo

### 1.5 Aplicar mudanças
Clique em **Fechar e aplicar** no canto superior esquerdo do Power Query.

---

## FASE 2 — Modelo de Dados (30 min)

### 2.1 Visualizar o modelo
Vá para a aba **Modelo** (ícone de tabelas conectadas na barra lateral esquerda).

Ao importar, o Power BI tenta detectar relacionamentos automaticamente. **Ignore os automáticos e configure manualmente** para ter certeza.

### 2.2 Excluir relacionamentos automáticos suspeitos
Delete todos os relacionamentos que aparecerem automaticamente (botão direito → Excluir).

### 2.3 Criar relacionamentos manualmente
Arraste a coluna de uma tabela para a outra. Para cada um, verifique:
- **Cardinalidade:** correta (ver tabela abaixo)
- **Direção do filtro:** Único (do "1" para o "N")
- **Ativar relacionamento:** Sim

| Origem (1) | Destino (N) | Cardinalidade | Ativo? |
|---|---|---|---|
| `calendario[data]` | `vendas[data_venda]` | 1:muitos | **Sim** |
| `calendario[data]` | `clientes[data_cadastro]` | 1:muitos | **NÃO (inativo)** |
| `filiais[id]` | `vendas[filial_id]` | 1:muitos | Sim |
| `filiais[id]` | `estoque[filial_id]` | 1:muitos | Sim |
| `clientes[id]` | `vendas[cliente_id]` | 1:muitos | Sim |
| `vendas[id]` | `itens_venda[venda_id]` | 1:muitos | Sim |
| `produtos[id]` | `itens_venda[produto_id]` | 1:muitos | Sim |
| `produtos[id]` | `estoque[produto_id]` | 1:muitos | Sim |
| `categorias[id]` | `produtos[categoria_id]` | 1:muitos | Sim |

**Atenção:** o relacionamento entre `calendario` e `clientes[data_cadastro]` fica **inativo** porque `calendario[data]` já está ligado a `vendas[data_venda]` (só pode ter 1 ativo por par). Ele será usado sob demanda via `USERELATIONSHIP` na medida `Novos Clientes`.

### 2.4 Marcar `calendario` como Tabela de Data
Aba **Modelagem** (ou botão direito na tabela `calendario`) → **Marcar como tabela de datas** → Coluna: `data`.

### 2.5 Data hierarchy: desativar auto-hierarquia
`Arquivo → Opções e configurações → Opções → Carregamento de dados → desmarque "Data/hora automática"`.
Isso remove hierarquias de data que o Power BI cria sozinho e que atrapalham (a `calendario` já supre isso).

---

## FASE 3 — Medidas DAX (2h)

### 3.1 Criar medidas na tabela vendas
Todas as medidas ficam em `vendas`. Botão direito → **Nova medida** → cole o código.

### 3.2 Ordem de criação
Siga a numeração para não ter erro de dependência:
1. Abra `dax/01_medidas_base.dax` → crie M01 a M13.
2. Abra `dax/02_medidas_temporais.dax` → crie M14 a M21.
3. Abra `dax/03_medidas_avancadas.dax` → crie M22 a M32.

### 3.3 Formatar cada medida
Selecione a medida → aba **Ferramentas de medida** → configure:
- **Faturamento *:** Moeda BRL, 2 decimais
- **Total *:** Número inteiro
- **Ticket / Margem / Média:** Moeda BRL, 2 decimais
- **Crescimento % / Taxa / Percentual:** Percentual, 2 decimais
- **Ranking:** Número inteiro

### 3.4 Organizar em pastas (opcional)
Botão direito na medida → **Nova pasta de exibição**.

Sugestão de nome de pastas:
- `KPIs Principais`
- `Time Intelligence`
- `Rankings`
- `Auxiliares`

### 3.5 Testar
Coloque uma tabela na página em branco. Arraste `Faturamento Total`, `Total Vendas`, `Ticket Medio`. Deve mostrar: R$ 224.418,17 / 1.458 / R$ 153,92 (aproximadamente).

---

## FASE 4 — Tema Visual (10 min)

1. Aba **Exibição** → **Temas** → **Procurar temas**.
2. Selecione `tema/tema_pharmasystem.json`.
3. Confirme.

O tema já traz as cores e fontes padrão. Nenhuma configuração adicional necessária.

---

## FASE 5 — Página 1: Visão Geral (90 min)

Referência visual: `docs/mockup_pagina1_visao_geral.png`

### 5.1 Configurar página
- Renomear página (aba de baixo, botão direito na "Página 1") para `Visao Geral`.
- **Formato da página** (painel direito, sem visual selecionado):
  - **Tamanho:** Personalizado 1600 × 900
  - **Cor da tela de fundo:** `#F5F5F5`

### 5.2 Cabeçalho superior (5 min)
1. **Inserir → Formas → Retângulo**. Redimensione para 1600 × 80, canto superior esquerdo em 0,0.
2. Preenchimento: gradiente vertical de `#00695C` para `#004D40`.
3. **Inserir → Caixa de texto**: adicione "PharmaSystem" (branco, Segoe UI, 20pt, bold) na posição (80, 15).
4. Segunda caixa de texto: "Dashboard Executivo — Visão Geral" (verde-água claro `#B2DFDB`, 13pt) em (80, 45).

### 5.3 Botões de navegação (15 min)
1. **Inserir → Botões → Em branco**. Configure para "Visão Geral":
   - Tamanho: 150 × 35
   - Fundo: `#00695C`
   - Texto: "Visão Geral", branco bold, 13pt
   - Ação: **Navegação de página** → mesma página
2. Repita para "Produtos" (fundo branco, borda `#00695C`) e "Clientes".
3. Alinhe os três lado a lado abaixo do cabeçalho.

### 5.4 Painel de filtros (20 min)
1. **Inserir → Formas → Retângulo**: 220 × 700 na posição (30, 160). Fundo branco, cantos arredondados 4.
2. **Título "FILTROS":** caixa de texto 14pt bold, `#424242`.
3. Adicione os segmentadores (ícone segmentador → arraste campo):
   - `calendario[ano]` → visual: Blocos
   - `filiais[estado]` → visual: Suspenso
   - `filiais[nome]` → visual: Lista
   - `categorias[nome]` → visual: Suspenso
   - `vendas[forma_pagamento]` → visual: Suspenso

### 5.5 Cartões KPI (20 min)
Insira 5 cartões. Cada um com um retângulo de fundo branco (240×120, sombra) e o cartão sobre ele:
1. **Faturamento Total** — cor `#00695C`
2. **Total Vendas** — cor `#1976D2`
3. **Ticket Medio** — cor `#FFA000`
4. **Margem Bruta** — cor `#26A69A`
5. **Clientes Ativos 90d** — cor `#7B1FA2`

Para cada cartão:
- Selecione o visual **Cartão**
- Arraste a medida para "Campos"
- **Formato do visual:**
  - Rótulo dos dados: 32pt bold, cor conforme lista acima
  - Rótulo da categoria: 11pt bold, `#757575`, MAIÚSCULAS
- Adicione uma **caixa de texto** abaixo com o KPI de contexto (crescimento, meta, etc)
- Adicione um **retângulo vertical** de 6px na cor do KPI como faixa lateral esquerda

### 5.6 Gráfico: Evolução Mensal (10 min)
1. Insira **Gráfico de linhas** (760 × 290).
2. Configure:
   - **Eixo X:** `calendario[ano_mes]`
   - **Valores:** `Faturamento Total` (linha 1, `#00695C`, espessura 3), `Media Movel 3M` (linha 2, `#26A69A`, tracejada, espessura 2)
3. Ativar **Rótulos de dados**.
4. Título: "Evolução do Faturamento Mensal".

### 5.7 Top 10 Filiais (10 min)
1. Insira **Gráfico de barras clusterizadas** (515 × 290).
2. Configure:
   - **Eixo Y:** `filiais[nome]`
   - **Eixo X:** `Faturamento Total`
   - **Filtros do visual:** TopN = 10 por Faturamento Total
3. Cor: `#00695C`.
4. Rótulos de dados ativados.

### 5.8 Rosca — Forma de Pagamento (5 min)
1. Insira **Rosca** (380 × 250).
2. **Legenda:** `vendas[forma_pagamento]`.
3. **Valores:** `Faturamento Total`.
4. Cores da paleta (`#00695C`, `#26A69A`, `#80CBC4`, `#1976D2`, `#B2DFDB`).

### 5.9 Vendas por dia da semana (5 min)
1. Insira **Gráfico de colunas empilhadas** (360 × 250).
2. **Eixo X:** `calendario[dia_semana_nome]` (ordenar por `dia_semana_num`).
3. **Eixo Y:** `Total Vendas`.

### 5.10 Tabela Resumo Filiais (5 min)
1. Insira **Tabela** (515 × 250).
2. Colunas: `filiais[nome]`, `Total Vendas`, `Faturamento Total`, `Ticket Medio`, `Percentual do Total`.
3. Filtro: TopN=5.
4. Barra de dados na coluna Faturamento (Formatação condicional).

### 5.11 Editar interações
Selecione cada cartão KPI → aba **Formato → Editar interações** → configure todos os outros visuais para "Filtrar", mas defina que gráficos NÃO devem filtrar os cartões (o clique num gráfico deve filtrar outros gráficos mas manter cartões estáveis) — ajuste conforme seu gosto.

### 5.12 Alinhamento fino
Use o menu **Formato → Alinhar** para garantir que tudo esteja alinhado (topo, esquerda, distribuição uniforme).

---

## FASE 6 — Página 2: Produtos (60 min)

Referência: `docs/mockup_pagina2_produtos.png`

Duplique a Página 1 (botão direito na aba → Duplicar página). Renomeie para `Produtos`. Depois:
1. Ajuste o subtítulo do cabeçalho.
2. Ative o botão "Produtos" (troque de fundo `#00695C`).
3. Substitua/adicione visuais conforme especificação em `docs/especificacao_visuais.md`.

Visuais específicos da Página 2:
- Cartão de várias linhas com "Produto Campeão" (usa `Produto Mais Vendido`)
- Cartões KPI: `Total Produtos Ativos`, `Total Itens Vendidos`, `Percentual de Margem`, `Concentracao Top 10 %`
- Top 10 produtos por unidades (barras)
- Rosca por categoria
- Margem % por categoria (barras)
- Tabela top 10 por faturamento
- Painel de alertas (3 caixas coloridas com formatação de texto)

---

## FASE 7 — Página 3: Clientes (60 min)

Referência: `docs/mockup_pagina3_clientes.png`

Duplique a Página 1, renomeie para `Clientes`, ajuste cabeçalho e navegação.

Visuais específicos:
- 5 KPIs: Total Clientes, Clientes Ativos 90d, Clientes Inativos, LTV Médio, Novos Clientes
- Tabela Top 10 Clientes por LTV
- Segmentação por faixa etária (barras horizontais)
- Evolução de novos cadastros (colunas)
- Distribuição geográfica (barras horizontais)

Antes de construir a página, crie a **coluna calculada** `Faixa Etaria` na tabela `clientes` (ver `docs/especificacao_visuais.md`).

---

## FASE 8 — Refinamento Visual (60 min)

### 8.1 Padronização
- Verifique que todas as fontes são **Segoe UI** (padrão do Power BI, alinha com Microsoft).
- Todos os títulos de visuais em 14pt bold `#424242`.
- Todos os subtítulos em 11pt `#9E9E9E`.

### 8.2 Sombras nos containers
Selecione os retângulos brancos que servem de container → **Formato → Efeitos → Sombra** ativada com opacidade 20%.

### 8.3 Tooltips
Selecione um visual → **Formato → Tooltip** → configure ao menos os campos principais.

### 8.4 Título dinâmico (opcional, avançado)
Crie uma caixa de texto com título dinâmico via medida:
```dax
Titulo Dinamico Pagina =
"Dashboard | " &
IF (
    ISFILTERED ( calendario[ano] ),
    "Ano: " & SELECTEDVALUE ( calendario[ano] ),
    "Todos os anos"
)
```

### 8.5 Botão "Limpar Filtros"
Insira um botão com ação **Marcador** (crie um marcador com todos os filtros limpos).

---

## FASE 9 — Publicação e Documentação (30 min)

### 9.1 Exportar prints
`Arquivo → Exportar → PDF` para gerar um PDF de todas as páginas.

Alternativa (melhor qualidade): use a ferramenta **Ferramenta de Captura** do Windows para PNG de cada página.

Salve os PNGs em `pharma-system/modulo-02-powerbi/docs/prints/`.

### 9.2 Salvar o .pbix
`Arquivo → Salvar`. Coloque em `pharma-system/modulo-02-powerbi/PharmaSystem.pbix`.

### 9.3 (Opcional) Publicar no Power BI Service
Se tiver conta gratuita:
`Página inicial → Publicar → Meu workspace`. Copie o link e adicione no README.

### 9.4 Preparar publicação
- README.md do módulo pronto (use o do pacote como base).
- Prints das 3 páginas no `docs/`.
- Post do LinkedIn com destaques.

---

## Checklist final

- [ ] Todos os 8 CSVs carregados corretamente.
- [ ] `calendario` marcada como tabela de datas.
- [ ] 9 relacionamentos criados (8 ativos + 1 inativo).
- [ ] 32 medidas DAX criadas e formatadas.
- [ ] Tema `tema_pharmasystem.json` aplicado.
- [ ] 3 páginas construídas (Visão Geral, Produtos, Clientes).
- [ ] Botões de navegação funcionam.
- [ ] Segmentadores filtram todos os visuais.
- [ ] Prints das 3 páginas salvos em `docs/prints/`.
- [ ] `.pbix` salvo e comitado no GitHub.
- [ ] Post do LinkedIn publicado.

**Tempo total estimado:** 8 a 10 horas de trabalho efetivo.
