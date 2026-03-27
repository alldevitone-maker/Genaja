import sys
import os
import time

# Adicionar src ao path para rodar o teste
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from PySide6.QtWidgets import QApplication
    from ui_qt.main_window import MainWindow
    from core.services.theme_service import ThemeService
    print("PySide6 carregado com sucesso.")
except ImportError as e:
    print(f"ERRO: PySide6 não instalado: {e}")
    sys.exit(1)

def run_smoke_test_qt():
    print("--- INICIANDO SMOKE TEST QT (v0.5.0 Alpha) ---")
    
    # Simula inicialização com Injeção de Dependência
    app = QApplication.instance() or QApplication(sys.argv)
    from core.services.etl_service import ETLService
    from core.services.mapping_engine import MappingEngine
    from core.services.validation_engine import ValidationEngine
    from core.services.config_service import ConfigService
    
    services = {
        "theme": ThemeService(),
        "config": ConfigService(),
        "etl": ETLService(),
        "mapping": MappingEngine(),
        "validation": ValidationEngine()
    }
    
    window = MainWindow(services)
    print("MainWindow (Qt) instanciada com sucesso.")
    
    # Abre por 1 segundo e fecha
    window.show()
    print("Interface Qt aberta. Validando fechamento...")
    time.sleep(1)
    window.close()
    
    print("Teste Finalizado! Shell Qt iniciado e encerrado com sucesso.")
    sys.exit(0)

if __name__ == "__main__":
    run_smoke_test_qt()
