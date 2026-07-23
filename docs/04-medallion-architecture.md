# Medallion Architecture (Bronze / Silver / Gold)

## O que é

Não é uma tecnologia — é um **padrão de organização de pipeline de dados** popularizado pela comunidade Databricks. A ideia é estruturar o fluxo de dados em camadas com responsabilidades bem definidas, cada uma sendo uma tabela Delta.

## As três camadas

### Bronze — dado cru
Ingestão dos dados exatamente como vieram da fonte (API, banco, arquivo CSV, streaming), sem transformação além de talvez adicionar metadados (timestamp de ingestão, nome do arquivo de origem). Serve como registro histórico imutável — se algo der errado nas camadas seguintes, sempre dá para reprocessar a partir da Bronze.

### Silver — dado limpo e validado
Aqui acontece: remoção de duplicatas, tratamento de nulos, correção de tipos, validação de schema, joins entre fontes diferentes. O resultado é um dado confiável, mas ainda granular (nível de registro individual), pronto para ser consumido por analistas ou cientistas de dados que precisam do detalhe.

### Gold — dado agregado, pronto para consumo
Agregações de negócio: métricas, KPIs, tabelas já modeladas para dashboards, relatórios ou modelos de ML consumirem diretamente. Ex: "receita total por categoria e mês", em vez de linha a linha de todos os pedidos brutos.

## Por que separar em camadas (e não fazer tudo de uma vez)

1. **Reprocessamento seguro**: se a lógica de limpeza (Silver) tiver um bug, você não perdeu o dado bruto — reprocessa a partir da Bronze sem precisar buscar na fonte de novo.
2. **Times diferentes usam camadas diferentes**: cientista de dados que precisa de granularidade usa Silver; analista de BI usa Gold.
3. **Auditoria e rastreabilidade**: dá para comparar Bronze vs Gold e entender exatamente que transformação foi aplicada em cada etapa até chegar no número final.
4. **Performance**: Gold é pequena e agregada — dashboards consultam ela, não a tabela bruta gigante.

## Fluxo típico

```
Fonte (API, banco, arquivo)
    │
    ▼
BRONZE  (ingestão bruta, append-only, com metadados)
    │  limpeza, deduplicação, schema validation
    ▼
SILVER  (dado confiável, granular)
    │  agregações, joins de negócio, cálculo de métricas
    ▼
GOLD    (pronto para dashboard/relatório/ML)
```

## Onde entra o Delta Lake aqui

Cada camada é uma tabela Delta. Isso permite usar `MERGE INTO` para atualizar a Silver incrementalmente (sem reprocessar tudo), e time travel para comparar versões entre execuções do pipeline.
