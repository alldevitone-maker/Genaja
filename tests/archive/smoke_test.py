import sys
import os

# --- CONFIGURACAO DE AMBIENTE PLATINUM (v0.5.9) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(0, SRC_DIR)

from app.bootstrap import AppBootstrap

def run_smoke_test():
    print("-" * 50)
    print("GENAJA PLATINUM AUDIT: SMOKE TEST (v0.5.9)")
    print("-" * 50)
    
    try:
        # 1. Instanciar Bootstrap (Inicia todos os serviços v2.0)
        bootstrap = AppBootstrap()
        print("[OK] Bootstrap & Core Services bootstrapped.")

        # 2. Validar Theme Service
        presets = list(bootstrap.theme_service.PRESETS.keys())
        if not presets:
            raise Exception("Theme Service: No presets found.")
        print(f"[OK] Theme Service: {len(presets)} presets detected ({', '.join(presets)}).")

        # 3. Validar Config Service v2.0
        config = bootstrap.config_service.get_config()
        if 'engine' not in config:
            raise Exception("Config Service v2.0: Schema incomplete.")
        print(f"[OK] Config Service v2.0: Schema validated (Active: {config.get('general', {}).get('app_title')}).")

        # 4. Validar Mapping Engine
        from core.services.mapping_engine import MappingEngine
        engine = MappingEngine()
        print("[OK] Mapping Engine: Available.")
        
        print("-" * 50)
        print("RESULT: SMOKE TEST PASSED (v0.5.9 Platinum Certified)")
        print("-" * 50)
        return True
        
    except Exception as e:
        print(f"RESULT: SMOKE TEST FAILED: {e}")
        return False

if __name__ == "__main__":
    if run_smoke_test():
        sys.exit(0)
    else:
        sys.exit(1)
