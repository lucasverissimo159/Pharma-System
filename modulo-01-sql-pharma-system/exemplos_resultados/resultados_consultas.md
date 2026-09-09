# Resultados das Consultas — PharmaSystem

Este arquivo contém o resultado esperado de cada uma das 25 consultas executadas contra o dataset gerado pelo `02_inserts.sql`.

**Observações importantes:**

- Os valores usam a semente `random.seed(42)` do gerador padrão.
- Se você regenerar os dados com outra semente ou modificar o script, os números vão mudar.
- Algumas consultas usam `CURRENT_DATE` (Q16, Q21, Q22, Q23, etc). Como as datas do dataset vão até 30/06/2026, executar essas consultas em datas diferentes vai produzir resultados levemente diferentes.
- Q18 usa `AGE()` do PostgreSQL — a validação foi feita com uma equivalência aproximada em SQLite; o valor final em PostgreSQL será equivalente.

---

## Q01 — Faturamento total da rede

| faturamento_total | total_vendas |
| --- | --- |
| 224418.17 | 1458 |

---

## Q02 — Faturamento por filial

| codigo | nome | cidade | total_vendas | faturamento |
| --- | --- | --- | --- | --- |
| FIL009 | PharmaMinas Belo Horizonte Savassi | Belo Horizonte | 234 | 42442.11 |
| FIL001 | PharmaMinas Centro Montes Claros | Montes Claros | 184 | 27420.02 |
| FIL010 | PharmaMinas Uberlandia Centro | Uberlandia | 184 | 27362.96 |
| FIL002 | PharmaMinas Todos os Santos | Montes Claros | 166 | 26056.73 |
| FIL003 | PharmaMinas Ibituruna | Montes Claros | 102 | 13926.56 |
| FIL004 | PharmaMinas Major Prates | Montes Claros | 106 | 13446.14 |
| FIL011 | PharmaMinas Diamantina | Diamantina | 58 | 11908.210000000001 |
| FIL007 | PharmaMinas Salinas | Salinas | 58 | 10904.06 |
| FIL014 | PharmaMinas Corinto | Corinto | 60 | 10226.51 |
| FIL013 | PharmaMinas Buritizeiro | Buritizeiro | 57 | 8227.69 |

_(15 linhas no total, mostrando 10 primeiras)_

---

## Q03 — Faturamento mensal (evolucao temporal)

| mes_ano | total_vendas | faturamento | ticket_medio |
| --- | --- | --- | --- |
| 2024-01 | 16 | 1360.73 | 85.05 |
| 2024-02 | 15 | 4393.44 | 292.9 |
| 2024-03 | 20 | 3790.49 | 189.52 |
| 2024-04 | 18 | 3087.76 | 171.54 |
| 2024-05 | 25 | 2870.73 | 114.83 |
| 2024-06 | 18 | 3258.68 | 181.04 |
| 2024-07 | 17 | 2420.7999999999997 | 142.4 |
| 2024-08 | 13 | 2608.5499999999997 | 200.66 |
| 2024-09 | 15 | 2267.7 | 151.18 |
| 2024-10 | 16 | 1366.17 | 85.39 |

_(30 linhas no total, mostrando 10 primeiras)_

---

## Q04 — Ticket medio por filial

| codigo | nome | qtd_vendas | ticket_medio |
| --- | --- | --- | --- |
| FIL011 | PharmaMinas Diamantina | 58 | 205.31 |
| FIL007 | PharmaMinas Salinas | 58 | 188.0 |
| FIL009 | PharmaMinas Belo Horizonte Savassi | 234 | 181.38 |
| FIL012 | PharmaMinas Grao Mogol | 46 | 174.78 |
| FIL014 | PharmaMinas Corinto | 60 | 170.44 |
| FIL002 | PharmaMinas Todos os Santos | 166 | 156.97 |
| FIL001 | PharmaMinas Centro Montes Claros | 184 | 149.02 |
| FIL010 | PharmaMinas Uberlandia Centro | 184 | 148.71 |
| FIL013 | PharmaMinas Buritizeiro | 57 | 144.35 |
| FIL003 | PharmaMinas Ibituruna | 102 | 136.53 |

_(15 linhas no total, mostrando 10 primeiras)_

---

## Q05 — Faturamento por forma de pagamento

| forma_pagamento | qtd_vendas | faturamento | percentual |
| --- | --- | --- | --- |
| CARTAO_CREDITO | 514 | 75582.44 | 33.68 |
| PIX | 368 | 60602.61 | 27.0 |
| CARTAO_DEBITO | 290 | 45959.83 | 20.48 |
| DINHEIRO | 217 | 32148.22 | 14.33 |
| CONVENIO | 69 | 10125.07 | 4.51 |

---

## Q06 — Comparativo de vendas: dia da semana

| dia_num | dia_semana | qtd_vendas | faturamento |
| --- | --- | --- | --- |
| 0 | Domingo | 219 | 32215.71 |
| 1 | Segunda | 216 | 33886.53 |
| 2 | Terca | 222 | 33772.52 |
| 3 | Quarta | 198 | 28100.22 |
| 4 | Quinta | 201 | 37069.52 |
| 5 | Sexta | 215 | 29587.16 |
| 6 | Sabado | 187 | 29786.51 |

---

## Q07 — Taxa de cancelamento por filial

| codigo | nome | total_vendas | canceladas | taxa_cancelamento_pct |
| --- | --- | --- | --- | --- |
| FIL014 | PharmaMinas Corinto | 64 | 4 | 6.25 |
| FIL006 | PharmaMinas Janauba | 41 | 2 | 4.88 |
| FIL005 | PharmaMinas Bocaiuva | 51 | 2 | 3.92 |
| FIL002 | PharmaMinas Todos os Santos | 172 | 6 | 3.49 |
| FIL013 | PharmaMinas Buritizeiro | 59 | 2 | 3.39 |
| FIL011 | PharmaMinas Diamantina | 60 | 2 | 3.33 |
| FIL008 | PharmaMinas Pirapora | 63 | 2 | 3.17 |
| FIL001 | PharmaMinas Centro Montes Claros | 190 | 6 | 3.16 |
| FIL003 | PharmaMinas Ibituruna | 105 | 3 | 2.86 |
| FIL004 | PharmaMinas Major Prates | 109 | 3 | 2.75 |

_(15 linhas no total, mostrando 10 primeiras)_

---

## Q08 — Top 10 produtos mais vendidos (quantidade)

| id | nome | categoria | unidades_vendidas | vendas_com_produto |
| --- | --- | --- | --- | --- |
| 54 | Shampoo Johnsons Baby 200ml | Infantil | 80 | 56 |
| 61 | Perfume Essencial Natura 100ml | Perfumaria | 78 | 57 |
| 69 | Aparelho Pressao Digital Omron | Primeiros Socorros | 78 | 54 |
| 18 | Buscopan Composto 20 comprimidos | Medicamentos de Referencia | 77 | 57 |
| 31 | Papel Higienico Neve 12 rolos | Higiene Pessoal | 75 | 51 |
| 26 | Creme Dental Colgate Total 12 90g | Higiene Pessoal | 74 | 55 |
| 9 | Captopril 25mg 30 comprimidos | Medicamentos Genericos | 73 | 52 |
| 19 | Cimegripe 24 capsulas | Medicamentos Similares | 73 | 52 |
| 1 | Dipirona Sodica 500mg 20 comprimidos | Medicamentos Genericos | 71 | 50 |
| 13 | Advil 400mg 20 comprimidos | Medicamentos de Referencia | 71 | 55 |

---

## Q09 — Top 10 produtos com maior faturamento

| id | nome | categoria | faturamento_produto | unidades_vendidas |
| --- | --- | --- | --- | --- |
| 69 | Aparelho Pressao Digital Omron | Primeiros Socorros | 32752.199999999997 | 78 |
| 61 | Perfume Essencial Natura 100ml | Perfumaria | 16372.2 | 78 |
| 42 | Serum Vitamina C Adcos 30ml | Dermocosmeticos | 13482.9 | 71 |
| 58 | Perfume Malbec Boticario 100ml | Perfumaria | 10329.7 | 53 |
| 41 | Creme Antissinais Vichy 50ml | Dermocosmeticos | 9827.4 | 66 |
| 59 | Perfume Egeo Boticario 90ml | Perfumaria | 9660.0 | 56 |
| 60 | Perfume Kaiak Natura 100ml | Perfumaria | 8544.300000000001 | 57 |
| 43 | Whey Protein Growth 1kg | Suplementos Alimentares | 8325.1 | 49 |
| 44 | Creatina Integralmedica 300g | Suplementos Alimentares | 6896.200000000001 | 58 |
| 38 | Protetor Solar La Roche FPS 60 60ml | Dermocosmeticos | 6428.5 | 65 |

---

## Q10 — Produtos que nunca foram vendidos

_(sem resultados)_

---

## Q11 — Faturamento e margem por categoria

| categoria | produtos_ativos | unidades_vendidas | faturamento | margem_bruta | margem_pct |
| --- | --- | --- | --- | --- | --- |
| Primeiros Socorros | 10 | 605 | 46045.1 | 25231.3 | 54.8 |
| Perfumaria | 4 | 249 | 45813.3 | 24858.600000000002 | 54.26 |
| Dermocosmeticos | 5 | 320 | 39184.0 | 21106.300000000003 | 53.86 |
| Suplementos Alimentares | 8 | 460 | 29621.6 | 16091.4 | 54.32 |
| Medicamentos de Referencia | 8 | 493 | 19260.8 | 10458.3 | 54.3 |
| Infantil | 7 | 444 | 16231.2 | 8894.1 | 54.8 |
| Medicamentos Genericos | 10 | 654 | 13701.4 | 7384.0 | 53.89 |
| Higiene Pessoal | 10 | 609 | 11813.4 | 6392.799999999999 | 54.11 |
| Cosmeticos | 5 | 270 | 5651.2 | 3212.7 | 56.85 |
| Medicamentos Similares | 4 | 250 | 4944.5 | 2702.7 | 54.66 |

---

## Q12 — Produtos que exigem receita medica - Top vendas

| nome | fabricante | unidades_vendidas | faturamento |
| --- | --- | --- | --- |
| Captopril 25mg 30 comprimidos | Medley | 73 | 744.5999999999999 |
| Losartana Potassica 50mg 30 comprimidos | EMS | 70 | 1386.0 |
| Sertralina 50mg 30 comprimidos | Eurofarma | 63 | 3143.7 |
| Amoxicilina 500mg 21 capsulas | Medley | 57 | 2274.2999999999997 |
| Metformina 850mg 30 comprimidos | Neo Quimica | 56 | 980.0 |
| Sinvastatina 20mg 30 comprimidos | EMS | 49 | 1367.1 |

---

## Q13 — Ranking de fabricantes por faturamento

| fabricante | qtd_produtos | unidades_vendidas | faturamento | pct_faturamento |
| --- | --- | --- | --- | --- |
| Omron | 1 | 78 | 32752.199999999997 | 14.46 |
| Natura | 2 | 135 | 24916.5 | 11.0 |
| Boticario | 2 | 109 | 19989.7 | 8.82 |
| Adcos | 1 | 71 | 13482.9 | 5.95 |
| Growth | 2 | 104 | 10739.6 | 4.74 |
| P&G | 6 | 322 | 9954.300000000001 | 4.39 |
| Vichy | 1 | 66 | 9827.4 | 4.34 |
| Integralmedica | 1 | 58 | 6896.200000000001 | 3.04 |
| Kimberly | 2 | 133 | 6777.7 | 2.99 |
| La Roche | 1 | 65 | 6428.5 | 2.84 |

_(44 linhas no total, mostrando 10 primeiras)_

---

## Q14 — Distribuicao de preco de venda por categoria (estatisticas)

| categoria | qtd_produtos | preco_min | preco_medio | preco_max | desvio_padrao |
| --- | --- | --- | --- | --- | --- |
| Perfumaria | 4 | 149.9 | 181.8 | 209.9 | 0.0 |
| Dermocosmeticos | 5 | 71.9 | 118.82 | 189.9 | 0.0 |
| Suplementos Alimentares | 8 | 28.5 | 67.05 | 169.9 | 0.0 |
| Primeiros Socorros | 10 | 9.5 | 63.05 | 419.9 | 0.0 |
| Medicamentos de Referencia | 8 | 24.5 | 38.4 | 62.9 | 0.0 |
| Infantil | 7 | 8.5 | 36.2 | 76.9 | 0.0 |
| Medicamentos Genericos | 10 | 8.9 | 21.47 | 49.9 | 0.0 |
| Cosmeticos | 5 | 7.9 | 21.02 | 42.5 | 0.0 |
| Medicamentos Similares | 4 | 17.2 | 20.02 | 22.5 | 0.0 |
| Higiene Pessoal | 10 | 4.9 | 19.33 | 34.5 | 0.0 |

---

## Q15 — Top 10 clientes por valor gasto

| id | nome | cidade | total_compras | total_gasto | ticket_medio |
| --- | --- | --- | --- | --- | --- |
| 31 | Kaique Barbosa Martins | Buritizeiro | 8 | 2871.4 | 358.93 |
| 20 | Gabriela Rodrigues Oliveira | Montes Claros | 6 | 2455.53 | 409.26 |
| 45 | Tatiana Rodrigues Ferreira | Diamantina | 8 | 2370.8 | 296.35 |
| 81 | Debora Cardoso Dias | Pirapora | 7 | 2365.25 | 337.89 |
| 200 | Heloisa Machado Machado | Salinas | 6 | 2346.9700000000003 | 391.16 |
| 183 | Patricia Lopes Silva | Belo Horizonte | 7 | 2303.2 | 329.03 |
| 91 | Sabrina Souza Rodrigues | Bocaiuva | 8 | 2254.37 | 281.8 |
| 117 | Carla Gomes Silva | Espinosa | 13 | 2233.58 | 171.81 |
| 94 | Camila Martins Araujo | Januaria | 11 | 2152.0 | 195.64 |
| 42 | Camila Machado Carvalho | Belo Horizonte | 6 | 2123.7 | 353.95 |

---

## Q16 — Clientes inativos ha mais de 90 dias

| id | nome | telefone | email | ultima_compra | dias_inativo |
| --- | --- | --- | --- | --- | --- |
| 160 | Camila Gomes Rodrigues | (38) 96015-3736 | camila.gomes160@yahoo.com.br | 2025-04-14 08:23:00 | 452 |
| 182 | Larissa Carvalho Ribeiro | (38) 91291-2681 | larissa.carvalho182@yahoo.com.br | 2025-08-29 10:14:00 | 315 |
| 124 | Otavio Martins Ferreira | (34) 94056-8303 | otavio.martins124@yahoo.com.br | 2025-08-30 16:12:00 | 314 |
| 30 | Vinicius Pereira Lima | (38) 97932-7176 | vinicius.pereira30@hotmail.com | 2025-09-03 21:20:00 | 310 |
| 62 | Vinicius Cardoso Mendes | (38) 92494-2559 | vinicius.cardoso62@yahoo.com.br | 2025-09-29 20:00:00 | 284 |
| 71 | Rodrigo Almeida Costa | (34) 92195-1273 | rodrigo.almeida71@hotmail.com | 2025-10-21 08:52:00 | 262 |
| 116 | Giovana Nascimento Martins | (31) 98855-4695 | giovana.nascimento116@yahoo.com.br | 2025-10-23 10:27:00 | 260 |
| 149 | Tatiana Lima Almeida | (38) 91578-4111 | tatiana.lima149@yahoo.com.br | 2025-10-23 17:56:00 | 260 |
| 46 | Mariana Correia Martins | (34) 99056-7809 | mariana.correia46@yahoo.com.br | 2025-10-26 19:20:00 | 257 |
| 92 | Camila Freitas Alves | (34) 95341-2964 | camila.freitas92@outlook.com | 2025-10-27 17:28:00 | 256 |

_(20 linhas no total, mostrando 10 primeiras)_

---

## Q17 — Distribuicao de clientes por cidade

| cidade | estado | qtd_clientes | percentual |
| --- | --- | --- | --- |
| Curvelo | MG | 18 | 9.0 |
| Uberlandia | MG | 17 | 8.5 |
| Corinto | MG | 16 | 8.0 |
| Januaria | MG | 16 | 8.0 |
| Diamantina | MG | 15 | 7.5 |
| Pirapora | MG | 15 | 7.5 |
| Grao Mogol | MG | 14 | 7.0 |
| Janauba | MG | 14 | 7.0 |
| Belo Horizonte | MG | 13 | 6.5 |
| Sao Francisco | MG | 13 | 6.5 |

_(15 linhas no total, mostrando 10 primeiras)_

---

## Q18 — Faixa etaria dos clientes

| faixa_etaria | qtd_clientes | percentual |
| --- | --- | --- |
| 1. Ate 24 anos | 35 | 17.5 |
| 2. 25 a 34 | 41 | 20.5 |
| 3. 35 a 44 | 23 | 11.5 |
| 4. 45 a 59 | 49 | 24.5 |
| 5. 60+ anos | 52 | 26.0 |

---

## Q19 — Produtos com estoque critico (abaixo do minimo)

| filial | cidade | produto | estoque_atual | estoque_minimo | reposicao_necessaria |
| --- | --- | --- | --- | --- | --- |
| FIL001 | Montes Claros | Sabonete Dove Original 90g | 0 | 30 | 30 |
| FIL006 | Janauba | Sabonete Dove Original 90g | 1 | 30 | 29 |
| FIL010 | Uberlandia | Sabonete Dove Original 90g | 3 | 30 | 27 |
| FIL009 | Belo Horizonte | Escova Dental Oral B Indicator | 1 | 25 | 24 |
| FIL011 | Diamantina | Sabonete Dove Original 90g | 6 | 30 | 24 |
| FIL009 | Belo Horizonte | Fio Dental Colgate 50m | 2 | 25 | 23 |
| FIL006 | Janauba | Escova Dental Oral B Indicator | 3 | 25 | 22 |
| FIL011 | Diamantina | Fio Dental Colgate 50m | 4 | 25 | 21 |
| FIL013 | Buritizeiro | Sabonete Johnsons Baby 80g | 4 | 25 | 21 |
| FIL001 | Montes Claros | Sabonete Johnsons Baby 80g | 5 | 25 | 20 |

_(158 linhas no total, mostrando 10 primeiras)_

---

## Q20 — Valor total do estoque por filial

| codigo | nome | cidade | total_unidades | valor_estoque_custo | valor_estoque_venda |
| --- | --- | --- | --- | --- | --- |
| FIL013 | PharmaMinas Buritizeiro | Buritizeiro | 5492 | 146610.4 | 321799.1 |
| FIL015 | PharmaMinas Curvelo | Curvelo | 5381 | 138675.4 | 304120.4 |
| FIL004 | PharmaMinas Major Prates | Montes Claros | 5583 | 137438.5 | 300596.7 |
| FIL008 | PharmaMinas Pirapora | Pirapora | 5173 | 136291.6 | 298775.8 |
| FIL010 | PharmaMinas Uberlandia Centro | Uberlandia | 4790 | 129317.6 | 283896.4 |
| FIL011 | PharmaMinas Diamantina | Diamantina | 4728 | 125233.7 | 274488.8 |
| FIL003 | PharmaMinas Ibituruna | Montes Claros | 5391 | 124906.4 | 273988.7 |
| FIL014 | PharmaMinas Corinto | Corinto | 5880 | 122027.6 | 267909.7 |
| FIL007 | PharmaMinas Salinas | Salinas | 5512 | 120690.4 | 264621.7 |
| FIL009 | PharmaMinas Belo Horizonte Savassi | Belo Horizonte | 5086 | 117319.3 | 256960.8 |

_(15 linhas no total, mostrando 10 primeiras)_

---

## Q21 — Cobertura de estoque (dias de venda restantes)

| nome | estoque_rede | media_venda_diaria | dias_de_cobertura |
| --- | --- | --- | --- |
| Esmalte Risque 8ml | 649 | 0.13 | 4868.0 |
| Pomada para Assadura Hipoglos 45g | 1071 | 0.21 | 5073.0 |
| Creme Antissinais Vichy 50ml | 1047 | 0.2 | 5235.0 |
| Perfume Kaiak Natura 100ml | 996 | 0.19 | 5273.0 |
| Paracetamol 750mg 20 comprimidos | 869 | 0.16 | 5586.0 |
| Mascara de Cilios Maybelline | 752 | 0.13 | 5640.0 |
| Shampoo Johnsons Baby 200ml | 1030 | 0.18 | 5794.0 |
| Alcool 70% 500ml | 1034 | 0.18 | 5816.0 |
| Losec 20mg 28 capsulas | 1237 | 0.21 | 5859.0 |
| Aparelho Pressao Digital Omron | 965 | 0.14 | 6681.0 |

_(20 linhas no total, mostrando 10 primeiras)_

---

## Q22 — Ranking de filiais por mes (Window Function)

| mes_ano | codigo | filial | faturamento | ranking |
| --- | --- | --- | --- | --- |
| 2026-06 | FIL009 | PharmaMinas Belo Horizonte Savassi | 4052.6 | 1 |
| 2026-06 | FIL010 | PharmaMinas Uberlandia Centro | 1875.97 | 2 |
| 2026-06 | FIL002 | PharmaMinas Todos os Santos | 1766.98 | 3 |
| 2026-06 | FIL007 | PharmaMinas Salinas | 1480.8700000000001 | 4 |
| 2026-06 | FIL013 | PharmaMinas Buritizeiro | 1470.7 | 5 |
| 2026-06 | FIL001 | PharmaMinas Centro Montes Claros | 1456.05 | 6 |
| 2026-06 | FIL005 | PharmaMinas Bocaiuva | 1172.5 | 7 |
| 2026-06 | FIL004 | PharmaMinas Major Prates | 1166.54 | 8 |
| 2026-06 | FIL003 | PharmaMinas Ibituruna | 1018.83 | 9 |
| 2026-06 | FIL012 | PharmaMinas Grao Mogol | 855.7 | 10 |

_(90 linhas no total, mostrando 10 primeiras)_

---

## Q23 — Crescimento mes a mes (comparativo com mes anterior)

| mes_ano | faturamento | faturamento_mes_anterior | variacao_absoluta | crescimento_pct |
| --- | --- | --- | --- | --- |
| 2024-01 | 1360.73 | NULL | NULL | NULL |
| 2024-02 | 4393.44 | 1360.73 | 3032.7099999999996 | 222.87 |
| 2024-03 | 3790.49 | 4393.44 | -602.9499999999998 | -13.72 |
| 2024-04 | 3087.76 | 3790.49 | -702.7299999999996 | -18.54 |
| 2024-05 | 2870.73 | 3087.76 | -217.0300000000002 | -7.03 |
| 2024-06 | 3258.68 | 2870.73 | 387.9499999999998 | 13.51 |
| 2024-07 | 2420.7999999999997 | 3258.68 | -837.8800000000001 | -25.71 |
| 2024-08 | 2608.5499999999997 | 2420.7999999999997 | 187.75 | 7.76 |
| 2024-09 | 2267.7 | 2608.5499999999997 | -340.8499999999999 | -13.07 |
| 2024-10 | 1366.17 | 2267.7 | -901.5299999999997 | -39.76 |

_(30 linhas no total, mostrando 10 primeiras)_

---

## Q24 — Media movel de 3 meses do faturamento

| mes_ano | faturamento | media_movel_3m |
| --- | --- | --- |
| 2024-01 | 1360.73 | 1360.73 |
| 2024-02 | 4393.44 | 2877.09 |
| 2024-03 | 3790.49 | 3181.55 |
| 2024-04 | 3087.76 | 3757.23 |
| 2024-05 | 2870.73 | 3249.66 |
| 2024-06 | 3258.68 | 3072.39 |
| 2024-07 | 2420.7999999999997 | 2850.07 |
| 2024-08 | 2608.5499999999997 | 2762.68 |
| 2024-09 | 2267.7 | 2432.35 |
| 2024-10 | 1366.17 | 2080.81 |

_(30 linhas no total, mostrando 10 primeiras)_

---

## Q25 — Analise de cesta: produtos frequentemente vendidos juntos

| produto_a | produto_b | vendas_juntos |
| --- | --- | --- |
| Voltaren Emulgel 60g | Buscopan Composto 20 comprimidos | 6 |
| Creme Antissinais Vichy 50ml | Perfume Malbec Boticario 100ml | 6 |
| Complexo B Sundown 30 comprimidos | Cafeina Growth 60 capsulas | 6 |
| Cafeina Growth 60 capsulas | Algodao 100g | 6 |
| Dipirona Sodica 500mg 20 comprimidos | Multigrip 20 capsulas | 5 |
| Paracetamol 750mg 20 comprimidos | Multigrip 20 capsulas | 5 |
| Omeprazol 20mg 28 capsulas | Whey Protein Growth 1kg | 5 |
| Amoxicilina 500mg 21 capsulas | Creme Dental Colgate Total 12 90g | 5 |
| Losartana Potassica 50mg 30 comprimidos | Termometro Digital Geratherm | 5 |
| Sertralina 50mg 30 comprimidos | Papel Higienico Neve 12 rolos | 5 |

_(15 linhas no total, mostrando 10 primeiras)_

---
