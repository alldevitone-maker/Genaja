import logging
import os
import sys
from core.paths import LOGS_MOTOR_DIR
from version import __version__

class LoggerService:
    """
    Serviço de Logging Corporativo.
    Garante registros auditáveis em UTF-8.
    """
    @staticmethod
    def setup():
        log_dir = LOGS_MOTOR_DIR
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'genaja_flet.log')
        
        if sys.platform == "win32":
            try: sys.stdout.reconfigure(encoding='utf-8')
            except: pass
            
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.info(f"--- Log System v{__version__} Stable Initialized ---")

    def info(self, msg): logging.info(msg)
    def error(self, msg): logging.error(msg)
    def warning(self, msg): logging.warning(msg)
