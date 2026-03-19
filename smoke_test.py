import os
import sys
import threading
import time
import make_backup  # Importa o script de backup para automação

# Lógica robusta para encontrar a pasta src independente de onde o script é executado
current_dir = os.path.dirname(os.path.abspath(__file__))

# Se estiver na raiz (JGDA/), src está aqui
if os.path.exists(os.path.join(current_dir, 'src')):
    PROJECT_ROOT = current_dir
    SRC_DIR = os.path.join(current_dir, 'src')
# Se estiver na pasta tests (JGDA/tests/), src está um nível acima
else:
    PROJECT_ROOT = os.path.dirname(current_dir)
    SRC_DIR = os.path.join(PROJECT_ROOT, 'src')

sys.path.insert(0, SRC_DIR)

try:
    from main import GenajaApp
    import tkinter as tk
except ImportError as e:
    print(f"❌ Erro Crítico de Importação: {e}")
    sys.exit(1)

def run_smoke_test():
    print("🔥 --- INICIANDO SMOKE TEST (TESTE DE FUMAÇA) ---")
    print(f"📂 Diretório do Projeto: {PROJECT_ROOT}")
    
    try:
        app = GenajaApp()
        print("✅ Classe GenajaApp instanciada com sucesso.")
        print("⏳ A interface gráfica será aberta e fechará automaticamente em 2 segundos...")
        
        # Agenda o fechamento automático para validar que o loop da UI iniciou
        app.root.after(2000, lambda: (print("✅ Interface carregada com sucesso. Fechando..."), app.root.destroy()))
        app.run()
        print("✅ Teste Finalizado! Módulos carregados e UI iniciada com sucesso.")
        
        # Automação de Backup após sucesso
        print("\n📦 Iniciando Backup Automático de Versão...")
        make_backup.create_backup()
        
    except Exception as e:
        print(f"❌ O TESTE FALHOU: {e}")

if __name__ == "__main__":
    run_smoke_test()