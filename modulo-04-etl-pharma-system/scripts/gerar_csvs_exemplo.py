"""
gerar_csvs_exemplo.py
---------------------
Gera 10 CSVs de vendas simulando o cenario real de recebimento diario:
- 5 arquivos "bons" (dados limpos)
- 5 arquivos com PROBLEMAS PROPOSITAIS para testar robustez do pipeline:
  * Arquivo com linhas em branco no meio
  * Arquivo com data em formato diferente (dd/mm/yyyy)
  * Arquivo com valores negativos (invalido)
  * Arquivo com duplicatas
  * Arquivo com encoding Latin-1 (nao UTF-8)
  * Arquivo com forma de pagamento invalida
  * Arquivo com coluna faltando (schema invalido)
  * Arquivo vazio

Uso:
    python scripts/gerar_csvs_exemplo.py
    python scripts/gerar_csvs_exemplo.py --limpar  (remove os anteriores primeiro)
"""

import argparse
import csv
import random
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Adicionar raiz ao path
ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))

# Reprodutibilidade
random.seed(42)


# Dados de referencia
FILIAIS = [
    ("FIL001", "Montes Claros Centro"),
    ("FIL002", "Todos os Santos"),
    ("FIL003", "Ibituruna"),
    ("FIL004", "BH Savassi"),
    ("FIL005", "Uberlandia Centro"),
]

PRODUTOS = [
    ("7891234567890", "Dipirona 500mg 20cp", 8.50),
    ("7891234567891", "Paracetamol 750mg 20cp", 12.30),
    ("7891234567892", "Omeprazol 20mg 30cp", 24.90),
    ("7891234567893", "Buscopan Composto 20cp", 32.40),
    ("7891234567894", "Loratadina 10mg 12cp", 15.80),
    ("7891234567895", "Shampoo Johnsons Baby 200ml", 18.90),
    ("7891234567896", "Papel Higienico Neve 12 rolos", 28.50),
    ("7891234567897", "Sabonete Dove 90g", 4.20),
    ("7891234567898", "Fralda Huggies Supreme G", 89.90),
    ("7891234567899", "Perfume Natura Essencial", 145.00),
    ("7891234567900", "Whey Protein Growth 1kg", 179.90),
    ("7891234567901", "Vitamina C 1g 10cp efervescente", 22.30),
]

FORMAS_PAGAMENTO = ["PIX", "DINHEIRO", "DEBITO", "CREDITO", "CONVENIO"]

CPFS = [
    "123.456.789-01", "234.567.890-12", "345.678.901-23", "456.789.012-34",
    "567.890.123-45", "678.901.234-56", "789.012.345-67", "890.123.456-78",
    "901.234.567-89", "012.345.678-90",
]

VENDEDORES = ["Ana Silva", "Bruno Santos", "Carla Oliveira", "Diego Costa",
              "Eduarda Lima", "Fernando Souza"]


def gerar_venda(data_base, formato_data="%Y-%m-%d %H:%M:%S", filial=None):
    """Gera uma linha de venda no formato normal."""
    if filial is None:
        filial = random.choice(FILIAIS)
    produto = random.choice(PRODUTOS)
    hora = timedelta(hours=random.randint(8, 21), minutes=random.randint(0, 59))
    quantidade = random.randint(1, 4)
    forma = random.choice(FORMAS_PAGAMENTO)
    cpf = random.choice(CPFS) if random.random() > 0.15 else ""
    desconto = round(random.uniform(0, 5), 2) if random.random() > 0.7 else 0.00

    return {
        "filial_codigo": filial[0],
        "data_venda": (data_base + hora).strftime(formato_data),
        "cliente_cpf": cpf,
        "produto_codigo": produto[0],
        "produto_nome": produto[1],
        "quantidade": quantidade,
        "preco_unitario": produto[2],
        "desconto": desconto,
        "forma_pagamento": forma,
        "vendedor": random.choice(VENDEDORES),
    }


def salvar_csv(caminho: Path, linhas: list, encoding="utf-8-sig"):
    """Escreve CSV com cabecalho baseado nas chaves da primeira linha."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    if not linhas:
        # Arquivo vazio
        caminho.write_text("", encoding=encoding)
        return

    with caminho.open("w", encoding=encoding, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        writer.writeheader()
        for linha in linhas:
            writer.writerow(linha)


def salvar_csv_com_brancos(caminho: Path, linhas: list, encoding="utf-8-sig"):
    """Igual mas insere linhas em branco no meio (aleatoriamente)."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding=encoding, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        writer.writeheader()
        for i, linha in enumerate(linhas):
            writer.writerow(linha)
            # A cada 5 linhas, insere uma vazia
            if i % 5 == 4:
                f.write("\n")


# =============================================================================
# GERADORES DE ARQUIVOS ESPECIFICOS
# =============================================================================

def gerar_arquivo_normal(caminho, data_base, filial, n_vendas=30):
    """CSV limpo, tudo correto."""
    linhas = [gerar_venda(data_base, filial=filial) for _ in range(n_vendas)]
    salvar_csv(caminho, linhas)
    return len(linhas)


def gerar_arquivo_com_brancos(caminho, data_base, filial, n_vendas=25):
    """CSV com linhas em branco no meio."""
    linhas = [gerar_venda(data_base, filial=filial) for _ in range(n_vendas)]
    salvar_csv_com_brancos(caminho, linhas)
    return n_vendas  # linhas efetivas (sem as em branco)


def gerar_arquivo_data_alternativa(caminho, data_base, filial, n_vendas=20):
    """CSV com data em formato brasileiro dd/mm/yyyy."""
    linhas = [gerar_venda(data_base, "%d/%m/%Y %H:%M", filial=filial)
              for _ in range(n_vendas)]
    salvar_csv(caminho, linhas)
    return len(linhas)


def gerar_arquivo_com_negativos(caminho, data_base, filial, n_vendas=20):
    """CSV com valores negativos (invalidos por regra de negocio)."""
    linhas = [gerar_venda(data_base, filial=filial) for _ in range(n_vendas)]
    # Corromper 4 linhas com valores negativos
    for idx in random.sample(range(len(linhas)), 4):
        linhas[idx]["quantidade"] = -random.randint(1, 3)
    for idx in random.sample(range(len(linhas)), 2):
        linhas[idx]["preco_unitario"] = -linhas[idx]["preco_unitario"]
    salvar_csv(caminho, linhas)
    return len(linhas)


def gerar_arquivo_com_duplicatas(caminho, data_base, filial, n_vendas=15):
    """CSV com linhas duplicadas propositais."""
    linhas = [gerar_venda(data_base, filial=filial) for _ in range(n_vendas)]
    # Duplicar 5 linhas
    duplicatas = random.sample(linhas, 5)
    linhas.extend(duplicatas)
    random.shuffle(linhas)
    salvar_csv(caminho, linhas)
    return len(linhas)


def gerar_arquivo_encoding_latin1(caminho, data_base, filial, n_vendas=20):
    """CSV em encoding Latin-1 (nao UTF-8), com acentos nos nomes."""
    linhas = [gerar_venda(data_base, filial=filial) for _ in range(n_vendas)]
    # Adicionar acentos nos vendedores para forcar problema de encoding
    for linha in linhas:
        linha["vendedor"] = linha["vendedor"].replace("Ana", "Anália")
    salvar_csv(caminho, linhas, encoding="latin-1")
    return len(linhas)


def gerar_arquivo_pagamento_invalido(caminho, data_base, filial, n_vendas=18):
    """CSV com formas de pagamento invalidas."""
    linhas = [gerar_venda(data_base, filial=filial) for _ in range(n_vendas)]
    # Corromper 3 formas de pagamento
    invalidos = ["BOLETO", "CHEQUE", "VOUCHER"]
    for idx in random.sample(range(len(linhas)), 3):
        linhas[idx]["forma_pagamento"] = random.choice(invalidos)
    salvar_csv(caminho, linhas)
    return len(linhas)


def gerar_arquivo_coluna_faltando(caminho, data_base, filial, n_vendas=15):
    """CSV sem a coluna 'quantidade' — schema invalido, sera rejeitado no extract."""
    linhas = [gerar_venda(data_base, filial=filial) for _ in range(n_vendas)]
    for linha in linhas:
        del linha["quantidade"]  # coluna obrigatoria removida
    salvar_csv(caminho, linhas)
    return len(linhas)


def gerar_arquivo_vazio(caminho):
    """Arquivo completamente vazio — sera rejeitado."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("", encoding="utf-8-sig")
    return 0


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Gera CSVs de exemplo para o ETL")
    parser.add_argument("--pasta", default=str(ROOT / "dados_brutos"),
                        help="Pasta onde salvar os CSVs")
    parser.add_argument("--limpar", action="store_true",
                        help="Remove arquivos existentes antes de gerar")
    args = parser.parse_args()

    pasta = Path(args.pasta)
    pasta.mkdir(parents=True, exist_ok=True)

    if args.limpar:
        for arq in pasta.glob("*.csv"):
            arq.unlink()
        print(f"Pasta limpa: {pasta}")

    print("=" * 70)
    print("Gerando CSVs de exemplo com cenarios variados...")
    print("=" * 70)

    data_ref = datetime(2026, 6, 15, 8, 0, 0)

    arquivos = [
        # (nome, funcao, filial, descricao)
        ("vendas_filial_01_2026-06-15.csv", gerar_arquivo_normal, FILIAIS[0],
         "OK — arquivo limpo (Montes Claros Centro)"),
        ("vendas_filial_02_2026-06-15.csv", gerar_arquivo_normal, FILIAIS[1],
         "OK — arquivo limpo (Todos os Santos)"),
        ("vendas_filial_03_2026-06-15.csv", gerar_arquivo_com_brancos, FILIAIS[2],
         "AVISO — linhas em branco no meio (Ibituruna)"),
        ("vendas_filial_04_2026-06-15.csv", gerar_arquivo_data_alternativa, FILIAIS[3],
         "AVISO — data em formato dd/mm/yyyy (BH Savassi)"),
        ("vendas_filial_05_2026-06-15.csv", gerar_arquivo_com_negativos, FILIAIS[4],
         "AVISO — algumas linhas com valores negativos (Uberlandia)"),
        ("vendas_filial_01_2026-06-16.csv", gerar_arquivo_com_duplicatas, FILIAIS[0],
         "AVISO — algumas duplicatas (Montes Claros Centro, dia 16)"),
        ("vendas_filial_02_2026-06-16.csv", gerar_arquivo_encoding_latin1, FILIAIS[1],
         "AVISO — encoding Latin-1 (Todos os Santos, dia 16)"),
        ("vendas_filial_03_2026-06-16.csv", gerar_arquivo_pagamento_invalido, FILIAIS[2],
         "AVISO — algumas formas de pagamento invalidas (Ibituruna, dia 16)"),
        ("vendas_filial_04_2026-06-16.csv", gerar_arquivo_coluna_faltando, FILIAIS[3],
         "ERRO — coluna 'quantidade' faltando, sera REJEITADO (BH Savassi, dia 16)"),
        ("vendas_filial_05_2026-06-16.csv", None, None,
         "ERRO — arquivo vazio, sera REJEITADO"),
    ]

    total = 0
    for nome, funcao, filial, descricao in arquivos:
        caminho = pasta / nome
        if funcao is None:
            n = gerar_arquivo_vazio(caminho)
        else:
            data_dia = data_ref if "2026-06-15" in nome else data_ref + timedelta(days=1)
            n = funcao(caminho, data_dia, filial)

        print(f"  [OK] {nome}: {n} linhas  — {descricao}")
        total += n

    print()
    print(f"Gerados {len(arquivos)} arquivos com {total} linhas totais em: {pasta}")


if __name__ == "__main__":
    main()
