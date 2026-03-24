import sys
from PySide6.QtWidgets import QApplication
from ui_qt.main_window import MainWindow

def start_qt_app(services):
    app = QApplication(sys.argv)
    
    # Instanciar Janela Principal com Injeção de Dependência
    window = MainWindow(services)
    window.show()
    
    sys.exit(app.exec())
