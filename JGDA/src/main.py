import os
import sys

# Adicionar src ao path se necessário
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.bootstrap import AppBootstrap
from utils.logger_setup import setup_logger, get_logger
from version import __version__, __title__

def main():
    # 1. 🔍 INICIALIZAÇÃO DE GOVERNANÇA
    setup_logger()
    logger = get_logger()
    logger.info(f"--- {__title__} v{__version__} Initiated ---")
    
    try:
        # 2. 🚀 DISPARO DO BOOTSTRAP PLATINUM
        # O Bootstrap agora direciona para a arquitetura Flet Stateless.
        bootstrap = AppBootstrap()
        bootstrap.run()
        
    except Exception as e:
        logger.exception("FATAL ERROR during startup")
        sys.exit(1)

if __name__ == "__main__":
    main()
