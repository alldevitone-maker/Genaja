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
        # O Genaja v0.5.4 agora é estritamente PySide6.
        return self._run_qt()

    def _run_qt(self):
        try:
            from ui_qt.genaja_qt_app import start_qt_app
            
            # Injeção de Dependência Consolidada
            services = {
                "theme": self.theme_service,
                "config": self.config_service,
                "etl": self.etl_service,
                "mapping": self.mapping_engine,
                "validation": self.validation_engine
            }
            
            start_qt_app(services)
            
        except ImportError as e:
            print(f"❌ ERRO CRÍTICO (v0.5.4): Arquitetura Qt não encontrada: {e}")
            print("Verifique se o PySide6 está instalado: pip install PySide6")
            sys.exit(1)
        except Exception as e:
            print(f"❌ ERRO DE INICIALIZAÇÃO: {e}")
            sys.exit(1)
