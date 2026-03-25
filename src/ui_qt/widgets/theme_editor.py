from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QStackedWidget, QWidget, 
                             QScrollArea, QColorDialog)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from ui_qt.widgets.settings_widgets import SettingCard, SidebarButton

class PreviewWidget(QFrame):
    """Mini-App Preview aprimorado para o Customizer 2026"""
    def __init__(self, theme_service, parent=None):
        super().__init__(parent)
        self.theme_service = theme_service
        self.setObjectName("PreviewCard")
        self.setFixedSize(400, 200)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.lbl_title = QLabel("Preview 2026 Pro")
        self.lbl_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.lbl_sub = QLabel("Explore como as cores interagem na interface.")
        self.lbl_sub.setStyleSheet("opacity: 0.7; font-size: 12px;")
        
        self.layout.addWidget(self.lbl_title)
        self.layout.addWidget(self.lbl_sub)
        self.layout.addStretch()
        
        btn_layout = QHBoxLayout()
        self.btn_act = QPushButton("Botão de Ação")
        self.btn_act.setMinimumHeight(40)
        self.btn_sec = QPushButton("Secundário")
        self.btn_sec.setStyleSheet("background: transparent; border: 1px solid #3F3F46;")
        
        btn_layout.addWidget(self.btn_act)
        btn_layout.addWidget(self.btn_sec)
        self.layout.addLayout(btn_layout)
        
        self.update_style()

    def update_style(self):
        t = self.theme_service.current_theme
        self.setStyleSheet(f"""
            QFrame#PreviewCard {{
                background-color: {t['bg_col']};
                border: 2px solid {t['action_bg']};
                border-radius: 16px;
            }}
            QLabel {{ color: {t['fg_col']}; }}
            QPushButton {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
                border-radius: 8px;
            }}
        """)

class ThemeEditor(QDialog):
    themeUpdated = Signal()

    def __init__(self, theme_service, parent=None):
        super().__init__(parent)
        self.theme_service = theme_service
        self.setWindowTitle("Phoenix Customizer 2026")
        self.resize(900, 650)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.container = QFrame(self)
        self.container.setObjectName("EditorContainer")
        self.container.setStyleSheet(f"""
            QFrame#EditorContainer {{
                background-color: {self.theme_service.get_color('bg_col')};
                border: 1px solid {self.theme_service.get_color('border_col')};
                border-radius: 16px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.container)
        
        self.setup_ui()

    def setup_ui(self):
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # 1. SIDEBAR
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setFixedWidth(200)
        self.sidebar_frame.setStyleSheet(f"background-color: {self.theme_service.get_color('surface_col')}; border-right: 1px solid {self.theme_service.get_color('border_col')}; border-top-left-radius: 16px; border-bottom-left-radius: 16px;")
        
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(5)
        
        brand_label = QLabel("PHOENIX")
        brand_label.setStyleSheet(f"color: {self.theme_service.get_color('action_bg')}; font-weight: bold; font-size: 18px; margin-left: 20px; margin-bottom: 20px;")
        sidebar_layout.addWidget(brand_label)
        
        self.nav_buttons = []
        nav_items = [("🎨 Presets", 0), ("🔥 Core Brand", 1), ("🧱 UI Elements", 2)]
        for text, idx in nav_items:
            btn = SidebarButton(text)
            btn.setObjectName("SidebarButton")
            btn.setProperty("active", idx == 0)
            btn.clicked.connect(lambda chk=False, i=idx: self.switch_page(i))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        sidebar_layout.addStretch()
        container_layout.addWidget(self.sidebar_frame)
        
        # 2. CONTENT AREA
        self.content_area = QFrame()
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(30, 30, 30, 20)
        
        # Preview Card (Sempre Visível no topo do editor)
        self.preview = PreviewWidget(self.theme_service)
        content_layout.addWidget(self.preview, 0, Qt.AlignCenter)
        content_layout.addSpacing(20)
        
        self.page_stack = QStackedWidget()
        content_layout.addWidget(self.page_stack)
        
        self._create_pages()
        
        # Footer
        footer_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Close")
        self.btn_cancel.setStyleSheet("background: transparent; border: 1px solid #3F3F46;")
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_apply = QPushButton("Save & Adopt Theme")
        self.btn_apply.clicked.connect(self.save_and_exit)
        
        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_cancel)
        footer_layout.addWidget(self.btn_apply)
        content_layout.addLayout(footer_layout)
        
        container_layout.addWidget(self.content_area)

    def _create_pages(self):
        # PAGE 0: PRESETS
        p0 = QWidget()
        l0 = QVBoxLayout(p0)
        for key, p in self.theme_service.PRESETS.items():
            btn = QPushButton(f"Apply {p['name']}")
            btn.setFixedHeight(45)
            btn.clicked.connect(lambda chk=False, k=key: self.apply_preset(k))
            l0.addWidget(btn)
        l0.addStretch()
        self.page_stack.addWidget(p0)
        
        # PAGE 1: CORE BRAND
        p1 = QScrollArea()
        p1.setWidgetResizable(True)
        w1 = QWidget()
        l1 = QVBoxLayout(w1)
        core_keys = ["bg_col", "surface_col", "fg_col", "action_bg", "action_fg"]
        for k in core_keys:
            self._add_color_card(l1, k)
        l1.addStretch()
        p1.setWidget(w1)
        self.page_stack.addWidget(p1)
        
        # PAGE 2: UI ELEMENTS
        p2 = QScrollArea()
        p2.setWidgetResizable(True)
        w2 = QWidget()
        l2 = QVBoxLayout(w2)
        ui_keys = ["titlebar_bg", "titlebar_text", "border_col", "success_bg", "warning_bg", "danger_bg", "pk_bg"]
        for k in ui_keys:
            self._add_color_card(l2, k)
        l2.addStretch()
        p2.setWidget(w2)
        self.page_stack.addWidget(p2)

    def _add_color_card(self, layout, key):
        color = self.theme_service.get_color(key)
        btn = QPushButton()
        btn.setFixedSize(50, 30)
        btn.setStyleSheet(f"background-color: {color}; border: 1px solid white; border-radius: 6px;")
        btn.clicked.connect(lambda: self.pick_color(key, btn))
        
        label = self.theme_service.TOKEN_LABELS.get(key, key)
        layout.addWidget(SettingCard(label, f"Hex: {color}", btn))

    def switch_page(self, index):
        self.page_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def pick_color(self, key, btn):
        color = QColorDialog.getColor(QColor(self.theme_service.get_color(key)), self)
        if color.isValid():
            hex_c = color.name()
            self.theme_service.current_theme[key] = hex_c
            
            # Se mudar um fundo, sincronizar contraste automaticamente
            if key in ["bg_col", "action_bg", "titlebar_bg"]:
                self.theme_service.auto_sync_contrast()
                
            btn.setStyleSheet(f"background-color: {hex_c}; border: 1px solid white; border-radius: 6px;")
            self.preview.update_style()
            self.themeUpdated.emit()

    def apply_preset(self, key):
        self.theme_service.apply_preset(key)
        self.preview.update_style()
        self.themeUpdated.emit()
        self.close()
        ThemeEditor(self.theme_service, self.parent()).show()

    def save_and_exit(self):
        self.theme_service.save_theme()
        self.accept()
