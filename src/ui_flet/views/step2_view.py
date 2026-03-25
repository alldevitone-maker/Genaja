import flet as ft
from ui_flet.theme import PlatinumTheme
from core.engines.mapping_engine import MappingEngine
from services.logger_service import LoggerService

class Step2View(ft.Column):
    """
    PASSO 2: Definicao de Chaves (v0.6.0).
    Restauracao v0.4.6: Exibe Top Compatibilidades Matematicas.
    """
    def __init__(self, state, on_next, on_back):
        super().__init__(expand=True, spacing=20)
        self.state = state
        self.on_next = on_next
        self.on_back = on_back
        self.engine = MappingEngine()
        
        self.combo_src = ft.Dropdown(label="Chave na Origem", expand=True)
        self.combo_src.tooltip = "Coluna da planilha de ORIGEM usada para cruzamento"
        self.combo_tgt = ft.Dropdown(label="Chave no Destino", expand=True)
        self.combo_tgt.tooltip = "Coluna da planilha de DESTINO usada para cruzamento"
        
        # Top Matches display (v0.4.6)
        self.matches_display = ft.Text("Analisando...", size=12, italic=True, color=PlatinumTheme.TEXT_SECONDARY)
        
        # Advanced settings
        self.chk_a1 = ft.Checkbox(label="Ativar Blindagem na Posicao A1", value=True)
        self.chk_a1.tooltip = "Fixa a coluna selecionada como ancora na primeira posicao da saida"
        self.chk_a1.on_change = self._on_a1_toggle
        
        self.chk_shielding = ft.Checkbox(label="Data Shielding (Safe-Merge)", value=False)
        self.chk_shielding.tooltip = "Impede sobrescrita de celulas preenchidas no destino"
        self.chk_shielding.on_change = lambda e: setattr(self.state, "shielding", e.control.value)
        
        # Fixar Chave A1 (v0.4.6: "Fixar Chave Posicao A1")
        self.combo_a1 = ft.Dropdown(label="Fixar Chave (Posicao A1)", expand=True)
        self.combo_a1.tooltip = "Selecione qual coluna do destino sera fixada na posicao A1"
        
        self.controls = [
            ft.Text("Configuracao de Chaves", size=24, weight=ft.FontWeight.W_600),
            # Top Matches Card (v0.4.6 "Interseccao Matematica")
            ft.Container(
                **PlatinumTheme.card_style(),
                content=ft.Column([
                    ft.Text("Top Compatibilidades Matematicas:", weight=ft.FontWeight.W_600),
                    self.matches_display,
                ], spacing=5)
            ),
            # Key Selection
            ft.Container(
                **PlatinumTheme.card_style(),
                content=ft.Column([
                    ft.Text("Selecione os campos para cruzamento de dados:"),
                    ft.Row([self.combo_src, ft.Icon(ft.Icons.LINK), self.combo_tgt]),
                    ft.Divider(color=PlatinumTheme.BORDER_DARK),
                    ft.Row([
                        self.combo_a1,
                        self.chk_a1,
                        self.chk_shielding,
                    ]),
                ], spacing=10)
            ),
            ft.Row([
                ft.TextButton("Voltar", on_click=lambda _: self.on_back()),
                ft.Row(expand=True),
                ft.ElevatedButton("Validar e Prosseguir", on_click=self._validate_and_next)
            ])
        ]

    def _on_a1_toggle(self, e):
        """v0.4.7: Habilita/desabilita o combo A1 baseado no checkbox."""
        self.state.protected_a1 = e.control.value
        self.combo_a1.disabled = not e.control.value
        self.update()

    def load_data(self):
        """Popula os dropdowns e sugere chaves."""
        cols_src = list(self.state.df_src.columns)
        cols_tgt = list(self.state.df_tgt.columns)
        
        self.combo_src.options = [ft.dropdown.Option(c) for c in cols_src]
        self.combo_tgt.options = [ft.dropdown.Option(c) for c in cols_tgt]
        self.combo_a1.options = [ft.dropdown.Option(c) for c in cols_tgt]
        
        # Sugestao de chaves com display de resultados (v0.4.6)
        matches = self.engine.suggest_primary_keys(self.state.df_src, self.state.df_tgt)
        if matches:
            match_lines = []
            for i, m in enumerate(matches[:5]):
                match_lines.append(f"{i+1}. '{m['src']}' <-> '{m['tgt']}' ({int(m['score'])} matches)")
            self.matches_display.value = " | ".join(match_lines)
            self.combo_src.value = matches[0]['src']
            self.combo_tgt.value = matches[0]['tgt']
        else:
            self.matches_display.value = "Nenhuma compatibilidade encontrada automaticamente."
        
        # Default A1 to first column of target
        if cols_tgt:
            self.combo_a1.value = cols_tgt[0]
            
        self.update()

    def _validate_and_next(self, e):
        if not self.combo_src.value or not self.combo_tgt.value:
            sb = ft.SnackBar(ft.Text("Selecione ambas as chaves para prosseguir."), bgcolor=PlatinumTheme.WARNING)
            self.page.overlay.append(sb)
            sb.open = True
            self.page.update()
            return
            
        self.state.key_src = self.combo_src.value
        self.state.key_tgt = self.combo_tgt.value
        self.state.key_tgt_final = self.combo_a1.value or self.combo_tgt.value
        self.on_next()
