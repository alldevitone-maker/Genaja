# 🛡️ PROTOCOLO DE ENGENHARIA E GOVERNANÇA GENAJA (v0.5.8)

Este documento resume como o desenvolvimento do Genaja é blindado contra falhas e como mantemos a paridade entre código, design e documentação.

## 1. Versão Atual e Título
> **Versão:** `0.5.6`
> **Título:** `Premium Customizer 2026`

## 2. Padrões de Código
- **GUI:** PySide6 (Pure Qt).
- **Core:** Motores desacoplados em `src/core/services/`.
- **Temas:** Centralizados em `ThemeService`.

## 3. Fluxo de Lançamento (Release Flow)
1. **Desenvolvimento:** Mudanças em `src/`.
2. **Atualização de Versão:** Sincronizar `version.py`, `README.md` e `CHANGELOG.md`.
3. **Validação:** Rodar `scripts/automate.py --quick`.
4. **Backup:** Gerar ZIP via `scripts/make_backup.py`.
5. **Commit/Push:** Só após validação bem-sucedida.

## 4. Smoke Test Obrigatório
Monitorar carregamento dos widgets críticos:
- MainWindow
- TitleBar
- MappingPanel
- SummaryPanel
- ThemeEditor

---
*Assinado: Motor de Governança Genaja.*
