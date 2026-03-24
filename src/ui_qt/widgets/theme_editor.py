from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QColorDialog, QRadioButton, 
                             QButtonGroup, QScrollArea, QWidget, QTabWidget)
from PySide6.QtCore import Qt, Signal

class PreviewWidget(QFrame):
    """Mini-App Preview para o Customizer 2026"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setFixedSize(400, 180)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Simulação de Header
        self.lbl_title = QLabel("Preview em Tempo Real")
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.lbl_title)
        
        self.lbl_sub = QLabel("Explore como as cores interagem na interface.")
        self.lbl_sub.setStyleSheet("opacity: 0.7;")
        layout.addWidget(self.lbl_sub)
        
        layout.addStretch()
        
        # Simulação de Ações
        btn_layout = QHBoxLayout()
        self.btn_act = QPushButton("Botão de Ação")
        self.btn_sec = QPushButton("Secundário")
        self.btn_sec.setStyleSheet("background: transparent; border: 1px solid gray;") # Override local p/ preview
        
        btn_layout.addWidget(self.btn_act)
        btn_layout.addWidget(self.btn_sec)
        layout.addLayout(btn_layout)

    def update_style(self, theme_qss):
        self.setStyleSheet(theme_qss)

class ThemeEditor(QDialog):
    themeUpdated = Signal()

    def __init__(self, theme_service, parent=None):
        super().__init__(parent)
        self.theme_service = theme_service
        self.setWindowTitle("Phoenix Customizer 2026 (Premium)")
        self.resize(500, 750)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        self._setup_ui()

    def _setup_ui(self):
        # 🧪 PREVIEW AREA
        self.preview = PreviewWidget()
        self.main_layout.addWidget(QLabel("<b>📺 Preview 2026 Pro</b>"))
        self.main_layout.addWidget(self.preview)
        self.preview.update_style(self.theme_service.get_qss())

        # 🗂️ TABS DE CATEGORIA
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        self._add_presets_tab()
        self._add_fine_tuning_tab()
        self._add_ui_elements_tab()

        # 🏁 RODAPÉ DE AÇÕES
        btn_layout = QHBoxLayout()
        self.btn_reset = QPushButton("♻️ Restaurar Padrão")
        self.btn_reset.clicked.connect(self._reset_defaults)
        
        self.btn_save = QPushButton("💾 Salvar & Aplicar")
        self.btn_save.clicked.connect(self._save_exit)
        self.btn_save.setMinimumHeight(45)
        
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addWidget(self.btn_save)
        self.main_layout.addLayout(btn_layout)

    def _add_presets_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("<b>⚡ Galeria de Estilos Oficiais</b>"))
        
        self.preset_group = QButtonGroup(self)
        for key, preset in self.theme_service.PRESETS.items():
            btn = QPushButton(f"Adoptar: {preset['name']}")
            btn.setCheckable(True)
            if self.theme_service.current_theme.get("name") == preset["name"]:
                btn.setChecked(True)
            btn.clicked.connect(lambda k=key: self._apply_preset(k))
            layout.addWidget(btn)
        layout.addStretch()
        self.tabs.addTab(tab, "Estilos")

    def _add_fine_tuning_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        grid = QVBoxLayout(content)
        
        # Mapeamento do Core Brand
        core_keys = ["bg_col", "surface_col", "fg_col", "action_bg", "action_fg"]
        grid.addWidget(QLabel("<b>🔥 Identidade de Marca</b>"))
        
        for key in core_keys:
            self._create_color_row(grid, key)
            
        scroll.setWidget(content)
        layout.addWidget(scroll)
        self.tabs.addTab(tab, "Identidade")

    def _add_ui_elements_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        grid = QVBoxLayout(content)
        
        # UI & System elements
        ui_keys = ["titlebar_bg", "titlebar_text", "border_col", "success_bg", "warning_bg", "danger_bg", "pk_bg"]
        grid.addWidget(QLabel("<b>🎨 Detalhes de Interface</b>"))
        
        for key in ui_keys:
            self._create_color_row(grid, key)
            
        scroll.setWidget(content)
        layout.addWidget(scroll)
        self.tabs.addTab(tab, "Elementos")

    def _create_color_row(self, layout, key):
        row = QHBoxLayout()
        label_text = self.theme_service.TOKEN_LABELS.get(key, key)
        lbl = QLabel(label_text)
        
        btn = QPushButton()
        btn.setFixedSize(60, 24)
        color = self.theme_service.get_color(key)
        btn.setStyleSheet(f"background-color: {color}; border: 2px solid white; border-radius: 12px;")
        btn.clicked.connect(lambda k=key, b=btn: self._pick_color(k, b))
        
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(btn)
        layout.addLayout(row)

    def _pick_color(self, key, btn):
        current_color = self.theme_service.get_color(key)
        color = QColorDialog.getColor(current_color, self, f"Ajustar: {self.theme_service.TOKEN_LABELS.get(key)}")
        if color.isValid():
            hex_color = color.name()
            self.theme_service.current_theme[key] = hex_color
            btn.setStyleSheet(f"background-color: {hex_color}; border: 2px solid white; border-radius: 12px;")
            self.preview.update_style(self.theme_service.get_qss())
            self.themeUpdated.emit()

    def _apply_preset(self, key):
        self.theme_service.apply_preset(key)
        self.preview.update_style(self.theme_service.get_qss())
        self.themeUpdated.emit()
        # Refresh UI
        self.close()
        ThemeEditor(self.theme_service, self.parent()).show()

    def _save_exit(self):
        self.theme_service.save_theme()
        self.accept()

    def _reset_defaults(self):
        self.theme_service.reset_to_defaults()
        self.themeUpdated.emit()
        self.accept()
