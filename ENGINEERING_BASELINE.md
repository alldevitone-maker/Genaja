# 🛠️ Genaja Engineering Baseline: v0.6.4

Este documento serve como guia de orientação rápida para desenvolvedores e agentes de I.A que atuarão no projeto.

## 🏁 Estado da Arte (v0.6.1)
- **Framework**: Flet (Pure Python Flutter).
- **Paradigma**: Arquitetura desacoplada (Core Services vs. UI).
- **UI Style**: 2026 High-Fidelity (Frameless, Custom Titlebar, Tokens Dinâmicos).

## 📂 Estrutura de Diretórios
- `src/main.py`: Ponto de entrada (utiliza `AppBootstrap`).
- `src/core/services/`: Motores de inteligência (ETL, Mapping, Config).
- `src/core/learning/`: Motores de aprendizado (Store, Logger, Suggestion).
- `src/ui_flet/`: Camada visual Flet moderna e reativa.
- `docs/`: Documentação técnica e manuais em paridade (PT / EN).
- `scripts/`: Automação de ciclo de vida (`automate.py`, `make_backup.py`).
- `tests/`: Infraestrutura de QA (`test_smoke_flet.py`).

## ⚙️ Motores Críticos
1. **Config Service v2.0**: Usa `DEFAULTS` em `config_service.py` como schema para `data/genaja_config.json`.
2. **Theme Service**: Centraliza a geração de Tokens Dinâmicos. Novos widgets DEVEM herdar cores dos tokens disponíveis nos Presets.

## 🛡️ Governança (Must Know)
- **Versionamento**: Sempre sincronizado entre `version.py`, `README` e `CHANGELOG`.
- **Pre-commit**: Rodar `python scripts/automate.py --quick` antes de qualquer commit.
- **Backup**: Snapshots ZIP automáticos no diretório `backups/`.

---
*Assinado: Genaja Core Team (Audit Baseline v0.6.4)*
