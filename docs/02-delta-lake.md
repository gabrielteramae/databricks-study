# Delta Lake — o coração técnico do Databricks

## O que é, tecnicamente

Delta Lake não é um banco de dados separado. É um **formato de arquivo** construído em cima do Parquet, acompanhado de um **log de transações** (a pasta `_delta_log/`) que registra toda alteração feita na tabela.

Quando você escreve numa tabela Delta, o Databricks não sobrescreve arquivos direto — ele:
1. Escreve novos arquivos Parquet
2. Registra no log de transações (formato JSON) o que mudou: quais arquivos foram adicionados/removidos
3. Só depois de o log confirmar, a mudança é considerada "commitada"

Isso é o que garante propriedades ACID em cima de um sistema de arquivos que originalmente não tinha isso.

## As funcionalidades que isso destrava

### 1. Transações ACID
Sem Delta, se dois processos escrevem no mesmo diretório de um data lake ao mesmo tempo, o resultado pode corromper dados (leituras parciais, arquivos conflitantes). Com Delta, cada escrita é atômica — ou completa inteira, ou não acontece, mesmo com múltiplos processos concorrentes.

### 2. Time Travel
Como cada mudança fica registrada no log de transações com um número de versão, você consegue consultar a tabela como ela estava em qualquer ponto do passado:

```sql
SELECT * FROM tabela VERSION AS OF 5
SELECT * FROM tabela TIMESTAMP AS OF '2026-01-15'
```

Isso é útil para auditoria (rastrear por que um valor mudou), debugging de pipelines, e reverter erros (`RESTORE TABLE tabela TO VERSION AS OF 5`).

### 3. Schema Enforcement e Evolution
Por padrão, o Delta rejeita uma escrita se o schema dos dados não bater com o schema da tabela — isso evita que um pipeline quebrado "envenene" a tabela com dados errados silenciosamente. Quando a mudança de schema é intencional (ex: nova coluna), você habilita `mergeSchema` explicitamente.

### 4. Upserts eficientes (MERGE)
Data lakes tradicionais eram só append-only (só adicionar, nunca atualizar) porque atualizar um arquivo Parquet exigia reescrever o arquivo inteiro. Delta permite `MERGE INTO` — atualizar, inserir ou deletar registros de forma eficiente, essencial para sincronizar tabelas com fontes que mudam (ex: cadastro de clientes).

### 5. Otimização de performance
- **Compaction (`OPTIMIZE`)**: data lakes acumulam muitos arquivos pequenos ao longo do tempo (cada escrita gera novos arquivos), o que deixa a leitura lenta. O comando `OPTIMIZE` compacta arquivos pequenos em arquivos maiores.
- **Z-Ordering**: reorganiza fisicamente os dados dentro dos arquivos para acelerar filtros em colunas específicas.
- **Vacuum**: remove arquivos antigos não mais referenciados (após um período de retenção), liberando espaço.

## Analogia prática

Pensa no Delta Lake como um "Git para tabelas de dados": cada commit (escrita) fica registrado, você pode ver o histórico, reverter, e o sistema garante que ninguém corrompe o estado ao escrever ao mesmo tempo.

## Onde isso aparece no dia a dia de um pipeline

No padrão Medallion (ver `04-medallion-architecture.md`), cada camada — Bronze, Silver, Gold — é uma tabela Delta. O time travel permite comparar a Silver de hoje com a de ontem; o MERGE permite atualizar a Gold incrementalmente sem reprocessar tudo.
