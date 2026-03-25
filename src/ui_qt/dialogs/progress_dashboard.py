from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QProgressBar, QPlainTextEdit, QPushButton, QFrame)
from PySide6.QtCore import Qt, Signal, QTimer

class ProgressDashboard(QDialog):
    def __init__(self, services, parent=None):
        super().__init__(parent)
        self.services = services
        self.theme = services["theme"].current_theme
        
        self.setWindowTitle("Sincronizacao em Curso - Genaja 2026")
        self.resize(650, 480)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.container = QFrame(self)
        self.container.setObjectName("DashboardContainer")
        self.container.setStyleSheet(f"""
            QFrame#DashboardContainer {{
                background-color: {self.theme['bg_col']};
                border: 2px solid {self.theme['action_bg']};
                border-radius: 16px;
            }}
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(self.container)
        
        self._setup_ui()

    def _setup_ui(self):
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        # Header Status
        self.lbl_title = QLabel("🚀 Sincronizando Estruturas Corporativas...")
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #0D6EFD;")
        self.layout.addWidget(self.lbl_title)
        
        # Progress Bar
        self.pbar = QProgressBar()
        self.pbar.setHeight = 25
        self.pbar.setValue(0)
        self.pbar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {self.theme['border_col']};
                border-radius: 8px;
                text-align: center;
                background-color: {self.theme['surface_col']};
            }}
            QProgressBar::chunk {{
                background-color: {self.theme['action_bg']};
                border-radius: 6px;
            }}
        """)
        self.layout.addWidget(self.pbar)
        
        # Log Area
        self.log_area = QPlainTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("Aguardando início do motor...")
        self.log_area.setStyleSheet(f"background-color: #111827; color: #10B981; font-family: 'Consolas'; font-size: 12px; border-radius: 8px;")
        self.layout.addWidget(self.log_area)
        
        # Stats Area
        self.stats = QLabel("Iniciando cruzamento de dados...")
        self.stats.setStyleSheet("color: #6B7280; font-style: italic;")
        self.layout.addWidget(self.stats)
        
        # Footer
        footer = QHBoxLayout()
        self.btn_done = QPushButton("CONCLUÍDO")
        self.btn_done.setEnabled(False)
        self.btn_done.clicked.connect(self.accept)
        footer.addStretch()
        footer.addWidget(self.btn_done)
        self.layout.addLayout(footer)

    def log(self, message):
        self.log_area.appendPlainText(f"> {message}")
        self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())

    def update_progress(self, current, total):
        pct = int((current / total) * 100) if total > 0 else 0
        self.pbar.setValue(pct)
        self.stats.setText(f"Processando: {current} de {total} registros...")

    def finalize(self, success=True):
        if success:
            self.lbl_title.setText("✅ Sincronização Concluída com Sucesso!")
            self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #198754;")
            self.pbar.setValue(100)
            self.log("🏁 Operação finalizada conforme Governance Protocol.")
        else:
            self.lbl_title.setText("❌ Erro no Processamento")
            self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #DC3545;")
        
        self.btn_done.setEnabled(True)
