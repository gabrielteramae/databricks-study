# Databricks notebook source
# MAGIC %md
# MAGIC # 03 - Pipeline Medallion (Bronze → Silver → Gold)
# MAGIC
# MAGIC Simulação de um pipeline de dados de vendas de e-commerce: pedidos brutos,
# MAGIC limpos e agregados numa métrica final de receita por categoria.
# MAGIC
# MAGIC Cada camada é gravada como tabela Delta separada, propositalmente, para permitir
# MAGIC reprocessar qualquer etapa isoladamente.

# COMMAND ----------

from pyspark.sql import Row
from pyspark.sql.functions import col, when, avg, sum as spark_sum, count, round as spark_round, current_timestamp

base_path = "/tmp/delta/medallion_ecommerce"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Camada BRONZE — ingestão bruta
# MAGIC
# MAGIC Simula dados exatamente como chegariam de uma fonte externa: com sujeira proposital
# MAGIC (valores nulos, duplicatas) para depois tratarmos na Silver.

# COMMAND ----------

dados_brutos = [
    Row(pedido_id="PED001", categoria="Eletrônicos", valor=1200.0, quantidade=2),
    Row(pedido_id="PED002", categoria="Eletrônicos", valor=350.0, quantidade=None),  # dado faltante
    Row(pedido_id="PED003", categoria="Livros", valor=89.0, quantidade=3),
    Row(pedido_id="PED003", categoria="Livros", valor=89.0, quantidade=3),  # duplicata
    Row(pedido_id="PED004", categoria="Casa", valor=540.0, quantidade=1),
    Row(pedido_id="PED005", categoria="Beleza", valor=210.0, quantidade=4),
]

df_bronze = spark.createDataFrame(dados_brutos).withColumn("data_ingestao", current_timestamp())

(
    df_bronze.write.format("delta")
    .mode("overwrite")
    .save(f"{base_path}/bronze")
)

print(f"Bronze gravada: {df_bronze.count()} registros (com sujeira proposital)")
df_bronze.show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Camada SILVER — limpeza e validação
# MAGIC
# MAGIC Regras aplicadas aqui:
# MAGIC 1. Remover duplicatas exatas
# MAGIC 2. Descartar registros sem quantidade (dado essencial pro cálculo — não dá para inferir)
# MAGIC 3. Validar que valor é positivo

# COMMAND ----------

df_bronze_lido = spark.read.format("delta").load(f"{base_path}/bronze")

df_silver = (
    df_bronze_lido
    .dropDuplicates(["pedido_id"])
    .filter(col("quantidade").isNotNull())
    .filter(col("valor") > 0)
)

registros_removidos = df_bronze_lido.count() - df_silver.count()
print(f"Bronze: {df_bronze_lido.count()} registros | Silver: {df_silver.count()} | Removidos: {registros_removidos}")

(
    df_silver.write.format("delta")
    .mode("overwrite")
    .save(f"{base_path}/silver")
)

df_silver.show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Camada GOLD — agregação de negócio
# MAGIC
# MAGIC Aqui calculamos métricas prontas para dashboard: receita total e ticket médio por categoria.

# COMMAND ----------

df_silver_lido = spark.read.format("delta").load(f"{base_path}/silver")

df_gold = (
    df_silver_lido
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

(
    df_gold.write.format("delta")
    .mode("overwrite")
    .save(f"{base_path}/gold")
)

df_gold.show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Por que essa separação importa aqui
# MAGIC
# MAGIC Se a regra de negócio da Gold mudar (ex: mudar o threshold de "Alta receita" de 1000 para 800),
# MAGIC só precisamos reprocessar a partir da Silver — não precisamos buscar a fonte de novo
# MAGIC nem refazer a limpeza. Isso é o ganho prático da arquitetura em camadas.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximo passo
# MAGIC
# MAGIC Ver `04_time_travel_demo.py` para simular uma correção de dados e comparar versões
# MAGIC da Gold antes/depois.
