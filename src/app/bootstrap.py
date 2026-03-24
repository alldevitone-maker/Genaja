import sys
import argparse
from ui_tk.genaja_tk_window import GenajaUI
from services.theme_service import ThemeService
from core.services.config_service import ConfigService
from core.services.etl_service import ETLService
from core.services.mapping_engine import MappingEngine
from core.services.validation_engine import ValidationEngine

class AppBootstrap:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Genaja - Inteligência de Sincronização")
        self.parser.add_argument("--ui", choices=["tk", "qt"], default="qt", help="Escolher interface (Nova: qt, Legada: tk)")
        self.args = self.parser.parse_args()
        
        # Iniciar Serviços Neutros (Portados v0.5.0)
        self.theme_service = ThemeService()
        self.config_service = ConfigService()
        self.etl_service = ETLService()
        self.mapping_engine = MappingEngine()
        self.validation_engine = ValidationEngine()
        
    def run(self, root_tk=None):
        if self.args.ui == "qt":
            return self._run_qt()
        else:
            return self._run_tk(root_tk)

    def _run_tk(self, root):
        # Aqui injetamos a lógica v0.4.9
        # No need to import here, already imported at top
        # O main.py original passará o root e os callbacks
        return self.args.ui

    def _run_qt(self):
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
        except ImportError as e:
            print(f"❌ Erro ao carregar PySide6: {e}")
            print("Certifique-se de que as dependências do v0.5.0 foram instaladas (pip install PySide6)")
            sys.exit(1)
