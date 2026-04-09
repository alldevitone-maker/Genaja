import sys
from core.services.theme_service import ThemeService
from core.services.config_service import ConfigService
from core.services.etl_service import ETLService
from core.engines.mapping_engine import MappingEngine
from core.engines.validation_engine import ValidationEngine

class AppBootstrap:
    def __init__(self):
        # 🧪 SERVIÇOS NEUTROS
        self.theme_service = ThemeService()
        self.config_service = ConfigService()
        self.etl_service = ETLService()
        self.mapping_engine = MappingEngine()
        self.validation_engine = ValidationEngine()
        
    def run(self):
        # O Genaja agora é estritamente Flet (Platinum Architecture).
        # Fallback para Qt removido para garantir pureza da nova arquitetura.
        return self._run_flet()

    def _run_flet(self):
        try:
            import flet as ft
            from ui_flet.main import main as flet_main
            
            # Inicialização Platinum (Pure Flet)
            ft.app(target=flet_main)
            
        except ImportError as e:
            print(f"ERROR: Arquitetura Flet nao encontrada: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: ERRO DE INICIALIZACAO FLET: {e}")
            sys.exit(1)
