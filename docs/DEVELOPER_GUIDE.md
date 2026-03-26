# Genaja Developer & Architecture Guide (v0.6.1 Alfa v2)

[🇺🇸 English](DEVELOPER_GUIDE.en.md) | [🇧🇷 Português](DEVELOPER_GUIDE.md)

Este documento contém o registro avançado da infraestrutura sob o capô do Genaja (JGDA) em sua fase **Flet Integration (v0.6.x)**.

## 🏗️ Arquitetura do Software (O Motor JGDA v2.0)

A aplicação segue um modelo de arquitetura desacoplada, garantindo que a lógica de negócio (ETL) seja agnóstica à interface gráfica.

1. **`src/ui_flet/` (Camada Visual):** Implementada exclusivamente em **Flet**. 
   - Utiliza um modelo **Frameless Architecture** com uma barra de título customizada (`TitleBar`).
   - Gerenciamento de temas centralizado via `ThemeService` (QSS Injection).
   - Wizard Stack de 4 passos com transições suaves (QPropertyAnimation).

2. **`src/core/services/` (Motores de Negócio):**
   - **`etl_service.py`**: Motor de processamento vetorial baseado em Pandas. Utiliza operações bit-wise para processamento de alto volume com complexidade O(n).
   - **`mapping_engine.py`**: Lógica heurística para sugestão de Primary Keys e mapeamento de colunas.
   - **`config_service.py` (v2.0)**: Gerenciador de preferências globais com suporte a Schema e valores padrão persistentes.

3. **`src/services/` (Serviços de Integração):**
   - **`excel_loader.py`**: Leitor heurístico de cabeçalhos (`find_best_header`).
   - **`theme_service.py`**: Motor de tokens visuais que gera o design 2026 Premium.

4. **`src/main.py`**: Ponto de entrada que inicializa o `AppBootstrap` e injeta as dependências necessárias nos painéis da UI Flet.

## 🛠️ Trilha de Engenharia (Milestones Técnicos)

### v0.5.4 - Pure Qt Transition (The Purge)
- **Eliminação de Legado**: Remoção completa de 100% das dependências e arquivos do Tkinter.
- **Unificação**: A entrada `--ui` foi extinta, consolidando o ciclo de vida do projeto em uma única stack de alta performance.

### v0.5.6 - Phoenix Customizer 2.0 (Premium)
- **QSS v2.2**: Estilização avançada com 16px radius, glassmorphism e micro-interações.
- **Live Preview**: Integramos um "Mini-App" dentro do editor para feedback instantâneo de design.

### v0.5.8 - Professional Settings Suite
- **Global Config HUD**: Novo diálogo com navegação por Sidebar (QListWidget#sidebar).
- **Schema Persistence**: Implementação de `DEFAULTS` no `ConfigService` para proteção de estado.

## CI/CD & Governança Local
O projeto utiliza um pipeline de validação rigoroso:
- **`scripts/automate.py`**: Centro de comando para validações rápidas (`--quick`) e sincronismo de versão.
- **Pre-commit Hooks**: Impedem o commit se houver discrepância entre `version.py`, `README` e `CHANGELOG`.
- **`scripts/make_backup.py`**: Gerador de snapshots ZIP com nomenclatura SemVer automatizada.

---
*Assinado: Genaja Engineering Protocol v0.6.1 Alfa v2*
