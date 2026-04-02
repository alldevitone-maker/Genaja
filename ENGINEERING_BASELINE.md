# Genaja Engineering Baseline — v0.7.0

Guia de referência para desenvolvedores e agentes de IA atuando no projeto.

## Stack Atual

- **Framework UI:** Flet (Python)
- **Python:** 3.10+
- **Dependências principais:** pandas, sqlalchemy>=2.0, openpyxl, flet>=0.82

## Arquitetura por Camadas

```
UI (Flet Wizard)
    ↓
WizardState (estado centralizado da sessão)
    ↓
ConnectorFactory (Registry Pattern)
    ↓
BaseConnector → PandasAdapter | DatabaseConnector
    ↓
ETLEngine (neutro — recebe DataFrames independente da fonte)
```

O ETLEngine não conhece a origem dos dados. Toda resolução de fonte é feita pela ConnectorFactory antes de chegar ao motor.

## Estrutura de Diretórios

- `src/main.py` — ponto de entrada
- `src/app/wizard_state.py` — estado da sessão (WizardState)
- `src/core/connectors/` — BaseConnector, DatabaseConnector
- `src/core/services/` — ConnectorFactory, ETLEngine, ConfigService, AuditService
- `src/core/learning/` — histórico de mapeamentos (offline)
- `src/core/engines/` — ValidationEngine, MappingEngine
- `src/adapters/` — PandasAdapter (fonte local)
- `src/ui_flet/` — views do Wizard (Step 1–4), tema, roteamento
- `scripts/` — automate.py, validate.py, make_backup.py
- `tests/` — smoke test, testes de conector, validação de lógica de UI

## Regras de Implementação

1. **Novos conectores** devem herdar `BaseConnector` e registrar-se via `ConnectorFactory.register_connector()`.
2. **A UI não acessa adaptadores diretamente** — toda resolução passa pela ConnectorFactory.
3. **Credenciais SQL** são separadas em `source_config_safe` (persistível) e `source_config_runtime` (senha, ephemeral). Nunca serializar runtime.
4. **Novos widgets** devem usar tokens de cor do `PlatinumTheme` — sem hardcode de valores hexadecimais.
5. **Preview SQL:** limitado a 100 linhas na etapa de seleção (Step 1). Carga completa apenas no processamento final.

## Governança

- Versionamento: `version.py` ↔ `README` ↔ `CHANGELOG` (PT e EN) sempre em sincronia
- Validação: `python scripts/automate.py --quick` antes de qualquer commit
- Backup: snapshots ZIP automáticos em `backups/` a cada release
- `.agent/` é pasta de instrução interna — nunca entra no repositório (excluída no `.gitignore`)

---
*Baseline atualizado: v0.7.0 — 02/04/2026*
