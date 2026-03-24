import sys
import os

# CONFIGURACAO DE AMBIENTE (v0.5.4 Pure)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(0, SRC_DIR)

from app.bootstrap import AppBootstrap

def run_smoke_test():
    print("--- INICIANDO SMOKE TEST (v0.5.4 PURE QT) ---")
    
    try:
        # 1. Instanciar Bootstrap
        bootstrap = AppBootstrap()
        print("OK: Bootstrap instanciado com sucesso.")

        # 2. Validar integridade dos servicos
        presets = list(bootstrap.theme_service.PRESETS.keys())
        print(f"OK: Services: {presets}")
        
        print("OK: Teste de fumaca validou a integridade dos servicos e do entrypoint.")
        print("Teste Finalizado com Sucesso (v0.5.4 Certified).")
        return True
        
    except Exception as e:
        # Evitar Emojis para nao quebrar encoding no Windows Shell
        print(f"FAIL: O TESTE FALHOU: {e}")
        return False

if __name__ == "__main__":
    if run_smoke_test():
        sys.exit(0)
    else:
        sys.exit(1)