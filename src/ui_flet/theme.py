import flet as ft
from core.services.theme_service import ThemeService

class PlatinumTheme:
    """
    Sistema de Temas v0.6.0 (Platinum Edition).
    Ponte entre o ThemeService (Tokens) e a UI Flet.
    """
    _service = ThemeService()
    
    # 🎨 GETTERS DINÂMICOS (v0.6.0 Platinum - Estabilização Arquitetural)
    # Garantem que ao trocar de tema, a UI acesse o valor atualizado e não o congelado no boot.

    @classmethod
    def token(cls, key: str): return cls._service.current_theme.get(key, "#FF00FF")

    @classmethod
    def PRIMARY(cls): return cls.token("action_bg")
    
    @classmethod
    def SUCCESS(cls): return cls.token("success_bg")
    
    @classmethod
    def WARNING(cls): return cls.token("warning_bg")
    
    @classmethod
    def DANGER(cls): return cls.token("danger_bg")
    
    @classmethod
    def SURFACE_DARK(cls): return cls.token("surface_col")
    
    @classmethod
    def BG_DARK(cls): return cls.token("bg_col")
    
    @classmethod
    def BORDER_DARK(cls): return cls.token("border_col")
    
    @classmethod
    def TEXT_PRIMARY(cls): return cls.token("fg_col")
    
    @classmethod
    def TEXT_SECONDARY(cls): return cls.token("fg_secondary")
    
    @classmethod
    def TEXT_MUTED(cls): return cls.token("fg_muted")
    
    @classmethod
    def TEXT_PLACEHOLDER(cls): return cls.token("fg_placeholder")

    # Iconografia Centralizada
    Icons = ThemeService.Icons

    @staticmethod
    def apply_to_page(page: ft.Page):
        """Aplica o tema atual do ThemeService à página Flet (v0.6.0 Alpha)."""
        t = PlatinumTheme._service.current_theme
        
        # 🔗 ThemeMode Dinâmico via Luminância (Elimina Conflitos no Light Mode)
        bg_color = t["bg_col"]
        is_dark = PlatinumTheme._service.get_contrast_color(bg_color) == "#FFFFFF"
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        
        page.theme = PlatinumTheme._service.get_flet_theme()
        page.bgcolor = bg_color
        
        # Window API v0.82+
        page.window.title_bar_hidden = True
        page.window.title_bar_buttons_hidden = True

    @staticmethod
    def card_style():
        """Retorna o estilo padrão para cards em conformidade com o tema ativo."""
        t = PlatinumTheme._service.current_theme
        return {
            "bgcolor": t["surface_col"],
            "border": ft.border.all(1, t["border_col"]),
            "border_radius": 12,
            "padding": 20
        }
