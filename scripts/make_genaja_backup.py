import os
import re
import zipfile
import logging
import datetime

# Root of the product
GENAJA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_DIR = os.path.join(GENAJA_ROOT, "JGDA", "backups", "genaja_product_backup")
LOG_DIR = os.path.join(GENAJA_ROOT, "shared", "logs")

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("product_backup")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, "product_backup.log"), encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

DATE_STR = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
ZIP_NAME = f"Genaja_Product_Full_Backup_{DATE_STR}.zip"
ZIP_PATH = os.path.join(BACKUP_DIR, ZIP_NAME)

# Paths relative to the root
INCLUDE_ROOTS = ["JGDA", "brains", "docs"]
IGNORE_DIRS = {"backups", "__pycache__", ".git", ".vscode", "venv", "logs", "tmp", "migration", "shared"}
IGNORE_FILES = {ZIP_NAME, "backup_engine.log", "product_backup.log"}

def create_full_backup():
    logger.info("Iniciando Backup Global do Produto...")
    count = 0
    
    try:
        with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root_subdir in INCLUDE_ROOTS:
                full_root = os.path.join(GENAJA_ROOT, root_subdir)
                if not os.path.exists(full_root):
                    continue
                
                for root, dirs, files in os.walk(full_root):
                    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                    
                    for file in files:
                        if file in IGNORE_FILES or file.endswith((".pyc", ".log")):
                            continue
                        
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, GENAJA_ROOT)
                        zipf.write(file_path, arcname)
                        count += 1
                        
        logger.info("-" * 50)
        logger.info(f"Backup global finalizado! {count} arquivos incluídos.")
        logger.info(f"Local: {ZIP_PATH}")
        logger.info("-" * 50)
        
    except Exception:
        logger.error("Falha crítica no backup global do produto.", exc_info=True)

if __name__ == "__main__":
    create_full_backup()
