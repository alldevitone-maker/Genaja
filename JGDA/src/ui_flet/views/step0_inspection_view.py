import flet as ft
import asyncio
from core.engines.source_inspection_engine import SourceInspectionEngine

class Step0_InspectionView(ft.Container):
    """
    Inspect Box — A 'Alfândega' de entrada. 
    Sem escolha de destino, apenas Inspeção Profunda (Omni-data).
    """
    def __init__(self, state, router):
        super().__init__()
        self.state = state
        self.router = router
        self.file_path = None
        
        # Lista de formatos tolerados na alfândega forense
        self.lbl_formats = ft.Text(
            "Formatos rastreáveis via Byte-Scanner: JSON | PARQUET | CSV / TXT / TSV | SAP XML SPREADSHEET | SQLITE | EXCEL | PDF | DLL / ELF (ASSEMBLY)",
            color="#555555",
            size=11,
            italic=True,
            font_family="Consolas"
        )
        
        # Interface de Seleção da Lupa Minimalista
        self.lbl_status = ft.Text("Selecione ou arraste arquivos para Análise Forense de Dados", size=14, color="grey")
        self.btn_picker = ft.IconButton(
            icon=ft.Icons.SEARCH,
            icon_color="#00FFFF",
            tooltip="Localizar matriz fisicamente",
            on_click=self.pick_file
        )
        self.header_row = ft.Row([self.btn_picker, self.lbl_status], alignment="center")
        
        # Botão "Omni-data" com Hook de Hover
        self.btn_inspect = ft.Container(
            content=ft.Text("Ativar o Omni-data", color="#00ff00", weight="bold"),
            bgcolor="#0a0a0a",
            padding=ft.padding.symmetric(horizontal=30, vertical=15),
            border_radius=8,
            border=ft.border.all(1, "#333333"),
            on_hover=self._on_btn_hover,
            on_click=self.mock_inspection,
            ink=True,
            tooltip="Inspecionar Falso XLS Mock"
        )
        
        # Spinner de carregamento "pensando...."
        self.loading_ring = ft.Column([
            ft.ProgressRing(color="#00ff00", stroke_width=3, width=40, height=40),
            ft.Text("pensando....", color="grey", size=12)
        ], alignment="center", horizontal_alignment="center", visible=False)

        self.log_list = ft.ListView(expand=1, spacing=5, auto_scroll=True)
        self.log_container = ft.Container(
            content=self.log_list,
            bgcolor="#0a0a0a", # Hacker dark
            border=ft.border.all(1, "#333333"),
            border_radius=8,
            padding=15,
            height=200,
            visible=False,
            width=600
        )

        self.row_actions = ft.Row([
            ft.OutlinedButton("Recomeçar Análise", icon=ft.Icons.RESTART_ALT, on_click=self.reset_view),
            ft.ElevatedButton(
                content=ft.Text("Prosseguir Mapeamento ➡️", weight="bold"), 
                on_click=lambda _: self.router.navigate("intent_router"), 
                bgcolor="#00ff00", 
                color="black"
            )
        ], alignment="center", visible=False)

        self.content = ft.Column([
            self.lbl_formats,
            self.header_row,
            ft.Text("Ou clique direto para acionar o Inspetor de Testes", size=12, color="grey"),
            self.btn_inspect,
            self.loading_ring,
            self.log_container,
            self.row_actions
        ], horizontal_alignment="center", spacing=15)
        
        self.alignment = ft.Alignment(0, 0)
        self.padding = 40

    def reset_view(self, e):
        self.log_container.visible = False
        self.row_actions.visible = False
        self.btn_inspect.visible = True
        self.btn_inspect.disabled = False
        self.file_path = None
        self.lbl_status.value = "Selecione a fonte de dados para rastreio profundo."
        self.lbl_status.color = "grey"
        self.log_list.controls.clear()
        self.update()

    def pick_file(self, e):
        import tkinter as tk
        from tkinter import filedialog
        import os
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askopenfilename(
            title="Injetar Arquivo na Quarentena Genaja",
            filetypes=[("Arquivos Omni-Data", "*.*")]
        )
        root.destroy()
        
        if path:
            self.file_path = path
            self.lbl_status.value = f"Fonte engatilhada: {os.path.basename(path)}"
            self.lbl_status.color = "#00FF00" # Hacker green
            self.btn_inspect.disabled = False
            self.update()

    def _on_btn_hover(self, e):
        # Efeito de brilho (Glow) ativável no hover
        if e.data == "true":
            e.control.border = ft.border.all(1, "#00ff00")
            e.control.shadow = ft.BoxShadow(spread_radius=1, blur_radius=15, color="#00ff00", offset=ft.Offset(0,0))
        else:
            e.control.border = ft.border.all(1, "#333333")
            e.control.shadow = None
        e.control.update()

    async def mock_inspection(self, e):
        if not self.file_path:
            self.file_path = "C:/mock/falso_sap.xls" 
            
        # self.lbl_status não está mais visivel de forma travada, não mudamos o valor aqui pois a UI muda pro loading
        
        # Troca botão por Loading de propósito por 2 segundos
        self.btn_inspect.visible = False
        self.loading_ring.visible = True
        self.log_list.controls.clear()
        self.update()
        
        # Delay intencional para carregar o visual vs processamento
        await asyncio.sleep(2.0)
        
        # Swap loading -> logs
        self.loading_ring.visible = False
        self.log_container.visible = True
        self.update()
        
        def log(msg, color="#00ff00", prefix=">_ "): 
            self.log_list.controls.append(ft.Text(f"{prefix}{msg}", color=color, font_family="Consolas", size=13))
            self.update()
            
        import os
        from core.adapters.rust_omni_adapter import RustOmniAdapter
        
        # MOCK ONLY: Permite que testemos mesmo se o arquivo não existir fisicamente 
        # (mas chamando o adaptador pra ele reagir com fallback se for path falso).
        report = RustOmniAdapter.inspect(self.file_path)
        
        # Override pro mock tático do SAP se o file_path "C:/mock" não for achado na máquina
        if not os.path.exists(self.file_path) and "falso_sap" in self.file_path:
             report = {
                "declared_type": "xls",
                "detected_type": "xml_spreadsheet_2003",
                "risk_level": "high",
                "recommended_action": "auto_convert",
                "can_auto_convert": True,
                "container_type": "xml",
                "notes": ["Falso XLS detectado (Estrutura XML nativa do SAP Business One)."],
                "_engine": "python_fallback"
            }
             
        file_size = os.path.getsize(self.file_path) if os.path.exists(self.file_path) else 14889500 # 14.2 MB mock
        size_str = f"{file_size / (1024 * 1024):.1f} MB" if file_size > 1024 * 1024 else f"{file_size / 1024:.1f} KB"
        
        engine_used = report.get("_engine", "unknown_engine")
        risk_colors = {"high": "#FF5252", "medium": "#FFAB40", "low": "#00FF00", "critical": "#FF0000"}
        risk_color = risk_colors.get(report.get("risk_level", "low").lower(), "#00FFFF")
        engine_color = "#00FFFF" if "rust" in engine_used.lower() else "#FFAB40"
        
        log("GENAJA OMNI-DATA ENGINE", "#00ff00", prefix="> ")
        log("", prefix="")
        await asyncio.sleep(0.3)
        
        log("[FILE]")
        log(f"name................ {os.path.basename(self.file_path)}")
        log(f"size................ {size_str}")
        log(f"declared_type....... {report.get('declared_type', 'N/A')}", "#00FFFF")
        log("", prefix="")
        await asyncio.sleep(0.5)

        log("[SCAN]")
        log(f"header_bytes........ 2048")
        log(f"engine.............. {engine_used.lower()}", engine_color)
        log("", prefix="")
        await asyncio.sleep(0.5)

        log("[RESULT]")
        log(f"detected_type....... {report.get('detected_type', 'N/A')}", "#FFFF00") 
        log(f"container_type...... {report.get('container_type', 'N/A')}")
        log(f"risk_level.......... {report.get('risk_level', 'low')}", risk_color)
        log(f"recommended_action.. {report.get('recommended_action', 'N/A')}")
        log("", prefix="")
        await asyncio.sleep(0.6)

        notes = report.get("notes", [])
        if notes:
            log("[NOTE]")
            for note in notes:
                log(note, "#9E9E9E")
                await asyncio.sleep(0.3)
            log("", prefix="")
        
        self.state.inspection_report = report
        self.state.source_ready = True
        
        # Popula o Operation Plan
        self.state.operation_plan["source_a"] = self.file_path
        self.state.operation_plan["inspection"] = report
        
        # Exibe os botões finais em vez de avançar automaticamente (permitindo que o operador leia o log tático)
        self.row_actions.visible = True
        self.update()


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, "0.7.1", "Interface forense para inspeção de cabeçalhos via Omni-data Engine")
