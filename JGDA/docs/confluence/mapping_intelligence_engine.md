# Confluence: Mapping Intelligence Engine (v0.6.7)

## 🎯 Objetivo
Proporcionar automação de mapeamento "Zero-Touch" baseada em densidade estatística e história evolutiva.

## 🧠 Algoritmos de Inferência
O motor agora opera em três níveis de prioridade:

1. **Exact/Historical Match (Alta Confiança)**:
   - Utiliza a assinatura MD5 do contexto da coluna e o histórico de uso.
   - Peso na sugestão: 100%.

2. **Statistical Inference (Média/Alta Confiança)**:
   - Baseado na maratona de 12k+ associações. Identifica que `Código NCM` quase sempre mapeia para `Código` em contextos SAP.
   - Peso na sugestão: 85%.

3. **Fuzzy Profile Match (Média Confiança)**:
   - Combina Levenshtein com o Profiling de dados (v0.6.5).
   - Peso na sugestão: 70%.

## 📊 Métricas da Maratona (v0.6.7-Ultimate)
- **Ciclos de Simulação (Fase 2)**: 1.000.000
- **Relatórios Ingeridos (BigData)**: 1.675
- **Associações Memorizadas**: 1.001.675
- **Densidade de Conhecimento**: 315 colunas primárias (Padrão SAP/Enterprise).
- **Localização do Cérebro**: Pasta visível `learn/` (v0.6.7).

## 🛡️ Data Guard
Mesmo com alta automação, o sistema preserva:
- Zeros à esquerda (Strings vs Ints).
- Tipagem rigorosa detectada no Profiling.

---
*Documento gerado automaticamente pelo Genaja Governance Engine v0.6.7.*
