import json
import os
from version import __version__
import flet as ft

class ThemeService:
    # 🏁 METADADOS AMIGÁVEIS
    TOKEN_LABELS = {
        "bg_col": "Fundo da Janela",
        "fg_col": "Texto Principal",
        "fg_secondary": "Texto Secundário",
        "fg_muted": "Texto Subtil/Muted",
        "fg_placeholder": "Texto de Placeholder",
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
            "bg_col": "#09090B",
            "fg_col": "#FAFAFA",
            "fg_secondary": "#A1A1AA", # Zinc 400
            "fg_muted": "#71717A",     # Zinc 500
            "fg_placeholder": "#52525B",# Zinc 600
            "surface_col": "#18181B",
            "border_col": "#27272A",
            "action_bg": "#3B82F6",
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
            "bg_col": "#F1F5F9",        # Slate 100 - Mais claro p/ contraste real
            "fg_col": "#0F172A",        # Deep Navy
            "fg_secondary": "#334155",  # Slate 700 - Muito mais nítido
            "fg_muted": "#64748B",      # Slate 500
            "fg_placeholder": "#94A3B8",# Slate 400
            "surface_col": "#FFFFFF",
            "border_col": "#CBD5E1",
            "action_bg": "#1D4ED8",
            "action_fg": "#FFFFFF",
            "titlebar_bg": "#E2E8F0",
            "titlebar_text": "#1E293B",
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
        self.auto_sync_contrast() # Forçar carga dos tokens dinâmicos no boot

    def load_theme(self):
        """Carrega o tema ativo garantindo isolamento total."""
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

    def _interpolate_color(self, color1_hex, color2_hex, factor):
        """Interpola entre duas cores para criar variações de contraste."""
        c1 = self.get_rgb(color1_hex)
        c2 = self.get_rgb(color2_hex)
        r = int(c1[0] + (c2[0] - c1[0]) * factor)
        g = int(c1[1] + (c2[1] - c1[1]) * factor)
        b = int(c1[2] + (c2[2] - c1[2]) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def auto_sync_contrast(self):
        """Sincroniza automaticamente os tokens de texto com seus respectivos fundos."""
        bg = self.current_theme["bg_col"]
        # Texto Principal (Máximo Contraste)
        primary = self.get_contrast_color(bg)
        self.current_theme["fg_col"] = primary
        
        # Hierarquia Baseada no Fundo (Interpolação p/ evitar visual lavado)
        # Se o fundo é claro, interpolamos em direção ao preto. Se escuro, em direção ao fundo.
        # No Flet, para placeholders e secundários, precisamos de cores sólidas nítidas.
        is_dark = self.get_contrast_color(bg) == "#FFFFFF"
        
        # Níveis de Contraste (Fatores de suavização)
        self.current_theme["fg_secondary"] = self._interpolate_color(primary, bg, 0.2)
        self.current_theme["fg_muted"] = self._interpolate_color(primary, bg, 0.45)
        self.current_theme["fg_placeholder"] = self._interpolate_color(primary, bg, 0.6)
        
        self.current_theme["action_fg"] = self.get_contrast_color(self.current_theme["action_bg"])
        self.current_theme["titlebar_text"] = self.get_contrast_color(self.current_theme["titlebar_bg"])
        
    def get_flet_theme(self):
        """Conversor Dinâmico Platinum: Transforma tokens puros em ft.Theme robusto, reativo e compatível."""
        t = self.current_theme
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=t["action_bg"],
                on_primary=t["action_fg"],
                surface=t["surface_col"],
                on_surface=t["fg_col"],
                outline=t["border_col"],
                error=t["danger_bg"],
                on_error="#FFFFFF", # O erro quase sempre exige fundo branco p/ icones mas t["fg_col"] é mais seguro
            ),
            visual_density=ft.VisualDensity.COMPACT,
        )

    class Icons:
        """Iconografia Linear Platinum 2026 (Chat-GPT Style)"""
        WIZARD = ft.Icons.AUTO_AWESOME_OUTLINED
        HISTORY = ft.Icons.HISTORY_OUTLINED
        SETTINGS = ft.Icons.SETTINGS_OUTLINED
        FILE_SOURCE = ft.Icons.UPLOAD_FILE_OUTLINED
        FILE_TARGET = ft.Icons.DOWNLOAD_DONE_OUTLINED
        LINK = ft.Icons.LINK_OUTLINED
        CHECK = ft.Icons.CHECK_CIRCLE_OUTLINED
        ERROR = ft.Icons.ERROR_OUTLINE_ROUNDED
        INFO = ft.Icons.INFO_OUTLINE_ROUNDED
        CLOSE = ft.Icons.CLOSE_OUTLINED
        MAXIMIZE = ft.Icons.MAXIMIZE_OUTLINED
        APP_LOGO = ft.Icons.DATA_EXPLORATION_OUTLINED

    # get_qss() removido (Cleanup de Legado Qt)


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Serviço de temas dinâmicos com cálculo de luminância e bridge para Flet")
