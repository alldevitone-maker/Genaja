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
            
            # Injeção de Dependência Consolidada
            # O flet_main precisará ser adaptado para aceitar esses serviços no futuro
            # Por enquanto, ele já os instancia internamente, mas mantemos o padrão
            
            ft.app(target=flet_main)
            
        except ImportError as e:
            print(f"ERROR: Arquitetura Flet nao encontrada: {e}")
            print("Verifique se o Flet esta instalado: pip install flet")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: ERRO DE INICIALIZACAO FLET: {e}")
            sys.exit(1)

    def _run_qt(self):
        # Legado mantido apenas para referência interna se necessário
        try:
            from ui_qt.genaja_qt_app import start_qt_app
            
            services = {
                "theme": self.theme_service,
                "config": self.config_service,
                "etl": self.etl_service,
                "mapping": self.mapping_engine,
                "validation": self.validation_engine
            }
            
            start_qt_app(services)
            
        except Exception as e:
            print(f"ERROR: Falha ao carregar fallback Qt: {e}")
            sys.exit(1)
