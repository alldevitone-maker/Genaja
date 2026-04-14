import flet as ft
import asyncio
import os
from ui_flet.theme import PlatinumTheme

class SinglePrepView(ft.Container):
    """
    Genaja Stable - Interface Exclusiva para Modo B (prepare_single).
    Normalização MDM 1:N Integrada.
    """
    def __init__(self, state, router):
        super().__init__()
        self.state = state
        self.router = router
        
        # 🔗 Gestão de Sessões v0.7.3
        self.active_tasks = {} # (col_id, col_mvf) -> ResultCard object
        self.results_gallery = ft.Column(spacing=15)
        
        self.lbl_file = ft.Text("Selecione um arquivo para iniciar a perícia", size=16, weight="bold")
        self.lbl_stats = ft.Text("Aguardando análise...", size=12, color=PlatinumTheme.TEXT_MUTED())
        
        # 📊 Tabela de Amostra (Forensic Preview)
        self.data_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("..."))],
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

        # --- Smart MVF Normalizer UI ---
        self.chk_mvf = ft.Switch(label="Normalização MDM (Smart 1:N)", value=False, on_change=self._on_toggle_mvf)
        self.dd_mvf_id = ft.Dropdown(label="Coluna ID (Origem)", width=200, text_size=11)
        self.dd_mvf_source = ft.Dropdown(label="Coluna MVF (Emails/Telefones)", width=250, text_size=11)
        
        self.btn_mvf_process = ft.ElevatedButton(
            "EXECUTAR SPLIT INTELIGENTE", 
            icon=ft.Icons.AUTO_FIX_HIGH,
            on_click=self._process_mvf,
            height=45,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=PlatinumTheme.PRIMARY(),
                color="white"
            )
        )

        self.mvf_config_area = ft.Column([
            ft.Text("Selecione os campos para separação Mestre/Detalhe:", size=11, italic=True),
            ft.Row([self.dd_mvf_id, self.dd_mvf_source], alignment="start"),
            self.btn_mvf_process
        ], spacing=15, visible=False)

        self.mvf_panel = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ACCOUNT_TREE_ROUNDED, color=PlatinumTheme.PRIMARY()),
                    ft.Text("SMART MVF NORMALIZER", weight="bold", color=PlatinumTheme.PRIMARY()),
                    ft.Container(expand=True),
                    self.chk_mvf
                ]),
                self.mvf_config_area,
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, PlatinumTheme.PRIMARY())),
                self.results_gallery
            ], spacing=10),
            padding=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, PlatinumTheme.PRIMARY())),
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            visible=False
        )

        self.btn_back = ft.OutlinedButton("Voltar", on_click=lambda _: self.router.navigate("intent_router"))
        self.btn_restart = ft.TextButton("Recomeçar", on_click=lambda _: self.router.navigate("step0_quarantine"))

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
                        self.table_container,
                        self.mvf_panel
                    ], spacing=15),
                    **PlatinumTheme.card_style()
                )
            ),
            
            ft.Container(height=10),
            ft.Row([self.btn_back, self.btn_restart], alignment="center", spacing=20)
        ], horizontal_alignment="center", spacing=25)
        
        self.padding = 60
        self.alignment = ft.Alignment(0, 0)

    def _on_toggle_mvf(self, e):
        self.mvf_config_area.visible = self.chk_mvf.value
        self.update()

    def _close_dlg(self, dlg):
        dlg.open = False
        self.page.update()

    async def _process_mvf(self, e):
        if not self.dd_mvf_source.value or not self.dd_mvf_id.value:
            sb = ft.SnackBar(ft.Text("⚠️ Selecione as colunas de Origem e ID Primeiro!"), bgcolor=ft.Colors.ORANGE_900)
            self.page.overlay.append(sb)
            sb.open = True
            self.page.update()
            return

        self.btn_mvf_process.disabled = True
        self.btn_mvf_process.text = "PROCESSANDO..."
        self.update()
        
        try:
            from core.engines.validation_engine import ValidationEngine
            df_full = self.state.df_src
            engine = ValidationEngine()
            
            results = await asyncio.to_thread(
                engine.normalize_multivalue_field, 
                df_full, 
                self.dd_mvf_source.value, 
                self.dd_mvf_id.value
            )
            
            if results:
                self.state.mvf_header_df = results["entity_primary"]
                self.state.mvf_detail_df = results["entity_contacts"]
                self.state.mvf_active = True
                
                # --- Lógica de Galeria Inteligente v0.7.3 ---
                from ui_flet.components.result_card import ResultCard
                
                col_id_name = str(self.dd_mvf_id.value)
                col_mvf_name = str(self.dd_mvf_source.value)
                session_key = (col_id_name, col_mvf_name)
                record_count = len(results['entity_contacts'])
                
                # Closures para ações (vínculo dinâmico aos dados atuais)
                async def export_primary(e): await self._export_mvf_file("primary", results["entity_primary"])
                async def export_contacts(e): await self._export_mvf_file("contacts", results["entity_contacts"])
                
                def open_kanban(e):
                    import logging
                    # 🎯 Contexto sagrado do Flet: e.page é a instância real do clique
                    active_page = e.page if e.page else self.page
                    logging.info(f"--- TRIGGER PLATINUM: Abrindo Curadoria Visual ---")
                    try:
                        from ui_flet.components.contact_kanban import ContactKanban
                        contacts_list = results["entity_contacts"].to_dict('records')
                        
                        # 🧩 Componente de Curadoria v0.7.2
                        kanban = ContactKanban(contacts=contacts_list, on_change=lambda: self.update())
                        
                        dlg = ft.AlertDialog(
                            title=ft.Text(f"CURADORIA: {col_id_name} ➔ {col_mvf_name}", weight="bold"),
                            content=ft.Container(kanban, width=1200, height=600),
                            actions=[
                                ft.ElevatedButton("Concluir Curadoria", 
                                                icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                                                on_click=lambda _: self._close_dlg(dlg))
                            ]
                        )
                        
                        # 🔗 Injeção por contexto de evento (Resiliência Máxima)
                        active_page.dialog = dlg
                        dlg.open = True
                        active_page.update()
                        logging.info("--- SUCCESS PLATINUM: Diálogo renderizado com sucesso ---")
                        
                    except Exception as err:
                        logging.error(f"--- FAILURE PLATINUM: {err} ---")
                        if active_page:
                            sb = ft.SnackBar(ft.Text(f"❌ Erro de UI: {str(err)}"), bgcolor=ft.Colors.RED_900)
                            active_page.overlay.append(sb)
                            sb.open = True
                            active_page.update()

                if session_key in self.active_tasks:
                    # Atualiza card existente e seus eventos físicos (v0.7.2 Fix)
                    card = self.active_tasks[session_key]
                    card.update_count(record_count)
                    card.update_actions(
                        on_curadoria=open_kanban,
                        on_export_primary=export_primary,
                        on_export_contacts=export_contacts
                    )
                else:
                    # Cria novo card
                    new_card = ResultCard(
                        col_id=col_id_name,
                        col_mvf=col_mvf_name,
                        count=record_count,
                        on_curadoria=open_kanban,
                        on_export_primary=export_primary,
                        on_export_contacts=export_contacts
                    )
                    self.active_tasks[session_key] = new_card
                    self.results_gallery.controls.append(new_card)

                sb = ft.SnackBar(ft.Text(f"✅ Sessão Atualizada: {record_count} registros processados."), bgcolor=PlatinumTheme.SUCCESS())
                self.page.overlay.append(sb)
                sb.open = True
            else:
                sb = ft.SnackBar(ft.Text("❌ Falha na normalização."), bgcolor=PlatinumTheme.DANGER())
                self.page.overlay.append(sb)
                sb.open = True
                
        except Exception as ex:
            import logging
            logging.error(f"Erro no Split Inteligente: {ex}")
            sb = ft.SnackBar(ft.Text(f"❌ Erro Crítico: {str(ex)}"), bgcolor=PlatinumTheme.DANGER())
            self.page.overlay.append(sb)
            sb.open = True
            
        finally:
            self.btn_mvf_process.text = "REPROCESSAR SPLIT"
            self.btn_mvf_process.disabled = False
            self.update()

    async def _export_mvf_file(self, mode, df):
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        filename = "Fornecedores_Mestre.csv" if mode == "primary" else "Contatos_Normalizados.csv"
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=filename)
        root.destroy()
        
        if file_path:
            df.to_csv(file_path, index=False, sep=';', encoding='utf-8-sig')
            
            async def open_folder(e):
                import subprocess
                subprocess.run(['explorer', '/select,', os.path.normpath(file_path)])

            sb = ft.SnackBar(
                content=ft.Row([
                    ft.Text(f"✅ Salvo: {os.path.basename(file_path)}"),
                    ft.TextButton("ABRIR PASTA", on_click=open_folder)
                ]),
                bgcolor=PlatinumTheme.SUCCESS()
            )
            self.page.overlay.append(sb)
            sb.open = True
            self.page.update()

    async def on_route_mounted(self):
        filepath = self.state.operation_plan.get("source_a")
        if not filepath: return

        self.lbl_file.value = f"Perícia em: {os.path.basename(filepath)}"
        self.lbl_stats.value = "Analisando Matriz..."
        self.update()

        from core.engines.loader_engine import LoaderEngine
        loader = LoaderEngine()
        
        try:
            workbook, _ = await asyncio.to_thread(loader.load_workbook, filepath)
            if workbook:
                sheet = list(workbook.keys())[0]
                df = workbook[sheet]
                self.state.df_src = df
                self.state.path_src = filepath
                
                headers = list(df.columns)
                self.dd_mvf_id.options = [ft.dropdown.Option(h) for h in headers]
                self.dd_mvf_source.options = [ft.dropdown.Option(h) for h in headers]
                
                if "Cdigo" in headers: self.dd_mvf_id.value = "Cdigo"
                elif "CPF/CNPJ" in headers: self.dd_mvf_id.value = "CPF/CNPJ"
                if "E-mail" in headers: self.dd_mvf_source.value = "E-mail"
                
                self.data_table.columns = [ft.DataColumn(ft.Text(h, size=11, weight="bold")) for h in headers]
                self.data_table.rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(str(row.get(h, "")))) for h in headers]) for row in df.head(10).to_dict('records')]
                
                self.table_container.visible = True
                self.mvf_panel.visible = True
                self.lbl_stats.value = f"{len(headers)} colunas detectadas."
                self.lbl_stats.color = ft.Colors.GREEN_400
        except Exception as e:
            self.lbl_stats.value = f"Erro: {str(e)}"
            self.lbl_stats.color = ft.Colors.RED_400
        self.update()


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version import __version__
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Interface de preparação e Split Inteligente MDM 1:N com resiliência UI")
