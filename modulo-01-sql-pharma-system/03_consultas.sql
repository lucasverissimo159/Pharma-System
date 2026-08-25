-- =============================================================================
-- PharmaSystem - Consultas SQL para Analise de Dados
-- Modulo 01 - Semana 1 do Portfolio
-- =============================================================================
-- Autor: Lucas Verissimo
-- SGBD: PostgreSQL 13+
-- Descricao: 25 consultas SQL organizadas por categoria de analise,
--            documentadas com objetivo, tecnicas usadas e resultado esperado.
-- =============================================================================
-- COMO USAR:
--   1. Execute 01_schema.sql e 02_inserts.sql primeiro.
--   2. Rode cada consulta individualmente e observe o resultado.
--   3. Cada consulta tem um cabecalho explicando o objetivo de negocio.
-- =============================================================================


-- #############################################################################
-- SECAO 1 - ANALISE DE VENDAS (Q01 a Q07)
-- #############################################################################


-- -----------------------------------------------------------------------------
-- Q01 - Faturamento total da rede
-- -----------------------------------------------------------------------------
-- Objetivo: Qual e o faturamento total (liquido) da rede considerando apenas
--           vendas concluidas?
-- Tecnica:  SUM com filtro WHERE
-- -----------------------------------------------------------------------------
SELECT
    SUM(valor_total - desconto) AS faturamento_total,
    COUNT(*) AS total_vendas
FROM vendas
WHERE status = 'CONCLUIDA';


-- -----------------------------------------------------------------------------
-- Q02 - Faturamento por filial
-- -----------------------------------------------------------------------------
-- Objetivo: Ranking de filiais pelo faturamento acumulado.
-- Tecnica:  JOIN + GROUP BY + ORDER BY DESC
-- -----------------------------------------------------------------------------
SELECT
    f.codigo,
    f.nome,
    f.cidade,
    COUNT(v.id) AS total_vendas,
    SUM(v.valor_total - v.desconto) AS faturamento
FROM vendas v
INNER JOIN filiais f ON v.filial_id = f.id
WHERE v.status = 'CONCLUIDA'
GROUP BY f.id, f.codigo, f.nome, f.cidade
ORDER BY faturamento DESC;


-- -----------------------------------------------------------------------------
-- Q03 - Faturamento mensal (evolucao temporal)
-- -----------------------------------------------------------------------------
-- Objetivo: Evolucao mensal do faturamento para analise de tendencia.
-- Tecnica:  Funcoes de data (TO_CHAR / DATE_TRUNC) + GROUP BY
-- -----------------------------------------------------------------------------
SELECT
    TO_CHAR(data_venda, 'YYYY-MM') AS mes_ano,
    COUNT(*) AS total_vendas,
    SUM(valor_total - desconto) AS faturamento,
    ROUND(AVG(valor_total - desconto), 2) AS ticket_medio
FROM vendas
WHERE status = 'CONCLUIDA'
GROUP BY TO_CHAR(data_venda, 'YYYY-MM')
ORDER BY mes_ano;


-- -----------------------------------------------------------------------------
-- Q04 - Ticket medio por filial
-- -----------------------------------------------------------------------------
-- Objetivo: Qual filial tem o maior ticket medio?
-- Tecnica:  AVG + GROUP BY
-- -----------------------------------------------------------------------------
SELECT
    f.codigo,
    f.nome,
    COUNT(v.id) AS qtd_vendas,
    ROUND(AVG(v.valor_total - v.desconto), 2) AS ticket_medio
FROM vendas v
INNER JOIN filiais f ON v.filial_id = f.id
WHERE v.status = 'CONCLUIDA'
GROUP BY f.id, f.codigo, f.nome
ORDER BY ticket_medio DESC;


-- -----------------------------------------------------------------------------
-- Q05 - Faturamento por forma de pagamento
-- -----------------------------------------------------------------------------
-- Objetivo: Como esta distribuido o faturamento entre as formas de pagamento?
-- Tecnica:  GROUP BY + calculo de percentual com Window Function
-- -----------------------------------------------------------------------------
SELECT
    forma_pagamento,
    COUNT(*) AS qtd_vendas,
    SUM(valor_total - desconto) AS faturamento,
    ROUND(
        100.0 * SUM(valor_total - desconto) / SUM(SUM(valor_total - desconto)) OVER (),
        2
    ) AS percentual
FROM vendas
WHERE status = 'CONCLUIDA'
GROUP BY forma_pagamento
ORDER BY faturamento DESC;


-- -----------------------------------------------------------------------------
-- Q06 - Comparativo de vendas: dia da semana
-- -----------------------------------------------------------------------------
-- Objetivo: Quais dias da semana tem maior volume de vendas?
-- Tecnica:  EXTRACT + CASE para nome do dia
-- -----------------------------------------------------------------------------
SELECT
    EXTRACT(DOW FROM data_venda) AS dia_num,
    CASE EXTRACT(DOW FROM data_venda)
        WHEN 0 THEN 'Domingo'
        WHEN 1 THEN 'Segunda'
        WHEN 2 THEN 'Terca'
        WHEN 3 THEN 'Quarta'
        WHEN 4 THEN 'Quinta'
        WHEN 5 THEN 'Sexta'
        WHEN 6 THEN 'Sabado'
    END AS dia_semana,
    COUNT(*) AS qtd_vendas,
    SUM(valor_total - desconto) AS faturamento
FROM vendas
WHERE status = 'CONCLUIDA'
GROUP BY EXTRACT(DOW FROM data_venda)
ORDER BY dia_num;


-- -----------------------------------------------------------------------------
-- Q07 - Taxa de cancelamento por filial
-- -----------------------------------------------------------------------------
-- Objetivo: Identificar filiais com maior taxa de cancelamento (possivel
--           problema operacional).
-- Tecnica:  Contagem condicional com FILTER + calculo de percentual
-- -----------------------------------------------------------------------------
SELECT
    f.codigo,
    f.nome,
    COUNT(*) AS total_vendas,
    COUNT(*) FILTER (WHERE v.status = 'CANCELADA') AS canceladas,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE v.status = 'CANCELADA') / COUNT(*),
        2
    ) AS taxa_cancelamento_pct
FROM vendas v
INNER JOIN filiais f ON v.filial_id = f.id
GROUP BY f.id, f.codigo, f.nome
ORDER BY taxa_cancelamento_pct DESC;


-- #############################################################################
-- SECAO 2 - ANALISE DE PRODUTOS (Q08 a Q14)
-- #############################################################################


-- -----------------------------------------------------------------------------
-- Q08 - Top 10 produtos mais vendidos (quantidade)
-- -----------------------------------------------------------------------------
-- Objetivo: Ranking dos produtos com maior giro (unidades vendidas).
-- Tecnica:  JOIN triplo + SUM + LIMIT
-- -----------------------------------------------------------------------------
SELECT
    p.id,
    p.nome,
    c.nome AS categoria,
    SUM(iv.quantidade) AS unidades_vendidas,
    COUNT(DISTINCT iv.venda_id) AS vendas_com_produto
FROM itens_venda iv
INNER JOIN produtos p ON iv.produto_id = p.id
INNER JOIN categorias c ON p.categoria_id = c.id
INNER JOIN vendas v ON iv.venda_id = v.id
WHERE v.status = 'CONCLUIDA'
GROUP BY p.id, p.nome, c.nome
ORDER BY unidades_vendidas DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- Q09 - Top 10 produtos com maior faturamento
-- -----------------------------------------------------------------------------
-- Objetivo: Ranking dos produtos que mais geram receita para a rede.
-- Tecnica:  SUM de subtotal + ORDER + LIMIT
-- -----------------------------------------------------------------------------
SELECT
    p.id,
    p.nome,
    c.nome AS categoria,
    SUM(iv.subtotal) AS faturamento_produto,
    SUM(iv.quantidade) AS unidades_vendidas
FROM itens_venda iv
INNER JOIN produtos p ON iv.produto_id = p.id
INNER JOIN categorias c ON p.categoria_id = c.id
INNER JOIN vendas v ON iv.venda_id = v.id
WHERE v.status = 'CONCLUIDA'
GROUP BY p.id, p.nome, c.nome
ORDER BY faturamento_produto DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- Q10 - Produtos que nunca foram vendidos
-- -----------------------------------------------------------------------------
-- Objetivo: Identificar produtos parados no catalogo (candidatos a promocao
--           ou descontinuidade).
-- Tecnica:  LEFT JOIN + IS NULL (anti-join)
-- -----------------------------------------------------------------------------
SELECT
    p.id,
    p.nome,
    c.nome AS categoria,
    p.preco_venda
FROM produtos p
INNER JOIN categorias c ON p.categoria_id = c.id
LEFT JOIN itens_venda iv ON iv.produto_id = p.id
WHERE iv.id IS NULL
  AND p.ativo = TRUE
ORDER BY c.nome, p.nome;


-- -----------------------------------------------------------------------------
-- Q11 - Faturamento e margem por categoria
-- -----------------------------------------------------------------------------
-- Objetivo: Qual categoria e mais rentavel? Considera margem (venda - custo).
-- Tecnica:  Multiplos JOINs + SUM ponderado
-- -----------------------------------------------------------------------------
SELECT
    c.nome AS categoria,
    COUNT(DISTINCT p.id) AS produtos_ativos,
    SUM(iv.quantidade) AS unidades_vendidas,
    SUM(iv.subtotal) AS faturamento,
    SUM(iv.quantidade * (p.preco_venda - p.preco_custo)) AS margem_bruta,
    ROUND(
        100.0 * SUM(iv.quantidade * (p.preco_venda - p.preco_custo))
              / NULLIF(SUM(iv.subtotal), 0),
        2
    ) AS margem_pct
FROM categorias c
LEFT JOIN produtos p ON p.categoria_id = c.id
LEFT JOIN itens_venda iv ON iv.produto_id = p.id
LEFT JOIN vendas v ON iv.venda_id = v.id AND v.status = 'CONCLUIDA'
GROUP BY c.id, c.nome
ORDER BY faturamento DESC NULLS LAST;


-- -----------------------------------------------------------------------------
-- Q12 - Produtos que exigem receita medica - Top vendas
-- -----------------------------------------------------------------------------
-- Objetivo: Analise regulatoria: quais medicamentos controlados mais vendem?
-- Tecnica:  Filtro por flag booleana
-- -----------------------------------------------------------------------------
SELECT
    p.nome,
    p.fabricante,
    SUM(iv.quantidade) AS unidades_vendidas,
    SUM(iv.subtotal) AS faturamento
FROM produtos p
INNER JOIN itens_venda iv ON iv.produto_id = p.id
INNER JOIN vendas v ON iv.venda_id = v.id
WHERE p.exige_receita = TRUE
  AND v.status = 'CONCLUIDA'
GROUP BY p.id, p.nome, p.fabricante
ORDER BY unidades_vendidas DESC;


-- -----------------------------------------------------------------------------
-- Q13 - Ranking de fabricantes por faturamento
-- -----------------------------------------------------------------------------
-- Objetivo: Concentracao de vendas por fabricante (analise de dependencia
--           de fornecedores).
-- Tecnica:  GROUP BY + Window Function para calcular participacao
-- -----------------------------------------------------------------------------
SELECT
    p.fabricante,
    COUNT(DISTINCT p.id) AS qtd_produtos,
    SUM(iv.quantidade) AS unidades_vendidas,
    SUM(iv.subtotal) AS faturamento,
    ROUND(
        100.0 * SUM(iv.subtotal) / SUM(SUM(iv.subtotal)) OVER (),
        2
    ) AS pct_faturamento
FROM produtos p
INNER JOIN itens_venda iv ON iv.produto_id = p.id
INNER JOIN vendas v ON iv.venda_id = v.id
WHERE v.status = 'CONCLUIDA'
GROUP BY p.fabricante
ORDER BY faturamento DESC;


-- -----------------------------------------------------------------------------
-- Q14 - Distribuicao de preco de venda por categoria (estatisticas)
-- -----------------------------------------------------------------------------
-- Objetivo: Estatisticas descritivas de precos por categoria.
-- Tecnica:  Funcoes de agregacao MIN, MAX, AVG, STDDEV
-- -----------------------------------------------------------------------------
SELECT
    c.nome AS categoria,
    COUNT(p.id) AS qtd_produtos,
    ROUND(MIN(p.preco_venda), 2) AS preco_min,
    ROUND(AVG(p.preco_venda), 2) AS preco_medio,
    ROUND(MAX(p.preco_venda), 2) AS preco_max,
    ROUND(STDDEV(p.preco_venda), 2) AS desvio_padrao
FROM categorias c
INNER JOIN produtos p ON p.categoria_id = c.id
WHERE p.ativo = TRUE
GROUP BY c.id, c.nome
ORDER BY preco_medio DESC;


-- #############################################################################
-- SECAO 3 - ANALISE DE CLIENTES (Q15 a Q18)
-- #############################################################################


-- -----------------------------------------------------------------------------
-- Q15 - Top 10 clientes por valor gasto
-- -----------------------------------------------------------------------------
-- Objetivo: Identificar os clientes de maior valor (Lifetime Value) para
--           acoes de retencao.
-- Tecnica:  JOIN + GROUP BY + LIMIT
-- -----------------------------------------------------------------------------
SELECT
    cl.id,
    cl.nome,
    cl.cidade,
    COUNT(v.id) AS total_compras,
    SUM(v.valor_total - v.desconto) AS total_gasto,
    ROUND(AVG(v.valor_total - v.desconto), 2) AS ticket_medio
FROM clientes cl
INNER JOIN vendas v ON v.cliente_id = cl.id
WHERE v.status = 'CONCLUIDA'
GROUP BY cl.id, cl.nome, cl.cidade
ORDER BY total_gasto DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- Q16 - Clientes inativos ha mais de 90 dias
-- -----------------------------------------------------------------------------
-- Objetivo: Identificar clientes para campanha de reativacao (RFM basico).
-- Tecnica:  Subconsulta com MAX + calculo de dias
-- -----------------------------------------------------------------------------
SELECT
    cl.id,
    cl.nome,
    cl.telefone,
    cl.email,
    MAX(v.data_venda)::DATE AS ultima_compra,
    CURRENT_DATE - MAX(v.data_venda)::DATE AS dias_inativo
FROM clientes cl
INNER JOIN vendas v ON v.cliente_id = cl.id
WHERE v.status = 'CONCLUIDA'
GROUP BY cl.id, cl.nome, cl.telefone, cl.email
HAVING CURRENT_DATE - MAX(v.data_venda)::DATE > 90
ORDER BY dias_inativo DESC
LIMIT 20;


-- -----------------------------------------------------------------------------
-- Q17 - Distribuicao de clientes por cidade
-- -----------------------------------------------------------------------------
-- Objetivo: Cobertura geografica da base de clientes.
-- Tecnica:  GROUP BY + calculo de percentual
-- -----------------------------------------------------------------------------
SELECT
    cidade,
    estado,
    COUNT(*) AS qtd_clientes,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentual
FROM clientes
GROUP BY cidade, estado
ORDER BY qtd_clientes DESC;


-- -----------------------------------------------------------------------------
-- Q18 - Faixa etaria dos clientes
-- -----------------------------------------------------------------------------
-- Objetivo: Segmentacao etaria da base de clientes.
-- Tecnica:  CASE + AGE + EXTRACT
-- -----------------------------------------------------------------------------
SELECT
    CASE
        WHEN EXTRACT(YEAR FROM AGE(data_nascimento)) < 25 THEN '1. Ate 24 anos'
        WHEN EXTRACT(YEAR FROM AGE(data_nascimento)) BETWEEN 25 AND 34 THEN '2. 25 a 34'
        WHEN EXTRACT(YEAR FROM AGE(data_nascimento)) BETWEEN 35 AND 44 THEN '3. 35 a 44'
        WHEN EXTRACT(YEAR FROM AGE(data_nascimento)) BETWEEN 45 AND 59 THEN '4. 45 a 59'
        ELSE '5. 60+ anos'
    END AS faixa_etaria,
    COUNT(*) AS qtd_clientes,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentual
FROM clientes
WHERE data_nascimento IS NOT NULL
GROUP BY 1
ORDER BY 1;


-- #############################################################################
-- SECAO 4 - ANALISE DE ESTOQUE (Q19 a Q21)
-- #############################################################################


-- -----------------------------------------------------------------------------
-- Q19 - Produtos com estoque critico (abaixo do minimo)
-- -----------------------------------------------------------------------------
-- Objetivo: Alerta operacional: produtos que precisam ser repostos.
-- Tecnica:  JOIN + comparacao com coluna referencial
-- -----------------------------------------------------------------------------
SELECT
    f.codigo AS filial,
    f.cidade,
    p.nome AS produto,
    e.quantidade AS estoque_atual,
    p.estoque_minimo,
    p.estoque_minimo - e.quantidade AS reposicao_necessaria
FROM estoque e
INNER JOIN produtos p ON e.produto_id = p.id
INNER JOIN filiais f ON e.filial_id = f.id
WHERE e.quantidade < p.estoque_minimo
  AND p.ativo = TRUE
ORDER BY reposicao_necessaria DESC, f.codigo;


-- -----------------------------------------------------------------------------
-- Q20 - Valor total do estoque por filial
-- -----------------------------------------------------------------------------
-- Objetivo: Valor imobilizado em estoque em cada filial (preco de custo).
-- Tecnica:  JOIN + SUM ponderado
-- -----------------------------------------------------------------------------
SELECT
    f.codigo,
    f.nome,
    f.cidade,
    SUM(e.quantidade) AS total_unidades,
    ROUND(SUM(e.quantidade * p.preco_custo), 2) AS valor_estoque_custo,
    ROUND(SUM(e.quantidade * p.preco_venda), 2) AS valor_estoque_venda
FROM estoque e
INNER JOIN filiais f ON e.filial_id = f.id
INNER JOIN produtos p ON e.produto_id = p.id
GROUP BY f.id, f.codigo, f.nome, f.cidade
ORDER BY valor_estoque_custo DESC;


-- -----------------------------------------------------------------------------
-- Q21 - Cobertura de estoque (dias de venda restantes)
-- -----------------------------------------------------------------------------
-- Objetivo: Estimar quantos dias o estoque atual dura para cada produto,
--           com base na media de vendas diarias dos ultimos 90 dias.
-- Tecnica:  CTE + Subconsulta + calculo de razao
-- -----------------------------------------------------------------------------
WITH vendas_recentes AS (
    SELECT
        iv.produto_id,
        SUM(iv.quantidade) * 1.0 / 90 AS media_diaria
    FROM itens_venda iv
    INNER JOIN vendas v ON iv.venda_id = v.id
    WHERE v.status = 'CONCLUIDA'
      AND v.data_venda >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY iv.produto_id
),
estoque_total AS (
    SELECT
        produto_id,
        SUM(quantidade) AS estoque_rede
    FROM estoque
    GROUP BY produto_id
)
SELECT
    p.nome,
    et.estoque_rede,
    ROUND(vr.media_diaria::NUMERIC, 2) AS media_venda_diaria,
    CASE
        WHEN vr.media_diaria > 0
        THEN ROUND(et.estoque_rede / vr.media_diaria::NUMERIC, 0)
        ELSE NULL
    END AS dias_de_cobertura
FROM produtos p
INNER JOIN estoque_total et ON et.produto_id = p.id
LEFT JOIN vendas_recentes vr ON vr.produto_id = p.id
WHERE p.ativo = TRUE
  AND vr.media_diaria > 0
ORDER BY dias_de_cobertura ASC NULLS LAST
LIMIT 20;


-- #############################################################################
-- SECAO 5 - ANALISES AVANCADAS (Q22 a Q25)
-- #############################################################################


-- -----------------------------------------------------------------------------
-- Q22 - Ranking de filiais por mes (Window Function)
-- -----------------------------------------------------------------------------
-- Objetivo: Como cada filial se posicionou no ranking em cada mes? Ideal
--           para acompanhar performance.
-- Tecnica:  Window Function RANK() com PARTITION BY
-- -----------------------------------------------------------------------------
WITH fat_mensal AS (
    SELECT
        TO_CHAR(v.data_venda, 'YYYY-MM') AS mes_ano,
        f.codigo,
        f.nome AS filial,
        SUM(v.valor_total - v.desconto) AS faturamento
    FROM vendas v
    INNER JOIN filiais f ON v.filial_id = f.id
    WHERE v.status = 'CONCLUIDA'
    GROUP BY TO_CHAR(v.data_venda, 'YYYY-MM'), f.id, f.codigo, f.nome
)
SELECT
    mes_ano,
    codigo,
    filial,
    faturamento,
    RANK() OVER (PARTITION BY mes_ano ORDER BY faturamento DESC) AS ranking
FROM fat_mensal
WHERE mes_ano >= TO_CHAR(CURRENT_DATE - INTERVAL '6 months', 'YYYY-MM')
ORDER BY mes_ano DESC, ranking;


-- -----------------------------------------------------------------------------
-- Q23 - Crescimento mes a mes (comparativo com mes anterior)
-- -----------------------------------------------------------------------------
-- Objetivo: Analise de crescimento MoM (Month over Month).
-- Tecnica:  CTE + Window Function LAG() para pegar valor do mes anterior
-- -----------------------------------------------------------------------------
WITH fat_mensal AS (
    SELECT
        DATE_TRUNC('month', data_venda)::DATE AS mes,
        SUM(valor_total - desconto) AS faturamento
    FROM vendas
    WHERE status = 'CONCLUIDA'
    GROUP BY DATE_TRUNC('month', data_venda)
)
SELECT
    TO_CHAR(mes, 'YYYY-MM') AS mes_ano,
    faturamento,
    LAG(faturamento) OVER (ORDER BY mes) AS faturamento_mes_anterior,
    faturamento - LAG(faturamento) OVER (ORDER BY mes) AS variacao_absoluta,
    ROUND(
        100.0 * (faturamento - LAG(faturamento) OVER (ORDER BY mes))
              / NULLIF(LAG(faturamento) OVER (ORDER BY mes), 0),
        2
    ) AS crescimento_pct
FROM fat_mensal
ORDER BY mes;


-- -----------------------------------------------------------------------------
-- Q24 - Media movel de 3 meses do faturamento
-- -----------------------------------------------------------------------------
-- Objetivo: Suavizar oscilacoes mensais e identificar tendencia real.
-- Tecnica:  Window Function AVG com ROWS BETWEEN
-- -----------------------------------------------------------------------------
WITH fat_mensal AS (
    SELECT
        DATE_TRUNC('month', data_venda)::DATE AS mes,
        SUM(valor_total - desconto) AS faturamento
    FROM vendas
    WHERE status = 'CONCLUIDA'
    GROUP BY DATE_TRUNC('month', data_venda)
)
SELECT
    TO_CHAR(mes, 'YYYY-MM') AS mes_ano,
    faturamento,
    ROUND(
        AVG(faturamento) OVER (
            ORDER BY mes
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS media_movel_3m
FROM fat_mensal
ORDER BY mes;


-- -----------------------------------------------------------------------------
-- Q25 - Analise de cesta: produtos frequentemente vendidos juntos
-- -----------------------------------------------------------------------------
-- Objetivo: Identificar pares de produtos que mais aparecem na mesma venda
--           (base para cross-sell / posicionamento na loja).
-- Tecnica:  Self-join da tabela itens_venda + agrupamento por par
-- -----------------------------------------------------------------------------
SELECT
    p1.nome AS produto_a,
    p2.nome AS produto_b,
    COUNT(*) AS vendas_juntos
FROM itens_venda iv1
INNER JOIN itens_venda iv2 ON iv1.venda_id = iv2.venda_id
                          AND iv1.produto_id < iv2.produto_id
INNER JOIN produtos p1 ON iv1.produto_id = p1.id
INNER JOIN produtos p2 ON iv2.produto_id = p2.id
INNER JOIN vendas v ON iv1.venda_id = v.id
WHERE v.status = 'CONCLUIDA'
GROUP BY p1.id, p1.nome, p2.id, p2.nome
HAVING COUNT(*) >= 3
ORDER BY vendas_juntos DESC
LIMIT 15;


-- =============================================================================
-- FIM DAS CONSULTAS
-- =============================================================================
-- Total de consultas: 25
-- Distribuicao:
--   Secao 1 - Vendas:            7 consultas (Q01 a Q07)
--   Secao 2 - Produtos:          7 consultas (Q08 a Q14)
--   Secao 3 - Clientes:          4 consultas (Q15 a Q18)
--   Secao 4 - Estoque:           3 consultas (Q19 a Q21)
--   Secao 5 - Analises Avancadas: 4 consultas (Q22 a Q25)
--
-- Tecnicas SQL demonstradas:
--   - JOINs (INNER, LEFT)
--   - GROUP BY, HAVING
--   - Subconsultas e CTEs (WITH)
--   - Window Functions (RANK, LAG, AVG com ROWS BETWEEN)
--   - Funcoes de data (EXTRACT, DATE_TRUNC, TO_CHAR, AGE)
--   - Agregacoes estatisticas (AVG, STDDEV, MIN, MAX)
--   - CASE WHEN
--   - Anti-join com LEFT JOIN + IS NULL
--   - Filtragem condicional com FILTER
--   - Self-join
-- =============================================================================
