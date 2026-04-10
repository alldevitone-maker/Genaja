import flet as ft
import asyncio
import os
from ui_flet.theme import PlatinumTheme
from core.engines.transform_engine import TransformEngine

class SinglePrepView(ft.Container):
    """
    Genaja Stable - Interface Exclusiva para Modo B (prepare_single).
    """
    def __init__(self, state, router):
        super().__init__()
        self.state = state
        self.router = router
        
        self.lbl_file = ft.Text("Selecione um arquivo para iniciar a perícia", size=16, weight="bold")
        self.lbl_stats = ft.Text("Aguardando análise...", size=12, color=PlatinumTheme.TEXT_MUTED())
        
        # 📊 Tabela de Amostra (Forensic Preview)
        # NOTA: DataTable no Flet não suporta border_radius. Aplicado via Container externo.
        self.data_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("..."))],  # placeholder para evitar crash no init
            rows=[],
            heading_row_color=ft.Colors.with_opacity(0.1, PlatinumTheme.PRIMARY()),
            border=ft.border.all(1, PlatinumTheme.BORDER_DARK()),
            vertical_lines=ft.border.BorderSide(0.5, PlatinumTheme.BORDER_DARK()),
            horizontal_lines=ft.border.BorderSide(0.5, PlatinumTheme.BORDER_DARK()),
        )
        
        self.table_container = ft.Container(
            content=ft.Column([
                ft.Text("AMOSTRA FORENSE (TOP 10)", size=12, weight="bold", color=PlatinumTheme.PRIMARY()),
                ft.Row([self.data_table], scroll=ft.ScrollMode.ADAPTIVE)
            ], spacing=10),
            visible=False,
            **PlatinumTheme.card_style()
        )

        self.btn_back = ft.OutlinedButton("Voltar (Trocar Intenção)", on_click=lambda _: self.router.navigate("intent_router"))
        self.btn_restart = ft.TextButton("Recomeçar do Zero", on_click=lambda _: self.router.navigate("step0_quarantine"))

        self.content = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.ANALYTICS_OUTLINED, color="green", size=30),
                ft.Text("PREPARAR E LIMPAR DADOS", size=28, weight="bold"),
            ], alignment="center"),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.DASHBOARD_CUSTOMIZE_ROUNDED, color="green"),
                            title=self.lbl_file,
                            subtitle=self.lbl_stats
                        ),
                        self.table_container
                    ], spacing=15),
                    **PlatinumTheme.card_style()
                )
            ),
            
            ft.Container(height=10),
            ft.Row([self.btn_back, self.btn_restart], alignment="center", spacing=20)
        ], horizontal_alignment="center", spacing=25)
        
        self.padding = 60
        self.alignment = ft.Alignment(0, 0)

    async def on_route_mounted(self):
        filepath = self.state.operation_plan.get("source_a")
        if not filepath:
            return

        self.lbl_file.value = f"Perícia em: {os.path.basename(filepath)}"
        self.lbl_stats.value = "Capturando Amostra Forense..."
        self.update()
        
        # 🧠 Captura de Amostra via Engine (Padrão Silicon Valley: Non-blocking)
        from core.engines.source_conversion_engine import SourceConversionEngine
        sample = await asyncio.to_thread(SourceConversionEngine.get_sample_rows, filepath, 10)
        
        if sample:
            self.state.sample_data = sample
            # Atualizar Tabela
            headers = list(sample[0].keys())
            self.data_table.columns = [ft.DataColumn(ft.Text(h, weight="bold", size=12)) for h in headers]
            
            rows = []
            for row in sample:
                cells = [ft.DataCell(ft.Text(str(row.get(h, "")), size=11)) for h in headers]
                rows.append(ft.DataRow(cells=cells))
            
            self.data_table.rows = rows
            self.table_container.visible = True
            self.lbl_stats.value = f"{len(headers)} colunas detectadas | Visualizando primeiras 10 linhas."
            self.lbl_stats.color = ft.Colors.GREEN_400
        else:
            self.lbl_stats.value = "Falha ao capturar amostra. O arquivo pode estar vazio ou inacessível."
            self.lbl_stats.color = ft.Colors.RED_400
            
        self.update()
