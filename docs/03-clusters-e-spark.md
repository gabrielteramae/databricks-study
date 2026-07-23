# Clusters e Apache Spark — como o processamento distribuído funciona

## Por que "distribuído"

Quando um arquivo tem 500 GB, uma única máquina não processa isso de forma rápida — mesmo com muita RAM, o processamento é sequencial e lento. A solução é dividir o trabalho entre várias máquinas processando em paralelo. É isso que o Apache Spark coordena, e o cluster do Databricks é o conjunto de máquinas onde isso roda.

## Anatomia de um cluster

- **Driver node**: a máquina "coordenadora". Roda seu código principal, decide como dividir o trabalho, e junta os resultados finais. É onde ficam as variáveis Python normais (fora do Spark).
- **Worker nodes (executors)**: as máquinas que efetivamente processam os pedaços de dados em paralelo. Cada worker roda um ou mais "executors", processos que executam as tarefas.

Quando você roda `df.filter(...).groupBy(...).count()`, o Spark:
1. Quebra os dados em **partições** (pedaços)
2. Distribui as partições entre os executors
3. Cada executor processa sua partição em paralelo
4. Os resultados parciais são combinados (shuffle) e devolvidos ao driver

## Lazy evaluation — o conceito que confunde no início

Operações como `.filter()`, `.select()`, `.groupBy()` **não executam nada na hora**. O Spark constrói um plano de execução (DAG — grafo acíclico direcionado) e só processa de verdade quando você chama uma **action** — `.show()`, `.count()`, `.write()`, `.collect()`.

Isso existe porque permite ao Spark **otimizar o plano inteiro antes de rodar** — reordenar filtros para reduzir dados processados, evitar leituras desnecessárias, etc. (o "Catalyst Optimizer").

## Tipos de cluster no Databricks

- **All-purpose cluster**: para uso interativo em notebooks, exploração, desenvolvimento. Fica ligado enquanto você usa (e você paga por isso).
- **Job cluster**: sobe automaticamente quando um Job agendado começa, e desce sozinho ao terminar. Mais barato para pipelines automatizados, porque não fica ocioso.

## Autoscaling

Você define um mínimo e máximo de workers, e o Databricks adiciona/remove máquinas automaticamente conforme a carga de trabalho — evita pagar por capacidade ociosa e evita gargalo em picos de processamento.

## Photon Engine

É o motor de execução otimizado do Databricks (escrito em C++, não em JVM/Scala como o Spark tradicional) que acelera consultas SQL e operações de DataFrame, mantendo compatibilidade com a API do Spark. É uma vantagem competitiva do Databricks sobre "rodar Spark puro você mesmo" em VMs genéricas.

## Custo: DBU

O Databricks cobra em **DBU (Databricks Unit)** — uma unidade de capacidade de processamento — além do custo da VM do Azure por trás. O tipo de cluster (All-purpose custa mais DBU/hora que Job cluster) e o tipo de VM escolhida determinam o custo total.

## Resumo mental

Cluster = conjunto de VMs. Driver coordena, workers processam em paralelo. Lazy evaluation permite otimizar antes de rodar. Job clusters são mais baratos que all-purpose para automação porque não ficam ligados sem necessidade.
