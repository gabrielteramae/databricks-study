# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Introdução ao Spark DataFrame
# MAGIC
# MAGIC Objetivo: entender a diferença entre **transformations** (lazy) e **actions** (disparam execução real),
# MAGIC e como o Spark distribui o processamento entre partições.
# MAGIC
# MAGIC Rodar num cluster Databricks Community Edition. `spark` já vem disponível automaticamente no notebook.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Criando um DataFrame de exemplo
# MAGIC
# MAGIC Dados fictícios de vendas por loja.

# COMMAND ----------

from pyspark.sql import Row
from pyspark.sql.functions import col, avg, round as spark_round

dados = [
    Row(loja="Loja A", categoria="Eletrônicos", vendas=15200.0, unidades=42),
    Row(loja="Loja B", categoria="Eletrônicos", vendas=9800.0, unidades=27),
    Row(loja="Loja A", categoria="Vestuário", vendas=4300.0, unidades=110),
    Row(loja="Loja C", categoria="Vestuário", vendas=6100.0, unidades=150),
    Row(loja="Loja B", categoria="Alimentos", vendas=21000.0, unidades=830),
    Row(loja="Loja C", categoria="Alimentos", vendas=17500.0, unidades=690),
]

df = spark.createDataFrame(dados)
df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Transformations (lazy) vs Actions
# MAGIC
# MAGIC As linhas abaixo com `.filter()` e `.groupBy()` NÃO executam nada ainda.
# MAGIC O Spark só constrói o plano de execução (DAG). A execução real só acontece
# MAGIC quando chamamos uma **action** como `.show()` no final.

# COMMAND ----------

# Transformation: define o que fazer, não executa ainda
df_filtrado = df.filter(col("vendas") > 5000)

# Transformation: agrupa por categoria e calcula média
df_agregado = (
    df_filtrado
    .groupBy("categoria")
    .agg(
        spark_round(avg("vendas"), 2).alias("media_vendas"),
        spark_round(avg("unidades"), 1).alias("media_unidades"),
    )
    .orderBy(col("media_vendas").desc())
)

# COMMAND ----------

# MAGIC %md
# MAGIC Só agora, no `.show()`, o Spark de fato executa o plano — otimizando antes de rodar
# MAGIC (Catalyst Optimizer decide a ordem mais eficiente de filtrar/agrupar).

# COMMAND ----------

df_agregado.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Explorando o plano de execução
# MAGIC
# MAGIC `.explain()` mostra o plano físico que o Spark gerou — útil para entender
# MAGIC como ele decidiu paralelizar/otimizar a consulta.

# COMMAND ----------

df_agregado.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verificando partições
# MAGIC
# MAGIC Cada DataFrame é dividido em partições, que são distribuídas entre os executors do cluster.
# MAGIC Em datasets pequenos como este, geralmente há poucas partições — o ganho de paralelismo
# MAGIC aparece de verdade em volumes grandes (GBs/TBs).

# COMMAND ----------

print(f"Número de partições: {df.rdd.getNumPartitions()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximo passo
# MAGIC
# MAGIC Ver `02_delta_lake_basics.py` para gravar este DataFrame como tabela Delta
# MAGIC e explorar ACID transactions + time travel.
