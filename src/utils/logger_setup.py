import logging
import os

def configure_logging():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # volta de src/utils para JGDA
    log_dir = os.path.join(base_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        filename=os.path.join(log_dir, 'genaja.log'),
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8'
    )
