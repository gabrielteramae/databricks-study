# Databricks notebook source
# MAGIC %md
# MAGIC # 04 - Time Travel aplicado: auditando uma correção de dados
# MAGIC
# MAGIC Cenário: depois de publicado o relatório com a tabela Gold, descobrimos que
# MAGIC o valor do pedido PED004 (categoria Casa) estava errado na fonte — o valor
# MAGIC correto é diferente. Precisamos corrigir e conseguir provar, em auditoria,
# MAGIC qual era o número antes e depois da correção.
# MAGIC
# MAGIC Pré-requisito: rodar `03_medallion_pipeline_demo.py` antes deste notebook.

# COMMAND ----------

from pyspark.sql.functions import col
from delta.tables import DeltaTable

base_path = "/tmp/delta/medallion_ecommerce"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Estado da Gold ANTES da correção

# COMMAND ----------

df_gold_antes = spark.read.format("delta").load(f"{base_path}/gold")
print("Gold antes da correção:")
df_gold_antes.show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Corrigindo a Silver com MERGE
# MAGIC
# MAGIC A correção entra na Silver (fonte de verdade granular), não direto na Gold —
# MAGIC senão a Gold fica dessincronizada da Silver.

# COMMAND ----------

delta_silver = DeltaTable.forPath(spark, f"{base_path}/silver")

from pyspark.sql import Row
correcao = spark.createDataFrame([
    Row(pedido_id="PED004", categoria="Casa", valor=890.0, quantidade=1)
])

(
    delta_silver.alias("destino")
    .merge(correcao.alias("origem"), "destino.pedido_id = origem.pedido_id")
    .whenMatchedUpdate(set={"valor": "origem.valor"})
    .execute()
)

print("Silver corrigida. Histórico de versões da Silver:")
delta_silver.history().select("version", "timestamp", "operation").show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reprocessando a Gold a partir da Silver corrigida
# MAGIC
# MAGIC Como a Gold é derivada, não editamos ela diretamente — recalculamos a partir da Silver.
# MAGIC Isso é o benefício direto de ter separado as camadas.

# COMMAND ----------

from pyspark.sql.functions import when, avg, sum as spark_sum, count, round as spark_round

df_silver_corrigida = spark.read.format("delta").load(f"{base_path}/silver")

df_gold_depois = (
    df_silver_corrigida
    .groupBy("categoria")
    .agg(
        count("pedido_id").alias("qtd_pedidos"),
        spark_round(spark_sum("valor"), 2).alias("receita_total"),
        spark_round(avg("valor"), 2).alias("ticket_medio"),
    )
    .withColumn(
        "classificacao",
        when(col("receita_total") > 1000, "Alta receita")
        .when(col("receita_total") > 300, "Média receita")
        .otherwise("Baixa receita"),
    )
    .orderBy(col("receita_total").desc())
)

df_gold_depois.write.format("delta").mode("overwrite").save(f"{base_path}/gold")

print("Gold DEPOIS da correção:")
df_gold_depois.show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Auditoria: provando a mudança com time travel
# MAGIC
# MAGIC Mesmo já tendo sobrescrito a Gold, o log de transações da Silver preserva a versão
# MAGIC anterior. Conseguimos provar exatamente qual era o valor do PED004 antes da correção.

# COMMAND ----------

# Versão 0 = Silver original (antes da correção)
df_silver_v0 = spark.read.format("delta").option("versionAsOf", 0).load(f"{base_path}/silver")

print("Valor de PED004 ANTES (versão 0 da Silver):")
df_silver_v0.filter(col("pedido_id") == "PED004").show()

print("Valor de PED004 DEPOIS (versão atual da Silver):")
df_silver_corrigida.filter(col("pedido_id") == "PED004").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Por que isso importa na prática
# MAGIC
# MAGIC Numa auditoria de dados, não basta corrigir o valor — é preciso conseguir
# MAGIC responder "qual era o número reportado, quando mudou, e por quê". O log de
# MAGIC transações do Delta Lake dá essa rastreabilidade sem precisar de nenhum
# MAGIC processo manual de versionamento por fora.
