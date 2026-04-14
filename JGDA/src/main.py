import os
import sys

# Adicionar src ao path se necessário
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.bootstrap import AppBootstrap
from core.services.logger_service import LoggerService
from version import __version__, __title__

def main():
    # 1. 🔍 INICIALIZAÇÃO DE GOVERNANÇA (PLATINUM LOG)
    LoggerService.setup()
    logger = LoggerService()
    logger.info(f"--- {__title__} v{__version__} Initiated ---")
    
    try:
        # 2. 🚀 DISPARO DO BOOTSTRAP PLATINUM
        # O Bootstrap agora direciona para a arquitetura Flet Stateless.
        bootstrap = AppBootstrap()
        bootstrap.run()
        
    except Exception as e:
        logger.exception("FATAL ERROR during startup")
        sys.exit(1)


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Ponto de entrada (Bootstrap) do Sistema Genaja Platinum")

if __name__ == "__main__":
    main()
