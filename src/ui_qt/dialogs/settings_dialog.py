from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QListWidget, QStackedWidget, 
                             QWidget, QLineEdit, QCheckBox, QComboBox, QFileDialog)
from PySide6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, config_service, theme_service, parent=None):
        super().__init__(parent)
        self.config_service = config_service
        self.theme_service = theme_service
        
        self.setWindowTitle("Configurações Globais - Genaja 2026")
        self.resize(750, 550)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_ui()
        self.setStyleSheet(self.theme_service.get_qss())

    def _setup_ui(self):
        # 1. SIDEBAR (Navegação lateral premium)
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(180)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.addItems(["🏠 Geral", "⚙️ Motor de Dados", "📦 Exportação", "🛡️ Segurança"])
        self.sidebar.currentRowChanged.connect(self._on_tab_changed)
        self.main_layout.addWidget(self.sidebar)
        
        # 2. CONTENT AREA
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)
        
        self._create_general_tab()
        self._create_engine_tab()
        self._create_export_tab()
        self._create_security_tab()
        
        # 3. FOOTER (Ações)
        footer_container = QWidget()
        footer_layout = QVBoxLayout(footer_container)
        
        right_area = QWidget()
        right_layout = QVBoxLayout(right_area)
        right_layout.addWidget(self.content_stack)
        
        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save = QPushButton("💾 Salvar Configurações")
        self.btn_save.clicked.connect(self._save_config)
        self.btn_save.setMinimumHeight(40)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        right_layout.addLayout(btn_layout)
        
        self.main_layout.addWidget(right_area)

    def _create_general_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<b>Configurações Gerais</b>"))
        
        # Nome do App
        layout.addWidget(QLabel("Título da Aplicação:"))
        self.edit_app_name = QLineEdit(self.config_service.get_config("general", "app_name"))
        layout.addWidget(self.edit_app_name)
        
        # Operador
        layout.addWidget(QLabel("Nome do Operador/Analista:"))
        self.edit_operator = QLineEdit(self.config_service.get_config("general", "operator_name"))
        layout.addWidget(self.edit_operator)
        
        layout.addStretch()
        self.content_stack.addWidget(page)

    def _create_engine_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<b>Motor de Inteligência e Sincronização</b>"))
        
        self.chk_trim = QCheckBox("Auto-Trim (Remover espaços extras ao ler arquivos)")
        self.chk_trim.setChecked(self.config_service.get_config("engine", "auto_trim"))
        layout.addWidget(self.chk_trim)
        
        self.chk_upper = QCheckBox("Auto-Upper (Converter textos para MAIÚSCULO)")
        self.chk_upper.setChecked(self.config_service.get_config("engine", "auto_upper"))
        layout.addWidget(self.chk_upper)
        
        self.chk_case = QCheckBox("Sensível a Maiúsculas/Minúsculas nas Chaves")
        self.chk_case.setChecked(self.config_service.get_config("engine", "case_sensitive_match"))
        layout.addWidget(self.chk_case)
        
        layout.addStretch()
        self.content_stack.addWidget(page)

    def _create_export_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<b>Preferências de Exportação</b>"))
        
        layout.addWidget(QLabel("Formato Padrão:"))
        self.combo_format = QComboBox()
        self.combo_format.addItems([".xlsx", ".csv", ".json", ".sql"])
        self.combo_format.setCurrentText(self.config_service.get_config("export", "default_format"))
        layout.addWidget(self.combo_format)
        
        self.chk_timestamp = QCheckBox("Incluir data/hora no nome do arquivo")
        self.chk_timestamp.setChecked(self.config_service.get_config("export", "include_timestamp"))
        layout.addWidget(self.chk_timestamp)
        
        self.chk_open = QCheckBox("Abrir arquivo automaticamente após sucesso")
        self.chk_open.setChecked(self.config_service.get_config("export", "open_after_export"))
        layout.addWidget(self.chk_open)
        
        layout.addStretch()
        self.content_stack.addWidget(page)

    def _create_security_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<b>Segurança e Governança</b>"))
        
        self.chk_lock = QCheckBox("Bloquear mapeamento após iniciar processamento")
        self.chk_lock.setChecked(self.config_service.get_config("security", "lock_mapping_after_start"))
        layout.addWidget(self.chk_lock)
        
        self.chk_logs = QCheckBox("Logs detalhados de auditoria (Power User)")
        self.chk_logs.setChecked(self.config_service.get_config("security", "detailed_logging"))
        layout.addWidget(self.chk_logs)
        
        layout.addStretch()
        self.content_stack.addWidget(page)

    def _on_tab_changed(self, index):
        self.content_stack.setCurrentIndex(index)

    def _save_config(self):
        # Coleta dados
        self.config_service.set_config("general", "app_name", self.edit_app_name.text())
        self.config_service.set_config("general", "operator_name", self.edit_operator.text())
        
        self.config_service.set_config("engine", "auto_trim", self.chk_trim.isChecked())
        self.config_service.set_config("engine", "auto_upper", self.chk_upper.isChecked())
        self.config_service.set_config("engine", "case_sensitive_match", self.chk_case.isChecked())
        
        self.config_service.set_config("export", "default_format", self.combo_format.currentText())
        self.config_service.set_config("export", "include_timestamp", self.chk_timestamp.isChecked())
        self.config_service.set_config("export", "open_after_export", self.chk_open.isChecked())
        
        self.config_service.set_config("security", "lock_mapping_after_start", self.chk_lock.isChecked())
        self.config_service.set_config("security", "detailed_logging", self.chk_logs.isChecked())
        
        self.config_service.save_config()
        self.accept()
