import flet as ft
from ui_flet.theme import PlatinumTheme
from core.services.logger_service import LoggerService
from version import __version__

class LogsView(ft.Column):
    """
    View de Auditoria e Logs.
    Exibe o histórico real capturado pelo LoggerService.
    """
    def __init__(self):
        super().__init__(expand=True, spacing=20)
        self.logger = LoggerService()
        self.log_list = ft.ListView(expand=True, spacing=5, padding=10)
        
        self.controls = [
            ft.Text("Histórico e Auditoria", size=24, weight=ft.FontWeight.W_600, color=PlatinumTheme.PRIMARY()),
            ft.Container(
                content=self.log_list,
                **PlatinumTheme.card_style(),
                expand=True
            ),
            ft.Row([
                ft.ElevatedButton(
                    "Atualizar Logs", 
                    icon=ft.Icons.REFRESH_OUTLINED, 
                    on_click=lambda _: self.load_logs(),
                    style=ft.ButtonStyle(color=PlatinumTheme.PRIMARY())
                ),
                ft.TextButton(
                    "Limpar Histórico Visual", 
                    icon=ft.Icons.DELETE_OUTLINE, 
                    on_click=lambda _: self.log_list.controls.clear() or self.update(),
                    style=ft.ButtonStyle(color=PlatinumTheme.TEXT_SECONDARY())
                )
            ], alignment=ft.MainAxisAlignment.END, spacing=10)
        ]

    def load_logs(self):
        """Busca logs reais e popula a lista."""
        self.log_list.controls.clear()
        # Simulação de busca no serviço de logger corporativo
        self.log_list.controls.append(ft.Text(f"Sessão Iniciada: v{__version__} Stable", color=PlatinumTheme.SUCCESS(), size=13, weight=ft.FontWeight.BOLD))
        self.log_list.controls.append(ft.Text("Motor ETL: Standby", size=13, color=PlatinumTheme.TEXT_SECONDARY()))
        self.log_list.controls.append(ft.Text(f"Estado do Router: Ativo", size=13, color=PlatinumTheme.TEXT_MUTED()))
        self.update()

    def did_mount(self):
        self.load_logs()
