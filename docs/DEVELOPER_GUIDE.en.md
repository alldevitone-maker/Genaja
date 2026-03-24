# Genaja Developer & Architecture Guide (v0.5.9)

[🇺🇸 English](DEVELOPER_GUIDE.en.md) | [🇧🇷 Português](DEVELOPER_GUIDE.md)

This document contains the advanced technical record of Genaja's (JGDA) infrastructure in its **Pure Qt (v0.5.x)** phase.

## 🏗️ Software Architecture (The JGDA Engine v2.0)

The application follows a decoupled architectural model, ensuring that Business Logic (ETL) remains agnostic to the Graphical User Interface.

1. **`src/ui_qt/` (Visual Layer):** Implemented exclusively in **PySide6**. 
   - Uses a **Frameless Architecture** model with a custom title bar (`TitleBar`).
   - Centralized theme management via `ThemeService` (QSS Injection).
   - 4-step Wizard Stack with smooth transitions (`QPropertyAnimation`).

2. **`src/core/services/` (Business Engines):**
   - **`etl_service.py`**: Vector processing engine based on Pandas. Uses bit-wise operations for high-volume processing with O(n) complexity.
   - **`mapping_engine.py`**: Heuristic logic for Primary Key suggestion and column mapping.
   - **`config_service.py` (v2.0)**: Global preference manager with Schema support and persistent default values.

3. **`src/services/` (Integration Services):**
   - **`excel_loader.py`**: Heuristic header reader (`find_best_header`).
   - **`theme_service.py`**: Visual token engine generating the 2026 Premium design.

4. **`src/main.py`**: Entry point that initializes `AppBootstrap` and injects dependencies into UI panels.

## 🛠️ Engineering Trail (Technical Milestones)

### v0.5.4 - Pure Qt Transition (The Purge)
- **Legacy Elimination**: Complete removal of 100% of Tkinter dependencies and files.
- **Unification**: The `--ui` argument was retired, consolidating the project lifecycle into a single high-performance stack.

### v0.5.6 - Phoenix Customizer 2.0 (Premium)
- **QSS v2.2**: Advanced styling with 16px radius, glassmorphism, and micro-interactions.
- **Live Preview**: Integrated a "Mini-App" inside the editor for instant design feedback.

### v0.5.8 - Professional Settings Suite
- **Global Config HUD**: New dialogue with sidebar navigation (`QListWidget#sidebar`).
- **Schema Persistence**: Implementation of `DEFAULTS` in `ConfigService` for state protection.

## CI/CD & Local Governance
The project follows a rigorous validation pipeline:
- **`scripts/automate.py`**: Command center for quick validations (`--quick`) and version synchronization.
- **Pre-commit Hooks**: Prevent commits if there's a discrepancy between `version.py`, `README`, and `CHANGELOG`.
- **`scripts/make_backup.py`**: ZIP snapshot generator with automated SemVer naming.

---
*Signed: Genaja Engineering Protocol v0.5.9*
