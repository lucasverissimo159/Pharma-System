# Módulo 04 — Pipeline ETL Automatizado

**PharmaSystem — Semana 4 de 12 do portfólio**

Pipeline ETL completo em Python que processa CSVs de vendas das filiais da rede fictícia PharmaMinas, aplicando limpeza, validação de regras de negócio e carga idempotente em banco de dados. Foco em **robustez** e **observabilidade**.

---

## Números

Rodando com os CSVs de exemplo do próprio pacote (10 arquivos, 183 linhas de entrada):

| Métrica | 1ª execução | 2ª execução (idempotência) |
|---|---|---|
| Arquivos encontrados | 10 | 10 |
| Arquivos processados | 8 | 8 |
| Arquivos rejeitados | 2 | 0 |
| Linhas inseridas | 170 | **0** ✅ |
| Linhas atualizadas | 0 | **170** ✅ |
| Duração | 0,3s | 0,2s |
| Status | SUCESSO_PARCIAL | SUCESSO |

**Chave do sucesso:** rodar o pipeline duas vezes com os mesmos dados **não duplicou nada** — cada linha foi atualizada em vez de re-inserida. Idempotência garantida via `INSERT ... ON CONFLICT DO UPDATE` + tratamento do CPF nulo.

---

## Sobre o banco de destino

A apostila pede PostgreSQL. Este pacote usa **SQLite** por padrão (roda em qualquer máquina sem instalação), mas a estrutura de código está pronta para PostgreSQL:

- SQL usa sintaxe `INSERT ... ON CONFLICT DO UPDATE` que é **idêntica** em ambos.
- `config.yaml` permite trocar o backend em uma linha (`backend: postgres`).
- `src/load.py` tem esqueleto comentado da classe `CarregadorPostgres` para você completar com `psycopg2`.

Ver `docs/arquitetura.md → Trocando SQLite por PostgreSQL` para o passo-a-passo.

---

## Estrutura

```
modulo-04-etl-pharma-system/
├── README.md                          (este arquivo)
├── COMO_ESTUDAR.md                    Roteiro de reversa (7 dias)
├── requirements.txt
│
├── config/
│   ├── config.yaml                    Configuração principal (caminhos, banco, regras)
│   └── schema.yaml                    Schema esperado dos CSVs
│
├── src/                               Pacote Python modular
│   ├── __init__.py
│   ├── config.py                      Carrega YAMLs, expande ${VAR}
│   ├── logger.py                      Logger com console colorido + arquivo rotacionado
│   ├── extract.py                     Leitura + validação de schema
│   ├── transform.py                   Limpeza, validação, dedup, enriquecimento
│   ├── load.py                        UPSERT idempotente (SQLite → PostgreSQL)
│   └── pipeline.py                    Orquestração E → T → L
│
├── scripts/                           Pontos de entrada
│   ├── executar_pipeline.py           Rodar pipeline
│   ├── gerar_csvs_exemplo.py          Gera 10 CSVs com cenários variados
│   ├── inicializar_banco.py           Cria tabelas
│   └── limpar_ambiente.py             Reset completo
│
├── dados_brutos/                      CSVs "chegando" aqui
├── dados_processados/                 CSVs após processamento (com timestamp)
├── dados_rejeitados/                  CSVs com erro (prefixo REJEITADO_/ERRO_)
├── logs/                              pipeline.log com rotação diária
├── db/
│   └── pharma_dw.db                   SQLite (gerado)
│
├── docs/
│   ├── arquitetura.md                 Design decisions + fluxo detalhado
│   ├── diagrama_fluxo.png/.dot        Diagrama visual
│   ├── log_execucao_1_primeira_vez.txt
│   └── log_execucao_2_idempotencia.txt
│
└── tests/
    └── testes_manuais.md              12 cenários de teste com validação
```

---

## Cenários que o pipeline trata

Os CSVs gerados por `gerar_csvs_exemplo.py` cobrem **8 cenários reais** de dados sujos:

| Cenário | Como é tratado |
|---|---|
| Arquivo limpo (happy path) | Processado normalmente |
| Linhas em branco no meio | Removidas silenciosamente no Transform |
| Data em formato dd/mm/yyyy | Parser tenta múltiplos formatos definidos no config |
| Valores negativos (qtd/preço) | Removidos com WARNING |
| Duplicatas na chave natural | Removidas mantendo a primeira |
| Encoding Latin-1 | Detectado após falha do UTF-8; log de aviso |
| Forma de pagamento inválida | Removida (whitelist do schema) |
| Coluna obrigatória faltando | Arquivo REJEITADO, movido para `dados_rejeitados/` |
| Arquivo vazio | Arquivo REJEITADO |
| Re-executar o pipeline | Idempotência: 0 duplicatas |

Detalhes de cada cenário em `tests/testes_manuais.md`.

---

## Como usar

### Setup rápido (1 minuto)

```bash
# 1. Instalar dependências (só precisa de pandas + pyyaml)
pip install -r requirements.txt

# 2. Gerar CSVs de exemplo (com problemas variados)
python scripts/gerar_csvs_exemplo.py

# 3. Rodar pipeline
python scripts/executar_pipeline.py
```

### Consultar o resultado

```bash
python -c "
import sqlite3
conn = sqlite3.connect('db/pharma_dw.db')
cur = conn.cursor()
cur.execute('SELECT filial_codigo, COUNT(*), ROUND(SUM(valor_total), 2) FROM fato_vendas GROUP BY filial_codigo ORDER BY 3 DESC')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]} vendas, R\$ {row[2]:,.2f}')
"
```

Ou abra `db/pharma_dw.db` no [DB Browser for SQLite](https://sqlitebrowser.org/).

### Testar idempotência

```bash
# Copiar arquivos processados de volta para brutos
for arq in dados_processados/*.csv; do
    nome=$(basename "$arq" | sed 's/^[0-9_]*//')
    cp "$arq" "dados_brutos/$nome"
done

# Rodar de novo — deve mostrar "0 inseridas, 170 atualizadas"
python scripts/executar_pipeline.py
```

### Reset

```bash
python scripts/limpar_ambiente.py --confirmar
```

---

## Observabilidade

### Logs

Toda execução gera log em **dois canais**:

1. **Console:** colorido (INFO/WARNING/ERROR em cores distintas), só mensagens relevantes.
2. **Arquivo:** `logs/pipeline.log`, tudo (DEBUG+), rotação diária, retenção de 30 dias.

Exemplo real da execução:

```
2026-07-11 17:48:06 | INFO     | pipeline        | INICIANDO PIPELINE ETL
2026-07-11 17:48:06 | INFO     | pipeline.load   | Banco inicializado
2026-07-11 17:48:06 | INFO     | pipeline        | >> ETAPA: Extract
2026-07-11 17:48:06 | INFO     | pipeline.extract | Encontrados 10 arquivos
2026-07-11 17:48:06 | WARNING  | pipeline.extract | Arquivo vendas_filial_02_*.csv lido com encoding fallback: latin-1
2026-07-11 17:48:06 | ERROR    | pipeline.extract | [vendas_filial_04_*.csv] Schema invalido: colunas obrigatorias faltando: quantidade
2026-07-11 17:48:06 | WARNING  | pipeline.extract | [vendas_filial_05_*.csv] CSV sem dados
2026-07-11 17:48:06 | INFO     | pipeline.extract | Extract concluido: 8 sucesso, 2 rejeitados
2026-07-11 17:48:06 | WARNING  | pipeline.transform | Removendo 4 linhas com quantidade <= 0
2026-07-11 17:48:06 | INFO     | pipeline.transform | Transform: 20 -> 15 linhas (5 removidas...)
2026-07-11 17:48:06 | INFO     | pipeline.load   | Load: 15 inseridas, 0 atualizadas, 0 ignoradas
...
2026-07-11 17:48:06 | INFO     | pipeline        | RESUMO DA EXECUCAO
2026-07-11 17:48:06 | INFO     | pipeline        |   Status: SUCESSO_PARCIAL
2026-07-11 17:48:06 | INFO     | pipeline        |   Arquivos processados: 8
2026-07-11 17:48:06 | INFO     | pipeline        |   Linhas inseridas: 170
```

Log completo em `docs/log_execucao_1_primeira_vez.txt`.

### Auditoria no banco

Tabela `pipeline_execucoes` guarda o histórico de todas as execuções:

```sql
SELECT executado_em, arquivos_processados, linhas_inseridas, linhas_atualizadas,
       ROUND(duracao_segundos, 2) AS tempo, status
FROM pipeline_execucoes
ORDER BY id DESC;
```

Cada linha de `fato_vendas` tem `origem_arquivo`, `inserido_em` e `atualizado_em` para rastreabilidade completa.

---

## Diagrama

Ver `docs/diagrama_fluxo.png`. Fluxo simplificado:

```
CSVs → [Extract]  →  [Transform] → [Load] → SQLite/PostgreSQL
         ↓                                       ↑
    Se schema inválido                       INSERT ON CONFLICT
    → dados_rejeitados/                      (idempotente)
```

---

## Configuração (`config/config.yaml`)

Todos os parâmetros externos ao código. Destaques:

```yaml
banco:
  backend: sqlite            # ou "postgres"
  sqlite:
    caminho: db/pharma_dw.db

pipeline:
  padrao_arquivo: "vendas_filial_*.csv"
  em_caso_de_erro: continuar  # ou "abortar"
  chave_natural:              # define UPSERT
    - filial_codigo
    - data_venda
    - cliente_cpf
    - produto_codigo

regras:
  aceitar_quantidade_negativa: false
  formatos_data:
    - "%Y-%m-%d %H:%M:%S"
    - "%d/%m/%Y %H:%M"
    - "%d/%m/%Y"
```

Para adicionar uma nova regra de validação — por exemplo, aceitar novo formato de data — edite o YAML, sem tocar em código.

---

## Publicação no GitHub

Estrutura sugerida:

```
pharma-system/
├── modulo-01-sql/
├── modulo-02-powerbi/
├── modulo-03-python-pandas/
└── modulo-04-etl/       ← este módulo
    ├── config/
    ├── src/
    ├── scripts/
    ├── docs/
    ├── tests/
    ├── dados_brutos/    (deixar vazio no repo, adicionar .gitkeep)
    ├── README.md
    └── requirements.txt
```

Adicione um `.gitignore`:

```
db/*.db
logs/*.log
dados_processados/*.csv
dados_rejeitados/*.csv
__pycache__/
*.pyc
.venv/
```

---

## Post do LinkedIn — Rascunho

> ⚙️ Semana 4 do meu portfólio: Pipeline ETL completo em Python
>
> Construí um pipeline que processa CSVs de vendas de múltiplas filiais com robustez de produção. Highlights:
>
> ✅ **Idempotência garantida** — rodar N vezes = mesmo estado final (UPSERT com ON CONFLICT)
> ✅ **8 cenários de dados sujos** tratados: linhas em branco, encoding Latin-1, formatos de data variados, valores negativos, duplicatas, schema inválido, arquivo vazio, etc.
> ✅ **Arquitetura modular** com Extract/Transform/Load separados
> ✅ **Observabilidade completa** — logs coloridos no console + arquivo rotacionado + tabela de auditoria no banco
> ✅ **Configuração externa** em YAML (nenhum caminho hardcoded)
> ✅ **Fail-safe** — arquivo com erro é movido para `dados_rejeitados/`, pipeline continua
>
> Testado com 10 arquivos, 183 linhas de entrada, 170 carregadas em <1 segundo.
>
> Extensível para PostgreSQL trocando só uma linha no config.
>
> #ETL #Python #DataEngineering #Pipeline #Idempotência #EngenhariaDeSistemas

Anexe:
- Print do log de execução (colorido, do console)
- `docs/diagrama_fluxo.png`

---

## Próximos módulos

- **Módulo 05** — API REST consumindo o banco alimentado por este pipeline
- **Módulo 06+** — Docker, CI/CD, ML, etc.

---

## Créditos

- **Autor:** Lucas Veríssimo (UNIMONTES — Engenharia de Sistemas)
- **Assistência técnica:** Claude (Anthropic)
- **Ferramentas:** Python 3.10+, pandas, pyyaml, sqlite3 (nativo)
