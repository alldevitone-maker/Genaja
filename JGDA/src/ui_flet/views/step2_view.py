import flet as ft
import asyncio
from ui_flet.theme import PlatinumTheme
from core.engines.mapping_engine import MappingEngine
from core.services.logger_service import LoggerService
from ui_flet.views.base_view import RoutedViewMixin
from version import __version__

class Step2View(ft.Column, RoutedViewMixin):
    """
    PASSO 2: Definicao de Chaves.
    Exibe Top Compatibilidades Matematicas.
    """
    def __init__(self, state, on_next, on_back):
        super().__init__(expand=True, spacing=20)
        self.state = state
        self.on_next = on_next
        self.on_back = on_back
        self.engine = MappingEngine()
        
        self.combo_src = ft.Dropdown(
            label="Chave na Origem", 
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_SECONDARY()),
            color=PlatinumTheme.TEXT_PRIMARY(),
            border_color=PlatinumTheme.BORDER_DARK(),
            focused_border_color=PlatinumTheme.PRIMARY(),
            expand=True
        )
        self.combo_src.tooltip = "Coluna da planilha de ORIGEM usada para cruzamento"
        self.combo_tgt = ft.Dropdown(
            label="Chave no Destino", 
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_SECONDARY()),
            color=PlatinumTheme.TEXT_PRIMARY(),
            border_color=PlatinumTheme.BORDER_DARK(),
            focused_border_color=PlatinumTheme.PRIMARY(),
            expand=True
        )
        self.combo_tgt.tooltip = "Coluna da planilha de DESTINO usada para cruzamento"
        
        # Top Matches display
        self.matches_display = ft.Text("Analisando...", size=12, italic=True, color=PlatinumTheme.TEXT_SECONDARY())
        
        # Advanced settings
        self.chk_a1 = ft.Checkbox(
            label="Ativar Blindagem na Posicao A1", 
            value=True,
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_PRIMARY()),
            fill_color=PlatinumTheme.PRIMARY()
        )
        """Inicia resolução cognitiva para a coluna selecionada."""
        self.chk_a1.tooltip = "Fixa a coluna selecionada como ancora na primeira posicao da saida"
        self.chk_a1.on_change = self._on_a1_toggle
        
        self.chk_shielding = ft.Checkbox(
            label="Data Shielding (Safe-Merge)", 
            value=False,
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_PRIMARY()),
            fill_color=PlatinumTheme.PRIMARY()
        )
        self.chk_shielding.tooltip = "Impede sobrescrita de celulas preenchidas no destino"
        self.chk_shielding.on_change = lambda e: setattr(self.state, "shielding", e.control.value)
        
        self.chk_preserve_zeros = ft.Checkbox(
            label="Preservar Zeros à Esquerda", 
            value=True,
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_PRIMARY()),
            fill_color=PlatinumTheme.PRIMARY()
        )
        self.chk_preserve_zeros.tooltip = "Mantém 001 ao invés de converter para 1 (essencial para IDs e CEPs)"
        self.chk_preserve_zeros.on_change = lambda e: setattr(self.state, "preserve_leading_zeros", e.control.value)
        
        # Fixar Chave A1
        self.combo_a1 = ft.Dropdown(
            label="Fixar Chave (Posicao A1)", 
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_SECONDARY()),
            color=PlatinumTheme.TEXT_PRIMARY(),
            border_color=PlatinumTheme.BORDER_DARK(),
            focused_border_color=PlatinumTheme.PRIMARY(),
            expand=True
        )
        self.combo_a1.tooltip = "Selecione qual coluna do destino sera fixada na posicao A1"
        
        self.controls = [
            ft.Text("Configuração de Chaves", size=24, weight=ft.FontWeight.W_600, color=PlatinumTheme.PRIMARY()),
            # Top Matches Card
            ft.Container(
                **PlatinumTheme.card_style(),
                content=ft.Column([
                    ft.Text("Top Compatibilidades Matematicas:", weight=ft.FontWeight.W_600, color=PlatinumTheme.TEXT_PRIMARY()),
                    self.matches_display,
                ], spacing=5)
            ),
            # Key Selection (Responsiva)
            ft.Container(
                **PlatinumTheme.card_style(),
                content=ft.Column([
                    ft.Text("Selecione os campos para cruzamento de dados:", color=PlatinumTheme.TEXT_SECONDARY()),
                    ft.ResponsiveRow([
                        ft.Column([self.combo_src], col={"sm": 12, "md": 5}),
                        ft.Column([ft.Icon(PlatinumTheme.Icons.LINK, color=PlatinumTheme.PRIMARY())], col={"sm": 12, "md": 2}, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Column([self.combo_tgt], col={"sm": 12, "md": 5}),
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Divider(color=PlatinumTheme.BORDER_DARK()),
                    ft.ResponsiveRow([
                        ft.Column([self.combo_a1], col={"sm": 12, "md": 6}),
                        ft.Column([self.chk_a1, self.chk_shielding, self.chk_preserve_zeros], col={"sm": 12, "md": 6}),
                    ]),
                ], spacing=10)
            ),
            ft.Row([
                ft.TextButton("Voltar", on_click=lambda _: self.on_back(), style=ft.ButtonStyle(color=PlatinumTheme.TEXT_SECONDARY())),
                ft.Row(expand=True),
                ft.ElevatedButton(
                    "Validar e Prosseguir", 
                    on_click=self._validate_and_next,
                    style=ft.ButtonStyle(bgcolor=PlatinumTheme.PRIMARY(), color="white")
                )
            ])
        ]

    def _on_a1_toggle(self, e):
        """Habilita/desabilita o combo A1 baseado no checkbox."""
        self.state.protected_a1 = e.control.value
    async def on_route_mounted(self):
        """Asynchronous offloading - Renders instantly, processes AI later."""
        # Configurar estado de Carregamento (Skeleton UI)
        self.matches_display.value = "Gerando Modelagem Cognitiva em background..."
        self.matches_display.color = PlatinumTheme.PRIMARY()
        self.combo_src.disabled = True
        self.combo_tgt.disabled = True
        self.combo_a1.disabled = True
        self.update()
        
        # Iniciar thread assíncrona para Processamento Cognitivo
        await asyncio.to_thread(self._fetch_match_data)

    def _fetch_match_data(self):
        cols_src = list(self.state.df_src.columns) if self.state.df_src is not None else []
        cols_tgt = list(self.state.df_tgt.columns) if self.state.df_tgt is not None else []
        
        try:
            matches = self.engine.suggest_primary_keys(self.state.df_src, self.state.df_tgt)
        except Exception as e:
            LoggerService().error(f"Erro ao sugerir chaves: {e}")
            matches = []
            
        # Voltar pro Main Thread Context via dispatch ou call direta depois que o calculo acabou
        if self.page:
            self.page.run_task(self._apply_data_to_ui, cols_src, cols_tgt, matches)

    async def _apply_data_to_ui(self, cols_src, cols_tgt, matches):
        """Callback chamada no Main Thread após sucesso do Offload"""
        self.combo_src.options = [ft.dropdown.Option(c) for c in cols_src]
        self.combo_tgt.options = [ft.dropdown.Option(c) for c in cols_tgt]
        self.combo_a1.options = [ft.dropdown.Option(c) for c in cols_tgt]
        
        # Sugestao de chaves com display de resultados
        if matches and len(matches) > 0:
            match_lines = []
            for i, m in enumerate(matches[:5]):
                if isinstance(m, dict):
                    match_lines.append(f"{i+1}. '{m['src']}' <-> '{m['tgt']}' ({int(m['score'])} matches)")
            
            self.matches_display.value = " | ".join(match_lines)
            self.matches_display.color = PlatinumTheme.TEXT_SECONDARY()
            
            if isinstance(matches[0], dict):
                self.combo_src.value = matches[0]['src']
                self.combo_tgt.value = matches[0]['tgt']
        else:
            self.matches_display.value = "Nenhuma compatibilidade encontrada automaticamente."
            self.matches_display.color = PlatinumTheme.WARNING()
            
        # Default A1 to first column of target
        if cols_tgt:
            self.combo_a1.value = self.state.key_tgt_final or cols_tgt[0]
            
        # Sincronizar checkboxes e liberar inputs
        self.chk_a1.value = self.state.protected_a1
        self.chk_shielding.value = self.state.shielding
        self.chk_preserve_zeros.value = self.state.preserve_leading_zeros
        self.combo_a1.disabled = not self.chk_a1.value
        self.combo_src.disabled = False
        self.combo_tgt.disabled = False
        
        self.update()

    def load_data(self):
        """Mapeado para compatibilidade, mas o fluxo passa a ser async."""
        import asyncio
        if hasattr(self.page, "run_task"):
             self.page.run_task(self.on_route_mounted)
        elif self.page is None:
             pass # Aguardando mount
        else:
             asyncio.create_task(self.on_route_mounted())

    def _validate_and_next(self, e):
        if not self.combo_src.value or not self.combo_tgt.value:
            sb = ft.SnackBar(ft.Text("Selecione ambas as chaves para prosseguir."), bgcolor=PlatinumTheme.WARNING())
            self.page.overlay.append(sb)
            sb.open = True
            self.page.update()
            return
            
        self.state.key_src = self.combo_src.value
        self.state.key_tgt = self.combo_tgt.value
        self.state.key_tgt_final = self.combo_a1.value or self.combo_tgt.value
        self.on_next()

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Interface Legada - Passo 2: Mapeamento de Chaves Primárias e Fallbacks")
