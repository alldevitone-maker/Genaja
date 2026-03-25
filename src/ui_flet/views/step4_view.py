import flet as ft
import pandas as pd
import os
from ui_flet.theme import PlatinumTheme
from core.engines.etl_engine import ETLEngine
from core.engines.validation_engine import ValidationEngine
from services.export_service import ExportService
from services.audit_service import AuditService
from services.logger_service import LoggerService

class Step4View(ft.Column):
    """
    PASSO 4: Resumo, Execucao & Exportacao (v0.6.0).
    Restauracao completa do motor v0.4.6.
    """
    def __init__(self, state, on_finish, on_back):
        super().__init__(expand=True, spacing=20)
        self.state = state
        self.on_finish = on_finish
        self.on_back = on_back
        self.engine = ETLEngine()
        self.validator = ValidationEngine()
        self.exporter = ExportService()
        self.audit = AuditService(operator="Flet_User")
        self.logger = LoggerService()
        
        self.summary_text = ft.Text("Pronto para iniciar a sincronizacao.", size=16)
        self.progress_bar = ft.ProgressBar(width=400, color=PlatinumTheme.PRIMARY, visible=False)
        
        # Format selector (v0.4.6 parity)
        self.format_group = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="xlsx", label="Excel"),
                ft.Radio(value="csv", label="CSV"),
                ft.Radio(value="json", label="JSON"),
                ft.Radio(value="sql", label="SQL"),
            ]),
            value="xlsx"
        )
        
        # Higienizacao & Blindagem (v0.4.7 from summary_panel)
        self.chk_zeros = ft.Checkbox(label="I.A Sync: Auto-filtrar linhas com valor Zero/Nulo", value=False)
        self.chk_zeros.tooltip = "Remove automaticamente linhas onde a chave tem valor vazio ou zero"
        self.chk_zeros.on_change = lambda e: setattr(self.state, "remove_nulls", e.control.value)
        
        self.chk_clean = ft.Checkbox(label="Limpar colunas orfas na saida", value=True)
        self.chk_clean.tooltip = "Remove colunas que nao fazem parte do mapeamento no resultado final"
        
        self.btn_run = ft.ElevatedButton(
            "INICIAR SINCRONIZACAO CORPORATIVA", 
            on_click=self._run_sync, 
            bgcolor=PlatinumTheme.SUCCESS, 
            color="white", height=60, width=350
        )
        self.btn_run.tooltip = "Executa o motor ETL com todas as configuracoes definidas"
        
        # Module selector (v0.4.6: Sync vs Comparador tabs)
        self.module_selector = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="sync", label="Sincronizacao e Limpeza (ETL)"),
                ft.Radio(value="compare", label="Comparador Puro (Auditoria)"),
            ]),
            value="sync"
        )
        
        self.compare_mode = ft.Dropdown(
            label="Tipo de Comparacao",
            options=[
                ft.dropdown.Option("falta_destino", "Falta no Destino"),
                ft.dropdown.Option("falta_origem", "Falta na Origem"),
            ],
            value="falta_destino",
            expand=True,
            visible=False
        )
        self.module_selector.on_change = self._on_module_change
        
        self.controls = [
            ft.Text("Finalizacao & Auditoria", size=24, weight=ft.FontWeight.W_600),
            # Module selector
            ft.Container(
                **PlatinumTheme.card_style(),
                content=ft.Column([
                    ft.Text("Modulo de Execucao:", weight=ft.FontWeight.W_600),
                    self.module_selector,
                    self.compare_mode,
                ], spacing=10)
            ),
            ft.Container(
                **PlatinumTheme.card_style(),
                content=ft.Column([
                    self.summary_text,
                    ft.Divider(color=PlatinumTheme.BORDER_DARK),
                    ft.Text("O processo ira:"),
                    ft.Text("- Cruzar dados via Chave Primaria", size=13),
                    ft.Text("- Atualizar valores mapeados", size=13),
                    ft.Text("- Gerar log de auditoria compliance", size=13),
                ])
            ),
            # Higienizacao & Blindagem (v0.4.7)
            ft.Container(
                **PlatinumTheme.card_style(),
                content=ft.Column([
                    ft.Text("Higienizacao & Blindagem (Data Governance):", weight=ft.FontWeight.W_600),
                    self.chk_zeros,
                    self.chk_clean,
                ], spacing=5)
            ),
            ft.Container(
                **PlatinumTheme.card_style(),
                content=ft.Column([
                    ft.Text("Opcoes de Saida:", weight=ft.FontWeight.W_600),
                    self.format_group,
                ], spacing=10)
            ),
            ft.Column([self.progress_bar, self.btn_run], 
                       alignment=ft.MainAxisAlignment.CENTER, 
                       horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([ft.TextButton("Voltar", on_click=lambda _: self.on_back())])
        ]

    def _on_module_change(self, e):
        self.compare_mode.visible = (e.control.value == "compare")
        self.update()

    def load_data(self):
        m_count = len(self.state.mapping)
        src_rows = len(self.state.df_src) if self.state.df_src is not None else 0
        tgt_rows = len(self.state.df_tgt) if self.state.df_tgt is not None else 0
        self.summary_text.value = (
            f"Resumo:\n"
            f"- {src_rows} linhas na Origem\n"
            f"- {tgt_rows} linhas no Destino\n"
            f"- {m_count} colunas mapeadas\n"
            f"- Shielding: {'ON' if self.state.shielding else 'OFF'}\n"
            f"- A1 Protegida: {'ON' if self.state.protected_a1 else 'OFF'}"
        )
        if self.page:
            self.update()

    def _run_sync(self, e):
        self.btn_run.disabled = True
        self.progress_bar.visible = True
        self.update()
        
        try:
            selected_module = self.module_selector.value or "sync"
            
            if selected_module == "compare":
                # Modulo Comparador Puro (v0.4.6)
                cmp_mode = self.compare_mode.value or "falta_destino"
                df_result, count = self.engine.compare(
                    self.state.df_src,
                    self.state.df_tgt,
                    self.state.key_src,
                    self.state.key_tgt,
                    mode=cmp_mode,
                    auto_trim=self.state.auto_trim,
                    auto_upper=self.state.auto_upper
                )
                self.logger.info(f"Comparacao concluida ({cmp_mode}): {count} registros encontrados.")
            else:
                # Modulo Sincronizacao (Padrao)
                df_result = self.engine.synchronize(
                    self.state.df_src, 
                    self.state.df_tgt,
                    self.state.key_src, 
                    self.state.key_tgt,
                    self.state.mapping,
                    protected_a1=self.state.protected_a1,
                    shielding=self.state.shielding,
                    auto_trim=self.state.auto_trim,
                    auto_upper=self.state.auto_upper
                )
            
            # 2. Aplicar Filtro Numerico v0.4.8 (ValidationEngine)
            if hasattr(self.state, 'remove_nulls') and self.state.remove_nulls:
                filter_cols = self.state.null_filter_cols if self.state.null_filter_cols else list(df_result.columns)
                df_result = self.validator.apply_numeric_filter(df_result, filter_cols)
            
            # 3. Aplicar "Manter apenas colunas selecionadas"
            if hasattr(self.state, 'keep_only_mapped') and self.state.keep_only_mapped:
                keep_cols = list(self.state.mapping.values())
                if self.state.protected_a1 and self.state.df_tgt is not None:
                    a1 = self.state.df_tgt.columns[0]
                    if a1 not in keep_cols:
                        keep_cols.insert(0, a1)
                keep_cols = [c for c in keep_cols if c in df_result.columns]
                if keep_cols:
                    df_result = df_result[keep_cols]
            
            # 4. Exportacao Multi-Formato (v0.4.6 Parity)
            fmt = self.format_group.value or "xlsx"
            out_dir = os.path.join(os.getcwd(), "results")
            os.makedirs(out_dir, exist_ok=True)
            timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            out_path = os.path.join(out_dir, f"GENAJA_SYNC_{timestamp}.{fmt}")
            
            self.exporter.export(df_result, out_path)
            
            # 5. Auditoria
            self.audit.record_sync(self.state.path_src, self.state.path_tgt, len(df_result))
            self.logger.info(f"Concluido: {len(df_result)} linhas -> {out_path}")
            
            # 6. Sucesso
            sb = ft.SnackBar(ft.Text(f"Sucesso! {len(df_result)} linhas salvas em: {out_path}"), bgcolor=PlatinumTheme.SUCCESS)
            self.page.overlay.append(sb)
            sb.open = True
            
        except Exception as ex:
            self.logger.error(f"Erro na sincronizacao: {ex}")
            sb = ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor=PlatinumTheme.DANGER)
            self.page.overlay.append(sb)
            sb.open = True
            
        self.progress_bar.visible = False
        self.btn_run.disabled = False
        self.update()
