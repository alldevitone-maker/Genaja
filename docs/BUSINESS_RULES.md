# Regras de Negócio e Lógica ETL - Genaja

Este documento descreve as regras de inteligência aplicadas pelo motor ETL do Genaja (JGDA Engine).

## 1. Mapeamento Semântico (AI Key Suggestion)
O sistema varre as primeiras 10.000 linhas de cada planilha e calcula a intersecção de valores únicos.
- **Critério**: Sugere as 3 colunas com maior taxa de coincidência.
- **Segurança**: Bloqueia o processamento se a intersecção for ZERO, evitando cruzamentos errôneos que destruiriam os dados.

## 2. Limpeza e Sincronização
- **Normalização de Chaves**: Todas as chaves primárias são convertidas para `string`, removendo `.0` (comum em Excel) e espaços em branco (`strip`).
- **Safe-Merge**: Ao unir tabelas, colunas com nomes idênticos no destino recebem um sufixo temporário e são descartadas em favor da versão da origem, evitando duplicação indesejada.
- **Tratamento de Nulos**: Colunas mapeadas são preenchidas com string vazia ou `0` (se numéricas) antes do processamento.

## 3. Filtros de Blindagem
- **Shielding Zeros**: Os itens com valor `0` ou `NaN` em colunas numéricas críticas podem ser removidos da base final para evitar "fantasmas" no estoque/relatório.
- **Trim & Case**: Espaços extras são removidos e, se ativado, todos os textos são convertidos para CAIXA ALTA (Upper Case).

## 4. Exportação
- **O(1) Engine**: Otimizado para Big Data.
- **SQL Rápido**: Gera comandos `INSERT INTO` nativos para integração direta com bancos de dados.
- **Excel/CSV/JSON**: Formatos padrão corporativos.
