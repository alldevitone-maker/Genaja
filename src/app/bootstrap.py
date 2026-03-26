import sys
from services.theme_service import ThemeService
from core.services.config_service import ConfigService
from core.services.etl_service import ETLService
from core.services.mapping_engine import MappingEngine
from core.services.validation_engine import ValidationEngine

class AppBootstrap:
    def __init__(self):
        # 🧪 SERVIÇOS NEUTROS (v0.5.4 Pure Edition)
        self.theme_service = ThemeService()
        self.config_service = ConfigService()
        self.etl_service = ETLService()
        self.mapping_engine = MappingEngine()
        self.validation_engine = ValidationEngine()
        
    def run(self):
        # O Genaja v0.5.9 agora é estritamente Flet (Platinum Architecture).
        # Fallback para Qt removido para garantir pureza da nova arquitetura.
        return self._run_flet()

    def _run_flet(self):
        try:
            import flet as ft
            from ui_flet.main import main as flet_main
            
            # Inicialização Platinum v0.6.0 (Pure Flet)
            ft.app(target=flet_main)
            
        except ImportError as e:
            print(f"ERROR: Arquitetura Flet nao encontrada: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: ERRO DE INICIALIZACAO FLET: {e}")
            sys.exit(1)
