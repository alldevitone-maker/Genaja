import os
import sys
import pandas as pd
import logging
from datetime import datetime

# 1. ⚓ ANCHORING
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from core.paths import (
    BRAINS_DIR, LEARN_DIR, AUDIT_DIR, 
    SHARED_DIR, RESULTS_DIR, LOGS_MOTOR_DIR,
    JGDA_DIR, ensure_dirs
)
from version import __version__

# 2. SETUP SMOKE LOGGER
ensure_dirs()
smoke_log = os.path.join(LOGS_MOTOR_DIR, f"smoke_test_{__version__.replace('.', '')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(smoke_log, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(f"SMOKE_V{__version__.replace('.', '')}")

def run_test(name, func):
    logger.info(f"--- RUNNING TEST: {name} ---")
    try:
        result = func()
        logger.info(f"--- [PASS] {name} ---")
        return True, result
    except Exception as e:
        logger.error(f"--- [FAIL] {name}: {str(e)} ---")
        return False, None

# --- TEST FUNCTIONS ---

def test_boot_imports():
    from core.engines.loader_engine import LoaderEngine
    from core.engines.etl_engine import ETLEngine
    from core.learning.suggestion_engine import HistoricalSuggestionEngine
    from core.services.audit_service import AuditService
    from core.services.logger_service import LoggerService
    from core.services.config_service import ConfigService
    return "All critical modules imported successfully."

def test_step1_load_local():
    from core.engines.loader_engine import LoaderEngine
    loader = LoaderEngine()
    test_file = os.path.join(JGDA_DIR, "tests", "index", "V2.xlsx")
    if not os.path.exists(test_file):
        raise FileNotFoundError(f"Test file not found: {test_file}")
    
    workbook, headers = loader.load_workbook(test_file)
    sheet_name = list(workbook.keys())[0]
    df = workbook[sheet_name]
    logger.info(f"Loaded {len(df)} rows from {test_file} [{sheet_name}]")
    return df

def test_step3_historical_brain():
    from core.learning.suggestion_engine import HistoricalSuggestionEngine
    # Points to the new BRAINS_DIR
    engine = HistoricalSuggestionEngine(BRAINS_DIR)
    # Mocking col names to see if it reads learn/ data
    cols = ["NOME", "CPF", "DATA"]
    suggestions = engine.get_smart_suggestions(cols, cols)
    logger.info(f"Suggestions fetched from brain: Source={suggestions.get('source')}")
    return suggestions

def test_step4_etl_export():
    from core.engines.etl_engine import ETLEngine
    etl = ETLEngine()
    df_src = pd.DataFrame({"ID": ["1", "2"], "NOME": ["ALPHA", "BETA"]})
    df_tgt = pd.DataFrame({"ID": ["1", "2"], "NOME": ["", ""]})
    mapping = {"NOME": "NOME"}
    
    result = etl.synchronize(df_src, df_tgt, "ID", "ID", mapping)
    
    # Save to shared/results
    out_path = os.path.join(RESULTS_DIR, f"SMOKE_EXPORT_{__version__.replace('.', '')}.xlsx")
    result.to_excel(out_path, index=False)
    logger.info(f"ETL Result exported to: {out_path}")
    return out_path

def test_services_audit_logging():
    from core.services.audit_service import AuditService
    from core.services.logger_service import LoggerService
    
    audit = AuditService()
    audit.record_sync("smoke_src", "smoke_tgt", 100)
    
    motor_log = LoggerService()
    motor_log.info("SMOKE TEST: Verificando persistencia de logs no motor.")
    
    # Check if files created (Check for JSONL instead of JSON)
    import glob
    audit_files = glob.glob(os.path.join(AUDIT_DIR, "audit_*.jsonl"))
    if audit_files:
        logger.info(f"Audit file(s) verified: {len(audit_files)} file(s) found in BRAINS_DIR.")
    else:
        raise FileNotFoundError("Audit file (.jsonl) not created in BRAINS_DIR.")
    return True

def test_backups():
    import subprocess
    # Local Backup
    logger.info("Running Local Backup script...")
    res1 = subprocess.run([sys.executable, os.path.join(JGDA_DIR, "scripts", "make_backup.py")], capture_output=True, text=True)
    if res1.returncode != 0:
        raise Exception(f"Local backup failed: {res1.stderr}")
    
    # Global Backup
    logger.info("Running Global Backup script...")
    global_backup_script = os.path.join(os.path.dirname(JGDA_DIR), "scripts", "make_genaja_backup.py")
    res2 = subprocess.run([sys.executable, global_backup_script], capture_output=True, text=True)
    if res2.returncode != 0:
        raise Exception(f"Global backup failed: {res2.stderr}")
    return "Both backups executed successfully."

# --- MAIN EXECUTION ---

def main():
    results = {}
    
    results["IMPORT_BOOT"] = run_test("Modules Boot", test_boot_imports)
    results["STEP1_LOCAL"] = run_test("Step 1 Load", test_step1_load_local)
    results["STEP3_BRAIN"] = run_test("Step 3 Brain Memory", test_step3_historical_brain)
    results["STEP4_EXPORT"] = run_test("Step 4 ETL Export", test_step4_etl_export)
    results["SERVICES"] = run_test("Audit & Logging Persistence", test_services_audit_logging)
    results["BACKUPS"] = run_test("Backups Connectivity", test_backups)
    
    logger.info("\n" + "="*50)
    logger.info(f"SMOKE TEST SUMMARY v{__version__}")
    logger.info("="*50)
    
    all_pass = True
    for test, (status, _) in results.items():
        mark = "✅" if status else "❌"
        logger.info(f"{mark} {test:20}: {'PASS' if status else 'FAIL'}")
        if not status: all_pass = False
        
    if all_pass:
        logger.info(f"\nCONGRATULATIONS: Runtime v{__version__} is officially stable and valid.")
    else:
        logger.error("\nCRITICAL: Runtime validation failed. Check smoke_stable.log.")
    
    logger.info("="*50)

if __name__ == "__main__":
    main()
