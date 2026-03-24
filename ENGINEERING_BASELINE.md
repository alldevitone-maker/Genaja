# 🛠️ Genaja Engineering Baseline: v0.5.9 Platinum

Este documento serve como guia de orientação rápida para desenvolvedores e agentes de I.A que atuarão no projeto.

## 🏁 Estado da Arte (v0.5.9)
- **Framework**: PySide6 (Pure Qt).
- **Paradigma**: Arquitetura desacoplada (Core Services vs. UI).
- **UI Style**: 2026 High-Fidelity (Frameless, Custom Titlebar, QSS Dynamic).

## 📂 Estrutura de Diretórios
- `src/main.py`: Ponto de entrada (utiliza `AppBootstrap`).
- `src/core/services/`: Motores de inteligência (ETL, Mapping, Config).
- `src/ui_qt/`: Camada visual PySide6.
- `docs/`: Documentação técnica e manuais em paridade (PT / EN).
- `scripts/`: Automação de ciclo de vida (`automate.py`, `make_backup.py`).
- `tests/`: Infraestrutura de QA (`smoke_test.py`).

## ⚙️ Motores Críticos
1. **Config Service v2.0**: Usa `DEFAULTS` em `config_service.py` como schema para `data/genaja_config.json`.
2. **Theme Service**: Centraliza a geração de QSS. Novos widgets DEVEM herdar cores dos tokens disponíveis nos Presets.

## 🛡️ Governança (Must Know)
- **Versionamento**: Sempre sincronizado entre `version.py`, `README` e `CHANGELOG`.
- **Pre-commit**: Rodar `python scripts/automate.py --quick` antes de qualquer commit.
- **Backup**: Snapshots ZIP automáticos no diretório `backups/`.

---
*Assinado: Genaja Core Team (Audit Baseline)*
