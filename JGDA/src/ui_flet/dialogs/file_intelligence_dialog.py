import flet as ft
from version import __version__

class FileIntelligenceDialog(ft.AlertDialog):
    """
    Janela de Pré-Análise Inteligente.
    Interceptador entre Step 1 e Step 2.
    """
    def __init__(self, state, on_apply, on_manual):
        self.state = state
        self.on_apply = on_apply
        self.on_manual = on_manual
        
        # Dados para exibição
        src_name = self.state.path_src.split('/')[-1] if self.state.path_src else "Origem"
        tgt_name = self.state.path_tgt.split('/')[-1] if self.state.path_tgt else "Destino"
        
        src_info = f"{len(self.state.df_src.columns)} colunas, {len(self.state.df_src)} linhas" if self.state.df_src is not None else "N/A"
        tgt_info = f"{len(self.state.df_tgt.columns)} colunas, {len(self.state.df_tgt)} linhas" if self.state.df_tgt is not None else "N/A"
        
        # Sugestões (Lógica de Pré-Análise)
        common_cols = self.state.suggested_mapping.keys()
        common_text = f"Encontradas {len(common_cols)} correspondências." if common_cols else "Nenhum mapeamento automático óbvio."
        key_text = f"Chave Sugerida: {self.state.suggested_key_src} -> {self.state.suggested_key_tgt}" if self.state.suggested_key_src else "Nenhuma chave automática sugerida."
        
        is_history = self.state.suggested_source == "history"

        super().__init__(
            title=ft.Text("Métricas de Interoperabilidade Cognitiva", weight=ft.FontWeight.BOLD, size=20),
            content=ft.Container(
                width=500,
                content=ft.Column([
                    ft.Text("Análise rápida dos datasets carregados:", size=14, color=ft.Colors.GREY_400),
                    ft.Divider(),
                    ft.Row([
                        ft.Icon(ft.Icons.UPLOAD_FILE_OUTLINED, color=ft.Colors.BLUE_400),
                        ft.Column([
                            ft.Text(f"Origem: {src_name}", weight=ft.FontWeight.W_600),
                            ft.Text(src_info, size=12, color=ft.Colors.GREY_500)
                        ], spacing=2)
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.FILE_DOWNLOAD_OUTLINED, color=ft.Colors.GREEN_400),
                        ft.Column([
                            ft.Text(f"Destino: {tgt_name}", weight=ft.FontWeight.W_600),
                            ft.Text(tgt_info, size=12, color=ft.Colors.GREY_500)
                        ], spacing=2)
                    ]),
                    ft.Container(
                        padding=15,
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.AMBER_400),
                        border_radius=8,
                        content=ft.Column([
                            ft.Row([ft.Icon(ft.Icons.LIGHTBULB_OUTLINED, size=18, color=ft.Colors.AMBER_400), ft.Text("Recomendações:", weight=ft.FontWeight.BOLD)]),
                            ft.Text("🚀 Genaja encontrou sugestões baseadas em execuções anteriores." if is_history else "Sugestões de I.A. Local para este contexto:", 
                                    size=12, color=ft.Colors.AMBER_300, italic=is_history),
                            ft.Text(common_text, size=13),
                            ft.Text(key_text, size=13),
                        ], spacing=5)
                    ),
                    ft.Text("Deseja aplicar estas pré-seleções e avançar para o mapeamento detalhado?", size=13)
                ], spacing=15, tight=True)
            ),
            actions=[
                ft.TextButton("CANCELAR", on_click=lambda e: self._handle_close(e)),
                ft.OutlinedButton("CONTINUAR MANUALMENTE", on_click=lambda e: self.on_manual()),
                ft.ElevatedButton(
                    "USAR PRÉ-SELEÇÕES E AVANÇAR", 
                    on_click=lambda e: self.on_apply(),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_ACCENT_700, color="white")
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=12)
        )

    def _handle_close(self, e):
        self.open = False
        e.page.update()

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Janela de inteligência de dados com preview de mapeamento")
