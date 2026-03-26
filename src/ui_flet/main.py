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
from version import __version__, __title__

# Views
from ui_flet.views.step1_view import Step1View
from ui_flet.views.step2_view import Step2View
from ui_flet.views.step3_view import Step3View
from ui_flet.views.step4_view import Step4View
from ui_flet.views.logs_view import LogsView
from ui_flet.views.settings_view import SettingsView

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

    # 5. Router de Views (Lifecycle-Safe v0.6.0)
    def navigate_to(index):
        # Mapeamento de Views
        mapping = {
            0: v1, 1: v2, 2: v3, 3: v4,
            10: logs_view,
            20: settings_view
        }
        
        target_view = mapping.get(index, v1)
        
        # Limpeza e Inserção Atômica
        view_container.content.controls.clear()
        view_container.content.controls.append(target_view)
        
        # Atualização do Estado do Wizard apenas se for um passo do Wizard (0-3)
        if index < 10:
            state.current_step_index = index
            nav_rail.selected_index = 0 # Mantém "Wizard ETL" selecionado visualmente
        
        page.update()
        
        # Power-up: Popular dados após montagem
        if index == 1: v2.load_data()
        elif index == 2: v3.load_data()
        elif index == 3: v4.load_data()
        elif index == 10: logs_view.load_logs()

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
                bgcolor=PlatinumTheme.WARNING()
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
    
    logs_view = LogsView()
    settings_view = SettingsView()

    # 6. Sidebar (NavigationRail)
    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0:
            # Retorna ao passo onde o usuário estava no Wizard
            navigate_to(state.current_step_index)
        elif idx == 1:
            navigate_to(10) # 10 = Logs
        elif idx == 2:
            navigate_to(20) # 20 = Settings
        page.update()

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
        """Sincronia Nativa (v0.6.0): Atualiza ícone baseado no estado real do SO."""
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

    # 🛠️ COMPONENTES DE JANELA CUSTOMIZADOS (v0.6.0 Platinum)
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
                    ft.Text(f"v{__version__} {__title__} | {config.get('general', 'operator_name')}", color=PlatinumTheme.TEXT_SECONDARY(), size=12),
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

    # Initial View
    view_container.content.controls = [v1]
    
    # 8. Layout Final (Shell: Sidebar + Main Area)
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

if __name__ == "__main__":
    ft.app(target=main)
