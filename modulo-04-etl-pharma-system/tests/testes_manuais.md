# Cenários de Teste Manual

Este arquivo lista os cenários que o pipeline deve tratar corretamente, e como validar cada um.

**Todos os testes assumem que você:**
1. Rodou `scripts/limpar_ambiente.py` para começar do zero
2. Depois rodou `scripts/gerar_csvs_exemplo.py` para gerar os CSVs de teste

---

## Cenário 1 — Arquivo Limpo (happy path)

**Arquivos afetados:** `vendas_filial_01_2026-06-15.csv`, `vendas_filial_02_2026-06-15.csv`

**Esperado:**
- Extract: `Lido: 30 linhas, encoding=utf-8-sig`
- Transform: `30 -> 30 linhas (0 removidas)`
- Load: `30 inseridas, 0 atualizadas`
- Arquivo movido para `dados_processados/`

**Como validar:** ver log da execução.

---

## Cenário 2 — Linhas em branco no meio

**Arquivo:** `vendas_filial_03_2026-06-15.csv`

**Esperado:**
- Extract lê OK (linhas em branco não quebram)
- Transform remove linhas em branco silenciosamente ou com WARNING
- Load processa normalmente

**Como validar:**
```
INFO | transform | [vendas_filial_03_*.csv] Transform: N -> M linhas (K removidas: branco=K, ...)
```

---

## Cenário 3 — Data em formato dd/mm/yyyy

**Arquivo:** `vendas_filial_04_2026-06-15.csv`

**Esperado:**
- Transform reconhece o formato brasileiro (definido em `config.yaml → regras.formatos_data`)
- Zero linhas removidas por data inválida

**Como validar:** `data_inv=0` no log de transform.

---

## Cenário 4 — Valores negativos (regra de negócio violada)

**Arquivo:** `vendas_filial_05_2026-06-15.csv`

**Esperado:**
- Transform detecta `quantidade <= 0` e `preco_unitario <= 0`
- Remove essas linhas com WARNING
- Restante é carregado normalmente

**Como validar:**
```
WARNING | transform | Removendo 4 linhas com quantidade <= 0
WARNING | transform | Removendo 1 linhas com preco_unitario <= 0
```

---

## Cenário 5 — Duplicatas

**Arquivo:** `vendas_filial_01_2026-06-16.csv`

**Esperado:**
- Transform detecta duplicatas por chave natural (filial + data + cliente + produto)
- Mantém primeira ocorrência, remove as demais

**Como validar:**
```
INFO | transform | Removidas 5 duplicatas por chave natural
```

---

## Cenário 6 — Encoding Latin-1

**Arquivo:** `vendas_filial_02_2026-06-16.csv`

**Esperado:**
- Extract falha ao ler UTF-8 → tenta Latin-1 → sucesso
- WARNING avisando o fallback

**Como validar:**
```
WARNING | extract | Arquivo vendas_filial_02_2026-06-16.csv lido com encoding fallback: latin-1
```

Se o CSV tem acentos e o WARNING não aparecer, algo mudou no gerador. Verificar.

---

## Cenário 7 — Forma de pagamento inválida

**Arquivo:** `vendas_filial_03_2026-06-16.csv`

**Esperado:**
- Transform detecta valores fora da lista `[PIX, DINHEIRO, DEBITO, CREDITO, CONVENIO]`
- Remove linhas com valores como `BOLETO`, `CHEQUE`, `VOUCHER`

**Como validar:**
```
WARNING | transform | Removendo 3 linhas com forma_pagamento invalida: ['CHEQUE', 'BOLETO']
```

---

## Cenário 8 — Coluna obrigatória faltando (schema inválido)

**Arquivo:** `vendas_filial_04_2026-06-16.csv` (sem a coluna `quantidade`)

**Esperado:**
- Extract detecta que a coluna obrigatória está faltando
- Arquivo é **REJEITADO** e movido para `dados_rejeitados/` com prefixo `REJEITADO_`
- Pipeline segue processando os outros arquivos

**Como validar:**
- Log: `ERROR | extract | Schema invalido: colunas obrigatorias faltando: quantidade`
- Arquivo em `dados_rejeitados/` com nome `REJEITADO_20260711_HHMMSS_vendas_filial_04_2026-06-16.csv`

---

## Cenário 9 — Arquivo vazio

**Arquivo:** `vendas_filial_05_2026-06-16.csv` (0 bytes)

**Esperado:**
- Extract detecta arquivo sem dados
- Arquivo é **REJEITADO** e movido para `dados_rejeitados/`
- Pipeline segue

**Como validar:**
```
WARNING | extract | [vendas_filial_05_2026-06-16.csv] CSV sem dados
```

---

## Cenário 10 — IDEMPOTÊNCIA (crítico)

**Como testar:**
```bash
# 1. Reset e primeira execução
python scripts/limpar_ambiente.py --confirmar
python scripts/gerar_csvs_exemplo.py
python scripts/executar_pipeline.py

# 2. Copiar arquivos processados de volta e re-rodar
for arq in dados_processados/*.csv; do
    nome=$(basename "$arq" | sed 's/^[0-9_]*//')
    cp "$arq" "dados_brutos/$nome"
done
python scripts/executar_pipeline.py
```

**Esperado na SEGUNDA execução:**
- `Linhas inseridas: 0`
- `Linhas atualizadas: 170`
- `total_linhas_fato_vendas: 170` (mesmo total da primeira execução)

**Se falhar:** total_linhas duplicou → verifique se a UNIQUE constraint está em vigor e se CPF nulo está sendo tratado.

---

## Cenário 11 — Nenhum arquivo em dados_brutos/

**Como testar:**
```bash
python scripts/limpar_ambiente.py --confirmar
python scripts/executar_pipeline.py
```

**Esperado:**
- `Nenhum arquivo com padrao 'vendas_filial_*.csv' em dados_brutos/`
- Pipeline termina com `Status: FALHA`, sem tocar no banco

---

## Cenário 12 — Configuração inválida

**Como testar:** editar `config.yaml` com um caminho inexistente:
```yaml
paths:
  dados_brutos: pasta_que_nao_existe
```

**Esperado:**
- Pipeline detecta e retorna erro claro
- Não deleta nem corrompe dados existentes
