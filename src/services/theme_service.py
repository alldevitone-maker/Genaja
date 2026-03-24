import json
import os

class ThemeService:
    # 🏁 METADADOS AMIGÁVEIS (v0.5.6 Professional 2026)
    TOKEN_LABELS = {
        "bg_col": "Fundo da Janela",
        "fg_col": "Texto Principal",
        "surface_col": "Superfície de Cards",
        "border_col": "Contornos e Divisores",
        "action_bg": "Ação Principal (Botões)",
        "action_fg": "Texto em Botões",
        "titlebar_bg": "Fundo da Barra de Título",
        "titlebar_text": "Texto da Barra de Título",
        "titlebar_close_hover": "Hover de Fechamento",
        "success_bg": "Status: Sucesso",
        "warning_bg": "Status: Alerta",
        "danger_bg": "Status: Erro Crítico",
        "pk_bg": "Destaque de Chave (PK)"
    }

    PRESETS = {
        "zinc_studio": {
            "name": "Zinc Studio (Default)",
            "bg_col": "#09090B",        # Deep Zinc
            "fg_col": "#FAFAFA",
            "surface_col": "#18181B",
            "border_col": "#27272A",
            "action_bg": "#3B82F6",     # Modern Azure
            "action_fg": "#FFFFFF",
            "titlebar_bg": "#18181B",
            "titlebar_text": "#A1A1AA",
            "titlebar_close_hover": "#EF4444",
            "success_bg": "#10B981",
            "warning_bg": "#F59E0B",
            "danger_bg": "#EF4444",
            "pk_bg": "#F59E0B"
        },
        "phoenix_dark": {
            "name": "Phoenix Dark",
            "bg_col": "#0D0F12",
            "fg_col": "#E1E1E1",
            "surface_col": "#16191D",
            "border_col": "#2C313A",
            "action_bg": "#8B5CF6",     # Vibrant Violet
            "action_fg": "#FFFFFF",
            "titlebar_bg": "#16191D",
            "titlebar_text": "#CCCCCC",
            "titlebar_close_hover": "#FF4B4B",
            "success_bg": "#10B981",
            "warning_bg": "#F59E0B",
            "danger_bg": "#EF4444",
            "pk_bg": "#F59E0B"
        },
        "light_grey_saas": {
            "name": "Light Grey SaaS",
            "bg_col": "#F8FAFC",
            "fg_col": "#0F172A",
            "surface_col": "#FFFFFF",
            "border_col": "#E2E8F0",
            "action_bg": "#2563EB",
            "action_fg": "#FFFFFF",
            "titlebar_bg": "#FFFFFF",
            "titlebar_text": "#64748B",
            "titlebar_close_hover": "#EF4444",
            "success_bg": "#059669",
            "warning_bg": "#D97706",
            "danger_bg": "#DC2626",
            "pk_bg": "#D97706"
        }
    }

    def __init__(self, config_dir="data"):
        self.config_dir = config_dir
        self.theme_path = os.path.join(config_dir, "theme_active.json")
        self.current_theme = self.load_theme()

    def load_theme(self):
        default = self.PRESETS["zinc_studio"].copy()
        if os.path.exists(self.theme_path):
            try:
                with open(self.theme_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    theme = default.copy()
                    theme.update(saved)
                    return theme
            except Exception:
                return default
        return default

    def save_theme(self, theme_dict=None):
        if theme_dict:
            self.current_theme = theme_dict
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        with open(self.theme_path, "w", encoding="utf-8") as f:
            json.dump(self.current_theme, f, indent=4)

    def apply_preset(self, preset_key):
        if preset_key in self.PRESETS:
            self.current_theme = self.PRESETS[preset_key].copy()
            self.save_theme()
            return True
        return False

    def reset_to_defaults(self):
        self.apply_preset("zinc_studio")

    def get_color(self, key):
        return self.current_theme.get(key, "#FF00FF")

    def get_qss(self):
        t = self.current_theme
        
        return f"""
            QMainWindow, QDialog {{ 
                background-color: {t['bg_col']}; 
                color: {t['fg_col']};
            }}
            
            QWidget#centralWidget {{ 
                background-color: {t['bg_col']}; 
            }}
            
            QLabel {{ 
                color: {t['fg_col']}; 
                font-family: 'Segoe UI', 'Outfit', sans-serif; 
                font-size: 13px;
                border: none;
            }}
            
            QMenuBar {{
                background-color: {t['titlebar_bg']};
                color: {t['titlebar_text']};
                border-bottom: 1px solid {t['border_col']};
                padding: 4px;
            }}
            QMenuBar::item:selected {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
                border-radius: 6px;
            }}
            
            QMenu {{
                background-color: {t['surface_col']};
                color: {t['fg_col']};
                border: 1px solid {t['border_col']};
                border-radius: 8px;
                padding: 6px;
            }}
            QMenu::item:selected {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
                border-radius: 4px;
            }}
            
            QPushButton {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
            QPushButton#titleBarBtn {{
                background-color: transparent;
                border-radius: 0;
            }}
            QPushButton#titleBarClose:hover {{
                background-color: {t['titlebar_close_hover']};
            }}

            QFrame#card {{
                background-color: {t['surface_col']};
                border: 1px solid {t['border_col']};
                border-radius: 16px;
            }}
            
            QStatusBar {{
                background-color: {t['titlebar_bg']};
                color: {t['titlebar_text']};
                border-top: 1px solid {t['border_col']};
            }}
            
            QLineEdit, QComboBox, QScrollArea, QListWidget, QListView {{
                background-color: {t['surface_col']};
                color: {t['fg_col']};
                border: 1px solid {t['border_col']};
                border-radius: 8px;
                padding: 8px;
            }}
            
            QScrollArea {{ border: none; }}
            
            QTabWidget::pane {{
                border: 1px solid {t['border_col']};
                border-radius: 8px;
                background: {t['surface_col']};
            }}
            QTabBar::tab {{
                background: {t['bg_col']};
                color: {t['titlebar_text']};
                padding: 10px 20px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: {t['surface_col']};
                color: {t['fg_col']};
                border: 1px solid {t['border_col']};
                border-bottom-color: {t['surface_col']};
            }}
        """
