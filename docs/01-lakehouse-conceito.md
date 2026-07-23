# O que é o Lakehouse (e por que o Databricks existe)

## O problema histórico

Por décadas, empresas tiveram que escolher entre dois modelos de arquitetura de dados:

### Data Warehouse
- Dados estruturados, com schema definido antes de gravar
- Rápido para consultas de BI/relatórios
- Caro para armazenar grandes volumes
- Rígido: dados semiestruturados (JSON, logs) ou não estruturados (imagens, texto) não cabem bem
- Exemplos: Teradata, Oracle, SQL Server tradicional

### Data Lake
- Armazena qualquer tipo de dado, em qualquer formato, barato (storage tipo S3/ADLS)
- Schema-on-read: você decide a estrutura só na hora de ler, não de gravar
- Problema: sem controle de qualidade, sem transações, sem versionamento — vira o "data swamp" (pântano de dados). Arquivos corrompidos por escritas simultâneas, dados duplicados, sem histórico confiável.

Resultado prático: empresas mantinham as duas coisas em paralelo. Data Lake para dados brutos e ML, Data Warehouse para BI confiável. Isso significa pipelines de ETL duplicados, dados dessincronizados entre os dois sistemas, e custo dobrado.

## A proposta do Lakehouse

Databricks (criado pelos autores originais do Apache Spark) propôs unir as duas coisas: armazenamento barato de data lake + confiabilidade transacional de data warehouse, na mesma camada.

Isso é possível através do **Delta Lake** (ver `02-delta-lake.md`): um formato de arquivo que roda em cima do storage barato (Parquet + log de transações) e adiciona:

- Transações ACID (atomicidade, consistência, isolamento, durabilidade)
- Schema enforcement e evolution
- Versionamento e time travel
- Suporte tanto para BI (SQL) quanto para ML (Python/Spark) na mesma tabela

## Por que isso importa na prática

Antes: analista de BI usa o Data Warehouse, cientista de dados usa o Data Lake, e os dois trabalham com versões diferentes da "verdade" dos dados.

Com Lakehouse: uma única fonte de dados serve os dois times, com a mesma tabela Delta sendo consultada via SQL (BI) ou via DataFrame do Spark (ML/engenharia), sempre com garantia de consistência.

## Onde o Azure entra

Azure Databricks é a versão do Databricks integrada nativamente ao Azure — ele roda os clusters sobre VMs do Azure e usa o **Azure Data Lake Storage (ADLS) Gen2** como camada de armazenamento. A integração nativa facilita autenticação via Azure AD (Entra ID), conexão com Azure Data Factory para orquestração, e Unity Catalog para governança.

## Resumo mental

| | Data Warehouse | Data Lake | Lakehouse (Databricks) |
|---|---|---|---|
| Custo de storage | Alto | Baixo | Baixo |
| Confiabilidade transacional | Alta | Baixa | Alta (via Delta Lake) |
| Tipos de dado | Estruturado | Qualquer | Qualquer |
| Uso típico | BI/relatórios | ML/dados brutos | Ambos |
