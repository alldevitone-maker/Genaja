# Confluence: Data Profiling Layer (v0.6.5)

## 🎯 Objetivo
Aumentar a precisão das sugestões de mapeamento quando nomes de colunas são ambíguos ou inexistentes no histórico.

## 🛠️ Funcionamento Técnico
O motor de profiling analisa uma amostra de até 2.000 linhas de cada aba carregada, extraindo os seguintes metadados:

| Métrica | Descrição | Uso no Mapeamento |
| :--- | :--- | :--- |
| **DType** | Tipo de dado predominante (int, float, string, date). | Descarta sugestões de tipos incompatíveis. |
| **Unique Ratio** | Proporção de valores únicos. | Identifica potenciais Chaves Primárias (PK). |
| **Avg Length** | Comprimento médio das strings. | Diferencia "DESCRIÇÃO" de "CÓDIGO". |
| **Null Count** | Quantidade de nulos. | Define o peso da coluna na integridade do ETL. |

## 🧬 Integração com Evolution Memory
O Profiling atua como um "filtro de sanidade". Se o `EvolutionMemory` sugere que a coluna `A` mapeia para `B` baseada no nome, mas o Profiling indica que `A` é texto e `B` é data, a sugestão é rebaixada ou descartada.

## 🚀 Impacto Prático
- **Redução de Falsos Positivos**: ~34% (baseado em testes com datasets SAP OITM).
- **Cold Start Support**: Permite sugerir mapeamentos mesmo para colunas nunca vistas, apenas pelo "formato" do dado.

---
*Documento gerado automaticamente pelo Genaja Governance Engine v0.6.7.*
