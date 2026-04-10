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
        """Busca logs reais via LoggerService e popula a lista."""
        self.log_list.controls.clear()
        try:
            raw_logs = LoggerService.read_last_logs(limit=120)
            for entry in raw_logs:
                # Destaque para erros e avisos
                text_color = PlatinumTheme.TEXT_SECONDARY()
                weight = ft.FontWeight.NORMAL
                
                if "[ERROR]" in entry:
                    text_color = PlatinumTheme.DANGER()
                    weight = ft.FontWeight.BOLD
                elif "[WARNING]" in entry:
                    text_color = PlatinumTheme.WARNING()
                elif "--- Log System" in entry:
                    text_color = PlatinumTheme.SUCCESS()
                    weight = ft.FontWeight.BOLD

                self.log_list.controls.append(
                    ft.Text(entry, size=12, color=text_color, weight=weight, font_family="Consolas")
                )
        except Exception as e:
            self.log_list.controls.append(ft.Text(f"Erro ao carregar logs: {e}", color=PlatinumTheme.DANGER()))
            
        self.update()

    def did_mount(self):
        self.load_logs()


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Interface de auditoria tática com extração de logs do disco em tempo real")
