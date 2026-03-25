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
            "bg_col": "#E2E8F0",        # Slate 200 - Fundo Profundo
            "fg_col": "#0F172A",        # Deep Navy
            "surface_col": "#FFFFFF",   # Pure White - Cards "Papel"
            "border_col": "#CBD5E1",    # Slate 300 - Bordas Definidas
            "action_bg": "#1D4ED8",     # Saturated Blue
            "action_fg": "#FFFFFF",
            "titlebar_bg": "#F1F5F9",   # Slate 100
            "titlebar_text": "#1E293B", # Dark Slate
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
        """Carrega o tema ativo garantindo isolamento total (v0.5.9 Phase 5)"""
        # Sempre começar com uma cópia pura do preset default (Zinc)
        default_preset = self.PRESETS["zinc_studio"].copy()
        
        if os.path.exists(self.theme_path):
            try:
                with open(self.theme_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                
                # REVISÃO DE ISOLAMENTO: 
                # Se o tema salvo não for o Zinc, ele pode ter chaves viciadas.
                # Vamos identificar se há um 'preset_origin' salvo ou assumir Zinc.
                origin = saved.get("preset_origin", "zinc_studio")
                if origin not in self.PRESETS: origin = "zinc_studio"
                
                # 1. Obter snapshot puro do preset original
                full_theme = self.PRESETS[origin].copy()
                
                # 2. Aplicar APENAS tokens válidos do arquivo salvo (Nada de chaves fantasmas)
                for key in self.TOKEN_LABELS:
                    if key in saved:
                        full_theme[key] = saved[key]
                
                # 3. Guardar origem para persistência futura
                full_theme["preset_origin"] = origin
                return full_theme
            except Exception:
                return default_preset
        return default_preset

    def save_theme(self, theme_dict=None):
        if theme_dict:
            self.current_theme = theme_dict
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        # Garantir limpeza de lixo antes de salvar o snapshot
        clean_snapshot = {k: self.current_theme[k] for k in self.TOKEN_LABELS if k in self.current_theme}
        clean_snapshot["preset_origin"] = self.current_theme.get("preset_origin", "zinc_studio")
        clean_snapshot["name"] = self.current_theme.get("name", "Custom Theme")
        
        with open(self.theme_path, "w", encoding="utf-8") as f:
            json.dump(clean_snapshot, f, indent=4)

    def apply_preset(self, preset_key):
        """Substituição total por Snapshot Puro (Sem contaminação)"""
        if preset_key in self.PRESETS:
            # 1. Cópia profunda do preset oficial
            self.current_theme = self.PRESETS[preset_key].copy()
            # 2. Marcar origem original
            self.current_theme["preset_origin"] = preset_key
            # 3. Forçar recalculação de contrastes (Luminance Guard)
            self.auto_sync_contrast()
            # 4. Persistir snapshot limpo
            self.save_theme()
            return True
        return False

    def reset_to_defaults(self):
        self.apply_preset("zinc_studio")

    def get_color(self, key):
        return self.current_theme.get(key, "#FF00FF")

    def get_contrast_color(self, hex_color):
        """Calcula se o texto deve ser preto ou branco com base na luminância"""
        r, g, b = self.get_rgb(hex_color)
        # Formula de Luminância Perceptual (W3C)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return "#000000" if luminance > 0.5 else "#FFFFFF"

    def get_rgb(self, hex_color):
        """Retorna tupla (R, G, B) a partir de hex."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6: return (255, 0, 255)
        return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

    def auto_sync_contrast(self):
        """Sincroniza automaticamente os tokens de texto com seus respectivos fundos"""
        self.current_theme["fg_col"] = self.get_contrast_color(self.current_theme["bg_col"])
        self.current_theme["action_fg"] = self.get_contrast_color(self.current_theme["action_bg"])
        self.current_theme["titlebar_text"] = self.get_contrast_color(self.current_theme["titlebar_bg"])
        
    def get_qss(self):
        t = self.current_theme
        
        # Helperes para opacidade dinâmica
        r_act, g_act, b_act = self.get_rgb(t['action_bg'])
        r_fg, g_fg, b_fg = self.get_rgb(t['fg_col'])
        
        return f"""
            /* RESET GLOBAL E ISOLAMENTO */
            * {{
                outline: none;
            }}

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
                background-color: transparent;
                border: none;
            }}
            
            QWidget#titleBar {{
                background-color: {t['titlebar_bg']};
                border-bottom: 2px solid {t['border_col']};
            }}
            
            QMenuBar {{
                background-color: transparent;
                color: {t['titlebar_text']};
                border: none;
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
                border-radius: 10px;
                padding: 8px;
            }}
            QMenu::item {{
                padding: 6px 25px 6px 15px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
            }}
            
            QListView::item:selected {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
                border-radius: 6px;
            }}
            
            QListWidget#sidebar {{
                background-color: {t['surface_col']};
                border: none;
                border-right: 1px solid {t['border_col']};
                border-radius: 0;
            }}
            QListWidget#sidebar::item {{
                padding: 15px;
                border-bottom: 1px solid {t['border_col']};
            }}
            QListWidget#sidebar::item:selected {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
                border-left: 4px solid {t['fg_col']};
            }}

            QFrame#sidebar_main {{
                background-color: {t['surface_col']};
                border-right: 1px solid {t['border_col']};
            }}
        
            QPushButton {{
                background-color: transparent;
                color: {t['action_bg']};
                border: 2px solid {t['action_bg']};
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
            }}
            QPushButton#titleBarBtn {{
                background-color: transparent;
                border: none;
                border-radius: 0;
                color: {t['titlebar_text']};
                font-size: 16px;
            }}
            QPushButton#titleBarBtn:hover {{
                background-color: rgba({r_fg}, {g_fg}, {b_fg}, 0.1);
            }}
            QPushButton#titleBarClose:hover {{
                background-color: {t['titlebar_close_hover']};
                color: #FFFFFF;
            }}

            QFrame#card, QFrame#SettingCard, QFrame#SettingsContainer, QFrame#EditorContainer {{
                background-color: {t['surface_col']};
                border: 1px solid {t['border_col']};
                border-radius: 16px;
            }}
            QFrame#SettingsContainer, QFrame#EditorContainer {{
                background-color: {t['bg_col']};
            }}
            QFrame#SettingCard:hover {{
                border: 1px solid {t['action_bg']};
            }}
            
            QStatusBar {{
                background-color: {t['titlebar_bg']};
                color: {t['titlebar_text']};
                border-top: 1px solid {t['border_col']};
                font-size: 11px;
            }}
            
            QLineEdit, QComboBox, QListWidget, QListView {{
                background-color: {t['surface_col']};
                color: {t['fg_col']};
                border: 2px solid {t['border_col']};
                border-radius: 8px;
                padding: 8px;
            }}
            QLineEdit:focus {{
                border: 2px solid {t['action_bg']};
            }}
            
            QScrollArea {{ 
                background-color: transparent;
                border: none; 
            }}
            
            /* CUSTOM SCROLLBAR HARMONY */
            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {t['border_col']};
                min-height: 30px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {t['action_bg']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

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

            QPushButton#SidebarButton {{
                background-color: transparent;
                color: {t['titlebar_text']};
                text-align: center;
                border: none;
                border-radius: 12px;
                font-size: 20px;
            }}
            QPushButton#SidebarButton:hover {{
                background-color: rgba({r_fg}, {g_fg}, {b_fg}, 0.08);
                color: {t['fg_col']};
            }}
            QPushButton#SidebarButton[active="true"] {{
                background-color: rgba({r_act}, {g_act}, {b_act}, 0.15);
                color: {t['action_bg']};
                border: 1px solid rgba({r_act}, {g_act}, {b_act}, 0.3);
            }}

            QToolTip {{
                background-color: {t['surface_col']};
                color: {t['fg_col']};
                border: 1px solid {t['border_col']};
                border-radius: 6px;
                padding: 6px;
            }}

            .secondary-text {{
                color: {t['titlebar_text']};
                background-color: transparent;
            }}

            QPushButton#PrimaryButton, .primary-btn {{
                background-color: {t['action_bg']};
                color: {t['action_fg']};
                border: none;
            }}

            QPushButton#SuccessButton, .success-btn {{
                background-color: {t['success_bg']};
                color: #FFFFFF;
                border: none;
            }}

            QPushButton#DangerButton, .danger-btn {{
                background-color: {t['danger_bg']};
                color: #FFFFFF;
                border: none;
            }}

            QLabel#TitleLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {t['action_bg']};
                background: transparent;
            }}

            QFrame#DropZone {{
                border: 2px dashed {t['border_col']};
                border-radius: 16px;
                background-color: rgba({r_act}, {g_act}, {b_act}, 0.02);
            }}
            QFrame#DropZone[active="true"] {{
                border: 2px dashed {t['action_bg']};
                background-color: rgba({r_act}, {g_act}, {b_act}, 0.1);
            }}

            /* THEME PREVIEW CARD */
            QFrame#PreviewCard {{
                background-color: {t['bg_col']};
                border: 2px solid {t['action_bg']};
                border-radius: 16px;
            }}
            QFrame#PreviewCard QLabel {{ font-weight: bold; }}
            
            .success-text {{ color: {t['success_bg']}; font-weight: bold; }}
            .danger-text {{ color: {t['danger_bg']}; font-weight: bold; }}
            .action-text {{ color: {t['action_bg']}; font-weight: bold; }}
        """
