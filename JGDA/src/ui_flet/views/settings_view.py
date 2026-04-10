import flet as ft
from ui_flet.theme import PlatinumTheme
from core.services.config_service import ConfigService
from version import __version__, __title__

class SettingsView(ft.Column):
    """
    View de Ajustes do Sistema.
    Gerencia parâmetros via ConfigService.
    """
    def __init__(self):
        super().__init__(expand=True, spacing=20)
        self.config = ConfigService()
        
        self.op_name_field = ft.TextField(
            label="Nome do Operador",
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_SECONDARY()),
            hint_style=ft.TextStyle(color=PlatinumTheme.TEXT_PLACEHOLDER()),
            color=PlatinumTheme.TEXT_PRIMARY(),
            border_color=PlatinumTheme.BORDER_DARK(),
            focused_border_color=PlatinumTheme.PRIMARY(),
            value=self.config.get("general", "operator_name"),
            col={"sm": 12, "md": 6}
        )
        
        self.controls = [
            ft.Text("Ajustes do Sistema", size=24, weight=ft.FontWeight.W_600, color=PlatinumTheme.PRIMARY()),
            ft.ResponsiveRow([
                ft.Container(
                    **PlatinumTheme.card_style(),
                    col={"sm": 12, "md": 8},
                    content=ft.Column([
                        ft.Text("Informações do Operador", weight=ft.FontWeight.BOLD, color=PlatinumTheme.TEXT_PRIMARY()),
                        self.op_name_field,
                        ft.ElevatedButton(
                            "Salvar Configurações", 
                            on_click=self._on_save,
                            style=ft.ButtonStyle(bgcolor=PlatinumTheme.SURFACE_DARK(), color=PlatinumTheme.PRIMARY())
                        ),
                    ], spacing=15)
                ),
                ft.Container(
                    **PlatinumTheme.card_style(),
                    col={"sm": 12, "md": 4},
                    content=ft.Column([
                        ft.Text("Status do Sistema", weight=ft.FontWeight.BOLD, color=PlatinumTheme.TEXT_PRIMARY()),
                        ft.Text(f"Versão: v{__version__}", color=PlatinumTheme.TEXT_SECONDARY()),
                        ft.Text(f"Modo: {__title__}", color=PlatinumTheme.TEXT_SECONDARY()),
                        ft.Divider(color=PlatinumTheme.BORDER_DARK()),
                        ft.Text("Licença: Ativa", color=PlatinumTheme.SUCCESS(), weight=ft.FontWeight.BOLD),
                    ], spacing=10)
                )
            ])
        ]

    def _on_save(self, e):
        new_name = self.op_name_field.value
        self.config.set("general", "operator_name", new_name)
        
        snack = ft.SnackBar(
            ft.Text(f"Configurações de {new_name} salvas com sucesso!"), 
            bgcolor=PlatinumTheme.SUCCESS()
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Interface de Configurações - Gestão de Preferências e Parâmetros de Operação")
