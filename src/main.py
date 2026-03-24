import os
import sys

# Adicionar src ao path se necessário
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.bootstrap import AppBootstrap
from utils.logger_setup import setup_logger, get_logger
from version import __version__, __title__

def main():
    # 1. 🔍 INICIALIZAÇÃO DE GOVERNANÇA (v0.5.4 Pure)
    setup_logger()
    logger = get_logger()
    logger.info(f"--- {__title__} v{__version__} Initiated ---")
    
    try:
        # 2. 🚀 DISPARO DO BOOTSTRAP PURE QT
        # O Bootstrap v0.5.4 já não aceita argumentos de UI e vai direto para Qt.
        bootstrap = AppBootstrap()
        bootstrap.run()
        
    except Exception as e:
        logger.error(f"FATAL ERROR during startup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
