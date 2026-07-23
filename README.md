# Databricks — Estudo de Conceitos e Prática

Repositório de estudo sobre Azure Databricks: conceitos, arquitetura e notebooks práticos rodados no Databricks Community Edition.

Objetivo: entender **por que** o Databricks existe e resolve problemas reais de engenharia de dados, não só decorar comandos.

## Estrutura

```
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
```

## Como rodar os notebooks

1. Crie uma conta gratuita em [community.cloud.databricks.com](https://community.cloud.databricks.com)
2. Suba os arquivos `.py` da pasta `notebooks/` — o Databricks reconhece o marcador `# COMMAND ----------` e importa como células separadas automaticamente
3. Suba um cluster (Community Edition tem 1 cluster free, 15GB)
4. Rode as células em ordem

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


