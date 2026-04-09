import sys
import os

# --- ENVIRONMENT CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(0, SRC_DIR)

def run_flet_smoke_test():
    from version import __version__
    print("-" * 50)
    print(f"GENAJA FLET PLATINUM AUDIT: SMOKE TEST ({__version__})")
    print("-" * 50)
    
    try:
        # 1. Validate CORE Bootstrap
        from app.bootstrap import AppBootstrap
        bootstrap = AppBootstrap()
        print("[OK] Bootstrap & Core Services initialized.")

        # 2. Validate Flet UI Components
        import flet as ft
        from ui_flet.main import main as flet_main
        from ui_flet.theme import PlatinumTheme
        print("[OK] Flet UI Modules: Imported successfully.")

        # 3. Validate Theme Tokens (Platinum Harmony)
        if not hasattr(PlatinumTheme, 'PRIMARY') or not str(PlatinumTheme.PRIMARY()).startswith("#"):
            raise Exception("PlatinumTheme: Primary color token invalid or missing.")
        print("[OK] PlatinumTheme: Visual tokens validated.")

        # 4. Validate Mapping Engine (O(1) Data Layer)
        from core.engines.mapping_engine import MappingEngine
        engine = MappingEngine()
        if not hasattr(engine, 'suggest_primary_keys'):
            raise Exception("Mapping Engine: suggest_primary_keys missing.")
        print("[OK] Mapping Engine: Intelligence layer verified.")

        # 5. Validate Audit Service
        from core.services.audit_service import AuditService
        audit = AuditService(operator="SMOKE_TEST")
        audit.log_event("SMOKE_TEST", {"status": "SUCCESS"})
        print("[OK] Audit Service: Event logging functional.")

        print("-" * 50)
        print(f"RESULT: SMOKE TEST PASSED ({__version__} Platinum Certified)")
        print("-" * 50)
        return True
        
    except Exception as e:
        print(f"RESULT: SMOKE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if run_flet_smoke_test():
        sys.exit(0)
    else:
        sys.exit(1)
