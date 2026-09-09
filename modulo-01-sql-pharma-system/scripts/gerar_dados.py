"""
Gerador de dados sinteticos para o PharmaSystem.
Produz o arquivo 02_inserts.sql com dados realistas para uma rede de farmacias.

Autor: Lucas Verissimo
Uso: python gerar_dados.py
"""

import random
from datetime import datetime, timedelta, date

# Semente fixa para dados reproduziveis
random.seed(42)

# =============================================================================
# CONFIGURACAO
# =============================================================================
NUM_CLIENTES = 200
NUM_VENDAS = 1500
DATA_INICIO = date(2024, 1, 1)
DATA_FIM = date(2026, 6, 30)

# =============================================================================
# DADOS BASE
# =============================================================================

FILIAIS = [
    ('FIL001', 'PharmaMinas Centro Montes Claros',   'Montes Claros',    'MG', 'Av. Cula Mangabeira, 1200',   '(38) 3221-1001', '2015-03-10'),
    ('FIL002', 'PharmaMinas Todos os Santos',        'Montes Claros',    'MG', 'Rua Correia Machado, 890',    '(38) 3221-1002', '2016-07-22'),
    ('FIL003', 'PharmaMinas Ibituruna',              'Montes Claros',    'MG', 'Av. Deputado Esteves, 450',   '(38) 3221-1003', '2017-05-15'),
    ('FIL004', 'PharmaMinas Major Prates',           'Montes Claros',    'MG', 'Av. Mestra Fininha, 1500',    '(38) 3221-1004', '2018-11-08'),
    ('FIL005', 'PharmaMinas Bocaiuva',               'Bocaiuva',         'MG', 'Praca da Matriz, 100',        '(38) 3251-2001', '2018-02-14'),
    ('FIL006', 'PharmaMinas Janauba',                'Janauba',          'MG', 'Rua Bias Fortes, 350',        '(38) 3821-3001', '2019-04-30'),
    ('FIL007', 'PharmaMinas Salinas',                'Salinas',          'MG', 'Av. Rio Branco, 800',         '(38) 3841-4001', '2019-08-12'),
    ('FIL008', 'PharmaMinas Pirapora',               'Pirapora',         'MG', 'Praca Melo Viana, 200',       '(38) 3741-5001', '2020-01-20'),
    ('FIL009', 'PharmaMinas Belo Horizonte Savassi', 'Belo Horizonte',   'MG', 'Rua Pernambuco, 1120',        '(31) 3221-6001', '2020-06-05'),
    ('FIL010', 'PharmaMinas Uberlandia Centro',      'Uberlandia',       'MG', 'Av. Afonso Pena, 2500',       '(34) 3221-7001', '2021-03-18'),
    ('FIL011', 'PharmaMinas Diamantina',             'Diamantina',       'MG', 'Rua da Quitanda, 45',         '(38) 3531-8001', '2021-09-22'),
    ('FIL012', 'PharmaMinas Grao Mogol',             'Grao Mogol',       'MG', 'Praca Central, 15',           '(38) 3238-9001', '2022-02-10'),
    ('FIL013', 'PharmaMinas Buritizeiro',            'Buritizeiro',      'MG', 'Rua Sao Francisco, 220',      '(38) 3742-1101', '2022-08-15'),
    ('FIL014', 'PharmaMinas Corinto',                'Corinto',          'MG', 'Av. Getulio Vargas, 600',     '(38) 3751-1201', '2023-05-20'),
    ('FIL015', 'PharmaMinas Curvelo',                'Curvelo',          'MG', 'Rua Coronel Prates, 340',     '(38) 3721-1301', '2024-01-15'),
]

CATEGORIAS = [
    ('Medicamentos Genericos',      'Medicamentos genericos com principio ativo comprovado'),
    ('Medicamentos de Referencia',  'Medicamentos de marca original com patente'),
    ('Medicamentos Similares',      'Medicamentos similares aos de referencia'),
    ('Higiene Pessoal',             'Produtos de higiene e cuidado pessoal'),
    ('Cosmeticos',                  'Produtos de beleza e cosmeticos'),
    ('Dermocosmeticos',             'Cosmeticos com finalidade dermatologica'),
    ('Suplementos Alimentares',     'Vitaminas, minerais e suplementos'),
    ('Infantil',                    'Produtos para bebes e criancas'),
    ('Perfumaria',                  'Perfumes e fragrancias'),
    ('Primeiros Socorros',          'Materiais de curativo e primeiros socorros'),
]

# (codigo_barras, nome, categoria_id, fabricante, preco_custo, preco_venda, estoque_min, exige_receita)
PRODUTOS = [
    # Medicamentos Genericos
    ('7891234000101', 'Dipirona Sodica 500mg 20 comprimidos',        1, 'EMS',           4.20,  8.90,  20, False),
    ('7891234000102', 'Paracetamol 750mg 20 comprimidos',            1, 'Medley',        5.10,  10.50, 20, False),
    ('7891234000103', 'Ibuprofeno 400mg 20 comprimidos',             1, 'Neo Quimica',   6.30,  13.20, 15, False),
    ('7891234000104', 'Omeprazol 20mg 28 capsulas',                  1, 'EMS',           7.80,  16.90, 15, False),
    ('7891234000105', 'Amoxicilina 500mg 21 capsulas',               1, 'Medley',        18.50, 39.90, 10, True),
    ('7891234000106', 'Losartana Potassica 50mg 30 comprimidos',     1, 'EMS',           9.20,  19.80, 20, True),
    ('7891234000107', 'Metformina 850mg 30 comprimidos',             1, 'Neo Quimica',   8.10,  17.50, 15, True),
    ('7891234000108', 'Sinvastatina 20mg 30 comprimidos',            1, 'EMS',           12.40, 27.90, 15, True),
    ('7891234000109', 'Captopril 25mg 30 comprimidos',               1, 'Medley',        4.80,  10.20, 20, True),
    ('7891234000110', 'Sertralina 50mg 30 comprimidos',              1, 'Eurofarma',     22.50, 49.90, 10, True),

    # Medicamentos de Referencia
    ('7891234000201', 'Dorflex 30 comprimidos',                      2, 'Sanofi',        11.20, 24.50, 15, False),
    ('7891234000202', 'Tylenol 750mg 20 comprimidos',                2, 'Janssen',       14.80, 32.90, 15, False),
    ('7891234000203', 'Advil 400mg 20 comprimidos',                  2, 'Pfizer',        18.20, 39.80, 10, False),
    ('7891234000204', 'Losec 20mg 28 capsulas',                      2, 'AstraZeneca',   28.50, 62.90, 10, False),
    ('7891234000205', 'Cataflam 50mg 20 comprimidos',                2, 'Novartis',      16.40, 35.90, 15, False),
    ('7891234000206', 'Voltaren Emulgel 60g',                        2, 'Novartis',      21.80, 47.50, 12, False),
    ('7891234000207', 'Neosaldina 30 drageas',                       2, 'Takeda',        13.90, 29.90, 15, False),
    ('7891234000208', 'Buscopan Composto 20 comprimidos',            2, 'Sanofi',        15.60, 33.80, 12, False),

    # Medicamentos Similares
    ('7891234000301', 'Cimegripe 24 capsulas',                       3, 'Cimed',         8.90,  19.50, 15, False),
    ('7891234000302', 'Multigrip 20 capsulas',                       3, 'EMS',           7.80,  17.20, 15, False),
    ('7891234000303', 'Naldecon 12 comprimidos',                     3, 'Bristol',       9.40,  20.90, 12, False),
    ('7891234000304', 'Coristina D Pro 20 comprimidos',              3, 'Mantecorp',     10.20, 22.50, 12, False),

    # Higiene Pessoal
    ('7891234000401', 'Sabonete Dove Original 90g',                  4, 'Unilever',      2.10,  4.90,  30, False),
    ('7891234000402', 'Shampoo Pantene 400ml',                       4, 'P&G',           12.50, 26.90, 20, False),
    ('7891234000403', 'Condicionador Pantene 400ml',                 4, 'P&G',           12.80, 27.50, 20, False),
    ('7891234000404', 'Creme Dental Colgate Total 12 90g',           4, 'Colgate',       4.80,  10.20, 25, False),
    ('7891234000405', 'Escova Dental Oral B Indicator',              4, 'P&G',           5.60,  12.50, 25, False),
    ('7891234000406', 'Desodorante Rexona Aerossol 150ml',           4, 'Unilever',      9.80,  21.50, 20, False),
    ('7891234000407', 'Fio Dental Colgate 50m',                      4, 'Colgate',       3.20,  7.20,  25, False),
    ('7891234000408', 'Absorvente Always Noturno 8un',               4, 'P&G',           7.90,  17.20, 20, False),
    ('7891234000409', 'Papel Higienico Neve 12 rolos',               4, 'Kimberly',      14.20, 30.90, 15, False),
    ('7891234000410', 'Enxaguante Bucal Listerine 500ml',            4, 'J&J',           15.80, 34.50, 15, False),

    # Cosmeticos
    ('7891234000501', 'Base Liquida Ruby Rose 30ml',                 5, 'Ruby Rose',     8.90,  19.90, 15, False),
    ('7891234000502', 'Batom Avon Ultra Color',                      5, 'Avon',          6.50,  15.90, 20, False),
    ('7891234000503', 'Mascara de Cilios Maybelline',                5, 'Maybelline',    18.90, 42.50, 12, False),
    ('7891234000504', 'Esmalte Risque 8ml',                          5, 'Risque',        3.20,  7.90,  25, False),
    ('7891234000505', 'Delineador Vult Liquido',                     5, 'Vult',          7.80,  18.90, 15, False),

    # Dermocosmeticos
    ('7891234000601', 'Protetor Solar La Roche FPS 60 60ml',         6, 'La Roche',      45.20, 98.90, 10, False),
    ('7891234000602', 'Sabonete Facial Cetaphil 250ml',              6, 'Galderma',      32.50, 71.90, 10, False),
    ('7891234000603', 'Hidratante Cerave 236ml',                     6, 'Cerave',        38.90, 84.50, 10, False),
    ('7891234000604', 'Creme Antissinais Vichy 50ml',                6, 'Vichy',         67.80, 148.90, 8,  False),
    ('7891234000605', 'Serum Vitamina C Adcos 30ml',                 6, 'Adcos',         89.50, 189.90, 8,  False),

    # Suplementos Alimentares
    ('7891234000701', 'Whey Protein Growth 1kg',                     7, 'Growth',        78.90, 169.90, 10, False),
    ('7891234000702', 'Creatina Integralmedica 300g',                7, 'Integralmedica',54.20, 118.90, 12, False),
    ('7891234000703', 'Vitamina C Sundown 30 comprimidos',           7, 'Sundown',       15.80, 34.90, 20, False),
    ('7891234000704', 'Vitamina D 2000 UI Vitgold 30 caps',          7, 'Vitgold',       18.90, 41.50, 20, False),
    ('7891234000705', 'Omega 3 1000mg Nature Made 60 caps',          7, 'Nature Made',   28.50, 62.90, 15, False),
    ('7891234000706', 'Complexo B Sundown 30 comprimidos',           7, 'Sundown',       16.20, 35.90, 20, False),
    ('7891234000707', 'Ferro Combiron 30 comprimidos',               7, 'Mantecorp',     12.80, 28.50, 20, False),
    ('7891234000708', 'Cafeina Growth 60 capsulas',                  7, 'Growth',        19.90, 43.90, 15, False),

    # Infantil
    ('7891234000801', 'Fralda Pampers Confort M 30un',               8, 'P&G',           32.50, 71.90, 15, False),
    ('7891234000802', 'Fralda Huggies Supreme G 26un',               8, 'Kimberly',      34.80, 76.90, 15, False),
    ('7891234000803', 'Lenco Umedecido Pampers 48un',                8, 'P&G',           8.90,  19.50, 25, False),
    ('7891234000804', 'Shampoo Johnsons Baby 200ml',                 8, 'J&J',           7.20,  16.20, 20, False),
    ('7891234000805', 'Sabonete Johnsons Baby 80g',                  8, 'J&J',           3.80,  8.50,  25, False),
    ('7891234000806', 'Pomada para Assadura Hipoglos 45g',           8, 'Nycomed',       12.50, 27.90, 15, False),
    ('7891234000807', 'Chupeta Nuk Silicone Tam 1',                  8, 'Nuk',           14.90, 32.50, 12, False),

    # Perfumaria
    ('7891234000901', 'Perfume Malbec Boticario 100ml',              9, 'Boticario',     89.50, 194.90, 8,  False),
    ('7891234000902', 'Perfume Egeo Boticario 90ml',                 9, 'Boticario',     78.90, 172.50, 8,  False),
    ('7891234000903', 'Perfume Kaiak Natura 100ml',                  9, 'Natura',        68.50, 149.90, 10, False),
    ('7891234000904', 'Perfume Essencial Natura 100ml',              9, 'Natura',        95.80, 209.90, 8,  False),

    # Primeiros Socorros
    ('7891234001001', 'Band Aid Johnson 40un',                      10, 'J&J',           7.80,  17.20, 20, False),
    ('7891234001002', 'Gaze Esteril 7,5x7,5cm 10un',                10, 'Cremer',        4.20,  9.50,  25, False),
    ('7891234001003', 'Esparadrapo 25mm x 4,5m',                    10, 'Cremer',        6.90,  15.20, 20, False),
    ('7891234001004', 'Algodao 100g',                               10, 'Cremer',        5.80,  12.90, 25, False),
    ('7891234001005', 'Soro Fisiologico 500ml',                     10, 'Fresenius',     8.20,  17.90, 20, False),
    ('7891234001006', 'Alcool 70% 500ml',                           10, 'Rioquimica',    6.50,  14.20, 25, False),
    ('7891234001007', 'Termometro Digital Geratherm',               10, 'Geratherm',     18.90, 41.90, 15, False),
    ('7891234001008', 'Aparelho Pressao Digital Omron',             10, 'Omron',         189.50, 419.90, 5, False),
    ('7891234001009', 'Mascara Descartavel Tripla 50un',            10, 'Descarpack',    12.80, 27.90, 20, False),
    ('7891234001010', 'Luva Descartavel Latex M 100un',             10, 'Supermax',      24.50, 53.90, 15, False),
]

NOMES = [
    'Ana', 'Bruno', 'Carla', 'Daniel', 'Eduarda', 'Fabio', 'Gabriela', 'Henrique',
    'Isabela', 'Joao', 'Karina', 'Lucas', 'Mariana', 'Nicolas', 'Olivia', 'Pedro',
    'Rafaela', 'Samuel', 'Tatiana', 'Vinicius', 'Amanda', 'Bernardo', 'Camila',
    'Diego', 'Elisa', 'Felipe', 'Giovana', 'Hugo', 'Isadora', 'Julia', 'Kaique',
    'Larissa', 'Marcos', 'Natalia', 'Otavio', 'Patricia', 'Rodrigo', 'Sabrina',
    'Thiago', 'Vanessa', 'Wesley', 'Yasmin', 'Alexandre', 'Beatriz', 'Cesar',
    'Debora', 'Emerson', 'Fernanda', 'Guilherme', 'Heloisa'
]

SOBRENOMES = [
    'Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves',
    'Pereira', 'Lima', 'Gomes', 'Ribeiro', 'Costa', 'Martins', 'Almeida',
    'Carvalho', 'Nascimento', 'Araujo', 'Lopes', 'Barbosa', 'Rocha', 'Dias',
    'Nunes', 'Mendes', 'Cardoso', 'Freitas', 'Cavalcanti', 'Correia', 'Machado'
]

CIDADES_CLIENTES = [
    ('Montes Claros', 'MG'), ('Bocaiuva', 'MG'), ('Janauba', 'MG'),
    ('Salinas', 'MG'), ('Pirapora', 'MG'), ('Belo Horizonte', 'MG'),
    ('Uberlandia', 'MG'), ('Diamantina', 'MG'), ('Grao Mogol', 'MG'),
    ('Buritizeiro', 'MG'), ('Corinto', 'MG'), ('Curvelo', 'MG'),
    ('Sao Francisco', 'MG'), ('Januaria', 'MG'), ('Espinosa', 'MG')
]

FORMAS_PAGAMENTO = [
    ('DINHEIRO', 0.15),
    ('CARTAO_CREDITO', 0.35),
    ('CARTAO_DEBITO', 0.20),
    ('PIX', 0.25),
    ('CONVENIO', 0.05),
]


# =============================================================================
# FUNCOES AUXILIARES
# =============================================================================

def gerar_cpf(seq):
    """Gera um CPF ficticio formatado."""
    base = f"{seq:09d}"
    return f"{base[:3]}.{base[3:6]}.{base[6:9]}-{random.randint(10, 99)}"


def gerar_telefone():
    """Gera telefone celular ficticio."""
    ddd = random.choice(['31', '34', '38'])
    return f"({ddd}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"


def gerar_email(nome, sobrenome, seq):
    dominios = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com.br']
    return f"{nome.lower()}.{sobrenome.lower()}{seq}@{random.choice(dominios)}"


def escapa_aspas(texto):
    """Escapa aspas simples para SQL."""
    return texto.replace("'", "''")


def escolher_forma_pagamento():
    """Escolhe forma de pagamento respeitando as probabilidades."""
    r = random.random()
    acumulado = 0
    for forma, prob in FORMAS_PAGAMENTO:
        acumulado += prob
        if r <= acumulado:
            return forma
    return 'DINHEIRO'


# =============================================================================
# GERACAO DO SQL
# =============================================================================

sql_lines = []

sql_lines.append("-- " + "=" * 76)
sql_lines.append("-- PharmaSystem - Insercao de Dados")
sql_lines.append("-- Gerado automaticamente pelo script gerar_dados.py")
sql_lines.append("-- " + "=" * 76)
sql_lines.append("")
sql_lines.append("BEGIN;")
sql_lines.append("")

# ---------------------------------------------------------------------------
# FILIAIS
# ---------------------------------------------------------------------------
sql_lines.append("-- " + "-" * 76)
sql_lines.append("-- FILIAIS")
sql_lines.append("-- " + "-" * 76)
sql_lines.append("INSERT INTO filiais (codigo, nome, cidade, estado, endereco, telefone, data_abertura) VALUES")
values = []
for codigo, nome, cidade, estado, end, tel, data in FILIAIS:
    values.append(f"    ('{codigo}', '{escapa_aspas(nome)}', '{cidade}', '{estado}', '{escapa_aspas(end)}', '{tel}', '{data}')")
sql_lines.append(",\n".join(values) + ";")
sql_lines.append("")

# ---------------------------------------------------------------------------
# CATEGORIAS
# ---------------------------------------------------------------------------
sql_lines.append("-- " + "-" * 76)
sql_lines.append("-- CATEGORIAS")
sql_lines.append("-- " + "-" * 76)
sql_lines.append("INSERT INTO categorias (nome, descricao) VALUES")
values = []
for nome, desc in CATEGORIAS:
    values.append(f"    ('{nome}', '{escapa_aspas(desc)}')")
sql_lines.append(",\n".join(values) + ";")
sql_lines.append("")

# ---------------------------------------------------------------------------
# PRODUTOS
# ---------------------------------------------------------------------------
sql_lines.append("-- " + "-" * 76)
sql_lines.append("-- PRODUTOS")
sql_lines.append("-- " + "-" * 76)
sql_lines.append("INSERT INTO produtos (codigo_barras, nome, categoria_id, fabricante, preco_custo, preco_venda, estoque_minimo, exige_receita) VALUES")
values = []
for cb, nome, cat, fab, pc, pv, em, er in PRODUTOS:
    er_str = 'TRUE' if er else 'FALSE'
    values.append(f"    ('{cb}', '{escapa_aspas(nome)}', {cat}, '{escapa_aspas(fab)}', {pc:.2f}, {pv:.2f}, {em}, {er_str})")
sql_lines.append(",\n".join(values) + ";")
sql_lines.append("")

# ---------------------------------------------------------------------------
# ESTOQUE (cada produto em cada filial)
# ---------------------------------------------------------------------------
sql_lines.append("-- " + "-" * 76)
sql_lines.append("-- ESTOQUE (produto x filial)")
sql_lines.append("-- " + "-" * 76)
sql_lines.append("INSERT INTO estoque (produto_id, filial_id, quantidade) VALUES")
values = []
for prod_id in range(1, len(PRODUTOS) + 1):
    for fil_id in range(1, len(FILIAIS) + 1):
        # Algumas filiais com estoque baixo propositalmente (uns 15% dos casos)
        if random.random() < 0.15:
            qtd = random.randint(0, 8)
        else:
            qtd = random.randint(15, 150)
        values.append(f"    ({prod_id}, {fil_id}, {qtd})")
sql_lines.append(",\n".join(values) + ";")
sql_lines.append("")

# ---------------------------------------------------------------------------
# CLIENTES
# ---------------------------------------------------------------------------
sql_lines.append("-- " + "-" * 76)
sql_lines.append("-- CLIENTES")
sql_lines.append("-- " + "-" * 76)
sql_lines.append("INSERT INTO clientes (nome, cpf, email, telefone, data_nascimento, cidade, estado, data_cadastro) VALUES")
values = []
clientes_info = []  # guarda para uso nas vendas
for i in range(1, NUM_CLIENTES + 1):
    nome = random.choice(NOMES)
    sobrenome = random.choice(SOBRENOMES)
    sobrenome2 = random.choice(SOBRENOMES)
    nome_completo = f"{nome} {sobrenome} {sobrenome2}"
    cpf = gerar_cpf(i)
    email = gerar_email(nome, sobrenome, i)
    tel = gerar_telefone()
    # Idade entre 18 e 75 anos
    dias_atras = random.randint(18 * 365, 75 * 365)
    nascimento = (date.today() - timedelta(days=dias_atras)).isoformat()
    cidade, estado = random.choice(CIDADES_CLIENTES)
    # Data cadastro distribuida no periodo
    dias_cad = random.randint(0, (DATA_FIM - DATA_INICIO).days)
    data_cadastro = (DATA_INICIO + timedelta(days=dias_cad)).isoformat()
    values.append(
        f"    ('{escapa_aspas(nome_completo)}', '{cpf}', '{email}', '{tel}', '{nascimento}', '{cidade}', '{estado}', '{data_cadastro}')"
    )
    clientes_info.append((i, data_cadastro))
sql_lines.append(",\n".join(values) + ";")
sql_lines.append("")

# ---------------------------------------------------------------------------
# VENDAS + ITENS_VENDA
# ---------------------------------------------------------------------------
sql_lines.append("-- " + "-" * 76)
sql_lines.append("-- VENDAS")
sql_lines.append("-- " + "-" * 76)

vendas_values = []
itens_values = []

# Filiais tem "peso" comercial diferente (filiais mais antigas / capital vendem mais)
pesos_filiais = [3, 3, 2, 2, 1, 1, 1, 1, 4, 3, 1, 1, 1, 1, 1]

for venda_id in range(1, NUM_VENDAS + 1):
    filial = random.choices(range(1, len(FILIAIS) + 1), weights=pesos_filiais)[0]

    # 80% das vendas tem cliente identificado
    if random.random() < 0.80:
        cliente_id = random.randint(1, NUM_CLIENTES)
        cliente_str = str(cliente_id)
    else:
        cliente_str = 'NULL'

    # Data da venda distribuida no periodo, com viés maior para últimos meses
    if random.random() < 0.60:
        # 60% no ultimo ano
        dias_inicio = (DATA_FIM - timedelta(days=365) - DATA_INICIO).days
        dias_offset = random.randint(dias_inicio, (DATA_FIM - DATA_INICIO).days)
    else:
        dias_offset = random.randint(0, (DATA_FIM - DATA_INICIO).days)
    data_venda = DATA_INICIO + timedelta(days=dias_offset)
    hora = random.randint(8, 21)
    minuto = random.randint(0, 59)
    data_venda_str = f"{data_venda.isoformat()} {hora:02d}:{minuto:02d}:00"

    forma_pgto = escolher_forma_pagamento()

    # Numero de itens da venda (1 a 5, media 2)
    num_itens = random.choices([1, 2, 3, 4, 5], weights=[35, 30, 20, 10, 5])[0]
    produtos_venda = random.sample(range(1, len(PRODUTOS) + 1), num_itens)

    valor_total = 0
    itens_dessa_venda = []
    for prod_id in produtos_venda:
        # Preco de venda vem dos dados dos produtos (index 5)
        preco_venda_produto = PRODUTOS[prod_id - 1][5]
        quantidade = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
        subtotal = round(preco_venda_produto * quantidade, 2)
        valor_total += subtotal
        itens_dessa_venda.append((prod_id, quantidade, preco_venda_produto, subtotal))

    # Desconto ocasional (10% das vendas)
    if random.random() < 0.10:
        desconto = round(valor_total * random.uniform(0.05, 0.15), 2)
    else:
        desconto = 0

    # 3% das vendas canceladas
    if random.random() < 0.03:
        status = 'CANCELADA'
    else:
        status = 'CONCLUIDA'

    vendas_values.append(
        f"    ({filial}, {cliente_str}, '{data_venda_str}', {valor_total:.2f}, {desconto:.2f}, '{forma_pgto}', '{status}')"
    )

    for prod_id, qtd, preco, sub in itens_dessa_venda:
        itens_values.append(f"    ({venda_id}, {prod_id}, {qtd}, {preco:.2f}, {sub:.2f})")

sql_lines.append("INSERT INTO vendas (filial_id, cliente_id, data_venda, valor_total, desconto, forma_pagamento, status) VALUES")
sql_lines.append(",\n".join(vendas_values) + ";")
sql_lines.append("")

sql_lines.append("-- " + "-" * 76)
sql_lines.append("-- ITENS_VENDA")
sql_lines.append("-- " + "-" * 76)
sql_lines.append("INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, subtotal) VALUES")
sql_lines.append(",\n".join(itens_values) + ";")
sql_lines.append("")

sql_lines.append("COMMIT;")
sql_lines.append("")
sql_lines.append("-- " + "=" * 76)
sql_lines.append(f"-- Resumo dos dados inseridos:")
sql_lines.append(f"--   Filiais:     {len(FILIAIS)}")
sql_lines.append(f"--   Categorias:  {len(CATEGORIAS)}")
sql_lines.append(f"--   Produtos:    {len(PRODUTOS)}")
sql_lines.append(f"--   Estoque:     {len(PRODUTOS) * len(FILIAIS)} registros")
sql_lines.append(f"--   Clientes:    {NUM_CLIENTES}")
sql_lines.append(f"--   Vendas:      {NUM_VENDAS}")
sql_lines.append(f"--   Itens:       {len(itens_values)}")
sql_lines.append("-- " + "=" * 76)


# Escreve arquivo
saida = "/home/claude/modulo-01-sql-pharma-system/02_inserts.sql"
with open(saida, "w", encoding="utf-8") as f:
    f.write("\n".join(sql_lines))

print(f"Arquivo gerado: {saida}")
print(f"Filiais:    {len(FILIAIS)}")
print(f"Categorias: {len(CATEGORIAS)}")
print(f"Produtos:   {len(PRODUTOS)}")
print(f"Estoque:    {len(PRODUTOS) * len(FILIAIS)} registros")
print(f"Clientes:   {NUM_CLIENTES}")
print(f"Vendas:     {NUM_VENDAS}")
print(f"Itens:      {len(itens_values)}")
