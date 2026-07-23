# Databricks Study
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=flat&logo=databricks&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5-E25A1C?style=flat&logo=apachespark&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-3.1-00ADD8?style=flat)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)

Estudo de conceitos e prática de Azure Databricks: Lakehouse, Delta Lake, Spark e arquitetura Medallion.

## Sobre

Repositório de estudo sobre Azure Databricks, com o objetivo de entender **por que** a plataforma existe e quais problemas reais de engenharia de dados ela resolve — não só decorar comandos. Combina documentação teórica em Markdown com notebooks práticos comentados, rodáveis no Databricks Community Edition.

## Conteúdo

- Conceito de Lakehouse e por que ele existe (Data Warehouse vs Data Lake)
- Delta Lake: transações ACID, schema enforcement, time travel, MERGE
- Clusters e Apache Spark: lazy evaluation, partições, autoscaling
- Arquitetura Medallion (Bronze → Silver → Gold) aplicada num pipeline real
- Unity Catalog: governança e linhagem de dados
- Comparação Azure Databricks vs Azure Synapse Analytics

## Stack

- **Processamento:** Apache Spark (PySpark)
- **Armazenamento:** Delta Lake
- **Ambiente:** Databricks Community Edition
- **Linguagem:** Python

---

## Estrutura

\```
databricks-study/
├── docs/                          # Teoria, conceitos, comparações
│   ├── 01-lakehouse-conceito.md
│   ├── 02-delta-lake.md
│   ├── 03-clusters-e-spark.md
│   ├── 04-medallion-architecture.md
│   ├── 05-unity-catalog.md
│   └── 06-databricks-vs-synapse.md
├── notebooks/                     # Código real, comentado
│   ├── 01_spark_dataframes_intro.py
│   ├── 02_delta_lake_basics.py
│   ├── 03_medallion_pipeline_demo.py
│   └── 04_time_travel_demo.py
└── requirements.txt
\```

## Como rodar localmente

**Pré-requisitos:** conta gratuita em [community.cloud.databricks.com](https://community.cloud.databricks.com)

1. Suba os arquivos `.py` da pasta `notebooks/` — o Databricks reconhece o marcador `# COMMAND ----------` e importa como células separadas automaticamente
2. Suba um cluster (Community Edition tem 1 cluster free, 15GB)
3. Rode as células em ordem

Alternativamente, dá para rodar localmente com PySpark + Delta Lake instalados (ver `requirements.txt`):
\```bash
pip install -r requirements.txt
\```

## Ordem de leitura sugerida

1. `docs/01-lakehouse-conceito.md` — o problema que o Databricks resolve
2. `docs/02-delta-lake.md` — o formato de dados que sustenta tudo
3. `docs/03-clusters-e-spark.md` — como o processamento distribuído funciona
4. `notebooks/01_spark_dataframes_intro.py` — primeira mão na massa
5. `notebooks/02_delta_lake_basics.py` — ACID, time travel na prática
6. `docs/04-medallion-architecture.md` — padrão de organização de dados
7. `notebooks/03_medallion_pipeline_demo.py` — pipeline Bronze → Silver → Gold
8. `notebooks/04_time_travel_demo.py` — versionamento de tabelas
9. `docs/05-unity-catalog.md` — governança de dados
10. `docs/06-databricks-vs-synapse.md` — quando usar cada um no ecossistema Azure
