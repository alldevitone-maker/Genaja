# Genaja - Intelligent Data Synchronization

[🇺🇸 English](README.en.md) | [🇧🇷 Português](README.md)

Welcome to **Genaja**, your ultimate tool for crossing and sanitizing corporate spreadsheets 100% autonomously and flawlessly.

## 🚀 What Genaja does?
Genaja replaces hours of manual Excel work (complex VLOOKUPs and report sanitization) with a simple 3-step process:
1. **Agile Mapping:** Connects two different spreadsheets based on a common key (Primary Key).
2. **Smart Transfer:** Automatically creates missing columns in one report by pulling data from the other.
3. **Cleaning & Comparator Hub:** The system acts like a Swiss Army knife for tables:
    - A powerful cleaner that drops gaps (null and unused quantities), fixes punctuation, removes invisible extra spaces, and uppercases texts.
    - An extra Comparison Module that precisely evaluates in 1 millisecond all the products/rows that were left out, existing in one base without appearing in the other.

## 🛠️ How to Start
If you already have Python installed and wish to run directly from the repository:
1. Open your terminal in the project folder and install the matrix dependencies:
   ```bash
   pip install pandas openpyxl
   ```
2. Run the Graphical Interface with a single click (or command):
   ```bash
   python src/main.py
   ```

## 📖 Update History (Real-Time Added Value)

> **Current Version:** `v0.4.5` (Enterprise Folder Architecture)  
> **Roadmap Status:** Active - Constant Module Evolution

**v0.4.4 (Internationalization & i18n)**
Global reach unlocked. Added English architectural docs, business manuals, and a dual-language tracking history to embrace global integrations.

**v0.4.3 (User Experience & Docs)**
The app's "showcase" was redesigned. Complex jargon-heavy language was replaced with a business-focused explanation highlighting real-world benefits. Advanced architectural details were isolated for IT analysts.

**v0.4.2 (Pro Comparator)**
Implemented the powerful Tab Hub in the tool. The "Reverse Mapping" comes online, finding items present in external system reports that mysteriously failed to download/exist in your real corporate base, generating highly filtered exports at the click of a button.

**v0.4.1 (Shielding High-Similarity Textual Bases)**
Prevented drastic scenarios where columns like internal codes filled with leading zeros were wiped from prediction reports. This solidifies the locks that prevent you from exporting garbage, thereby securing non-negotiable data.

**v0.4.0 (The Auto-Click Era)**
Removed manual entry boxes in the tool and replaced them with native, smart on-screen transfer selections. Inserted a crossed filter that only removes garbage if strictly useless across all chosen analytical branches.

*(Advanced architectural documentation for analysts and IT is located in the isolated `docs/` folder)*
