import flet as ft
import sys
import os
import asyncio

# Adicionar src ao path para importação modular
sys.path.append(os.path.abspath("src"))

from ui_flet.theme import PlatinumTheme
from services.config_service import ConfigService
from services.logger_service import LoggerService
from app.wizard_state import WizardState

# Views
from ui_flet.views.step1_view import Step1View
from ui_flet.views.step2_view import Step2View
from ui_flet.views.step3_view import Step3View
from ui_flet.views.step4_view import Step4View

async def main(page: ft.Page):
    # 1. Configuração Inicial
    config = ConfigService()
    LoggerService.setup()
    state = WizardState()
    
    # 2. Setup de Janela (API Flet v0.82+)
    page.title = "Genaja Pro v0.6.0 Alpha"
    page.window.width = 1100
    page.window.height = 800
    page.window.center()
    page.padding = 0
    page.spacing = 0
    PlatinumTheme.apply_to_page(page)
    
    # 3. Componentes de Navegação
    container = ft.Container(expand=True, padding=40)
    
    # 4. File Pickers (API v0.82.2 - Awaitable pick_files)
    picker_src = ft.FilePicker()
    picker_tgt = ft.FilePicker()
    page.overlay.extend([picker_src, picker_tgt])

    # 5. Router de Views
    def navigate_to(index):
        state.current_step_index = index
        if index == 0:
            container.content = v1
        elif index == 1:
            v2.load_data()
            container.content = v2
        elif index == 2:
            v3.load_data()
            container.content = v3
        elif index == 3:
            v4.load_data()
            container.content = v4
        page.update()

    # Callback para File Selection (Invocado pela Step1View)
    async def pick_file_handler(mode):
        if mode == "src":
            result = await picker_src.pick_files()
            if result: v1.update_file("src", result[0].path)
        else:
            result = await picker_tgt.pick_files()
            if result: v1.update_file("tgt", result[0].path)

    # Função wrapper para o Flet rodar a corrotina
    def trigger_pick(mode):
        page.run_task(pick_file_handler, mode)

    # Instanciar Views
    v1 = Step1View(state, on_next=lambda: navigate_to(1), on_pick_file=trigger_pick)
    v2 = Step2View(state, on_next=lambda: navigate_to(2), on_back=lambda: navigate_to(0))
    v3 = Step3View(state, on_next=lambda: navigate_to(3), on_back=lambda: navigate_to(1))
    v4 = Step4View(state, on_finish=lambda: navigate_to(0), on_back=lambda: navigate_to(2))

    # 6. Header
    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.DATA_EXPLORATION_ROUNDED, color=PlatinumTheme.PRIMARY, size=24),
            ft.Text("GENAJA PRO", weight=ft.FontWeight.BOLD, letter_spacing=1.5, size=16),
            ft.VerticalDivider(width=10, color=PlatinumTheme.BORDER_DARK),
            ft.Text(f"v0.6.0 Alpha | {config.get('general', 'operator_name')}", color=PlatinumTheme.TEXT_SECONDARY, size=13),
            ft.Row(expand=True),
            ft.IconButton(ft.Icons.CLOSE, on_click=lambda _: page.window_close(), icon_color=PlatinumTheme.DANGER),
        ]),
        padding=ft.padding.only(left=20, right=10, top=10, bottom=10),
        bgcolor=PlatinumTheme.SURFACE_DARK,
        height=60
    )

    # Initial View
    container.content = v1
    page.add(ft.Column([header, container], expand=True, spacing=0))

if __name__ == "__main__":
    ft.app(target=main)
