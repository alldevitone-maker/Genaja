# Security & Compliance — Genaja Context

Este documento descreve a arquitetura de segurança e a conformidade com leis de proteção de dados (LGPD) aplicadas ao ecossistema Genaja.

## 🛡️ Trust Boundaries (Limites de Confiança)

O Genaja opera sob o princípio de **Local-Only Processing**. Todos os dados e a inteligência aprendida permanecem no perímetro físico da máquina do usuário.

| Componente | Localização | Governança |
| :--- | :--- | :--- |
| **Código Fonte** | Repositório Git | Versionado (v0.7.1) |
| **Cognitive Intelligence Store** | `brains/learn/` | **EXCLUÍDO** do Git (Blindagem Master) |
| **Resultados (Excel/SQL)** | `shared/results/` | **EXCLUÍDO** do Git |
| **Logs de Auditoria** | `shared/logs/` | **EXCLUÍDO** do Git |

## ⚖️ Conformidade LGPD (General Data Protection Law)

1. **Privacidade por Design**: O sistema não transmite dados para servidores externos. O treinamento da "Intelligence Layer" é passivo e local.
2. **Minimização de Dados**: A exportação e sincronização manipulam apenas as chaves estritamente necessárias definidas pelo operador.
3. **Credenciais Efêmeras**: Senhas de bancos de dados SQL são tratadas em `runtime_config`, nunca sendo persistidas em arquivos de configuração ou logs de auditoria.

## 🛠️ Blindagem de Repositório

O projeto utiliza um **.gitignore Mestre** centralizado que impede acidentalmente o upload de:
- Arquivos de clientes (`.xlsx`, `.csv`, `.db`).
- Inteligência acumulada (Mapeamentos passados).
- Logs de rastreabilidade ruidosos.

---
*Status: Compliance Audit v0.7.1 Completed.*
