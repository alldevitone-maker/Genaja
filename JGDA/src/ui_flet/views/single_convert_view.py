import flet as ft
import os
import platform
import asyncio
import tkinter as tk
from tkinter import filedialog
from ui_flet.theme import PlatinumTheme
from core.engines.source_conversion_engine import SourceConversionEngine

from ui_flet.views.base_view import RoutedViewMixin

class SingleConvertView(ft.Container, RoutedViewMixin):
    """
    Genaja Stable - Interface Exclusiva para Modo A (convert_only).
    Desacoplada da Step2View clássica. Não pede arquivo Base 2.
    """
    def __init__(self, state, router):
        super().__init__()
        self.state = state
        self.router = router
        
        # ✅ Modo Engenharia (Zero FilePicker no Flet)
        # Usamos Tkinter para evitar caixas vermelhas e cliques perdidos.
        
        self.lbl_info = ft.Text("Pronto para Operação", size=18, weight="bold")
        self.lbl_path = ft.Text("Selecione o destino ou use a origem", size=12, italic=True, color=PlatinumTheme.TEXT_MUTED())
        
        self.btn_convert = ft.ElevatedButton(
            "EXECUTAR MISSÃO", 
            icon=ft.Icons.PLAY_ARROW_ROUNDED,
            on_click=self.process_conversion,
            height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
        
        self.drop_format = ft.Dropdown(
            label="Formato de Saída",
            value="csv",
            options=[
                ft.dropdown.Option("csv", "CSV (Excel Nativo)"),
                ft.dropdown.Option("parquet", "Parquet (Big Data)"),
                ft.dropdown.Option("json", "JSON (API)")
            ],
            width=200
        )
        
        self.chk_magic = ft.Checkbox(label="Magic Fix (Auto-Trim/Clean)", value=True)
        
        self.txt_out_folder = ft.TextField(
            label="Pasta de Destino",
            read_only=True,
            expand=True,
            hint_text="Padrão: Mesma pasta da origem",
            text_size=12
        )
        
        self.btn_pick_folder = ft.IconButton(
            icon=ft.Icons.FOLDER_OPEN,
            on_click=self._pick_folder_tkinter
        )
        
        self.btn_back = ft.OutlinedButton("Voltar (Trocar Intenção)", on_click=lambda _: self.router.navigate("intent_router"))
        self.btn_restart = ft.TextButton("Recomeçar do Zero", on_click=lambda _: self.router.navigate("step0_quarantine"))

        # Layout Dashboard Platinum
        self.content = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.AUTO_AWESOME, color="blue", size=30),
                ft.Text("CONVERTER E ISOLAR MATRIZ", size=28, weight="bold"),
            ], alignment="center"),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.FILE_PRESENT_ROUNDED),
                            title=self.lbl_info,
                            subtitle=self.lbl_path
                        ),
                        ft.Divider(height=1, color=PlatinumTheme.BORDER_DARK()),
                        ft.Row([
                            self.chk_magic,
                            self.drop_format
                        ], alignment="spaceBetween"),
                        ft.Row([
                            self.txt_out_folder,
                            self.btn_pick_folder
                        ], alignment="center")
                    ], spacing=20),
                    **PlatinumTheme.card_style()
                )
            ),
            
            ft.Container(height=10),
            self.btn_convert,
            ft.Container(height=20),
            ft.Row([self.btn_back, self.btn_restart], alignment="center", spacing=20)
        ], horizontal_alignment="center", spacing=25)
        
        self.padding = 60
        self.alignment = ft.Alignment(0, 0)

    def on_route_mounted(self):
        report = self.state.inspection_report or {}
        self.lbl_info.value = f"Deteção: {report.get('detected_type', 'Desconhecido')}"
        filepath = self.state.operation_plan.get("source_a", "")
        self.lbl_path.value = os.path.basename(filepath)
        self.update()
        
    def _pick_folder_tkinter(self, e):
        """Janela de Seleção Nativa de Out-Folder."""
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder = filedialog.askdirectory(title="Selecionar Destino da Matriz")
        root.destroy()
        
        if folder:
            self.txt_out_folder.value = folder
            self.state.temp_out_folder = folder
            self.update()

    def on_folder_selected(self, e: ft.FilePickerResultEvent):
        """Stub mantido por compatibilidade de legado."""
        pass

    async def process_conversion(self, e):
        self.btn_convert.disabled = True
        self.lbl_info.value = "Gerando DataFrame nativo (Aguarde...)"
        self.lbl_info.color = ft.Colors.BLUE_400
        self.update()
        
        # UI Aciona a Engine e Preenche Operation Plan
        filepath = self.state.operation_plan.get("source_a")
        
        # Validação Extra: Prevenir Hang por arquivo inexistente
        if not filepath or not os.path.exists(filepath):
            self.lbl_info.value = f"Erro: Arquivo não encontrado em {filepath}"
            self.lbl_info.color = ft.Colors.RED_400
            self.btn_convert.disabled = False
            self.update()
            return

        from core.adapters.rust_omni_adapter import RustOmniAdapter
        report_data = self.state.inspection_report or {}
        
        # O nome do arquivo gerado considera a escolha no dropdown
        export_ext = self.drop_format.value
        base_filename = os.path.basename(filepath)
        
        custom_folder = self.state.temp_out_folder
        if custom_folder:
            out_path = os.path.join(custom_folder, f"{base_filename}.extracted.{export_ext}")
        else:
            out_path = f"{filepath}.extracted.{export_ext}"
        
        # Injetar flag de Magic Fix no report temporariamente se necessário
        if self.chk_magic.value:
            report_data["magic_fix"] = True
        
        # Executa em Thread para não travar a UI do Flet
        try:
            res = await asyncio.to_thread(
                RustOmniAdapter.convert, 
                filepath, 
                report_data, 
                out_path=out_path
            )
        except Exception as e:
            from core.services.logger_service import LoggerService
            LoggerService().error(f"Erro crítico na thread de conversão: {e}")
            res = {"success": False, "warnings": [f"Erro de Sistema: {str(e)}"]}
        
        self.state.conversion_report = res
        self.state.operation_plan["conversion"] = res
        
        if res.get("success", False):
            extracted = res.get('output_path')
            engine_str = "Rust Native" if "rust" in res.get("_engine", "") else "Python Fallback"
            self.lbl_info.value = f"Matriz isolada ({engine_str})!\nSalvo em: {os.path.basename(extracted)}"
            self.lbl_info.color = ft.Colors.GREEN_400
            
            # Botão Extra Pós-Rotina (Abrir Pasta OS) - Limpeza de duplicados pragmática
            self.content.controls = [c for c in self.content.controls if not (isinstance(c, ft.ElevatedButton) and getattr(c, "text", None) == "Abrir Local do Arquivo")]
            
            def open_dir(e):
                folder = os.path.dirname(extracted)
                if platform.system() == "Windows":
                    os.startfile(folder)
                
            btn_folder = ft.ElevatedButton("Abrir Local do Arquivo", icon=ft.Icons.FOLDER_OPEN, on_click=open_dir)
            self.content.controls.insert(-1, btn_folder) # Insere antes dos botões de navegação
            self.btn_convert.disabled = False
        else:
            # Feedback resumido para não quebrar o layout
            warnings = res.get("warnings", [])
            err_msg = warnings[0] if warnings else "Erro interno desconhecido."
            short_err = err_msg.split('\n')[0] if '\n' in err_msg else err_msg
            self.lbl_info.value = f"Falha na Extração: {short_err[:100]}..."
            self.lbl_info.color = ft.Colors.RED_400
            self.btn_convert.disabled = False
            
        self.update()
