import json
import os

class ThemeService:
    # 1. RESERVATÓRIO DE PRESETS OFICIAIS (v0.5.3)
    PRESETS = {
        "zinc_studio": {
            "name": "Zinc Studio (Default)",
            "bg_col": "#1E1E1E",        # VS Code Dark
            "fg_col": "#CCCCCC",        # Neutral Light
            "surface_col": "#252526",   # Slightly Lighter
            "border_col": "#3F3F3F",    # Subtle Border
            "action_bg": "#007ACC",     # VS Code Blue
            "action_fg": "white",
            "titlebar_bg": "#323233",   # Titlebar
            "titlebar_text": "#919191",
            "titlebar_close_hover": "#E81123",
            "success_bg": "#198754",
            "success_fg": "white",
            "warning_bg": "#FFC107",
            "warning_fg": "#111827",
            "danger_bg": "#DC3545",
            "danger_fg": "white",
            "neutral_bg": "#6C757D",
            "neutral_fg": "white",
            "pk_bg": "#FFC107",
            "pk_fg": "#111827"
        },
        "phoenix_dark": {
            "name": "Phoenix Dark",
            "bg_col": "#0D0F12",        # Profundo
            "fg_col": "#E1E1E1",
            "surface_col": "#16191D",
            "border_col": "#2C313A",
            "action_bg": "#6D28D9",     # Purple Tech
            "action_fg": "white",
            "titlebar_bg": "#16191D",
            "titlebar_text": "#CCCCCC",
            "titlebar_close_hover": "#FF4B4B",
            "success_bg": "#10B981",
            "success_fg": "white",
            "warning_bg": "#F59E0B",
            "warning_fg": "white",
            "danger_bg": "#EF4444",
            "danger_fg": "white",
            "neutral_bg": "#4B5563",
            "neutral_fg": "white",
            "pk_bg": "#F59E0B",
            "pk_fg": "white"
        },
        "light_grey_saas": {
            "name": "Light Grey SaaS",
            "bg_col": "#F3F4F6",        # Grey Light Win11
            "fg_col": "#1F2937",
            "surface_col": "#FFFFFF",
            "border_col": "#E5E7EB",
            "action_bg": "#2563EB",     # SaaS Blue
            "action_fg": "white",
            "titlebar_bg": "#FFFFFF",
            "titlebar_text": "#4B5563",
            "titlebar_close_hover": "#E81123",
            "success_bg": "#059669",
            "success_fg": "white",
            "warning_bg": "#D97706",
            "warning_fg": "white",
            "danger_bg": "#B91C1C",
            "danger_fg": "white",
            "neutral_bg": "#9CA3AF",
            "neutral_fg": "white",
            "pk_bg": "#D97706",
            "pk_fg": "white"
        }
    }

    def __init__(self, config_dir="data"):
        self.config_dir = config_dir
        self.theme_path = os.path.join(config_dir, "theme_active.json")
        self.current_theme = self.load_theme()

    def load_theme(self):
        # Default de segurança (Zinc Studio)
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
        hover_bg = t.get('action_bg_hover', t['action_bg']) # Fallback dinâmico
        
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
                padding: 2px;
            }}
            QMenuBar::item:selected {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
                border-radius: 4px;
            }}
            
            QMenu {{
                background-color: {t['surface_col']};
                color: {t['fg_col']};
                border: 1px solid {t['border_col']};
                border-radius: 6px;
                padding: 4px;
            }}
            QMenu::item:selected {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
            }}
            
            QPushButton {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
                background-color: {hover_bg};
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
                border-radius: 12px;
            }}
            
            QStatusBar {{
                background-color: {t['titlebar_bg']};
                color: {t['titlebar_text']};
                border-top: 1px solid {t['border_col']};
                font-size: 11px;
            }}
            
            QLineEdit, QComboBox, QScrollArea {{
                background-color: {t['surface_col']};
                color: {t['fg_col']};
                border: 1px solid {t['border_col']};
                border-radius: 6px;
                padding: 5px;
            }}
            
            QListView, QListWidget {{
                background-color: {t['surface_col']};
                color: {t['fg_col']};
                border: 1px solid {t['border_col']};
                border-radius: 6px;
                padding: 5px;
            }}
            QListView::item:selected {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
                border-radius: 4px;
            }}
        """
