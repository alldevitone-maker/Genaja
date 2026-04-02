# Genaja — ETL and Data Synchronization

[🇺🇸 View in English](README.en.md) | [🇧🇷 Visualizar em Português](README.md)

> **Current Version:** `v0.7.0` (Universal Connector Strategy)
> **Status:** Stable — Python / Flet / SQLAlchemy

---

## About

Genaja is a data integration and synchronization tool built in Python with a Flet interface.
Designed for corporate analysts, it supports column mapping, data transformation, and multi-format export across Excel spreadsheets and relational databases — without writing code.

The ETL engine is fully decoupled from the interface. The UI operates via `WizardState` → `ConnectorFactory` → adapters, ensuring the ETLEngine receives only DataFrames regardless of the original data source.

---

## Features

- Column mapping with Levenshtein similarity (fuzzy matching)
- Automatic primary key detection via entropy (ID, SKU, CPF, CNPJ)
- Mapping suggestions based on local execution history (offline, no cloud)
- Excel workbook support with multi-sheet selection
- Statistical data profiling to reduce false positives in mapping
- Relational database connectivity via SQLAlchemy 2.0 (PostgreSQL, MySQL, SQLite)
- Export to Excel, CSV, JSON, and SQL
- 4-step Wizard interface with real-time preview

---

## Governance and Release Pipeline

```bash
# Quick validation before any commit
python scripts/automate.py --quick

# Full release: version + changelog + backup + push
python scripts/automate.py --release --push
```

The pipeline runs:
1. Version sync — `version.py` ↔ `README` ↔ `CHANGELOG` (PT/EN parity)
2. Smoke Test — module import and critical service initialization
3. File audit — naming conventions and temporary file detection
4. Auto backup — versioned ZIP snapshot in `backups/`
5. Git commit and push — executed only after full green validation

> **Pre-commit hook active:** commits are blocked if validation fails.

---

## Version History

### v0.7.0 — Universal Connectors (2026-04-02)

Introduction of the extensible connector layer via Registry Pattern.

- `DatabaseConnector`: PostgreSQL, MySQL, SQLite support via SQLAlchemy 2.0
- `ConnectorFactory`: dynamic adapter registration with no UI coupling
- Wizard Step 1: source selector (local file vs SQL database) with schema discovery
- Preview capped at 100 rows during selection step (memory protection)
- Ephemeral credentials: passwords never persisted in serialized state or logs

### v0.6.9-Master — Deterministic Curation (2026-03-27)

- `CuratedStore`: rule layer with absolute priority over probabilistic suggestions
- Auto-promotion of mappings scoring >= 20 to permanent rules

### v0.6.8-Master — Agent Protocol (2026-03-27)

- Secure data ingestion pipeline via `learn/inbox/`
- Automated repository sanitation script (`sanitation_hook.py`)

### v0.6.7 — Marathon Analysis (2026-03-27)

- Consolidation of 1,001,675 learned associations with statistical weights
- Learning history migrated to `learn/` (visible in the repository)

### v0.6.6 — Multi-Sheet Support (2026-03-27)

- Full Excel workbook reading (`sheet_name=None`)
- Dynamic sheet selection in Step 1 interface

### v0.6.5 — Profiling Engine (2026-03-27)

- Statistical analysis of `dtype`, `unique_ratio`, and `avg_len` per column
- Noisy column filtering before mapping suggestion

### v0.6.4 — Evolution Memory (2026-03-26)

- Local mapping history persistence in `learning_log.json`
- Context identification via column signatures (MD5)

### v0.6.3 — Data Intelligence Layer (2026-03-26)

- `ValidationEngine`, `LookupEngine`, and `SchemaMapper` implemented
- `FileIntelligenceDialog` and `CompatibilityDialog` added to UI
- Fuzzy matching via Levenshtein distance

### v0.6.2 — Cleanup (2026-03-26)

- Removal of legacy layer `src/legacy/ui_qt/`
- Script reorganization and archiving of obsolete tests

### v0.6.1 — Alpha v2 Stabilization (2026-03-26)

- Migration to `PlatinumTheme`: dynamic color and contrast tokens
- Automatic luminance calculation for `ThemeMode` adjustment
- Release audit: removal of private documents before publication

---

### Earlier Versions

**v0.6.0** — Flet migration (Python Flutter). Functional parity with v0.4.x series. Comparator module and Dual-List Transfer restored.

**v0.5.9** — History synchronization and pre-commit hook certification.

**v0.5.8** — Global settings panel (Trim/Case, export, security).

**v0.5.6** — Phoenix Customizer 2.0: theme editor with real-time preview.

**v0.5.5** — Stabilization after Tkinter removal.

**v0.5.4** — Complete removal of Tkinter support. Pure PySide6 application.

**v0.5.3** — Custom Title Bar (VS Code style), visual theme engine.

**v0.5.2** — Heuristic mapping engine fixes.

**v0.5.1** — Double window initialization bug fix.

**v0.5.0** — PySide6/Tkinter hybrid architecture, 4-step Wizard, real-time dashboard.

**v0.4.9** — Live Theme Customizer.

**v0.4.7** — Floating tooltips, global scroll, experimental Big Data support (JSON, CSV, SQL).

**v0.4.6** — Single Hub with Protected A1 Key via checkbox.

**v0.4.3** — Dual-layer documentation (Analyst / IT) with bilingual parity.

**v0.4.0** — Intelligent cross-filter and native transfer selections.

**v0.3.5** — Full refactor into decoupled architecture.

---

*Detailed technical documentation available in `docs/`.*
