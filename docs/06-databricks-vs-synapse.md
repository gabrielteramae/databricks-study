# Azure Databricks vs Azure Synapse Analytics

Pergunta comum de quem estuda dados no ecossistema Azure: os dois "processam dados", então qual usar?

## Origem e foco

**Azure Databricks**: nasceu do Apache Spark, focado em engenharia de dados pesada, processamento distribuído, ciência de dados/ML e notebooks colaborativos multi-linguagem (Python, SQL, Scala, R no mesmo notebook).

**Azure Synapse Analytics**: evolução do Azure SQL Data Warehouse, focado em análise SQL tradicional, integração nativa com Power BI, e um ambiente mais próximo de data warehouse clássico — embora também suporte Spark pools.

## Onde cada um brilha

| Cenário | Melhor opção |
|---|---|
| Pipeline de ETL complexo, transformações pesadas em Python/Spark | Databricks |
| Machine Learning, MLflow, experimentação de modelos | Databricks |
| Notebooks colaborativos multi-linguagem | Databricks |
| Data warehouse SQL tradicional, relatórios corporativos | Synapse |
| Integração direta e nativa com Power BI | Synapse |
| Ambiente de BI self-service para analistas não técnicos | Synapse |

## Na prática, muitas empresas usam os dois juntos

Um padrão comum: **Databricks processa e prepara os dados** (ingestão, limpeza, transformações pesadas, medallion architecture) e grava o resultado final (camada Gold) em formato consumível. **Synapse (ou Power BI direto)** consome essa camada Gold para servir dashboards e relatórios para o time de negócio.

## Overhead de decisão

Não é uma escolha binária excludente na maioria dos casos — é sobre "qual ferramenta faz o quê no pipeline". Databricks tende a vencer quando o volume de dados é grande e as transformações são complexas (múltiplas fontes, lógica de negócio elaborada, ML). Synapse tende a vencer quando o objetivo final é BI tradicional com SQL e a equipe consumidora já vive no ecossistema Microsoft (Power BI, Excel).

## Custo

Ambos cobram por uso (processamento), mas os modelos de billing são diferentes — Databricks por DBU + VM, Synapse por DWU (Data Warehouse Units) ou por Spark pool. Vale sempre simular custo com a calculadora de preços da Azure para o volume de dados real do projeto, em vez de decidir só por reputação da ferramenta.
