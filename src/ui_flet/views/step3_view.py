import flet as ft
import os
from ui_flet.theme import PlatinumTheme
from core.services.logger_service import LoggerService
from migration.schema_mapper import SchemaMapper
from core.learning.suggestion_engine import HistoricalSuggestionEngine
from ui_flet.dialogs.compatibility_dialog import CompatibilityDialog

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
        self.mapper = HistoricalSuggestionEngine(os.getcwd())
        self.mapping_pairs = {} # {src_col: tgt_col}
        
        self.list_src = ft.ListView(expand=True, spacing=5, padding=10)
        self.list_tgt = ft.ListView(expand=True, spacing=5, padding=10)
        
        # Regras de Linha
        self.chk_remove_nulls = ft.Checkbox(
            label="Remover linhas com valor zero ou nulo", 
            value=False,
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_PRIMARY()),
            fill_color=PlatinumTheme.PRIMARY()
        )
        self.chk_remove_nulls.on_change = lambda e: setattr(self.state, "remove_nulls", e.control.value)
        
        # Regras Estruturais
        self.chk_keep_only = ft.Checkbox(
            label="Manter APENAS as colunas selecionadas", 
            value=False,
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_PRIMARY()),
            fill_color=PlatinumTheme.PRIMARY()
        )
        self.chk_keep_only.on_change = lambda e: setattr(self.state, "keep_only_mapped", e.control.value)
        
        self.chk_trim = ft.Checkbox(
            label="Trim (limpar espacos extras)", 
            value=True,
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_PRIMARY()),
            fill_color=PlatinumTheme.PRIMARY()
        )
        self.chk_trim.on_change = lambda e: setattr(self.state, "auto_trim", e.control.value)
        
        self.chk_upper = ft.Checkbox(
            label="Maiusculas (converter para Capslock)", 
            value=False,
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_PRIMARY()),
            fill_color=PlatinumTheme.PRIMARY()
        )
        self.chk_upper.on_change = lambda e: setattr(self.state, "auto_upper", e.control.value)
        
        self.controls = [
            ft.Text("Mapeamento de Colunas", size=24, weight=ft.FontWeight.W_600, color=PlatinumTheme.PRIMARY()),
            ft.ResponsiveRow([
                # Left: Source Columns
                ft.Container(
                    **PlatinumTheme.card_style(),
                    col={"sm": 12, "md": 5},
                    height=400,
                    content=ft.Column([
                        ft.Text("Colunas Origem", weight=ft.FontWeight.BOLD, color=PlatinumTheme.TEXT_PRIMARY()),
                        self.list_src
                    ])
                ),
                # Center: Transfer buttons
                ft.Column([
                    ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT_OUTLINED, on_click=self._move_all_to_tgt, tooltip="Transpor Todas", icon_color=PlatinumTheme.PRIMARY()),
                    ft.IconButton(ft.Icons.ARROW_FORWARD_OUTLINED, on_click=self._move_selected_to_tgt, tooltip="Adicionar", icon_color=PlatinumTheme.PRIMARY()),
                    ft.IconButton(ft.Icons.ARROW_BACK_OUTLINED, on_click=self._move_selected_to_src, tooltip="Remover", icon_color=PlatinumTheme.PRIMARY()),
                    ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_OUTLINED, on_click=self._move_all_to_src, tooltip="Remover Todas", icon_color=PlatinumTheme.PRIMARY()),
                ], col={"sm": 12, "md": 2}, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                # Right: Target Columns
                ft.Container(
                    **PlatinumTheme.card_style(),
                    col={"sm": 12, "md": 5},
                    height=400,
                    content=ft.Column([
                        ft.Text("A Sincronizar (Destino Final)", weight=ft.FontWeight.BOLD, color=PlatinumTheme.TEXT_PRIMARY()),
                        self.list_tgt
                    ])
                )
            ]),
            # Rules Section (v0.4.6)
            ft.ResponsiveRow([
                ft.Container(
                    **PlatinumTheme.card_style(),
                    col={"sm": 12, "md": 6},
                    content=ft.Column([
                        ft.Text("Regras de Linha", weight=ft.FontWeight.W_600, color=PlatinumTheme.TEXT_PRIMARY()),
                        self.chk_remove_nulls,
                    ], spacing=5)
                ),
                ft.Container(
                    **PlatinumTheme.card_style(),
                    col={"sm": 12, "md": 6},
                    content=ft.Column([
                        ft.Text("Regras Estruturais", weight=ft.FontWeight.W_600, color=PlatinumTheme.TEXT_PRIMARY()),
                        self.chk_keep_only,
                        self.chk_trim,
                        self.chk_upper,
                    ], spacing=5)
                ),
            ], spacing=15),
            ft.Row([
                ft.TextButton("Voltar", on_click=lambda _: self.on_back(), style=ft.ButtonStyle(color=PlatinumTheme.TEXT_SECONDARY())),
                ft.Row(expand=True),
                ft.ElevatedButton(
                    "Finalizar Mapeamento", 
                    on_click=self._finish_mapping,
                    style=ft.ButtonStyle(bgcolor=PlatinumTheme.PRIMARY(), color="white")
                )
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
                    bgcolor=PlatinumTheme.BG_DARK(),
                    padding=8,
                    border_radius=8,
                    border=ft.border.all(1, PlatinumTheme.BORDER_DARK()),
                    on_click=lambda _, col=c: self._toggle_src_selection(col),
                    on_long_press=lambda _, col=c: self._open_assist(col),
                    content=ft.Text(c, size=13, color=PlatinumTheme.TEXT_PRIMARY(), weight=ft.FontWeight.W_500)
                )
            )
        
        self.update()

    def _toggle_src_selection(self, col):
        """Simple visual selection toggle using Active Tokens."""
        for ctrl in self.list_src.controls:
            if ctrl.content.value == col:
                is_selected = ctrl.bgcolor == PlatinumTheme.PRIMARY()
                ctrl.bgcolor = PlatinumTheme.PRIMARY() if not is_selected else PlatinumTheme.BG_DARK()
                ctrl.content.color = "white" if not is_selected else PlatinumTheme.TEXT_PRIMARY()
        self.update()

    def _toggle_tgt_selection(self, col):
        for ctrl in self.list_tgt.controls:
            if ctrl.content.value == col:
                is_selected = ctrl.bgcolor == PlatinumTheme.PRIMARY()
                ctrl.bgcolor = PlatinumTheme.PRIMARY() if not is_selected else PlatinumTheme.BG_DARK()
                ctrl.content.color = "white" if not is_selected else PlatinumTheme.TEXT_PRIMARY()
        self.update()

    def _get_selected_src(self):
        return [c.content.value for c in self.list_src.controls if c.bgcolor == PlatinumTheme.PRIMARY()]

    def _get_selected_tgt(self):
        return [c.content.value for c in self.list_tgt.controls if c.bgcolor == PlatinumTheme.PRIMARY()]

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
                        bgcolor=PlatinumTheme.BG_DARK(),
                        padding=8, border_radius=8,
                        border=ft.border.all(1, PlatinumTheme.BORDER_DARK()),
                        on_click=lambda _, col=c: self._toggle_src_selection(col),
                        on_long_press=lambda _, col=c: self._open_assist(col),
                        content=ft.Text(c, size=13, color=PlatinumTheme.TEXT_PRIMARY(), weight=ft.FontWeight.W_500)
                    )
                )
        
        for c in self.cols_in_tgt:
            self.list_tgt.controls.append(
                ft.Container(
                    bgcolor=PlatinumTheme.BG_DARK(),
                    padding=8, border_radius=8,
                    border=ft.border.all(1, PlatinumTheme.BORDER_DARK()),
                    on_click=lambda _, col=c: self._toggle_tgt_selection(col),
                    content=ft.Row([
                        ft.Text(c, size=13, color=PlatinumTheme.TEXT_PRIMARY(), weight=ft.FontWeight.W_500, expand=True),
                        ft.Text(f"→ {self.mapping_pairs.get(c, c)}", size=11, color=PlatinumTheme.PRIMARY(), italic=True)
                    ])
                )
            )
        
        self.update()

    def _open_assist(self, col):
        """Inicia assistência inteligente para a coluna selecionada."""
        tgt_cols = self.cols_src # Na v3 trabalhamos com as colunas de destino disponíveis
        if self.state.df_tgt is not None:
            tgt_cols = list(self.state.df_tgt.columns)

        smart = self.mapper.get_smart_suggestions([col], tgt_cols)
        
        if col in smart["mapping"]:
            target = smart["mapping"][col]
            def apply_suggested():
                self.mapping_pairs[col] = target
                if col not in self.cols_in_tgt:
                    self.cols_in_tgt.append(col)
                self._rebuild_lists()
            
            dialog = CompatibilityDialog(
                col, 
                target, 
                smart["confidence"], 
                f"Sugerido via {smart['source']}",
                on_apply=apply_suggested
            )
            
            # Gerenciamento de Overlay (Hardening Patch 2)
            to_remove = [ctrl for ctrl in self.page.overlay if isinstance(ctrl, CompatibilityDialog)]
            for ctrl in to_remove:
                self.page.overlay.remove(ctrl)
                
            self.page.overlay.append(dialog)
            dialog.open = True
            self.page.update()
        else:
            sb = ft.SnackBar(ft.Text(f"Nenhuma sugestão óbvia para '{col}'"), bgcolor=PlatinumTheme.WARNING())
            self.page.overlay.append(sb)
            sb.open = True
            self.page.update()

    def _finish_mapping(self, e):
        if not self.cols_in_tgt:
            sb = ft.SnackBar(ft.Text("Mapeie ao menos uma coluna."), bgcolor=PlatinumTheme.WARNING())
            self.page.overlay.append(sb)
            sb.open = True
            self.page.update()
            return
        
        # Build mapping: {col_src: col_src} (same name since we're transferring from origin)
        
        # Build mapping: {col_src: mapped_tgt}
        self.state.mapping = self.mapping_pairs.copy()
        # Ensure columns without explicit mapping stay mapped to themselves (Identity)
        for c in self.cols_in_tgt:
            if c not in self.state.mapping:
                self.state.mapping[c] = c
                
        self.state.null_filter_cols = self.cols_in_tgt if self.state.remove_nulls else []
        self.on_next()
