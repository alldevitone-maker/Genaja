# Genaja Pro - Unified Synchronization Intelligence

[🇺🇸 View in English](README.en.md) | [🇧🇷 Visualizar em Português](README.md)

> **Current Version:** `v0.6.1` (Alfa v2)
> **Project Status:** Active - Governance Audit & History Sync 🛡️

---

## 🚀 What is Genaja Pro?

**Genaja Pro** is a premium desktop platform for corporate data analysts who need to **reconcile, map and synchronize data across spreadsheets** — intelligently, without writing code.

Its **JGDA Engine** delivers:
- 🔑 **Intelligent primary key detection** (ID, SKU, CPF, CNPJ, EAN, Employee ID…)
- 🔗 **Semantic column mapping** via similarity heuristics (Simple AI)
- 🛡️ **Safe-Merge with Shielding** — prevents duplicates, ghost records and erroneous cross-joins
- 📦 **Multi-format export** — Excel, CSV, JSON, SQL (Big Data O(1) mode)
- 🎨 **2026 High-Fidelity frameless UI** — Pure PySide6, Custom TitleBar, Live Theme Studio

---

## 🛡️ Governance & Release Pipeline

Every commit and release goes through an automated validation pipeline:

```bash
# Quick validation (before any commit)
python scripts/automate.py --quick

# Full release (interactive: version + changelog + backup + push)
python scripts/automate.py --release --push
```

The pipeline automatically runs:
1. ✅ **Version sync** — `version.py` ↔ `README` ↔ `CHANGELOG` in PT/EN parity
2. ✅ **Smoke Test** — validates critical widget initialization
3. ✅ **File audit** — naming conventions + junk file detection
4. ✅ **Auto backup** — versioned ZIP snapshot in `backups/`
5. ✅ **Git commit & push** — executed only after 100% green validation

> ⚠️ **Pre-commit hook active**: commits are automatically blocked if validation fails.

---

## 📖 Update History (Audit Trail 2026)

<div id="latest-release">

### **v0.6.1 (Alfa v2)**
**The Stabilization Milestone.** This version consolidates the transition to the new reactive architecture, eliminating contrast bugs and ensuring absolute repository governance.
- 🎨 **Theme Stabilization**: Migration to the `PlatinumTheme` dynamic bridge, ensuring perfect legibility in Light mode.
- 🌓 **Intelligent Reactivity**: Automatic luminance calculation for native `ThemeMode` adjustment (OS Context).
- 🧹 **Release Audit**: Purge of technical residuals and private documents for secure public publication.
- ⚖️ **2026 Governance**: Rigorous metadata synchronization across UI, Version, and Docs.

> [!TIP]
> **Client Download:** [Link unavailable during Alpha phase] <!-- Future link here -->

</div>

---

**v0.6.0 (Alpha Platinum - Flet Migration)**
Massive technological transition replacing the PySide6 graphics engine with **Flet (Pure Python Flutter)**, maintaining functional parity with the v0.4.x series. Restoration of the Comparator Module and Dual-List Transfer.

**v0.5.9 (Governance & History Synchronization)**
Audit version focused on project history integrity. Synchronized all v0.5.x milestones across bilingual documentation and certified pre-commit hooks functionality.

**v0.5.8 (Professional Settings Suite)**
We unified Genaja's control. The new **Global Preferences** panel allows managing everything from data engine behavior (Trim/Case) to export and security details, all in a Sidebar-style interface with 2026 High-Fidelity finishing.

**v0.5.6 (Premium Customizer 2026)**
We reached the state-of-the-art in UI customization. The new **Phoenix Customizer 2.0** brings a categorized interface with real-time Preview, allowing fine adjustments with user-friendly names. The QSS v2.2 engine offers premium finishing (16px radius).

**v0.5.5 (Pure Qt Architecture Stabilization)**
Mandatory stabilization milestone. Validated system integrity after the Tkinter "Purge", ensuring a clean and high-performance build for the new PySide6 stack.

**v0.5.4 (Pure Qt Transition)**
Consolidation of modern architecture. Definitively removed Tkinter (Legacy) support and the `--ui` argument, making Genaja a Pure PySide6 application. Massive technical debt reduction.

**v0.5.3 (Modern UI & Premium Design)**
Aesthetic revolution. Implemented a **Custom Title Bar** (VS Code style), removing native Windows decorations for an immersive, frameless experience, along with the new visual theme engine.

**v0.5.2 (Engine Stability Patch)**
Fine-tuning of the heuristic mapping engine and fix for minor visual title bar glitches in maximized mode.

**v0.5.1 (Startup Bugfix & Governance)**
Post-Gold stage focused on stability. Fixed the double-window initialization bug and synchronized the first governance protocols for the v0.5.x cycle.

**v0.5.0 (The Next Frontier - Gold Release)**
The biggest technological evolution in Genaja's history. We implemented a full hybrid architecture (PySide6/Tkinter) with decoupled enterprise engines, 4-step Wizard interface, real-time monitoring dashboard, and Phoenix Qt theme studio.

**v0.4.9 (The Phoenix Absolute Edition)**
Introduction of the **Live Theme Customizer**. Absolute control of colors and styles via graphical interface in real-time for both Tkinter/PySide6 engines.

**v0.4.7 (The Premium Update & Big Data O(1))**
The corporate UI reached Premium status. The system now features a **Floating Tooltips** motor providing visual cues. The entire layout received a **Global Canvas Scroll**. Introduced red "Experimental" frames with Big Data support (`JSON`, `CSV`, `SQL`).

**v0.4.6 (Unified Hub Flex)**
Architecture refactoring joining Genaja into a single super-screen (Single Hub) while preserving classic features. The **Protected A1 Key** button became toggleable via Checkbox.

**v0.4.3 (User Experience & Docs)**
Rebranding of the app's showcase. Added dual-layer structuring (Analyst Manual & IT Technical Docs) with full bilingual parity.

**v0.4.0 (The Era of Auto-Click)**
Manual overhead removal for annotation boxes in favor of native, intelligent transfer selections. Inserted the intelligent cross-filter.

**v0.3.5 (Core Clean Architecture)**
The zero milestone of the new era. Complete refactor into decoupled architecture with a focus on high-performance data processing.
