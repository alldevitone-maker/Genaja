import flet as ft
from ui_flet.theme import PlatinumTheme
from core.engines.loader_engine import LoaderEngine

class Step1View(ft.Column):
    """
    PASSO 1: Seleção de Fontes (v0.6.0).
    Focada em clareza visual e heurística de cabeçalho.
    """
    def __init__(self, state, on_next, on_pick_file):
        super().__init__(expand=True, spacing=20)
        self.state = state
        self.on_next = on_next
        self.on_pick_file = on_pick_file
        self.loader = LoaderEngine()
        
        self.src_info = ft.Text("Nenhum arquivo de ORIGEM selecionado", color=PlatinumTheme.TEXT_SECONDARY)
        self.tgt_info = ft.Text("Nenhum arquivo de DESTINO selecionado", color=PlatinumTheme.TEXT_SECONDARY)
        
        # UI Elements
        self.btn_next = ft.ElevatedButton(
            "Prosseguir para Chaves ➡️", 
            on_click=lambda _: self.on_next(),
            disabled=True,
            bgcolor=PlatinumTheme.PRIMARY,
            color="white",
            height=50
        )
        
        self.controls = [
            ft.Text("📂 Seleção de Arquivos", size=24, weight=ft.FontWeight.W600),
            ft.Row([
                self._create_drop_zone("Planilha de ORIGEM (SAP/Export)", "src"),
                self._create_drop_zone("Planilha de DESTINO (Master)", "tgt"),
            ], spacing=20),
            ft.Row([ft.Container(expand=True), self.btn_next], alignment=ft.MainAxisAlignment.END)
        ]

    def _create_drop_zone(self, title, mode):
        # Nota: Usaremos o FilePicker do Flet no main.py, aqui apenas o visual
        return ft.Container(
            **PlatinumTheme.card_style(),
            expand=True,
            content=ft.Column([
                ft.Text(title, weight=ft.FontWeight.BOLD, size=16),
                ft.Divider(color=PlatinumTheme.BORDER_DARK),
                ft.Icon(ft.icons.UPLOAD_FILE_SHARP, size=40, color=PlatinumTheme.PRIMARY),
                self.src_info if mode == "src" else self.tgt_info,
                ft.OutlinedButton(
                    "Selecionar Arquivo", 
                    icon=ft.icons.SEARCH,
                    on_click=lambda _: self._trigger_picker(mode)
                )
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def _trigger_picker(self, mode):
        # Chama o callback passado pela main.py (que será invocado via run_task se necessário)
        self.on_pick_file(mode)

    def update_file(self, mode, path):
        try:
            df, skip = self.loader.load_excel(path)
            if mode == "src":
                self.state.df_src = df
                self.state.path_src = path
                self.src_info.value = f"✅ {path.split('/')[-1]}\n{len(df)} linhas | Cabeçalho: {skip}"
                self.src_info.color = PlatinumTheme.SUCCESS
            else:
                self.state.df_tgt = df
                self.state.path_tgt = path
                self.tgt_info.value = f"✅ {path.split('/')[-1]}\n{len(df)} linhas | Cabeçalho: {skip}"
                self.tgt_info.color = PlatinumTheme.SUCCESS
            
            if self.state.df_src is not None and self.state.df_tgt is not None:
                self.btn_next.disabled = False
            
            self.update()
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar arquivo: {e}"))
            self.page.snack_bar.open = True
            self.page.update()
