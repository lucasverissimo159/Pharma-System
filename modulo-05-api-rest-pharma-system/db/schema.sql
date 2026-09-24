-- =============================================================================
-- Schema do banco de dados PharmaSystem — SQLite
-- =============================================================================
-- Sete tabelas normalizadas (Star Schema simplificado):
--   Dimensoes: filiais, categorias, produtos, clientes
--   Fatos:     vendas, itens_venda, estoque
-- =============================================================================

DROP TABLE IF EXISTS itens_venda;
DROP TABLE IF EXISTS vendas;
DROP TABLE IF EXISTS estoque;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS filiais;


-- =============================================================================
-- FILIAIS
-- =============================================================================
CREATE TABLE filiais (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo         TEXT    UNIQUE NOT NULL,
    nome           TEXT    NOT NULL,
    cidade         TEXT    NOT NULL,
    estado         TEXT    NOT NULL,
    endereco       TEXT,
    telefone       TEXT,
    data_abertura  TEXT,
    ativa          INTEGER NOT NULL DEFAULT 1  CHECK (ativa IN (0, 1))
);

CREATE INDEX idx_filiais_cidade  ON filiais (cidade);
CREATE INDEX idx_filiais_estado  ON filiais (estado);


-- =============================================================================
-- CATEGORIAS
-- =============================================================================
CREATE TABLE categorias (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT    UNIQUE NOT NULL,
    descricao  TEXT
);


-- =============================================================================
-- PRODUTOS
-- =============================================================================
CREATE TABLE produtos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_barras   TEXT    UNIQUE NOT NULL,
    nome            TEXT    NOT NULL,
    categoria_id    INTEGER NOT NULL,
    fabricante      TEXT,
    preco_custo     REAL    NOT NULL  CHECK (preco_custo >= 0),
    preco_venda     REAL    NOT NULL  CHECK (preco_venda > 0),
    estoque_minimo  INTEGER NOT NULL DEFAULT 0,
    exige_receita   INTEGER NOT NULL DEFAULT 0  CHECK (exige_receita IN (0, 1)),
    ativo           INTEGER NOT NULL DEFAULT 1  CHECK (ativo IN (0, 1)),
    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
);

CREATE INDEX idx_produtos_categoria    ON produtos (categoria_id);
CREATE INDEX idx_produtos_ativo        ON produtos (ativo);
CREATE INDEX idx_produtos_codigo_barras ON produtos (codigo_barras);


-- =============================================================================
-- CLIENTES
-- =============================================================================
CREATE TABLE clientes (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    nome               TEXT    NOT NULL,
    cpf                TEXT    UNIQUE,
    email              TEXT,
    telefone           TEXT,
    data_nascimento    TEXT,
    cidade             TEXT,
    estado             TEXT,
    data_cadastro      TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clientes_cpf     ON clientes (cpf);
CREATE INDEX idx_clientes_cidade  ON clientes (cidade);


-- =============================================================================
-- ESTOQUE
-- =============================================================================
CREATE TABLE estoque (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id   INTEGER NOT NULL,
    filial_id    INTEGER NOT NULL,
    quantidade   INTEGER NOT NULL DEFAULT 0  CHECK (quantidade >= 0),
    FOREIGN KEY (produto_id) REFERENCES produtos (id),
    FOREIGN KEY (filial_id)  REFERENCES filiais (id),
    UNIQUE (produto_id, filial_id)
);


-- =============================================================================
-- VENDAS
-- =============================================================================
CREATE TABLE vendas (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    filial_id        INTEGER NOT NULL,
    cliente_id       INTEGER,
    data_venda       TEXT    NOT NULL,
    valor_total      REAL    NOT NULL  CHECK (valor_total >= 0),
    desconto         REAL    NOT NULL DEFAULT 0  CHECK (desconto >= 0),
    forma_pagamento  TEXT    NOT NULL,
    status           TEXT    NOT NULL DEFAULT 'CONCLUIDA'
                     CHECK (status IN ('CONCLUIDA', 'CANCELADA', 'PENDENTE')),
    FOREIGN KEY (filial_id)  REFERENCES filiais (id),
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
);

CREATE INDEX idx_vendas_filial  ON vendas (filial_id);
CREATE INDEX idx_vendas_cliente ON vendas (cliente_id);
CREATE INDEX idx_vendas_data    ON vendas (data_venda);
CREATE INDEX idx_vendas_status  ON vendas (status);


-- =============================================================================
-- ITENS_VENDA
-- =============================================================================
CREATE TABLE itens_venda (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id        INTEGER NOT NULL,
    produto_id      INTEGER NOT NULL,
    quantidade      INTEGER NOT NULL  CHECK (quantidade > 0),
    preco_unitario  REAL    NOT NULL  CHECK (preco_unitario > 0),
    subtotal        REAL    NOT NULL  CHECK (subtotal >= 0),
    FOREIGN KEY (venda_id)   REFERENCES vendas (id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
);

CREATE INDEX idx_itens_venda ON itens_venda (venda_id);
