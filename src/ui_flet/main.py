import flet as ft
import sys
import os

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

def main(page: ft.Page):
    # 1. Configuração Inicial
    config = ConfigService()
    LoggerService.setup()
    state = WizardState()
    
    # 2. Setup de Janela
    page.title = "Genaja Pro v0.6.0 Alpha"
    page.window_width = 1100
    page.window_height = 800
    page.window_center()
    page.padding = 0
    page.spacing = 0
    PlatinumTheme.apply_to_page(page)
    
    # 3. Componentes de Navegação
    container = ft.Container(expand=True, padding=40)
    
    # 4. File Pickers
    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            mode = e.control.data # 'src' ou 'tgt'
            v1.update_file(mode, e.files[0].path)

    picker_src = ft.FilePicker(on_result=on_file_result); picker_src.data = "src"
    picker_tgt = ft.FilePicker(on_result=on_file_result); picker_tgt.data = "tgt"
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

    # Instanciar Views
    v1 = Step1View(state, on_next=lambda: navigate_to(1))
    v2 = Step2View(state, on_next=lambda: navigate_to(2), on_back=lambda: navigate_to(0))
    v3 = Step3View(state, on_next=lambda: navigate_to(3), on_back=lambda: navigate_to(1))
    v4 = Step4View(state, on_finish=lambda: navigate_to(0), on_back=lambda: navigate_to(2))

    # Hack para o Step1 disparar o picker
    def on_page_event(e):
        if e.name == "open_picker":
            if e.data == "src": picker_src.pick_files()
            else: picker_tgt.pick_files()
            
    page.on_event = on_page_event

    # 6. Header
    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.DATA_EXPLORATION_ROUNDED, color=PlatinumTheme.PRIMARY, size=24),
            ft.Text("GENAJA PRO", weight=ft.FontWeight.BOLD, letter_spacing=1.5, size=16),
            ft.VerticalDivider(width=10, color=PlatinumTheme.BORDER_DARK),
            ft.Text(f"v0.6.0 Alpha | {config.get('general', 'operator_name')}", color=PlatinumTheme.TEXT_SECONDARY, size=13),
            ft.Row(expand=True),
            ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close(), icon_color=PlatinumTheme.DANGER),
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
