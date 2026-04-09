# Confluence: Multi-Sheet Processing (v0.6.6)

## 🎯 Objetivo
Transformar o Genaja em uma ferramenta capaz de processar Workbooks inteiros, não apenas arquivos isolados.

## 🏗️ Arquitetura de Carga
O `LoaderEngine` foi refatorado para utilizar o parâmetro `sheet_name=None` do Pandas, retornando um dicionário `{sheet_name: DataFrame}`.

### Mudanças no Fluxo de Dados:
1. **WizardState**: Agora armazena `workbook_src` e `workbook_tgt` como objetos persistentes.
2. **Active Sheet**: Introdução de ponteiros para a aba atualmente selecionada para o ETL.
3. **Lazy Learning**: O sistema perfila a aba ativa imediatamente e as outras abas em background/segundo plano para enriquecer a base de conhecimento.

## 🖥️ Interface Platinum
- **Dropdowns Dinâmicos**: Localizados na `Step1View`, aparecem apenas quando o arquivo possui > 1 aba.
- **Auto-Refresh**: Ao trocar de aba, o `FileIntelligenceDialog` é atualizado com o novo perfil sem necessidade de re-upload.

## ✅ Casos de Uso
- Migração de abas específicas de OITM (Itens) para OACT (Contas).
- Consolidação de dados distribuídos em múltiplas planilhas operacionais.

---
*Documento gerado automaticamente pelo Genaja Governance Engine v0.6.7.*
