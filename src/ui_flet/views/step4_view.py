import flet as ft
from ui_flet.theme import PlatinumTheme
from core.engines.etl_engine import ETLEngine
from services.audit_service import AuditService
from services.logger_service import LoggerService
import os

class Step4View(ft.Column):
    """
    PASSO 4: Resumo e Execução (v0.6.0).
    Ponto final onde a mágica do motor v0.4.8 acontece.
    """
    def __init__(self, state, on_finish, on_back):
        super().__init__(expand=True, spacing=20)
        self.state = state
        self.on_finish = on_finish
        self.on_back = on_back
        self.engine = ETLEngine()
        self.audit = AuditService(operator="Flet_User")
        self.logger = LoggerService()
        
        self.summary_text = ft.Text("Pronto para iniciar a sincronização.", size=16)
        self.progress_bar = ft.ProgressBar(width=400, color=PlatinumTheme.PRIMARY, visible=False)
        self.btn_run = ft.ElevatedButton("🚀 DISPARAR SINCRONIZAÇÃO!", on_click=self._run_sync, bgcolor=PlatinumTheme.SUCCESS, color="white", height=60, width=300)
        
        self.controls = [
            ft.Text("🚀 Finalização & Auditoria", size=24, weight=ft.FontWeight.W_600),
            ft.Container(
                **PlatinumTheme.card_style(),
                content=ft.Column([
                    self.summary_text,
                    ft.Divider(color=PlatinumTheme.BORDER_DARK),
                    ft.Text("O processo irá:"),
                    ft.Text("✅ Cruzar dados via Chave Primária", size=13),
                    ft.Text("✅ Atualizar valores mapeados", size=13),
                    ft.Text("✅ Gerar log de auditoria compliance", size=13),
                ])
            ),
            ft.Column([self.progress_bar, self.btn_run], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([ft.TextButton("⬅️ Voltar", on_click=lambda _: self.on_back())])
        ]

    def load_data(self):
        m_count = len(self.state.mapping)
        self.summary_text.value = f"Resumo:\n- {len(self.state.df_src)} linhas na Origem\n- {len(self.state.df_tgt)} linhas no Destino\n- {m_count} colunas mapeadas"
        self.update()

    def _run_sync(self, e):
        self.btn_run.disabled = True
        self.progress_bar.visible = True
        self.update()
        
        try:
            # EXECUÇÃO DO MOTOR (Logical Rollback v0.4.8)
            df_final = self.engine.synchronize(
                self.state.df_src,
                self.state.df_tgt,
                self.state.key_src,
                self.state.key_tgt,
                self.state.mapping,
                self.state.key_tgt_final
            )
            
            # Exportação (Placeholder simples para v0.6.0 Alpha)
            out_path = os.path.join(os.getcwd(), "data", "GENAJA_RESULT.xlsx")
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            df_final.to_excel(out_path, index=False)
            
            # Auditoria
            self.audit.record_sync(self.state.path_src, self.state.path_tgt, len(df_final))
            self.logger.info(f"Sincronização concluída: {len(df_final)} linhas.")
            
            # Sucesso
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Sincronização concluída com sucesso! Salvo em: {out_path}"), bgcolor=PlatinumTheme.SUCCESS)
            self.page.snack_bar.open = True
            
        except Exception as ex:
            self.logger.error(f"Erro na sincronização: {ex}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Erro Fatal: {ex}"), bgcolor=PlatinumTheme.DANGER)
            self.page.snack_bar.open = True
            
        self.progress_bar.visible = False
        self.btn_run.disabled = False
        self.update()
