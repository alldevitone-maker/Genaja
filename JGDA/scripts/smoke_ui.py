import subprocess
import time
import sys
import os

def smoke_test_ui():
    print("--- INICIANDO SMOKE TEST DE UI (v0.7.0) ---")
    
    # Adiciona src ao PYTHONPATH para o subprocesso
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath("src")
    
    cmd = [sys.executable, "src/main.py"]
    
    print(f"Executando: {' '.join(cmd)}")
    
    # Rodamos o processo e capturamos saída
    process = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True,
        env=env
    )
    
    # Aguardamos 10 segundos para ver se crasha no boot
    time.sleep(10)
    
    if process.poll() is not None:
        # Processo terminou (provavelmente erro)
        stdout, stderr = process.communicate()
        print("\n❌ FALHA NO BOOT DA UI!")
        print("--- STDOUT ---")
        print(stdout)
        print("--- STDERR ---")
        print(stderr)
        
        if "multiple values for keyword argument 'padding'" in stderr:
            print("\n🚨 CAUSA: Conflito de padding detectado!")
        elif "serialize 'set' object" in stderr:
            print("\n🚨 CAUSA: Erro de serialização de set detectado!")
            
        sys.exit(1)
    else:
        print("\n✅ UI ESTÁVEL APÓS 10 SEGUNDOS.")
        print("Encerrando processo de teste...")
        process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    smoke_test_ui()
