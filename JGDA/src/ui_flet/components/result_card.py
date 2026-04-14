import flet as ft
from ui_flet.theme import PlatinumTheme
from version import __version__

class ResultCard(ft.Container):
    """
    Card de Resultado Inteligente (v0.7.3).
    Representa uma sessão de extração única e consolidada.
    """
    def __init__(self, col_id, col_mvf, count, on_curadoria, on_export_primary, on_export_contacts):
        super().__init__()
        self.col_id = col_id
        self.col_mvf = col_mvf
        self.count = count
        
        # Estilização Platinum
        self.padding = 15
        self.border_radius = 12
        self.bgcolor = ft.Colors.with_opacity(0.03, PlatinumTheme.PRIMARY())
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.1, PlatinumTheme.BORDER_DARK()))
        
        # Referências de Botões (v0.7.2 Resiliente)
        self.btn_curadoria = ft.ElevatedButton(
            "Curadoria Visual", 
            icon=ft.Icons.DRAG_INDICATOR, 
            on_click=on_curadoria, 
            bgcolor=ft.Colors.ORANGE_900, 
            color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
        )
        
        self.btn_mestre = ft.ElevatedButton(
            "Mestre (1:1)", 
            icon=ft.Icons.SAVE_ALT, 
            on_click=on_export_primary, 
            bgcolor=ft.Colors.GREEN_900, 
            color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
        )
        
        self.btn_contatos = ft.ElevatedButton(
            "Contatos (1:N)", 
            icon=ft.Icons.CONTACT_PAGE, 
            on_click=on_export_contacts, 
            bgcolor=ft.Colors.BLUE_900, 
            color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
        )
        
        self.content = self._build()

    def update_count(self, new_count):
        """Atualiza o contador quando o mesmo split é reprocessado."""
        self.count = new_count
        self.lbl_count.value = f"📊 {new_count} registros extraídos"
        self.update()

    def update_actions(self, on_curadoria, on_export_primary, on_export_contacts):
        """Atualiza os callbacks de clique fisicamente nos botões."""
        self.btn_curadoria.on_click = on_curadoria
        self.btn_mestre.on_click = on_export_primary
        self.btn_contatos.on_click = on_export_contacts
        self.update()

    def _build(self):
        self.lbl_count = ft.Text(f"📊 {self.count} registros extraídos", size=12, color=PlatinumTheme.TEXT_SECONDARY())
        
        return ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.GREEN_400, size=20),
                ft.Column([
                    ft.Text(f"Sessão: {self.col_id} ➔ {self.col_mvf}", weight="bold", size=14, color=PlatinumTheme.PRIMARY()),
                    self.lbl_count
                ], spacing=2, expand=True),
                ft.IconButton(ft.Icons.AUTO_FIX_HIGH, tooltip="Purificar com MDM Intelligent", icon_color=PlatinumTheme.PRIMARY())
            ], alignment="spaceBetween"),
            
            ft.Divider(height=1, color=ft.Colors.with_opacity(0.05, PlatinumTheme.BORDER_DARK())),
            
            ft.Row([
                self.btn_curadoria,
                self.btn_mestre,
                self.btn_contatos
            ], alignment="start", spacing=10)
        ], spacing=12)

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Componente visual para gestão de sessões de extração MDM v0.7.2")
