import logging
import os
import sys

class LoggerService:
    """
    Serviço de Logging (v0.6.0) - Compliance v0.5.9.
    Garante registros auditáveis em UTF-8.
    """
    @staticmethod
    def setup():
        log_dir = os.path.join(os.getcwd(), 'logs')
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
        logging.info("--- Log System v0.6.0 Alpha Initialized ---")

    def info(self, msg): logging.info(msg)
    def error(self, msg): logging.error(msg)
    def warning(self, msg): logging.warning(msg)
