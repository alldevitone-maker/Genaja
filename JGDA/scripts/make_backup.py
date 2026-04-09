import os
import re
import zipfile
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- CONFIGURAÇÃO DE LOGGING ---
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("make_backup")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(
        os.path.join(LOG_DIR, "backup_engine.log"),
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

# --- CONFIGURAÇÃO DA VERSÃO ATUAL ---
version_vars = {}
version_file = os.path.join(BASE_DIR, "src", "version.py")

with open(version_file, encoding="utf-8") as f:
    exec(f.read(), {}, version_vars)

VERSION = version_vars.get("__version__", "unknown")
TITLE = version_vars.get("__title__", "").replace(" ", "_")
TITLE = re.sub(r'[\\/*?:"<>|]', "", TITLE)

# ------------------------------------

BACKUP_DIR = os.path.join(BASE_DIR, "backups", "genaja_jgda_backup")
suffix = f"_{TITLE}" if TITLE else ""
ZIP_NAME = f"Genaja_JGDA_v{VERSION}_AutoBackup{suffix}.zip"
ZIP_PATH = os.path.join(BACKUP_DIR, ZIP_NAME)

# Pastas/Arquivos a ignorar no backup
IGNORE_DIRS = {"backups", "__pycache__", ".git", ".vscode", "venv", "logs", "tmp", "migration"}
IGNORE_FILES = {ZIP_NAME, "genaja.log", "backup_engine.log"}


def create_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    logger.info("Iniciando snapshot seguro: %s...", ZIP_NAME)

    count = 0

    try:
        with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(BASE_DIR):
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

                for file in files:
                    if file in IGNORE_FILES or file.endswith((".pyc", ".log")):
                        continue

                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, BASE_DIR)

                    logger.debug("  -> Adicionando: %s", arcname)
                    zipf.write(file_path, arcname)
                    count += 1

        logger.info("-" * 50)
        logger.info(
            "Snapshot local concluído com sucesso! [%s arquivos vinculados ao ZIP]",
            count
        )
        logger.info("Local salvo: %s", ZIP_PATH)
        logger.info("-" * 50)

    except Exception:
        logger.error("Falha severa na montagem do backup.", exc_info=True)


if __name__ == "__main__":
    create_backup()