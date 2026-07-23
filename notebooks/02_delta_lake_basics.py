# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Delta Lake na prática
# MAGIC
# MAGIC Objetivo: ver ACID transactions, schema enforcement e time travel funcionando de verdade,
# MAGIC não só na teoria.

# COMMAND ----------

from pyspark.sql import Row

caminho_tabela = "/tmp/delta/vendas_lojas"

dados_v1 = [
    Row(loja="Loja A", vendas=15200.0, mes="Jan"),
    Row(loja="Loja B", vendas=9800.0, mes="Jan"),
    Row(loja="Loja C", vendas=17500.0, mes="Jan"),
]

df_v1 = spark.createDataFrame(dados_v1)

# Grava como tabela Delta (não é só Parquet - cria também o _delta_log)
df_v1.write.format("delta").mode("overwrite").save(caminho_tabela)

print("Tabela Delta criada. Versão 0.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Vendo o log de transações
# MAGIC
# MAGIC Toda escrita gera uma entrada no `_delta_log`. Vamos consultar o histórico da tabela.

# COMMAND ----------

from delta.tables import DeltaTable

delta_tabela = DeltaTable.forPath(spark, caminho_tabela)
delta_tabela.history().select("version", "timestamp", "operation").show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Schema enforcement
# MAGIC
# MAGIC Se tentarmos escrever dados com schema incompatível (coluna faltando, tipo errado),
# MAGIC o Delta rejeita por padrão — isso evita "envenenar" a tabela silenciosamente.

# COMMAND ----------

dados_schema_errado = [Row(loja="Loja D", vendas_errada="não é número")]
df_errado = spark.createDataFrame(dados_schema_errado)

try:
    df_errado.write.format("delta").mode("append").save(caminho_tabela)
except Exception as e:
    print("Escrita rejeitada, como esperado:")
    print(str(e)[:300])

# COMMAND ----------

# MAGIC %md
# MAGIC ## MERGE (upsert) — atualizar sem reescrever a tabela inteira
# MAGIC
# MAGIC Cenário: chegou um dado atualizado de vendas da "Loja A" (fechamento revisado do mês)
# MAGIC e um novo registro da "Loja D". Em vez de reescrever tudo, usamos MERGE.

# COMMAND ----------

dados_novos = [
    Row(loja="Loja A", vendas=15800.0, mes="Jan"),  # atualização
    Row(loja="Loja D", vendas=6200.0, mes="Jan"),  # novo
]
df_novos = spark.createDataFrame(dados_novos)

(
    delta_tabela.alias("destino")
    .merge(df_novos.alias("origem"), "destino.loja = origem.loja")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

spark.read.format("delta").load(caminho_tabela).orderBy("loja").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Time Travel
# MAGIC
# MAGIC Como cada mudança ficou registrada com versão, conseguimos consultar como a tabela
# MAGIC estava ANTES do merge (versão 0).

# COMMAND ----------

df_versao_0 = spark.read.format("delta").option("versionAsOf", 0).load(caminho_tabela)
print("Como a tabela estava na versão 0 (antes do merge):")
df_versao_0.orderBy("loja").show()

print("Como está agora (versão mais recente):")
spark.read.format("delta").load(caminho_tabela).orderBy("loja").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Restaurando uma versão anterior
# MAGIC
# MAGIC Se o merge tivesse sido um erro, dava para reverter com:
# MAGIC ```python
# MAGIC delta_tabela.restoreToVersion(0)
# MAGIC ```
# MAGIC (não executado aqui para preservar o estado para o próximo notebook)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximo passo
# MAGIC
# MAGIC Ver `03_medallion_pipeline_demo.py` para aplicar isso num pipeline Bronze → Silver → Gold completo.
