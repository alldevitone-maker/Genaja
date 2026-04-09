import flet as ft
import sys
import os
import asyncio

# Adicionar src ao path para importação modular
sys.path.append(os.path.abspath("src"))

from ui_flet.theme import PlatinumTheme
from core.services.config_service import ConfigService
from core.services.logger_service import LoggerService
from app.wizard_state import WizardState
from version import __version__, __title__

# Views
from ui_flet.views.step1_view import Step1View
from ui_flet.views.step2_view import Step2View
from ui_flet.views.step3_view import Step3View
from ui_flet.views.step4_view import Step4View
from ui_flet.views.logs_view import LogsView
from ui_flet.views.settings_view import SettingsView

# Adaptive Views
from ui_flet.flow_router import FlowRouter
from ui_flet.views.step0_inspection_view import Step0_InspectionView
from ui_flet.views.intent_router_view import IntentRouterView
from ui_flet.views.single_convert_view import SingleConvertView
from ui_flet.views.single_prep_view import SinglePrepView
from ui_flet.views.price_sync_view import PriceSyncView

async def main(page: ft.Page):
    # 0. Controles de Sistema - Modo Engenharia (Tkinter-First)
    # Erradicando ft.FilePicker para evitar as caixas vermelhas no overlay.
    # 1. Configuração Inicial
    config = ConfigService()
    LoggerService.setup()
    state = WizardState()
    
    # 2. Setup de Janela (API Flet v0.82+)
    page.title = f"Genaja Suite v{__version__} ({__title__})"
    page.window.width = 1100
    page.window.height = 800
    page.window.min_width = 800
    page.window.min_height = 600
    page.window.maximized = False
    page.window.resizable = True
    await page.window.center()
    page.padding = 0
    page.spacing = 0
    PlatinumTheme.apply_to_page(page)

    # 3. Componentes de Navegação
    # ViewContainer com Scroll Global para evitar cortes de conteúdo
    view_container = ft.Container(
        expand=True, 
        padding=40,
        content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    )

    # 5. Router de Views (Lifecycle-Safe & Intent-Driven)
    router = FlowRouter(view_container, state, page)
    
    # Função wrapper para o Flet rodar a corrotina (Legado Compatibilidade)
    def trigger_pick(mode):
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askopenfilename(
            title="Selecionar Matriz Genaja",
            filetypes=[("Arquivos Suportados", "*.xlsx;*.xls;*.csv;*.txt;*.tsv;*.parquet")]
        )
        root.destroy()
        if path:
            # Passo 1 Legado trata o sinal via on_pick_file (trigger_pick)
            v1_legacy.update_file(mode, path)

    # Instanciar Views
    step0 = Step0_InspectionView(state, router)
    intent_view = IntentRouterView(state, router)
    conv_view = SingleConvertView(state, router)
    prep_view = SinglePrepView(state, router)
    price_sync_view = PriceSyncView(state, router)
    
    # Instancias Legadas Modificadas para Roteador
    v1_legacy = Step1View(state, on_next=lambda: router.navigate("step2_legacy"), on_pick_file=trigger_pick, on_back=lambda: router.navigate("intent_router"))
    v2_legacy = Step2View(state, on_next=lambda: router.navigate("step3_legacy"), on_back=lambda: router.navigate("step1_legacy"))
    v3_legacy = Step3View(state, on_next=lambda: router.navigate("step4_legacy"), on_back=lambda: router.navigate("step2_legacy"))
    v4_legacy = Step4View(state, on_finish=lambda: router.navigate("step0_quarantine"), on_back=lambda: router.navigate("step3_legacy"))
    
    logs_view = LogsView()
    settings_view = SettingsView()

    # Registro no Roteador
    router.register_view("step0_quarantine", step0)
    router.register_view("intent_router", intent_view)
    router.register_view("single_convert", conv_view)
    router.register_view("single_prep", prep_view)
    router.register_view("price_sync", price_sync_view)
    
    # Registro do Legado
    router.register_view("step1_legacy", v1_legacy)
    router.register_view("step2_legacy", v2_legacy)
    router.register_view("step3_legacy", v3_legacy)
    router.register_view("step4_legacy", v4_legacy)

    # 6. Sidebar (NavigationRail)
    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0:
            router.navigate("step0_quarantine")
        elif idx == 1:
            # logs (não suportado pelo router headless - injeção manual)
            view_container.content.controls.clear()
            view_container.content.controls.append(logs_view)
            page.update()
        elif idx == 2:
            view_container.content.controls.clear()
            view_container.content.controls.append(settings_view)
            page.update()
        elif idx == 3:
            router.navigate("price_sync")

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        bgcolor=PlatinumTheme.SURFACE_DARK(),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.AUTO_AWESOME_OUTLINED,
                selected_icon=ft.Icons.AUTO_AWESOME,
                label="Wizard ETL",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.HISTORY_OUTLINED,
                selected_icon=ft.Icons.HISTORY,
                label="Logs",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Ajustes",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.CURRENCY_EXCHANGE_OUTLINED,
                selected_icon=ft.Icons.CURRENCY_EXCHANGE,
                label="Price Sync",
            ),
        ],
        on_change=on_nav_change,
    )

    # 7. Header (Info Bar com Support a Arraste e Window Controls)
    async def close_app(e):
        await page.window.close()

    async def toggle_maximize(e):
        # 🔗 API via Propriedade (Compatível v0.6x~0.8x)
        is_max = page.window.maximized
        page.window.maximized = not is_max
        # O ícone será atualizado via on_window_event automaticamente
        page.update()

    async def minimize_app(e):
        page.window.minimized = True
        page.update()

    def handle_window_event(e):
        """Atualiza ícone baseado no estado real do SO."""
        if e.data in ["maximize", "unmaximize", "restore"]:
            is_max = page.window.maximized
            # 🎨 Atualiza o conteúdo do botão de maximizar customizado (Stack de quadrados p/ Restore)
            max_icon_container.content = (
                ft.Stack([
                    ft.Container(width=9, height=9, border=ft.border.all(1.2, PlatinumTheme.TEXT_SECONDARY()), margin=ft.margin.only(top=3, left=3)),
                    ft.Container(width=9, height=9, border=ft.border.all(1.2, PlatinumTheme.TEXT_SECONDARY()), margin=ft.margin.only(bottom=3, right=3), bgcolor=None),
                ], width=12, height=12) if is_max else 
                ft.Container(width=10, height=10, border=ft.border.all(1.2, PlatinumTheme.TEXT_SECONDARY()))
            )
            page.update()

    page.on_window_event = handle_window_event

    # 🛠️ COMPONENTES DE JANELA CUSTOMIZADOS
    def win_button(content, on_click, hover_color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)):
        return ft.Container(
            content=content,
            on_click=on_click,
            width=46,
            height=32,
            alignment=ft.Alignment(0, 0),
            on_hover=lambda e: (setattr(e.control, "bgcolor", hover_color if e.data == "true" else None), e.control.update())
        )

    btn_min = win_button(ft.Container(width=12, height=1.2, bgcolor=PlatinumTheme.TEXT_SECONDARY()), minimize_app)
    
    max_icon_container = ft.Container(
        content=ft.Container(width=10, height=10, border=ft.border.all(1.2, PlatinumTheme.TEXT_SECONDARY())),
        alignment=ft.Alignment(0, 0)
    )
    btn_max = win_button(max_icon_container, toggle_maximize)

    btn_close = ft.Container(
        content=ft.Icon(ft.Icons.CLOSE, size=16, color=PlatinumTheme.TEXT_SECONDARY()),
        on_click=close_app,
        width=46,
        height=32,
        alignment=ft.Alignment(0, 0),
        on_hover=lambda e: (
            setattr(e.control, "bgcolor", ft.Colors.RED_ACCENT_700 if e.data == "true" else None),
            setattr(e.control.content, "color", "white" if e.data == "true" else PlatinumTheme.TEXT_SECONDARY()),
            e.control.update()
        )
    )

    header = ft.Container(
        content=ft.Row([
            # Area de Arraste (Título e Logo)
            ft.WindowDragArea(
                content=ft.Row([
                    ft.Icon(ft.Icons.AUTO_AWESOME, color=PlatinumTheme.PRIMARY(), size=22),
                    ft.Text("GENAJA SUITE", weight=ft.FontWeight.BOLD, size=15, color=PlatinumTheme.PRIMARY()),
                    ft.VerticalDivider(width=10, color=PlatinumTheme.BORDER_DARK()),
                    ft.Text(f"v{__version__} {__title__} | {config.get_config('general', 'operator_name')}", color=PlatinumTheme.TEXT_SECONDARY(), size=12),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True
            ),
            # Controles de Janela Customizados
            ft.Row([btn_min, btn_max, btn_close], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.only(left=20, right=0, top=0, bottom=0),
        bgcolor=PlatinumTheme.SURFACE_DARK(),
        height=32 # Slim and native height
    )

    # 8. Layout Final (Shell: Sidebar + Main Area)
    # ✅ ORDEM CORRETA: page.add() PRIMEIRO, overlay DEPOIS, navigate POR ÚLTIMO
    page.add(
        ft.Row([
            nav_rail,
            ft.VerticalDivider(width=1, color=PlatinumTheme.BORDER_DARK()),
            ft.Column([
                header,
                view_container
            ], expand=True, spacing=0)
        ], expand=True, spacing=0)
    )
    
    # 🩹 FIX FINAL: Modo Engenharia (Zero Overlay)
    # Removemos o ft.FilePicker do overlay para que o Flet não tente renderizar nada.
    # A seleção agora é 100% via Tkinter (já testado no Step 0).
    
    # Navegar DEPOIS que o layout está no ar
    router.navigate("step0_quarantine")

if __name__ == "__main__":
    ft.app(target=main)
