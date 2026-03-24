import logging
import os

def setup_logger():
    """Inicializa o sistema de logs do Genaja"""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    log_dir = os.path.join(base_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'genaja.log')
    
    # Configure logging to both file and console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging system initialized.")

def get_logger():
    """Retorna a instância do logger global"""
    return logging.getLogger("Genaja")

def configure_logging():
    """Alias para compatibilidade legado"""
    setup_logger()
