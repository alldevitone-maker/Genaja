# Genaja Developer & Architecture Guide

[🇺🇸 English](DEVELOPER_GUIDE.en.md) | [🇧🇷 Português](DEVELOPER_GUIDE.md)

This document contains the advanced tracking of Genaja's underlying infrastructure (JGDA).

## 🏗️ Software Architecture (The JGDA Engine)

The tool was designed by separating heavy Database logic from Graphical User Visualization (MVC inspired).

1. **`ui/genaja_ui.py` (Tactile View):** The entire application is drawn by blocks managed by the built-in `tkinter` package with the `ttk` styler wrapper. A `Hub` dynamically controls which Frames to load (`pack(fill=tk.BOTH)` and `pack_forget()`) depending on which "state" or "active module" was triggered by arrows and callbacks.  
2. **`services/etl_service.py` (ETL Controller):** Works heavily based on vectorization tied to `Pandas`. Deletions are performed by instantiating simultaneous Boolean matrices for parallel bit-wise comparison (`not_zero & valid_str % not_null`) avoiding catastrophic row loops (iterating `iterrows()`). 
3. **`services/excel_loader.py` (Heuristic Reader):** Uses advanced identification techniques (`isinstance(str)`) scanning the top 20 layers to locate "True Headers", bypassing the native Pandas error when reading merged blocks (`Unnamed: N`). Extraction relies on strict volume count of textual strings per row.
4. **`Main.py`**: Switcher and class instantiator. Receives the packed orders into a UI dictionary (`get_inputs()`) to avoid argument spaghetti and branches execution (if-else/switch) for the services corresponding to the instantiated UI Container modules.

## Local CI/CD Workflow
As the project does not have native cloud GitHub Actions (yet), versioning runs on a protected manual pipeline:
- Unit blind test: Developers test injections with the `smoke_test.py` script. This code guarantees commutative imports, undetectable syntax caching, and OS Encoding.
- Upon returning `sys.exit(0)`, `make_backup.py` is called silently backstage generating physical snapshots based on the clean directory to `backups/v_title.zip`.
- Release: Release creation is automated running interactive `python release.py` in the terminal. This script performs Regex on the Landing Page, file tree scanning, and injects `git commit/tag/push` autonomously preventing desyncs in the Branch-Tag tree.

---

## 🛠️ Engineering Commits Log (Technical Version History)

### v0.4.4 - Internationalization & i18n
- **Localization:** Cloned all markdown documents splitting them via `.en.md` suffix. Badges generated across files for dynamic routing. i18n implementation.

### v0.4.3 - Architectural Docs Refactoring (UX/Docs)
- **Docs:** Language bifurcation: explicit creation of `DEVELOPER_GUIDE.md` (This document you are reading right now), extracting pure logical jargon from the root `README.md`. The goal was cleaning the Changelog to make it a corporate release record, isolating raw stack documentation.

### v0.4.2 - Pro Comparator & Auto-Hub 
- **Refactoring:** `genaja_ui.py` interface modified with dynamic modular Views inside reusable `f3_container` wrappers featuring button state transitions with `hasattr`.
- **Feature:** Implemented `process_data_comparison` wrapper inside the Pandas engine in `etl_service`, resolving inter-dataframe disparities using pure iterable set logic: `missing_keys = set(df_src_cmp[key_src]) - set(df_tgt_cmp[key_tgt])` (Generic C Anti-Join native to CPython set for maximum algorithmic efficiency).
- **Bugfix (Heuristic Header Loader):** Radical change in `find_best_header()`. Formerly governed by "max cols dropna()", generating false-positives if a data row had more numbers filled than the merged header row. Changed to "sum of `isinstance(string)` cells" combined with bottom-header structure verification (>= score) to prioritize the last dual-header row (e.g., ignoring overlying sub-titles like in native SAP reports).
- **UI API Refactoring:** SAP/Simplesweb parametrically renamed in text vars and `.get()` dictionaries in `main.py` to agnostic Origin (`df_origem`) and Target (`df_destino`).

### v0.4.1 - ETL Filtering Fix & Encoding 
- **Bugfix (Engine):** The routine responsible for obliterating garbage iterables filled with nulls (`clean_empty_quantities_multi`), lacked native numeric validation because it was checked with a hardcoded String bit array `(s != '0.0')`. Fixed by casting via proxy method `pd.to_numeric()`, evaluating strict native 0s and extending protection to unintentional false-zeros read as text in Excel, keeping `000100` and other PKs in the database.
- **Bugfix (Console):** Resolved failing `cp1252` encoding prints and emojis crashing `release.py` Popen/Stdout pipes on Windows, ensuring forced UTF-8 in the process host.

### v0.4.0 - O(1) Mapping and Multibox
- **UI Rewrite:** Scrapped the heavy and dangerous Text Entry mechanics where the User had to paste columns and implemented the dynamic `tk.Listbox` model tied to the auto-detected payload in `read_excel`. Responsive search via `trace_add()` binding.
- **Expandable Logic Engine:** The row filter previously accepted strict 1x1 checks. Through a dynamic bitwise loop, it became cumulable. Table deletion is crossed by an OR Conditional matrix.

### v0.3.9 - Smart Headers Inception
- Created Auto Detection pre-wrapper functionality. Introduced the 20-row iterable method to calculate `non_nulls > max_non_nulls` expelling corrupted Unnamed nan's common in direct web exports. 
- Included "VSCode Dark" Theme, overriding TK frames.

### v0.3.8 - Expanded Synchronization
- Main architecture (`process_data_synchronization`) rewritten, evolving from the in-place Update model to Left Join (`.join()`) capturing dynamic unfolded columns from dataframe 2 to DF1.

### v0.3.1 to v0.3.7 - Compliance and Py Transition
- Versions where core stability was isolated from original scripts to protect against data bleeding and the engine was modularized from legacy spaghetti created outside the IDE. Birth of SemVer title-based backups for CI. Compliance applied in ignore and isolated tree map.
