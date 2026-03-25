import flet as ft
from ui_flet.theme import PlatinumTheme
from core.engines.mapping_engine import MappingEngine

class Step2View(ft.Column):
    """
    PASSO 2: Definição de Chaves (v0.6.0).
    Usa o MappingEngine v0.4.8 para sugerir PKs.
    """
    def __init__(self, state, on_next, on_back):
        super().__init__(expand=True, spacing=20)
        self.state = state
        self.on_next = on_next
        self.on_back = on_back
        self.engine = MappingEngine()
        
        self.combo_src = ft.Dropdown(label="Chave na Origem", expand=True)
        self.combo_tgt = ft.Dropdown(label="Chave no Destino", expand=True)
        
        self.controls = [
            ft.Text("🔗 Configuração de Chaves", size=24, weight=ft.FontWeight.W_600),
            ft.Container(
                **PlatinumTheme.card_style(),
                content=ft.Column([
                    ft.Text("Selecione os campos para cruzamento de dados:"),
                    ft.Row([self.combo_src, ft.Icon(ft.Icons.LINK), self.combo_tgt]),
                    ft.Text("Dica: O Genaja já pré-selecionou as chaves com maior probabilidade de acerto.", size=12, italic=True, color=PlatinumTheme.TEXT_SECONDARY)
                ])
            ),
            ft.Row([
                ft.TextButton("⬅️ Voltar", on_click=lambda _: self.on_back()),
                ft.Row(expand=True),
                ft.ElevatedButton("Validar e Prosseguir ➡️", on_click=self._validate_and_next)
            ])
        ]

    def load_data(self):
        """Popula os dropdowns e sugere chaves."""
        cols_src = list(self.state.df_src.columns)
        cols_tgt = list(self.state.df_tgt.columns)
        
        self.combo_src.options = [ft.dropdown.Option(c) for c in cols_src]
        self.combo_tgt.options = [ft.dropdown.Option(c) for c in cols_tgt]
        
        matches = self.engine.suggest_primary_keys(self.state.df_src, self.state.df_tgt)
        if matches:
            self.combo_src.value = matches[0]['src']
            self.combo_tgt.value = matches[0]['tgt']
            
        self.update()

    def _validate_and_next(self, e):
        if not self.combo_src.value or not self.combo_tgt.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Selecione ambas as chaves para prosseguir."))
            self.page.snack_bar.open = True
            self.page.update()
            return
            
        self.state.key_src = self.combo_src.value
        self.state.key_tgt = self.combo_tgt.value
        self.state.key_tgt_final = self.combo_tgt.value
        self.on_next()
