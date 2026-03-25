import flet as ft
from ui_flet.theme import PlatinumTheme
from services.logger_service import LoggerService

class Step3View(ft.Column):
    """
    PASSO 3: Mapeamento de Colunas + Regras (v0.6.0).
    Restauracao completa do motor v0.4.6 com Regras de Linha e Estruturais.
    """
    def __init__(self, state, on_next, on_back):
        super().__init__(expand=True, spacing=15)
        self.state = state
        self.on_next = on_next
        self.on_back = on_back
        
        self.list_src = ft.ListView(expand=True, spacing=5, padding=10)
        self.list_tgt = ft.ListView(expand=True, spacing=5, padding=10)
        
        # Regras de Linha
        self.chk_remove_nulls = ft.Checkbox(
            label="Remover linhas com valor zero ou nulo", 
            value=False
        )
        self.chk_remove_nulls.on_change = lambda e: setattr(self.state, "remove_nulls", e.control.value)
        
        # Regras Estruturais
        self.chk_keep_only = ft.Checkbox(
            label="Manter APENAS as colunas selecionadas", 
            value=False
        )
        self.chk_keep_only.on_change = lambda e: setattr(self.state, "keep_only_mapped", e.control.value)
        
        self.chk_trim = ft.Checkbox(label="Trim (limpar espacos extras)", value=True)
        self.chk_trim.on_change = lambda e: setattr(self.state, "auto_trim", e.control.value)
        
        self.chk_upper = ft.Checkbox(label="Maiusculas (converter para Capslock)", value=False)
        self.chk_upper.on_change = lambda e: setattr(self.state, "auto_upper", e.control.value)
        
        self.controls = [
            ft.Text("Mapeamento de Colunas", size=24, weight=ft.FontWeight.W_600),
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
                # Center: Transfer buttons
                ft.Column([
                    ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT, on_click=self._move_all_to_tgt, tooltip="Transpor Todas"),
                    ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=self._move_selected_to_tgt, tooltip="Adicionar"),
                    ft.IconButton(ft.Icons.ARROW_BACK, on_click=self._move_selected_to_src, tooltip="Remover"),
                    ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=self._move_all_to_src, tooltip="Remover Todas"),
                ], alignment=ft.MainAxisAlignment.CENTER),
                # Right: Target Columns
                ft.Container(
                    **PlatinumTheme.card_style(),
                    expand=True,
                    content=ft.Column([
                        ft.Text("A Sincronizar (Destino Final)", weight=ft.FontWeight.BOLD),
                        self.list_tgt
                    ])
                )
            ], expand=True),
            # Rules Section (v0.4.6)
            ft.Row([
                ft.Container(
                    **PlatinumTheme.card_style(),
                    expand=True,
                    content=ft.Column([
                        ft.Text("Regras de Linha", weight=ft.FontWeight.W_600),
                        self.chk_remove_nulls,
                    ], spacing=5)
                ),
                ft.Container(
                    **PlatinumTheme.card_style(),
                    expand=True,
                    content=ft.Column([
                        ft.Text("Regras Estruturais", weight=ft.FontWeight.W_600),
                        self.chk_keep_only,
                        self.chk_trim,
                        self.chk_upper,
                    ], spacing=5)
                ),
            ], spacing=15),
            ft.Row([
                ft.TextButton("Voltar", on_click=lambda _: self.on_back()),
                ft.Row(expand=True),
                ft.ElevatedButton("Finalizar Mapeamento", on_click=self._finish_mapping)
            ])
        ]

    def load_data(self):
        """Popula as listas com colunas da origem."""
        self.list_src.controls.clear()
        self.list_tgt.controls.clear()
        
        self.cols_src = sorted(list(self.state.df_src.columns))
        self.cols_in_tgt = []  # Track what's been transferred
        
        for c in self.cols_src:
            self.list_src.controls.append(
                ft.Container(
                    bgcolor=PlatinumTheme.BORDER_DARK,
                    padding=8,
                    border_radius=6,
                    on_click=lambda _, col=c: self._toggle_src_selection(col),
                    content=ft.Text(c, size=13)
                )
            )
        
        self.update()

    def _toggle_src_selection(self, col):
        """Simple visual selection toggle."""
        for ctrl in self.list_src.controls:
            if ctrl.content.value == col:
                is_selected = ctrl.bgcolor == PlatinumTheme.PRIMARY
                ctrl.bgcolor = PlatinumTheme.BORDER_DARK if is_selected else PlatinumTheme.PRIMARY
                ctrl.content.color = PlatinumTheme.TEXT_PRIMARY if is_selected else "white"
        self.update()

    def _toggle_tgt_selection(self, col):
        for ctrl in self.list_tgt.controls:
            if ctrl.content.value == col:
                is_selected = ctrl.bgcolor == PlatinumTheme.PRIMARY
                ctrl.bgcolor = PlatinumTheme.BORDER_DARK if is_selected else PlatinumTheme.PRIMARY
                ctrl.content.color = PlatinumTheme.TEXT_PRIMARY if is_selected else "white"
        self.update()

    def _get_selected_src(self):
        return [c.content.value for c in self.list_src.controls if c.bgcolor == PlatinumTheme.PRIMARY]

    def _get_selected_tgt(self):
        return [c.content.value for c in self.list_tgt.controls if c.bgcolor == PlatinumTheme.PRIMARY]

    def _move_selected_to_tgt(self, e=None):
        selected = self._get_selected_src()
        for col in selected:
            if col not in self.cols_in_tgt:
                self.cols_in_tgt.append(col)
        self._rebuild_lists()

    def _move_selected_to_src(self, e=None):
        selected = self._get_selected_tgt()
        for col in selected:
            if col in self.cols_in_tgt:
                self.cols_in_tgt.remove(col)
        self._rebuild_lists()

    def _move_all_to_tgt(self, e=None):
        self.cols_in_tgt = list(self.cols_src)
        self._rebuild_lists()

    def _move_all_to_src(self, e=None):
        self.cols_in_tgt = []
        self._rebuild_lists()

    def _rebuild_lists(self):
        self.list_src.controls.clear()
        self.list_tgt.controls.clear()
        
        for c in self.cols_src:
            if c not in self.cols_in_tgt:
                self.list_src.controls.append(
                    ft.Container(
                        bgcolor=PlatinumTheme.BORDER_DARK,
                        padding=8, border_radius=6,
                        on_click=lambda _, col=c: self._toggle_src_selection(col),
                        content=ft.Text(c, size=13)
                    )
                )
        
        for c in self.cols_in_tgt:
            self.list_tgt.controls.append(
                ft.Container(
                    bgcolor=PlatinumTheme.BORDER_DARK,
                    padding=8, border_radius=6,
                    on_click=lambda _, col=c: self._toggle_tgt_selection(col),
                    content=ft.Text(c, size=13)
                )
            )
        
        self.update()

    def _finish_mapping(self, e):
        if not self.cols_in_tgt:
            sb = ft.SnackBar(ft.Text("Mapeie ao menos uma coluna."), bgcolor=PlatinumTheme.WARNING)
            self.page.overlay.append(sb)
            sb.open = True
            self.page.update()
            return
        
        # Build mapping: {col_src: col_src} (same name since we're transferring from origin)
        self.state.mapping = {c: c for c in self.cols_in_tgt}
        self.state.null_filter_cols = self.cols_in_tgt if self.state.remove_nulls else []
        self.on_next()
