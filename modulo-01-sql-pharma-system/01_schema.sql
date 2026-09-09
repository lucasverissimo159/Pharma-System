-- =============================================================================
-- PharmaSystem - Sistema de Gestao para Rede de Farmacias
-- Modulo 01 - Modelagem do Banco de Dados
-- =============================================================================
-- Autor: Lucas Verissimo
-- SGBD: PostgreSQL 13+
-- Descricao: Script de criacao das tabelas, constraints e indices do sistema
-- =============================================================================

-- Remove o banco caso ja exista (executar como superusuario)
-- DROP DATABASE IF EXISTS pharma_system;
-- CREATE DATABASE pharma_system;
-- \c pharma_system;

-- =============================================================================
-- LIMPEZA - Remove tabelas caso ja existam (ordem inversa das dependencias)
-- =============================================================================
DROP VIEW IF EXISTS vw_estoque_critico CASCADE;
DROP VIEW IF EXISTS vw_clientes_top CASCADE;
DROP VIEW IF EXISTS vw_ranking_filiais CASCADE;
DROP VIEW IF EXISTS vw_ranking_produtos CASCADE;
DROP VIEW IF EXISTS vw_faturamento_mensal CASCADE;

DROP TABLE IF EXISTS itens_venda CASCADE;
DROP TABLE IF EXISTS vendas CASCADE;
DROP TABLE IF EXISTS estoque CASCADE;
DROP TABLE IF EXISTS produtos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS filiais CASCADE;

-- =============================================================================
-- TABELA: filiais
-- Descricao: Cadastro das filiais da rede de farmacias
-- =============================================================================
CREATE TABLE filiais (
    id              SERIAL PRIMARY KEY,
    codigo          VARCHAR(10) NOT NULL UNIQUE,
    nome            VARCHAR(100) NOT NULL,
    cidade          VARCHAR(80) NOT NULL,
    estado          CHAR(2) NOT NULL,
    endereco        VARCHAR(200),
    telefone        VARCHAR(20),
    data_abertura   DATE NOT NULL,
    ativa           BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_filiais_estado CHECK (estado ~ '^[A-Z]{2}$')
);

COMMENT ON TABLE filiais IS 'Cadastro das filiais da rede de farmacias';
COMMENT ON COLUMN filiais.codigo IS 'Codigo interno da filial (ex: FIL001)';
COMMENT ON COLUMN filiais.estado IS 'UF em duas letras maiusculas';

-- =============================================================================
-- TABELA: categorias
-- Descricao: Categorias de produtos (medicamentos, higiene, cosmeticos, etc)
-- =============================================================================
CREATE TABLE categorias (
    id              SERIAL PRIMARY KEY,
    nome            VARCHAR(80) NOT NULL UNIQUE,
    descricao       TEXT,
    data_criacao    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE categorias IS 'Categorias de produtos comercializados';

-- =============================================================================
-- TABELA: produtos
-- Descricao: Catalogo de produtos vendidos nas farmacias
-- =============================================================================
CREATE TABLE produtos (
    id              SERIAL PRIMARY KEY,
    codigo_barras   VARCHAR(20) UNIQUE,
    nome            VARCHAR(150) NOT NULL,
    categoria_id    INTEGER NOT NULL,
    fabricante      VARCHAR(100),
    preco_custo     DECIMAL(10, 2) NOT NULL,
    preco_venda     DECIMAL(10, 2) NOT NULL,
    estoque_minimo  INTEGER NOT NULL DEFAULT 10,
    exige_receita   BOOLEAN NOT NULL DEFAULT FALSE,
    ativo           BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_produtos_categoria FOREIGN KEY (categoria_id)
        REFERENCES categorias(id) ON DELETE RESTRICT,
    CONSTRAINT chk_produtos_preco_custo CHECK (preco_custo >= 0),
    CONSTRAINT chk_produtos_preco_venda CHECK (preco_venda >= 0),
    CONSTRAINT chk_produtos_margem CHECK (preco_venda >= preco_custo),
    CONSTRAINT chk_produtos_estoque_min CHECK (estoque_minimo >= 0)
);

COMMENT ON TABLE produtos IS 'Catalogo de produtos comercializados';
COMMENT ON COLUMN produtos.exige_receita IS 'Indica se o produto exige receita medica';

-- =============================================================================
-- TABELA: estoque
-- Descricao: Controle de estoque por produto e filial
-- =============================================================================
CREATE TABLE estoque (
    id                  SERIAL PRIMARY KEY,
    produto_id          INTEGER NOT NULL,
    filial_id           INTEGER NOT NULL,
    quantidade          INTEGER NOT NULL DEFAULT 0,
    data_atualizacao    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_estoque_produto FOREIGN KEY (produto_id)
        REFERENCES produtos(id) ON DELETE CASCADE,
    CONSTRAINT fk_estoque_filial FOREIGN KEY (filial_id)
        REFERENCES filiais(id) ON DELETE CASCADE,
    CONSTRAINT uk_estoque_produto_filial UNIQUE (produto_id, filial_id),
    CONSTRAINT chk_estoque_quantidade CHECK (quantidade >= 0)
);

COMMENT ON TABLE estoque IS 'Controle de estoque por produto e filial';

-- =============================================================================
-- TABELA: clientes
-- Descricao: Cadastro de clientes da rede
-- =============================================================================
CREATE TABLE clientes (
    id              SERIAL PRIMARY KEY,
    nome            VARCHAR(150) NOT NULL,
    cpf             VARCHAR(14) UNIQUE,
    email           VARCHAR(120),
    telefone        VARCHAR(20),
    data_nascimento DATE,
    cidade          VARCHAR(80),
    estado          CHAR(2),
    data_cadastro   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_clientes_cpf CHECK (cpf IS NULL OR cpf ~ '^\d{3}\.\d{3}\.\d{3}-\d{2}$'),
    CONSTRAINT chk_clientes_estado CHECK (estado IS NULL OR estado ~ '^[A-Z]{2}$')
);

COMMENT ON TABLE clientes IS 'Cadastro de clientes da rede de farmacias';

-- =============================================================================
-- TABELA: vendas
-- Descricao: Registro de vendas realizadas
-- =============================================================================
CREATE TABLE vendas (
    id                  SERIAL PRIMARY KEY,
    filial_id           INTEGER NOT NULL,
    cliente_id          INTEGER,
    data_venda          TIMESTAMP NOT NULL,
    valor_total         DECIMAL(10, 2) NOT NULL,
    desconto            DECIMAL(10, 2) NOT NULL DEFAULT 0,
    forma_pagamento     VARCHAR(20) NOT NULL,
    status              VARCHAR(20) NOT NULL DEFAULT 'CONCLUIDA',
    data_criacao        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_vendas_filial FOREIGN KEY (filial_id)
        REFERENCES filiais(id) ON DELETE RESTRICT,
    CONSTRAINT fk_vendas_cliente FOREIGN KEY (cliente_id)
        REFERENCES clientes(id) ON DELETE SET NULL,
    CONSTRAINT chk_vendas_valor CHECK (valor_total >= 0),
    CONSTRAINT chk_vendas_desconto CHECK (desconto >= 0),
    CONSTRAINT chk_vendas_forma_pgto CHECK (forma_pagamento IN
        ('DINHEIRO', 'CARTAO_CREDITO', 'CARTAO_DEBITO', 'PIX', 'CONVENIO')),
    CONSTRAINT chk_vendas_status CHECK (status IN
        ('CONCLUIDA', 'CANCELADA', 'PENDENTE'))
);

COMMENT ON TABLE vendas IS 'Registro de todas as vendas realizadas';
COMMENT ON COLUMN vendas.cliente_id IS 'Pode ser NULL para vendas sem identificacao do cliente';

-- =============================================================================
-- TABELA: itens_venda
-- Descricao: Itens individuais de cada venda
-- =============================================================================
CREATE TABLE itens_venda (
    id              SERIAL PRIMARY KEY,
    venda_id        INTEGER NOT NULL,
    produto_id      INTEGER NOT NULL,
    quantidade      INTEGER NOT NULL,
    preco_unitario  DECIMAL(10, 2) NOT NULL,
    subtotal        DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_itens_venda_venda FOREIGN KEY (venda_id)
        REFERENCES vendas(id) ON DELETE CASCADE,
    CONSTRAINT fk_itens_venda_produto FOREIGN KEY (produto_id)
        REFERENCES produtos(id) ON DELETE RESTRICT,
    CONSTRAINT chk_itens_venda_qtd CHECK (quantidade > 0),
    CONSTRAINT chk_itens_venda_preco CHECK (preco_unitario >= 0),
    CONSTRAINT chk_itens_venda_subtotal CHECK (subtotal >= 0)
);

COMMENT ON TABLE itens_venda IS 'Itens individuais que compoem cada venda';

-- =============================================================================
-- INDICES para otimizacao de consultas
-- =============================================================================
CREATE INDEX idx_vendas_data ON vendas(data_venda);
CREATE INDEX idx_vendas_filial ON vendas(filial_id);
CREATE INDEX idx_vendas_cliente ON vendas(cliente_id);
CREATE INDEX idx_vendas_status ON vendas(status);
CREATE INDEX idx_itens_venda_produto ON itens_venda(produto_id);
CREATE INDEX idx_itens_venda_venda ON itens_venda(venda_id);
CREATE INDEX idx_produtos_categoria ON produtos(categoria_id);
CREATE INDEX idx_produtos_ativo ON produtos(ativo);
CREATE INDEX idx_estoque_filial ON estoque(filial_id);
CREATE INDEX idx_clientes_cidade ON clientes(cidade);

-- =============================================================================
-- FIM DO SCHEMA
-- =============================================================================
-- Total de tabelas criadas: 7
-- Total de indices criados: 10
-- Proximo passo: executar 02_inserts.sql para popular o banco
-- =============================================================================
