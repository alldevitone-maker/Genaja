import os
import zipfile
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- CONFIGURAÇÃO DA VERSÃO ATUAL ---
# Lê a versão diretamente do código fonte para evitar descompasso
version_vars = {}
with open(os.path.join(BASE_DIR, 'src', 'version.py')) as f:
    exec(f.read(), version_vars)
VERSION = version_vars['__version__']
# ------------------------------------

BACKUP_DIR = os.path.join(BASE_DIR, "backups", "genaja_jgda_backup")
# Nome do arquivo: Genaja_JGDA_v0.3.3_AutoBackup.zip
ZIP_NAME = f"Genaja_JGDA_{VERSION}_AutoBackup.zip"
ZIP_PATH = os.path.join(BACKUP_DIR, ZIP_NAME)

# Pastas/Arquivos a ignorar no backup
IGNORE_DIRS = {'backups', '__pycache__', '.git', '.vscode', 'venv'}
IGNORE_FILES = {ZIP_NAME, 'genaja.log'}

def create_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"📁 Pasta de backup criada: {BACKUP_DIR}")

    print(f"📦 Iniciando backup: {ZIP_NAME}...")
    
    try:
        with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(BASE_DIR):
                # Filtra pastas ignoradas
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                
                for file in files:
                    if file in IGNORE_FILES:
                        continue
                    
                    file_path = os.path.join(root, file)
                    # Caminho relativo dentro do zip (para não pegar o caminho absoluto do C:/)
                    arcname = os.path.relpath(file_path, BASE_DIR)
                    
                    print(f"  -> Adicionando: {arcname}")
                    zipf.write(file_path, arcname)
        
        print("-" * 50)
        print(f"✅ Backup concluído com sucesso!")
        print(f"📂 Local: {ZIP_PATH}")
        print("-" * 50)

    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")

if __name__ == "__main__":
    create_backup()