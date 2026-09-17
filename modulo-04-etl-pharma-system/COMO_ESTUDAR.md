# Como Estudar Este Módulo — Roteiro de Engenharia Reversa

Este módulo é sobre **engenharia de dados**, não apenas Python. As decisões de arquitetura são o principal aprendizado — pipeline modular, idempotência, tratamento de erros, observabilidade.

**Carga total:** 8 a 12 horas em 7 dias (~1-2h por dia).

---

## Filosofia

Ao contrário dos módulos anteriores, este NÃO tem "gráfico bonito" como resultado visível. O resultado é um sistema que **funciona sozinho** e **não quebra** quando os dados chegam sujos.

O que você recebe:
- Pipeline completo, testado, rodando idempotência 100%
- 10 CSVs de exemplo cobrindo 8 cenários reais de dados sujos
- Logs de exemplo (1ª execução + teste de idempotência)
- Diagrama de fluxo do ETL
- Documentação de arquitetura + testes manuais

O que você vai construir:
- Sua própria versão do pipeline (mesma estrutura, seu código)
- Um novo cenário de teste que ainda não existe
- Sua própria consulta SQL para validar o resultado

---

## Pré-requisitos

- Python 3.10+ instalado
- Familiaridade básica com Pandas (Módulo 03 já cobre)
- Alguma exposição a SQL (Módulo 01 já cobre)

**Não é necessário:** PostgreSQL, Docker, ou qualquer serviço externo. O pipeline roda 100% offline com SQLite.

---

## Setup (10 minutos)

```bash
# Clone/extraia o pacote
cd modulo-04-etl-pharma-system

# Ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows

# Instale as (poucas) dependências
pip install -r requirements.txt

# Rode ponta a ponta pra ver funcionar
python scripts/gerar_csvs_exemplo.py
python scripts/executar_pipeline.py
```

Se você vê o resumo final com "Status: SUCESSO_PARCIAL, Arquivos processados: 8", está pronto.

---

## Roteiro de 7 Dias

### Dia 1 — Explorar (1h)

**Sem escrever código ainda.**

1. Leia `README.md` e `docs/arquitetura.md` (30 min).
2. Rode o pipeline e observe o console (10 min):
   ```bash
   python scripts/limpar_ambiente.py --confirmar
   python scripts/gerar_csvs_exemplo.py
   python scripts/executar_pipeline.py
   ```
3. Rode de novo (sem gerar novos CSVs, apenas re-execute). Observe: nada acontece porque `dados_brutos/` está vazio (arquivos foram movidos). Copie-os de volta e re-execute — teste a idempotência (10 min):
   ```bash
   for arq in dados_processados/*.csv; do
       nome=$(basename "$arq" | sed 's/^[0-9_]*//')
       cp "$arq" "dados_brutos/$nome"
   done
   python scripts/executar_pipeline.py
   ```
4. Compare os dois logs em `docs/`. Anote 3 diferenças (10 min).

**Entregável:** anotações à mão sobre o que muda entre 1ª e 2ª execução.

---

### Dia 2 — Extract (1,5h)

**Objetivo:** entender leitura robusta de arquivos.

1. **Estude o problema (30 min):**
   - Abra 3 CSVs em `dados_brutos/`: um limpo, um com Latin-1, um sem a coluna quantidade. Note as diferenças.
   - Leia `config/schema.yaml` e entenda o que é "obrigatória" vs "opcional".

2. **Recrie sozinho (60 min):**
   - Crie `meus_estudos/meu_extract.py` do zero.
   - Objetivo: função `extrair(caminho) -> DataFrame` que:
     - Tenta UTF-8, cai para Latin-1 se falhar
     - Retorna None se o schema não bate
     - Loga o que acontece
   - Depois compare com `src/extract.py`.

**Pergunta pra pensar:** por que o Extract retorna um objeto `ArquivoExtraido` com `sucesso: bool` em vez de levantar exceção quando algo dá errado?

**Resposta:** porque exceções param o pipeline inteiro. O padrão "objeto com erro" permite tratar arquivo por arquivo sem derrubar o resto.

---

### Dia 3 — Transform (2h)

**Objetivo:** aplicar regras de negócio em Pandas.

1. **Estude o config (15 min):**
   - Leia `regras` em `config/config.yaml`. Note como valores como `formatos_data` são listas — o parser tenta cada um em ordem.

2. **Recrie as etapas isoladamente (75 min):**
   - Em `meus_estudos/meu_transform.ipynb` (notebook), carregue um CSV sujo (`vendas_filial_05_2026-06-15.csv` tem valores negativos):
   ```python
   import pandas as pd
   df = pd.read_csv('../dados_brutos/vendas_filial_05_2026-06-15.csv')
   df.head()
   ```
   - Sem consultar `transform.py`, tente sozinho:
     - Padronizar colunas para snake_case (regex + `.rename()`)
     - Remover linhas 100% em branco
     - Converter `data_venda` tratando múltiplos formatos
     - Filtrar `quantidade <= 0` com WARNING
     - Remover duplicatas por chave natural
   - Compare com `src/transform.py`.

3. **Ponto de atenção (30 min):**
   - O que acontece se o CSV tiver `preco_unitario = "12,50"` (com vírgula)? Teste no seu notebook.
   - Veja como `_parse_decimal_br` em `src/transform.py` resolve isso. Detalhe traiçoeiro: `"1.234,56"` (formato BR com milhar).

**Desafio:** implemente uma regra nova: remover linhas onde `data_venda` cai em **fim de semana** (por alguma regra de negócio hipotética). Onde você colocaria essa regra?

---

### Dia 4 — Load + Idempotência (2h)

**Objetivo:** o coração deste módulo.

1. **Entenda a chave natural (30 min):**
   - Abra `src/load.py` na função `carregar_dataframe`. Localize o `INSERT ... ON CONFLICT (...)`.
   - Pergunta: por que a chave natural é `(filial_codigo, data_venda, cliente_cpf, produto_codigo)`? O que faria com que 2 linhas idênticas fossem tratadas como diferentes?
   - Resposta: se qualquer uma das 4 colunas variar, entra como linha nova.

2. **Teste o bug do CPF NULL (45 min):**
   - Vá em `src/transform.py` e comente a linha `df["cliente_cpf"] = df["cliente_cpf"].fillna("SEM_CPF")`.
   - Rode duas vezes o pipeline com os mesmos arquivos.
   - Você vai ver `total_linhas_fato_vendas` aumentar na segunda execução — isso é o bug.
   - Restaure a linha e teste de novo. Agora fica idempotente.
   - **Aprendizado profundo:** SQL trata `NULL != NULL`. Isso quebra UPSERTs que dependem de colunas nulláveis na chave.

3. **Recrie o UPSERT sozinho (45 min):**
   - Em `meus_estudos/meu_load.py`, escreva uma função que faz UPSERT em uma tabela SQLite simples (2 colunas: id, valor).
   - Rode 10 vezes seguidas o mesmo INSERT — o total tem que ficar em 1.
   - Isso te dá a intuição pura, sem o resto do pipeline atrapalhar.

---

### Dia 5 — Orquestração + Logs (1,5h)

**Objetivo:** costurar tudo.

1. **Leia `src/pipeline.py` (30 min):**
   - Note como ele instancia Extract, Transform e Load como objetos.
   - Note o loop principal: `for res_extract in resultados_extract`.
   - Note os 3 try/except: em cada camada, o erro é capturado e o arquivo movido para `dados_rejeitados/`.

2. **Leia `src/logger.py` (30 min):**
   - Entenda a **hierarquia de loggers**: `pipeline` (raiz) → `pipeline.extract`, `pipeline.transform`, `pipeline.load` (filhos que propagam).
   - Este é um detalhe crítico do módulo `logging` do Python que confunde muita gente.

3. **Faça o pipeline falhar de propósito (30 min):**
   - Introduza um erro no `transform.py` (ex: `raise ValueError("teste")` no meio).
   - Rode o pipeline.
   - Observe: o pipeline **continua** para o próximo arquivo, e o problemático vai para `dados_rejeitados/` com prefixo `ERRO_TRANSFORM_`.
   - Este é o valor da orquestração com fail-safe.

---

### Dia 6 — Cenários de erro extras (1h)

**Objetivo:** pensar em bordas.

1. **Rode os 12 cenários** de `tests/testes_manuais.md`. Anote os que quebram (não deveriam, mas se quebrar você aprende).

2. **Crie um novo cenário** que o pipeline atual NÃO trata bem:
   - Sugestões:
     - CSV com colunas em ordem diferente (Excel bagunçou)
     - CSV com header em português diferente (ex: "Data Venda" em vez de "data_venda")
     - CSV com aspas escapadas de forma exótica
     - CSV com CRLF vs LF misturado
   - Adicione a lógica de tratamento no `transform.py`.
   - Documente o cenário em `tests/testes_manuais.md`.

---

### Dia 7 — Documentação + publicação (1,5h)

**Objetivo:** deixar profissional.

1. **Verifique o `.gitignore` (15 min):**
   - Crie um `.gitignore` no seu repo local excluindo `db/*.db`, `logs/*.log`, `dados_*/*.csv`, `__pycache__/`.
   - Adicione `.gitkeep` vazio em cada pasta que deve permanecer estruturada.

2. **Escreva seu README (30 min):**
   - Use o `README.md` como base, mas escreva com suas palavras.
   - Adicione **um print da execução** rodando no seu terminal (que é bem colorido).

3. **Publique (30 min):**
   - Push no GitHub em `pharma-system/modulo-04-etl/`.
   - Post no LinkedIn com o print colorido do log + diagrama de fluxo.

4. **Bônus: agende (15 min):**
   - No Linux, adicione um cron `*/30 * * * *` para rodar a cada 30 min.
   - No Windows, use o Task Scheduler.
   - Este é o momento onde o pipeline vira **automático de verdade**.

---

## Checklist final

- [ ] Ambiente rodando 1ª execução com sucesso
- [ ] Teste de idempotência: 0 inseridas na 2ª execução ✅
- [ ] Meu extract próprio criado
- [ ] Meu transform próprio criado
- [ ] Bug do CPF NULL entendido a fundo
- [ ] Meu UPSERT SQLite próprio (teste isolado) rodando
- [ ] Um cenário novo de erro implementado
- [ ] README próprio escrito
- [ ] Repo no GitHub
- [ ] Post no LinkedIn

---

## Armadilhas comuns

**"Meu pipeline duplica linhas"** → você provavelmente:
- Está fazendo INSERT normal em vez de INSERT ON CONFLICT
- Ou não tem UNIQUE CONSTRAINT
- Ou tem NULL numa coluna da chave (bug clássico)

**"Meu Latin-1 vira `Anália` embora eu tenha lido em UTF-8"** → o arquivo é `utf-8-sig` mas com caracteres Latin-1 → precisa fallback. Ver `_ler_csv_com_fallback` em `extract.py`.

**"Meu logging duplica cada linha"** → um logger filho está com `propagate=True` E tem handlers próprios. Ou você configurou o root logger. Regra: 1 logger com handlers, os outros só propagam.

**"Preço 12,50 virou NaN"** → não tratou vírgula decimal BR. Ver `_parse_decimal_br`.

**"Não achou arquivo, mas o padrão parece certo"** → `glob` é case-sensitive no Linux. `VENDAS_FILIAL_01.CSV` não casa `vendas_filial_*.csv`.

---

## Recursos gratuitos

- **[Python logging docs](https://docs.python.org/3/library/logging.html)** — profundo mas essencial.
- **[Real Python — Build an ETL Pipeline](https://realpython.com/python-etl/)** — bom overview conceitual.
- **[SQLite ON CONFLICT docs](https://www.sqlite.org/lang_upsert.html)** — a documentação oficial do UPSERT.
- **[PostgreSQL Tutorial — UPSERT](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-upsert/)** — para quando você fizer o upgrade.
- **[Awesome Data Engineering](https://github.com/igorbarinov/awesome-data-engineering)** — repositório de referências.

---

## O que você vai saber ao final

- **Padrão ETL:** as 3 etapas, responsabilidades de cada uma.
- **Idempotência:** UPSERT, chave natural, tratamento de NULL.
- **Robustez:** fail-safe vs fail-loud, tratamento de encoding, formatos variados.
- **Observabilidade:** logging Python com console + arquivo + hierarquia.
- **Config externa:** YAML, expansão de variáveis de ambiente, separação código/dados.
- **SQLite avançado:** `INSERT ... ON CONFLICT`, `CHECK constraints`, `UNIQUE constraints`, timestamps.
- **Design de sistema:** módulos com uma responsabilidade cada, extensibilidade.

Habilidades **muito valorizadas** no mercado — engenharia de dados júnior/pleno praticamente vive disso.

**Bons estudos!**
