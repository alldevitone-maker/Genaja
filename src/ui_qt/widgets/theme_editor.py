from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QColorDialog, QRadioButton, 
                             QButtonGroup, QScrollArea, QWidget)
from PySide6.QtCore import Qt, Signal

class ThemeEditor(QDialog):
    themeUpdated = Signal()

    def __init__(self, theme_service, parent=None):
        super().__init__(parent)
        self.theme_service = theme_service
        self.setWindowTitle("Phoenix Customizer 2.0")
        self.resize(450, 650)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)
        
        self._setup_ui()

    def _setup_ui(self):
        # 1. PRESETS RÁPIDOS
        self.layout.addWidget(QLabel("<b>⚡ Temas Rápidos</b>"))
        self.preset_group = QButtonGroup(self)
        
        preset_layout = QHBoxLayout()
        for key, preset in self.theme_service.PRESETS.items():
            rb = QRadioButton(preset["name"])
            self.preset_group.addButton(rb)
            preset_layout.addWidget(rb)
            if self.theme_service.current_theme.get("name") == preset["name"]:
                rb.setChecked(True)
            rb.clicked.connect(lambda k=key: self._apply_preset(k))
        self.layout.addLayout(preset_layout)
        
        self.layout.addWidget(QFrame()) # Spacer
        
        # 2. EDITOR DE CORES (Scrollable)
        self.layout.addWidget(QLabel("<b>🎨 Personalização Fina</b>"))
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        self.grid = QVBoxLayout(content)
        
        # Categorias amigáveis
        categories = {
            "Cores Principais": ["bg_col", "surface_col", "fg_col", "border_col"],
            "Ações": ["action_bg"],
            "Barra de Título": ["titlebar_bg", "titlebar_text"],
            "Status": ["success_bg", "warning_bg", "danger_bg"]
        }
        
        for cat, keys in categories.items():
            self.grid.addWidget(QLabel(f"<i>{cat}</i>"))
            for key in keys:
                row = QHBoxLayout()
                lbl = QLabel(key.replace("_", " ").title())
                btn = QPushButton()
                btn.setFixedSize(50, 20)
                color = self.theme_service.get_color(key)
                btn.setStyleSheet(f"background-color: {color}; border: 1px solid white;")
                btn.clicked.connect(lambda k=key, b=btn: self._pick_color(k, b))
                
                row.addWidget(lbl)
                row.addStretch()
                row.addWidget(btn)
                self.grid.addLayout(row)
        
        scroll.setWidget(content)
        self.layout.addWidget(scroll)
        
        # 3. AÇÕES FINAIS
        self.layout.addWidget(QFrame())
        btn_layout = QHBoxLayout()
        
        self.btn_save = QPushButton("Salvar Permanentemente")
        self.btn_save.clicked.connect(self._save_exit)
        
        self.btn_reset = QPushButton("Restaurar Zinc (Padrão)")
        self.btn_reset.clicked.connect(self._reset_defaults)
        
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addWidget(self.btn_save)
        self.layout.addLayout(btn_layout)

    def _pick_color(self, key, btn):
        current_color = self.theme_service.get_color(key)
        color = QColorDialog.getColor(current_color, self, f"Escolha: {key}")
        if color.isValid():
            hex_color = color.name()
            self.theme_service.current_theme[key] = hex_color
            btn.setStyleSheet(f"background-color: {hex_color}; border: 1px solid white;")
            self.themeUpdated.emit()

    def _apply_preset(self, key):
        self.theme_service.apply_preset(key)
        self.themeUpdated.emit()
        self.close() # Reopen to refresh color pickers if needed, or better:
        ThemeEditor(self.theme_service, self.parent()).show()
        self.close()

    def _save_exit(self):
        self.theme_service.save_theme()
        self.accept()

    def _reset_defaults(self):
        self.theme_service.reset_to_defaults()
        self.themeUpdated.emit()
        self.accept()
