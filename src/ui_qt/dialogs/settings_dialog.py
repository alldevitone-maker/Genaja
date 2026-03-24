from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QStackedWidget, QWidget, 
                             QLineEdit, QComboBox, QScrollArea)
from PySide6.QtCore import Qt
from ui_qt.widgets.settings_widgets import ModernSwitch, SettingCard, SidebarButton

class SettingsDialog(QDialog):
    def __init__(self, config_service, theme_service, parent=None):
        super().__init__(parent)
        self.config_service = config_service
        self.theme_service = theme_service
        
        self.setWindowTitle("Global Preferences - Genaja 2026")
        self.resize(850, 600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Main Container (para bordas e sombra simulada via QSS)
        self.container = QFrame(self)
        self.container.setObjectName("SettingsContainer")
        self.container.setStyleSheet(f"""
            QFrame#SettingsContainer {{
                background-color: {self.theme_service.get_color('bg_col')};
                border: 1px solid {self.theme_service.get_color('border_col')};
                border-radius: 16px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.container)
        
        self.setup_ui()
        self.apply_initial_config()

    def setup_ui(self):
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # 1. SIDEBAR
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setFixedWidth(220)
        self.sidebar_frame.setStyleSheet(f"background-color: {self.theme_service.get_color('surface_col')}; border-right: 1px solid {self.theme_service.get_color('border_col')}; border-top-left-radius: 16px; border-bottom-left-radius: 16px;")
        
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(5)
        
        # Brand/Header in Sidebar
        brand_label = QLabel("GENAJA PRO")
        brand_label.setStyleSheet(f"color: {self.theme_service.get_color('action_bg')}; font-weight: bold; font-size: 18px; margin-left: 20px; margin-bottom: 20px;")
        sidebar_layout.addWidget(brand_label)
        
        self.nav_buttons = []
        nav_items = [
            ("🏠 Home & Identity", 0),
            ("⚙️ Engine & Logic", 1),
            ("📦 Data Export", 2),
            ("🛡️ Security & Privacy", 3)
        ]
        
        for text, idx in nav_items:
            btn = SidebarButton(text)
            btn.setObjectName("SidebarButton")
            btn.setProperty("active", idx == 0)
            btn.clicked.connect(lambda checked=False, i=idx: self.switch_page(i))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        sidebar_layout.addStretch()
        container_layout.addWidget(self.sidebar_frame)
        
        # 2. CONTENT AREA
        self.content_area = QFrame()
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(30, 30, 30, 20)
        
        self.page_stack = QStackedWidget()
        content_layout.addWidget(self.page_stack)
        
        self._create_pages()
        
        # 3. FOOTER ACTIONS
        footer_layout = QHBoxLayout()
        self.btn_close = QPushButton("Cancel")
        self.btn_close.setStyleSheet("background: transparent; border: 1px solid #3F3F46;")
        self.btn_close.clicked.connect(self.reject)
        
        self.btn_save = QPushButton("Apply Transformations")
        self.btn_save.clicked.connect(self.save_and_apply)
        
        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_close)
        footer_layout.addWidget(self.btn_save)
        content_layout.addLayout(footer_layout)
        
        container_layout.addWidget(self.content_area)

    def _create_pages(self):
        # PAGE 0: IDENTITY
        p0 = QWidget()
        l0 = QVBoxLayout(p0)
        l0.setSpacing(15)
        
        self.in_app_name = QLineEdit()
        l0.addWidget(SettingCard("Application Title", "Defina como o Genaja deve se identificar no Header.", self.in_app_name))
        
        self.in_operator = QLineEdit()
        l0.addWidget(SettingCard("Operator Identity", "Assinatura do analista responsável pelos cruzamentos.", self.in_operator))
        
        l0.addStretch()
        self.page_stack.addWidget(p0)
        
        # PAGE 1: ENGINE
        p1 = QWidget()
        l1 = QVBoxLayout(p1)
        l1.setSpacing(15)
        
        self.sw_trim = ModernSwitch(self.theme_service)
        l1.addWidget(SettingCard("Auto-Trim Engine", "Remove espaços fantasmas e quebras de linha invisíveis.", self.sw_trim))
        
        self.sw_upper = ModernSwitch(self.theme_service)
        l1.addWidget(SettingCard("Forced Case (Upper)", "Normaliza todas as strings para MAIÚSCULO no processamento.", self.sw_upper))
        
        self.sw_case_sens = ModernSwitch(self.theme_service)
        l1.addWidget(SettingCard("Strict Key Sensitivity", "Diferencia 'ID_01' de 'id_01' durante o mapeamento.", self.sw_case_sens))
        
        l1.addStretch()
        self.page_stack.addWidget(p1)
        
        # PAGE 2: EXPORT
        p2 = QWidget()
        l2 = QVBoxLayout(p2)
        l2.setSpacing(15)
        
        self.cb_format = QComboBox()
        self.cb_format.addItems([".xlsx", ".csv", ".json", ".sql"])
        l2.addWidget(SettingCard("Primary Export Format", "Extensão preferencial para disparos corporativos.", self.cb_format))
        
        self.sw_timestamp = ModernSwitch(self.theme_service)
        l2.addWidget(SettingCard("Naming Entropy (Timestamp)", "Anexa data e hora exata no final de cada exportação.", self.sw_timestamp))
        
        l2.addStretch()
        self.page_stack.addWidget(p2)
        
        # PAGE 3: SECURITY
        p3 = QWidget()
        l3 = QVBoxLayout(p3)
        l3.setSpacing(15)
        
        self.sw_lock = ModernSwitch(self.theme_service)
        l3.addWidget(SettingCard("Mapping Fortress", "Bloqueia edições na tabela após o início do motor ETL.", self.sw_lock))
        
        self.sw_audit = ModernSwitch(self.theme_service)
        l3.addWidget(SettingCard("Deep Audit Logs", "Gera rastro técnico completo de cada célula processada.", self.sw_audit))
        
        l3.addStretch()
        self.page_stack.addWidget(p3)

    def switch_page(self, index):
        self.page_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def apply_initial_config(self):
        cfg = self.config_service.get_config()
        self.in_app_name.setText(cfg['general']['app_name'])
        self.in_operator.setText(cfg['general']['operator_name'])
        
        self.sw_trim.setChecked(cfg['engine']['auto_trim'])
        self.sw_upper.setChecked(cfg['engine']['auto_upper'])
        self.sw_case_sens.setChecked(cfg['engine']['case_sensitive_match'])
        
        self.cb_format.setCurrentText(cfg['export']['default_format'])
        self.sw_timestamp.setChecked(cfg['export']['include_timestamp'])
        
        self.sw_lock.setChecked(cfg['security']['lock_mapping_after_start'])
        self.sw_audit.setChecked(cfg['security']['detailed_logging'])

    def save_and_apply(self):
        # Collect & Save
        self.config_service.set_config("general", "app_name", self.in_app_name.text())
        self.config_service.set_config("general", "operator_name", self.in_operator.text())
        
        self.config_service.set_config("engine", "auto_trim", self.sw_trim.isChecked())
        self.config_service.set_config("engine", "auto_upper", self.sw_upper.isChecked())
        self.config_service.set_config("engine", "case_sensitive_match", self.sw_case_sens.isChecked())
        
        self.config_service.set_config("export", "default_format", self.cb_format.currentText())
        self.config_service.set_config("export", "include_timestamp", self.sw_timestamp.isChecked())
        
        self.config_service.set_config("security", "lock_mapping_after_start", self.sw_lock.isChecked())
        self.config_service.set_config("security", "detailed_logging", self.sw_audit.isChecked())
        
        self.config_service.save_config()
        self.accept()
