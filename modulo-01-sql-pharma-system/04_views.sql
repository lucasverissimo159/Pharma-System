-- =============================================================================
-- PharmaSystem - Views para Consultas Frequentes
-- Modulo 01 - Semana 1 do Portfolio
-- =============================================================================
-- Autor: Lucas Verissimo
-- SGBD: PostgreSQL 13+
-- Descricao: Views (visoes materializadas logicamente) para simplificar as
--            consultas mais usadas em relatorios e dashboards.
-- =============================================================================


-- -----------------------------------------------------------------------------
-- VIEW: vw_faturamento_mensal
-- Descricao: Faturamento agregado por mes com metricas basicas.
-- Uso tipico: Serie temporal para dashboard executivo.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_faturamento_mensal AS
SELECT
    TO_CHAR(v.data_venda, 'YYYY-MM')            AS mes_ano,
    EXTRACT(YEAR FROM v.data_venda)::INTEGER    AS ano,
    EXTRACT(MONTH FROM v.data_venda)::INTEGER   AS mes,
    COUNT(v.id)                                 AS total_vendas,
    SUM(v.valor_total - v.desconto)             AS faturamento_liquido,
    SUM(v.valor_total)                          AS faturamento_bruto,
    SUM(v.desconto)                             AS total_descontos,
    ROUND(AVG(v.valor_total - v.desconto), 2)   AS ticket_medio
FROM vendas v
WHERE v.status = 'CONCLUIDA'
GROUP BY TO_CHAR(v.data_venda, 'YYYY-MM'),
         EXTRACT(YEAR FROM v.data_venda),
         EXTRACT(MONTH FROM v.data_venda);

COMMENT ON VIEW vw_faturamento_mensal IS
    'Faturamento mensal consolidado da rede (apenas vendas concluidas)';


-- -----------------------------------------------------------------------------
-- VIEW: vw_ranking_produtos
-- Descricao: Ranking completo de produtos por faturamento e quantidade.
-- Uso tipico: Analise de portifolio, decisoes de compra.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_ranking_produtos AS
SELECT
    p.id                                         AS produto_id,
    p.nome                                       AS produto,
    c.nome                                       AS categoria,
    p.fabricante,
    p.preco_venda,
    COALESCE(SUM(iv.quantidade), 0)              AS unidades_vendidas,
    COALESCE(SUM(iv.subtotal), 0)                AS faturamento_produto,
    COALESCE(COUNT(DISTINCT iv.venda_id), 0)     AS vendas_participadas,
    RANK() OVER (
        ORDER BY COALESCE(SUM(iv.subtotal), 0) DESC
    )                                            AS ranking_faturamento,
    RANK() OVER (
        ORDER BY COALESCE(SUM(iv.quantidade), 0) DESC
    )                                            AS ranking_quantidade
FROM produtos p
INNER JOIN categorias c ON p.categoria_id = c.id
LEFT JOIN itens_venda iv ON iv.produto_id = p.id
LEFT JOIN vendas v ON iv.venda_id = v.id AND v.status = 'CONCLUIDA'
WHERE p.ativo = TRUE
GROUP BY p.id, p.nome, c.nome, p.fabricante, p.preco_venda;

COMMENT ON VIEW vw_ranking_produtos IS
    'Ranking de produtos com posicao por faturamento e quantidade vendida';


-- -----------------------------------------------------------------------------
-- VIEW: vw_ranking_filiais
-- Descricao: Ranking de filiais com metricas principais consolidadas.
-- Uso tipico: Dashboard gerencial, comparativo de performance.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_ranking_filiais AS
SELECT
    f.id                                                 AS filial_id,
    f.codigo,
    f.nome                                               AS filial,
    f.cidade,
    f.estado,
    f.data_abertura,
    COUNT(v.id) FILTER (WHERE v.status = 'CONCLUIDA')    AS vendas_concluidas,
    COUNT(v.id) FILTER (WHERE v.status = 'CANCELADA')    AS vendas_canceladas,
    COALESCE(
        SUM(v.valor_total - v.desconto)
        FILTER (WHERE v.status = 'CONCLUIDA'),
        0
    )                                                    AS faturamento_liquido,
    COALESCE(
        ROUND(AVG(v.valor_total - v.desconto)
        FILTER (WHERE v.status = 'CONCLUIDA'), 2),
        0
    )                                                    AS ticket_medio,
    RANK() OVER (
        ORDER BY COALESCE(
            SUM(v.valor_total - v.desconto)
            FILTER (WHERE v.status = 'CONCLUIDA'),
            0
        ) DESC
    )                                                    AS ranking
FROM filiais f
LEFT JOIN vendas v ON v.filial_id = f.id
WHERE f.ativa = TRUE
GROUP BY f.id, f.codigo, f.nome, f.cidade, f.estado, f.data_abertura;

COMMENT ON VIEW vw_ranking_filiais IS
    'Ranking consolidado de filiais com KPIs principais';


-- -----------------------------------------------------------------------------
-- VIEW: vw_clientes_top
-- Descricao: Top clientes com metricas de Lifetime Value e recencia.
-- Uso tipico: CRM, campanhas de retencao, segmentacao.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_clientes_top AS
SELECT
    cl.id                                        AS cliente_id,
    cl.nome                                      AS cliente,
    cl.cidade,
    cl.telefone,
    cl.email,
    COUNT(v.id)                                  AS total_compras,
    SUM(v.valor_total - v.desconto)              AS lifetime_value,
    ROUND(AVG(v.valor_total - v.desconto), 2)    AS ticket_medio,
    MIN(v.data_venda)::DATE                      AS primeira_compra,
    MAX(v.data_venda)::DATE                      AS ultima_compra,
    (CURRENT_DATE - MAX(v.data_venda)::DATE)     AS dias_desde_ultima_compra
FROM clientes cl
INNER JOIN vendas v ON v.cliente_id = cl.id
WHERE v.status = 'CONCLUIDA'
GROUP BY cl.id, cl.nome, cl.cidade, cl.telefone, cl.email;

COMMENT ON VIEW vw_clientes_top IS
    'Clientes com metricas de valor e comportamento (base para CRM)';


-- -----------------------------------------------------------------------------
-- VIEW: vw_estoque_critico
-- Descricao: Produtos com estoque abaixo do minimo em cada filial.
-- Uso tipico: Alertas operacionais para reposicao.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_estoque_critico AS
SELECT
    f.codigo                                    AS codigo_filial,
    f.nome                                      AS filial,
    f.cidade,
    p.id                                        AS produto_id,
    p.nome                                      AS produto,
    c.nome                                      AS categoria,
    e.quantidade                                AS estoque_atual,
    p.estoque_minimo,
    (p.estoque_minimo - e.quantidade)           AS reposicao_sugerida,
    ROUND(
        (p.estoque_minimo - e.quantidade) * p.preco_custo,
        2
    )                                           AS valor_reposicao,
    p.exige_receita
FROM estoque e
INNER JOIN produtos p ON e.produto_id = p.id
INNER JOIN filiais f ON e.filial_id = f.id
INNER JOIN categorias c ON p.categoria_id = c.id
WHERE e.quantidade < p.estoque_minimo
  AND p.ativo = TRUE
  AND f.ativa = TRUE;

COMMENT ON VIEW vw_estoque_critico IS
    'Alerta de produtos com estoque abaixo do minimo por filial';


-- =============================================================================
-- EXEMPLOS DE USO DAS VIEWS
-- =============================================================================
-- Consultar as 5 melhores filiais rapidamente:
-- SELECT * FROM vw_ranking_filiais LIMIT 5;
--
-- Ver top 10 produtos:
-- SELECT * FROM vw_ranking_produtos ORDER BY ranking_faturamento LIMIT 10;
--
-- Ver clientes que nao compram ha mais de 60 dias:
-- SELECT * FROM vw_clientes_top WHERE dias_desde_ultima_compra > 60;
--
-- Ver evolucao mensal do ultimo ano:
-- SELECT * FROM vw_faturamento_mensal
-- WHERE ano = EXTRACT(YEAR FROM CURRENT_DATE)::INTEGER
-- ORDER BY mes;
--
-- Ver alertas de estoque de uma filial especifica:
-- SELECT * FROM vw_estoque_critico WHERE codigo_filial = 'FIL001';
-- =============================================================================
