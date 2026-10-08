# Databricks Study — lakehouse, Delta e Medallion

![Databricks](https://img.shields.io/badge/Databricks-FF3621?logo=databricks&logoColor=white)
![Apache%20Spark](https://img.shields.io/badge/Apache%20Spark-3.5.0-E25A1C?logo=apachespark&logoColor=white)
![Delta%20Lake](https://img.shields.io/badge/Delta%20Lake-3.1.0-00ADD8?logo=delta&logoColor=white)

Notas e notebooks de estudo sobre Azure Databricks: por que o lakehouse existe, o que o log do Delta Lake garante, como o Spark adia a execução, e um pipeline Bronze → Silver → Gold com dados fictícios de loja e de e-commerce. Unity Catalog e a comparação com o Synapse estão só na documentação; não há código deles aqui. Nada disso é um pipeline de produção.

| Cenário, segundo `docs/06-databricks-vs-synapse.md` | Onde o texto aponta |
| --- | --- |
| ETL pesado em Spark, ML, notebooks multilinguagem | Databricks |
| Warehouse SQL, Power BI nativo, BI para quem não escreve Spark | Synapse Analytics |

## Stack

- PySpark 3.5.0 e delta-spark 3.1.0 (`requirements.txt`)
- notebooks no formato do Databricks (`# Databricks notebook source`, células `# COMMAND ----------`)
- a variável `spark` é a do cluster; os scripts não criam `SparkSession`
- o repositório não fixa a versão do Python

## Estrutura

```
.
├── requirements.txt
├── docs/
│   ├── 01-lakehouse-conceito.md        # warehouse, data lake e o meio-termo
│   ├── 02-delta-lake.md                # ACID, time travel, schema enforcement
│   ├── 03-clusters-e-spark.md          # driver, particao e lazy evaluation
│   ├── 04-medallion-architecture.md    # Bronze, Silver, Gold
│   ├── 05-unity-catalog.md             # catálogo, GRANT e linhagem
│   └── 06-databricks-vs-synapse.md     # quando o texto escolhe cada um
└── notebooks/
    ├── 01_spark_dataframes_intro.py    # filter/groupBy só rodam no show
    ├── 02_delta_lake_basics.py         # overwrite, MERGE e versionAsOf
    ├── 03_medallion_pipeline_demo.py   # vendas sujas até a Gold
    └── 04_time_travel_demo.py          # corrige PED004 e lê a versão 0
```

`02` grava em `/tmp/delta/vendas_lojas`. `03` e `04` usam `/tmp/delta/medallion_ecommerce`. `04` assume que `03` já rodou. Os dados são `Row` montados no próprio notebook (lojas e pedidos `PED001`–`PED005`), com nulo e duplicata de propósito na Bronze.

## Como rodar

```bash
git clone https://github.com/gabrielteramae/databricks-study.git
cd databricks-study
```

No Databricks Community Edition, importe os `.py` de `notebooks/` (o marcador `# COMMAND ----------` vira célula), suba um cluster e rode na ordem 01 → 04. A Community Edition é o ambiente que os próprios notebooks citam.

Localmente, as bibliotecas instalam assim:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Isso não executa os notebooks: eles chamam `spark` e `DeltaTable` sem criar a sessão.

Ordem de leitura que o material pede: doc 01, doc 02, doc 03, notebook 01, notebook 02, doc 04, notebook 03, notebook 04, doc 05, doc 06.

## Testes realizados

Não há suíte de testes.

---

© 2026 Gabriel Teramae Chan
