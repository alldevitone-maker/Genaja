# Changelog

## [0.7.0] - 2026-04-02 (Universal Connector Strategy)
- **Universal Connector Foundation**: BaseConnector implementation and ETL engine decoupling.
- **SQL Database Connector**: Native SQLAlchemy 2.0 support with data streaming (Memory-Safe).
- **Registry Pattern Factory**: ConnectorFactory refactoring for dynamic adapter registration.
- **Wizard UI SQL Sprint**: New Step 1 with source selector, schema/table discovery, and safe preview.
- **Architecture v0.7 Patch**: Consolidation of architecture intelligence in the `.agent/` directory.

## [0.6.9-Master] - 2026-03-27 (Master Curated Strategy)
- **Master Curated Layer**: Introduction of `CuratedStore` for 'Iron-Clad' rule persistence (Priority 0).
- **Priority Orchestration**: Overhaul of the suggestion engine (Curated > MegaBrain > History > Fuzzy).
- **Auto-Promotion Logic**: `brain_feed.py` now automatically promotes mature mappings (Score >= 20).
- **Master Rules Persistence**: New deterministic database in `learn/curated/master_rules.json`.

## [0.6.8-Master] - 2026-03-27 (Master Agent Execution Protocol)
- **Master Agent Protocol**: Deep sanitation and learning orchestration protocol implementation.
- **Probabilistic Brain v2**: Dynamic weighting and state classification system (OBSERVED to CONFIRMED).
- **Brain Inbox (Sanitation Pipeline)**: `learn/inbox` flow for secure ingestion of external dirty datasets.
- **Pollution Filter**: Automatic quarantine mechanism for generic or suspicious mapping patterns.
- **Automation Toolkit**: Launch of `brain_feed.py` (Orchestrator) and `sanitation_hook.py` (Cleaner).

## [0.6.7-Ultimate] - 2026-03-27 (Marathon Analysis Release)
- **Ultimate Marathon Phase 2**: Massive consolidation of **1,001,675 learned associations**.
- **Brain Migration**: Centralization of Genaja's "Brain" in the visible `learn/` repository folder.
- **Statistical Mapping Inference**: Refined inference engine with 315 primary columns density.
- **Elite Performance**: 1 million stochastic cycles executed in 74 seconds.
- **Unified Governance**: Full synchronization of `v0.6.5`, `v0.6.6`, and `v0.6.7` tags with final audit.

## [0.6.6] - 2026-03-27 (Multi-Sheet Processing)
- **Multi-Sheet Loader**: Native support for reading all Excel Workbook sheets (`sheet_name=None`).
- **Iteration Layer**: Loop processing for independent sheet validation and profiling.
- **UI Flexibility**: Dynamic sheet selection in `Step1View` (Flet v0.82.2 compatibility).

## [0.6.5] - 2026-03-27 (Profiling Engine)
- **Data Profiling Layer**: Statistical content analysis (avg_len, unique_ratio) to reduce false positives.
- **Smart Suggestion v2**: Integration of structural profiles into the suggestion heuristics.

## [0.6.4] - 2026-03-26 (Evolution Memory Release)
- **Evolution Memory Layer**: Introduction of local learning persistence.
- **Learning Store**: Secure metadata storage in `learning_log.json`.
- **Signature Matching**: Context identification via column signatures.
- **Usage Tracking**: Suggestion prioritization based on usage frequency.
- **Local AI**: Intelligent suggestions based on previous executions.

## [0.6.3] - 2026-03-26 (Data Intelligence Layer)
- **Core Engines**: Implementation of `ValidationEngine`, `LookupEngine`, and `SchemaMapper`.
- **UI Intelligence**: Creation of `FileIntelligenceDialog` and `CompatibilityDialog`.
- **Fuzzy Mapping**: Support for editorial similarity (Levenshtein).

## [0.6.2] - 2026-03-26 (Cleanup)
- **Legacy Purge**: Permanent removal of the `src/legacy/ui_qt/` directory.
- **Theme Optimization**: Purged `get_qss()` from `ThemeService`.
- **Reorganization**: Created `/scripts/tools/` for development utilities.
- **QA Archive**: Archiving obsolete parity tests in `/tests/archive/`.
- **Documentation**: Engineering Baseline updated for Flet Stateless stack.

## [0.6.1] - 2026-03-26 (Alfa v2)
- **Architectural Freeze**: Final stabilization of the dynamic theme bridge.
- **Release Audit**: Cleanup of development residuals and private documents.
- **Governance**: Standardization of metadata and rigorous versioning.
- **UX**: Contrast refinement and reactivity in the Platinum Shell.

## [0.6.0] - 2026-03-25 (Alpha Platinum - Flet Migration & v0.4.x Parity)
- **Flet Migration**: 100% Flet architecture (v0.82.2+) with Lifecycle-Safe Router.
- **v0.4.6/0.4.7 Parity**: Restoration of Dual-List Transfer, Row Rules, and Structural Rules.
- **v0.4.8 Engine**: Integration of `ValidationEngine` and robust Numeric Filter.
- **Comparator Module**: Restoration of pure comparison mode (source vs destination).
- **Multi-Format Export**: Integrated support for Excel, CSV, JSON, and SQL.
- **UI UX**: Added v0.4.7 tooltips and Platinum visual stabilization.

## [0.5.9] - 2026-03-24 (Governance & History Synchronization)
- **Consolidated History**: Complete reconstruction of the v0.5.x audit trail in the README (PT/EN).
- **Audit Build**: Metadata synchronization and pre-commit hooks certification.
- **Document Parity**: Strict alignment between CHANGELOG and README for corporate compliance.

## [0.5.8] - 2026-03-24 (Professional Settings Suite)
- **Settings HUD 2026**: New global settings interface with sidebar navigation and categorized panels.
- **Config Engine v2.0**: Refactored `ConfigService` with Schema support, default values, and robust persistence.
- **Engine Control**: Added toggles for Auto-Trim, Auto-Upper, and Case-Sensitivity in data merging.
- **Export Preferences**: Visual interface to define formats, timestamps, and auto-opening of files.
- **UI Governance**: Integration of dynamic application title based on user settings.

## [0.5.6] - 2026-03-24 (Premium Customizer 2026)
- **Phoenix Customizer 2.0**: Complete SaaS Pro-style redesign with category tabs (Styles, Identity, Elements).
- **Interactive Preview Card**: Added a mini-app preview inside the editor that reflects colors in real-time.
- **User-Friendly Naming**: Replaced technical names (bg_col) with friendly ones (Main Background) in the settings interface.
- **Premium QSS v2.2**: Improved outlines (16px), simulated shadows, and modern tab styling.
- **Visual Stability**: Fixed visual artifacts in Light Grey SaaS mode.

## [v0.5.5] - 2026-03-24 (Pure Qt Architecture Stabilization)
- **v0.5.4 Refinement**: Stability adjustments following the Tkinter decommissioning.
- **Silent Homologation**: Smoke tests validated for the new Pure Qt directory tree.
- **2026 Ready**: Metadata cleanup for the upcoming Designer Suite.

## [v0.5.4] - 2026-03-24 (Pure Qt Transition)
- **Tkinter Decommissioning**: Total and definitive removal of v0.4.x legacy code (`ui_tk` folder).
- **Pure Entrypoint**: Refactored `main.py` and `AppBootstrap` for zero-redundancy, operating exclusively on PySide6.
- **Architecture Cleanup**: Eliminated over 250 lines of obsolete code and dead callbacks.
- **Governance Unification**: v0.5.x lifecycle now focused on a single high-performance tech stack.

## [v0.5.3] - 2026-03-24 (Modern UI & Premium Design)
- **Custom Title Bar**: Replaced native Windows title bar with a theme-integrated bar (VS Code/Slack style).
- **Frameless Architecture**: Clean, integrated window 100% controlled by Genaja's graphics engine.
- **Theme Engine 2.0**: Introduction of **Official Presets** (Zinc Studio, Phoenix Dark, Light Grey SaaS).
- **Phoenix Customizer 2.0**: Redesigned HUD with visual grouping, friendly color pickers, and enhanced live preview.
- **Visual Decoupling**: `MainWindow` is now visually blind, consuming 100% of identity via `ThemeService` tokens.
- **v0.5.3 Governance**: Validation pipeline updated to certify the new frameless architecture.

## [v0.5.1] - 2026-03-24 (The Next Frontier - v0.5.1 Bugfix)
- **White Window Fix**: Technical adjustment in Tkinter initialization to prevent double-root instantiation.
- **Metadata Synchronization**: Global standardization of version tags in compliance with the Governance Protocol.
- **Bootstrap Stabilization**: Refinement in UI selection logic (Qt as default).

## [v0.5.0] - 2026-03-23 (The Next Frontier - Gold Release)
- **Hybrid Infrastructure**: Implementation of dual architecture (PySide6/Tkinter).
- **Enterprise Engines**: Decoupling Business Logic (ETL, Mapping, Validation) from the Visual layer.
- **Real-Time Dashboard**: New progress monitor with corporate performance metrics.
- **Phoenix Qt Studio**: Dynamic theme engine with JSON persistence.
