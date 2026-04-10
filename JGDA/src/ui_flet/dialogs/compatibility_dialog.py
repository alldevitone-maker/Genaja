import flet as ft
from version import __version__

class CompatibilityDialog(ft.AlertDialog):
    """
    Diálogo de Compatibilidade Assistida.
    Inicia resolução cognitiva para a coluna selecionada e mapeamento.
    """
    def __init__(self, src_col, tgt_col, score, reason, on_apply):
        self.on_apply = on_apply
        
        super().__init__(
            title=ft.Text("Métricas de Interoperabilidade Cognitiva", weight=ft.FontWeight.BOLD, size=20),
            content=ft.Column([
                ft.Text("Vínculo sugerido:", size=14, color=ft.Colors.GREY_400),
                ft.Container(
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_400),
                    border_radius=8,
                    content=ft.Row([
                        ft.Text(src_col, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_ACCENT_400),
                        ft.Icon(ft.Icons.ARROW_FORWARD, size=16),
                        ft.Text(tgt_col, weight=ft.FontWeight.W_600, color=ft.Colors.GREEN_ACCENT_400)
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ),
                ft.Row([
                    ft.Text(f"Confiança: {int(score * 100)}%", size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Motivo: {reason}", size=12, italic=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Text("Deseja confirmar este mapeamento?", size=13)
            ], tight=True, spacing=15),
            actions=[
                ft.TextButton("IGNORAR", on_click=lambda e: self._close(e)),
                ft.ElevatedButton(
                    "ACEITAR MAPEAMENTO", 
                    on_click=lambda e: self._confirm(e),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700, color="white")
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=12)
        )

    def _close(self, e):
        self.open = False
        e.page.update()

    def _confirm(self, e):
        self.on_apply()
        self._close(e)


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Diálogo de assistência ao usuário com explicações de confiança do núcleo de inferência cognitiva")
