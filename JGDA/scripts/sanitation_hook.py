import os
import shutil
import sys

# Adicionar src ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from core.paths import LEARN_DIR

def clean_pycache():
    print("CLEANUP: Buscando poluicao de __pycache__...")
    cleaned = 0
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache_path)
            cleaned += 1
    print(f"DONE: Removidos {cleaned} diretorios de cache.")

def detect_large_artifacts():
    print("AUDIT: Auditando artefatos pesados (> 10MB)...")
    for root, dirs, files in os.walk("."):
        for f in files:
            p = os.path.join(root, f)
            if os.path.getsize(p) > 10 * 1024 * 1024:
                print(f"WARNING: Alerta: Arquivo grande detectado: {p} ({os.path.getsize(p)/1024/1024:.1f} MB)")

def check_structure():
    print("DIR: Verificando integridade da estrutura v0.7.0...")
    required = [
        os.path.join(LEARN_DIR, "inbox"), 
        os.path.join(LEARN_DIR, "consolidated"), 
        os.path.join(LEARN_DIR, "quarantine"), 
        os.path.join(LEARN_DIR, "reports")
    ]
    for r in required:
        if not os.path.exists(r):
            print(f"FAIL: Erro: Pasta obrigatoria ausente: {r}")
        else:
            print(f"OK: Estrutura OK: {r}")

def main():
    print("--- Genaja Sanitation Hook v0.6.8 ---")
    clean_pycache()
    detect_large_artifacts()
    check_structure()
    print("--- Saneamento Finalizado ---")

if __name__ == "__main__":
    main()
