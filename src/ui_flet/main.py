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
    # 0. Controles Não-Visuais (FilePickers desativados temporariamente por incompatibilidade do client)
    picker_src = ft.FilePicker()
    picker_tgt = ft.FilePicker()
    # page.overlay.extend([picker_src, picker_tgt]) # <-- REMOVIDO PARA EVITAR "Unknown Control: FilePicker"
    
    # 1. Configuração Inicial
    config = ConfigService()
    LoggerService.setup()
    state = WizardState()
    
    # 2. Setup de Janela (API Flet v0.82+)
    page.title = "Genaja Pro v0.6.0 Alpha"
    page.window.width = 1100
    page.window.height = 800
    await page.window.center()
    page.padding = 0
    page.spacing = 0
    PlatinumTheme.apply_to_page(page)

    # 3. Componentes de Navegação
    container = ft.Container(expand=True, padding=40)

    # 5. Router de Views (Lifecycle-Safe v0.6.0)
    def navigate_to(index):
        state.current_step_index = index
        if index == 0:
            container.content = v1
        elif index == 1:
            container.content = v2
        elif index == 2:
            container.content = v3
        elif index == 3:
            container.content = v4
        # PRIMEIRO: renderizar o controle na página
        page.update()
        # DEPOIS: popular dados (agora o controle já tem .page)
        if index == 1:
            v2.load_data()
        elif index == 2:
            v3.load_data()
        elif index == 3:
            v4.load_data()

    # Callback para File Selection (Invocado pela Step1View)
    async def pick_file_handler(mode):
        try:
            picker = picker_src if mode == "src" else picker_tgt
            # Verifica se o seletor está habilitado e presente
            if picker not in page.overlay:
                raise RuntimeError("Modo de Compatibilidade: Seletor Nativo Desativado.")
                
            result = await picker.pick_files()
            if result:
                v1.update_file(mode, result[0].path)
        except Exception as e:
            # Se o FilePicker falhar (ex: Unknown Control ou Timeout), avisamos o usuário
            LoggerService().error(f"Erro no FilePicker: {e}")
            sb = ft.SnackBar(
                ft.Text("Utilizando Modo de Compatibilidade. Por favor, use o campo de 'Caminho Manual' abaixo."),
                bgcolor=PlatinumTheme.WARNING
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()

    # Função wrapper para o Flet rodar a corrotina
    def trigger_pick(mode):
        page.run_task(pick_file_handler, mode)

    # Instanciar Views
    v1 = Step1View(state, on_next=lambda: navigate_to(1), on_pick_file=trigger_pick)
    v2 = Step2View(state, on_next=lambda: navigate_to(2), on_back=lambda: navigate_to(0))
    v3 = Step3View(state, on_next=lambda: navigate_to(3), on_back=lambda: navigate_to(1))
    v4 = Step4View(state, on_finish=lambda: navigate_to(0), on_back=lambda: navigate_to(2))

    # 6. Header
    async def close_app(e):
        await page.window.close()

    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.DATA_EXPLORATION_ROUNDED, color=PlatinumTheme.PRIMARY, size=24),
            ft.Text("GENAJA PRO", weight=ft.FontWeight.BOLD, size=16),
            ft.VerticalDivider(width=10, color=PlatinumTheme.BORDER_DARK),
            ft.Text(f"v0.6.0 Alpha | {config.get('general', 'operator_name')}", color=PlatinumTheme.TEXT_SECONDARY, size=13),
            ft.Row(expand=True),
            ft.IconButton(ft.Icons.CLOSE, on_click=close_app, icon_color=PlatinumTheme.DANGER),
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
