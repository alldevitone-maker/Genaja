import flet as ft
from version import __version__

class IntentRouterView(ft.Container):
    """
    Roteador Visual de Intenção do Operador.
    Não aciona motores diretamente, apenas altera o estado e delega roteamento.
    """
    def __init__(self, state, router):
        super().__init__()
        self.state = state
        self.router = router
        
        self.header = ft.Text("Quarentena Concluída. Escolha sua Intenção:", size=22, weight="bold")
        
        # Cards simplificados temporariamente para a Genaja Stable
        self.card_a = ft.ElevatedButton("Modo A: Só Converter e Exportar", on_click=lambda _: self.router.handle_intent_decision("convert_only"))
        self.card_b = ft.ElevatedButton("Modo B: Tratar Esta Base", on_click=lambda _: self.router.handle_intent_decision("prepare_single"))
        self.card_c = ft.ElevatedButton("Modo C: Comparar com Destino/SQL", on_click=lambda _: self.router.handle_intent_decision("compare_sync"))

        # Modo D: Price Sync (destaque visual — resolve o problema dos 14k itens)
        self.card_d = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.CURRENCY_EXCHANGE, color="black"),
                ft.Text("Modo D: Price Sync (PROCX Turbo)", weight="bold", color="black"),
            ], spacing=8),
            bgcolor=ft.Colors.AMBER_400,
            on_click=lambda _: self.router.navigate("price_sync"),
            height=48,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

        self.btn_back = ft.OutlinedButton("Cancelar e Recomeçar", icon=ft.Icons.RESTART_ALT, on_click=lambda _: self.router.navigate("step0_quarantine"))

        self.content = ft.Column([
            self.header,
            ft.Row([self.card_a, self.card_b, self.card_c], alignment="center", spacing=20),
            ft.Container(height=5),
            ft.Row([self.card_d], alignment="center"),
            ft.Container(height=40),
            self.btn_back
        ], horizontal_alignment="center", spacing=20)
        
        self.alignment = ft.Alignment(0, 0)
        self.padding = 60


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "IntentRouterView estabilizada com Modo D (Price Sync) integrado")
