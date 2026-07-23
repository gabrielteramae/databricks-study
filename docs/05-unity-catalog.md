# Unity Catalog — governança de dados

## O problema que resolve

Numa empresa com múltiplos workspaces Databricks (ex: um para engenharia, outro para o time de risco, outro para marketing), sem um sistema central de governança, cada workspace gerencia permissões de forma isolada. Isso gera inconsistência: alguém pode acessar dados sensíveis num workspace que não deveria acessar noutro, e não há visão unificada de quem acessou o quê.

## O que o Unity Catalog oferece

### 1. Modelo hierárquico de três níveis
```
Catalog (ex: producao, desenvolvimento)
   └── Schema/Database (ex: vendas, financeiro)
         └── Tabela/View (ex: pedidos_2026)
```
Isso é análogo à hierarquia `banco.schema.tabela` de bancos relacionais tradicionais, mas aplicado ao Lakehouse inteiro.

### 2. Controle de acesso centralizado
Permissões definidas uma vez (via SQL: `GRANT SELECT ON TABLE ... TO grupo_analistas`) valem para todos os workspaces conectados ao mesmo metastore. Isso é essencial em ambiente regulado — controlar exatamente quem acessa dados sensíveis (ex: financeiros, de RH, de clientes) sem precisar repetir a configuração em cada workspace.

### 3. Linhagem de dados (Data Lineage)
O Unity Catalog rastreia automaticamente de onde cada tabela/coluna veio e para onde os dados fluem — útil para auditoria ("esse número no relatório final veio de qual fonte, passando por quais transformações?") e para avaliar impacto antes de mudar uma tabela upstream.

### 4. Auditoria
Registra quem acessou o quê e quando — logs de auditoria centralizados, importante para compliance (LGPD, regulações do Banco Central em contexto financeiro).

### 5. Compartilhamento de dados entre organizações (Delta Sharing)
Protocolo aberto que permite compartilhar tabelas Delta com outra organização sem precisar copiar os dados ou dar acesso à infraestrutura inteira — só a tabela específica, com controle de quem vê o quê.

## Por que isso importa além de "boas práticas"

Em setores regulados (financeiro, saúde, qualquer área com dado sensível), a capacidade de provar quem acessou um dado e rastrear a origem de um número reportado não é opcional — é requisito de compliance. Unity Catalog é a peça do Databricks que endereça isso diretamente.

## Resumo mental

Sem Unity Catalog: cada workspace é uma ilha de permissões. Com Unity Catalog: um único lugar define quem pode acessar o quê, com rastreabilidade completa — essencial à medida que a empresa cresce e mais times/workspaces compartilham os mesmos dados.
