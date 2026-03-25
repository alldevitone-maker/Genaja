import flet as ft
from ui_flet.theme import PlatinumTheme

class Step3View(ft.Column):
    """
    PASSO 3: Mapeamento de Colunas (v0.6.0).
    Permite ao usuário escolher quais dados da origem alimentam o destino.
    """
    def __init__(self, state, on_next, on_back):
        super().__init__(expand=True, spacing=15)
        self.state = state
        self.on_next = on_next
        self.on_back = on_back
        
        self.list_src = ft.ListView(expand=True, spacing=10, padding=10)
        self.list_tgt = ft.ListView(expand=True, spacing=10, padding=10)
        
        self.controls = [
            ft.Text("⚙️ Mapeamento de Colunas", size=24, weight=ft.FontWeight.W600),
            ft.Row([
                # Left: Source Columns
                ft.Container(
                    **PlatinumTheme.card_style(),
                    expand=True,
                    content=ft.Column([
                        ft.Text("Colunas Origem", weight=ft.FontWeight.BOLD),
                        self.list_src
                    ])
                ),
                ft.Icon(ft.icons.ARROW_FORWARD_ROUNDED, color=PlatinumTheme.TEXT_SECONDARY),
                # Right: Target Columns (Mapped)
                ft.Container(
                    **PlatinumTheme.card_style(),
                    expand=True,
                    content=ft.Column([
                        ft.Text("Destino Mapeado", weight=ft.FontWeight.BOLD),
                        self.list_tgt
                    ])
                )
            ], expand=True),
            ft.Row([
                ft.TextButton("⬅️ Voltar", on_click=lambda _: self.on_back()),
                ft.Row(expand=True),
                ft.ElevatedButton("Finalizar Configurações ➡️", on_click=self._finish_mapping)
            ])
        ]

    def load_data(self):
        """Popula as listas e tenta sugerir de-para básico."""
        self.list_src.controls.clear()
        self.list_tgt.controls.clear()
        
        cols_src = sorted(list(self.state.df_src.columns))
        cols_tgt = sorted(list(self.state.df_tgt.columns))
        
        # Estado do mapeamento local
        self.temp_mapping = {} # {col_tgt: col_src}
        
        for c_tgt in cols_tgt:
            dropdown = ft.Dropdown(
                label=f"Fonte para {c_tgt}",
                options=[ft.dropdown.Option("(Vazio)")] + [ft.dropdown.Option(c) for c in cols_src],
                on_change=lambda e, ct=c_tgt: self._on_map_change(ct, e.control.value),
                expand=True,
                text_size=12
            )
            
            # Auto-map básico por nome exato
            if c_tgt in cols_src:
                dropdown.value = c_tgt
                self.temp_mapping[c_tgt] = c_tgt
            
            self.list_tgt.controls.append(
                ft.Container(
                    bgcolor=PlatinumTheme.BORDER_DARK,
                    padding=10,
                    border_radius=8,
                    content=ft.Row([
                        ft.Text(c_tgt, expand=True, size=13, weight=ft.FontWeight.W600),
                        ft.Icon(ft.icons.ARROW_RIGHT_ALT, color=PlatinumTheme.PRIMARY),
                        dropdown
                    ])
                )
            )
            
        for c_src in cols_src:
            self.list_src.controls.append(ft.Text(f"• {c_src}", size=12))
            
        self.update()

    def _on_map_change(self, col_tgt, col_src):
        if col_src == "(Vazio)":
            self.temp_mapping.pop(col_tgt, None)
        else:
            self.temp_mapping[col_tgt] = col_src

    def _finish_mapping(self, e):
        # Inverter para o formato do motor: {col_src: col_tgt}
        self.state.mapping = {v: k for k, v in self.temp_mapping.items()}
        if not self.state.mapping:
            self.page.snack_bar = ft.SnackBar(ft.Text("Mapeie ao menos uma coluna."))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.on_next()
