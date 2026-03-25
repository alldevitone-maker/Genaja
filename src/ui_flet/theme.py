import flet as ft

class PlatinumTheme:
    """
    Sistema de Temas v0.6.0 (Platinum Edition).
    Cores harmonizadas baseadas em HSL para UX premium.
    """
    # Palette - Dark Mode
    BG_DARK = "#09090b"
    SURFACE_DARK = "#18181b"
    BORDER_DARK = "#27272a"
    TEXT_PRIMARY = "#fafafa"
    TEXT_SECONDARY = "#a1a1aa"
    
    # Palette - Light Mode
    BG_LIGHT = "#f8fafc"
    SURFACE_LIGHT = "#ffffff"
    BORDER_LIGHT = "#e2e8f0"
    TEXT_PRIMARY_LIGHT = "#0f172a"
    TEXT_SECONDARY_LIGHT = "#64748b"
    
    # Brand Colors
    PRIMARY = "#3b82f6"      # Blue
    SUCCESS = "#10b981"      # Emerald
    WARNING = "#f59e0b"      # Amber
    DANGER = "#ef4444"       # Rose

    @staticmethod
    def apply_to_page(page: ft.Page):
        page.theme_mode = ft.ThemeMode.DARK # Padrão v0.6.0
        page.bgcolor = PlatinumTheme.BG_DARK
        page.window_title_bar_hidden = True
        page.window_title_bar_buttons_hidden = True
        
        # Custom Theme Configuration
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=PlatinumTheme.PRIMARY,
                surface=PlatinumTheme.SURFACE_DARK,
                on_surface=PlatinumTheme.TEXT_PRIMARY,
                outline=PlatinumTheme.BORDER_DARK
            ),
            visual_density=ft.VisualDensity.COMPACT
        )
        page.update()

    @staticmethod
    def card_style():
        return {
            "bgcolor": PlatinumTheme.SURFACE_DARK,
            "border": ft.border.all(1, PlatinumTheme.BORDER_DARK),
            "border_radius": 12,
            "padding": 20
        }
