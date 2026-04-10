import flet as ft
from version import __version__
import os
import tkinter as tk
from tkinter import filedialog
from core.paths import BRAINS_DIR
from ui_flet.theme import PlatinumTheme
from core.engines.loader_engine import LoaderEngine
from core.engines.suggestion_engine import SuggestionEngine
from core.services.logger_service import LoggerService
from core.engines.validation_engine import ValidationEngine
from core.engines.lookup_engine import LookupEngine
from core.learning.suggestion_engine import HistoricalSuggestionEngine
from core.learning.learning_logger import LearningLogger
from ui_flet.dialogs.file_intelligence_dialog import FileIntelligenceDialog
from core.services.connector_factory import ConnectorFactory

class Step1View(ft.Column):
    """
    PASSO 1: Seleção de Fontes.
    Focada em clareza visual e heurística de cabeçalho.
    """
    def _on_card_hover(self, e):
        """Efeito Visual Platinum: Altera a borda no hover."""
        e.control.border = ft.border.all(1, PlatinumTheme.PRIMARY() if e.data == "true" else PlatinumTheme.BORDER_DARK())
        e.control.update()

    def __init__(self, state, on_next, on_pick_file, on_back=None):
        super().__init__(expand=True, spacing=20)
        self.state = state
        self.on_next = on_next
        self.on_back = on_back
        self.on_pick_file = on_pick_file
        self.loader = LoaderEngine()
        self.suggester = SuggestionEngine()
        self.validator = ValidationEngine()
        self.lookup = LookupEngine()
        self.history_engine = HistoricalSuggestionEngine(BRAINS_DIR)
        
        self.src_info = ft.Text("Nenhum arquivo de ORIGEM selecionado", color=PlatinumTheme.TEXT_SECONDARY())
        self.tgt_info = ft.Text("Nenhum arquivo de DESTINO selecionado", color=PlatinumTheme.TEXT_SECONDARY())
        
        # UI Elements
        self.src_path_field = ft.TextField(
            label="Caminho Manual Selecionado (Origem)", 
            hint_text="Caminho/arquivo.xlsx",
            hint_style=ft.TextStyle(color=PlatinumTheme.TEXT_PLACEHOLDER()),
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_SECONDARY()),
            expand=True, 
            border_color=PlatinumTheme.BORDER_DARK(),
            focused_border_color=PlatinumTheme.PRIMARY(),
            color=PlatinumTheme.TEXT_PRIMARY(),
            on_submit=lambda e: self._on_manual_path("src", e.control.value), 
            on_blur=lambda e: self._on_manual_path("src", e.control.value),
            text_size=12
        )
        self.tgt_path_field = ft.TextField(
            label="Caminho Manual Selecionado (Destino)", 
            hint_text="Caminho/arquivo.xlsx",
            hint_style=ft.TextStyle(color=PlatinumTheme.TEXT_PLACEHOLDER()),
            label_style=ft.TextStyle(color=PlatinumTheme.TEXT_SECONDARY()),
            expand=True, 
            border_color=PlatinumTheme.BORDER_DARK(),
            focused_border_color=PlatinumTheme.PRIMARY(),
            color=PlatinumTheme.TEXT_PRIMARY(),
            on_submit=lambda e: self._on_manual_path("tgt", e.control.value), 
            on_blur=lambda e: self._on_manual_path("tgt", e.control.value),
            text_size=12
        )
        
        # Multi-Sheet Selectors
        self.src_sheet_dropdown = ft.Dropdown(
            label="Selecionar Aba (Origem)",
            visible=False,
            height=40,
            text_size=12,
            border_radius=8
        )
        self.src_sheet_dropdown.on_change = lambda e: self._on_sheet_change("src", e.data)
        
        self.tgt_sheet_dropdown = ft.Dropdown(
            label="Selecionar Aba (Destino)",
            visible=False,
            height=40,
            text_size=12,
            border_radius=8
        )
        self.tgt_sheet_dropdown.on_change = lambda e: self._on_sheet_change("tgt", e.data)

        self.btn_next = ft.ElevatedButton(
            "Prosseguir para Chaves ➡️", 
            on_click=self._intercept_next,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor={"": PlatinumTheme.PRIMARY()},
                color={"": "white"}, # Action FG fixo p/ este fundo
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            height=50
        )
        
        self.controls = [
            ft.Row([
                ft.Text("Configuração da Origem", size=24, weight=ft.FontWeight.W_600, color=PlatinumTheme.PRIMARY()),
                ft.Container(expand=True),
                ft.OutlinedButton(
                    "Voltar (Trocar Intenção)", 
                    icon=ft.Icons.ARROW_BACK, 
                    on_click=lambda _: self.on_back() if self.on_back else None,
                    visible=True if self.on_back else False
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self._build_source_selector(),
            ft.Divider(color=PlatinumTheme.BORDER_DARK()),
            self._build_file_section() if self.state.source_type == "local_file" else self._build_sql_section(),
            ft.Divider(color=PlatinumTheme.BORDER_DARK()),
            # DESTINO (Sempre Local nesta sprint)
            self._create_drop_zone("Planilha de DESTINO", "tgt"),
            ft.Row([
                ft.ElevatedButton(
                    "🤖 Sugerir Arquivos Recentes (Smart-Pull)", 
                    icon=ft.Icons.AUTO_AWESOME,
                    on_click=self._on_suggest_click,
                    bgcolor=PlatinumTheme.SURFACE_DARK(),
                    color=PlatinumTheme.PRIMARY(),
                    visible=(self.state.source_type == "local_file")
                ),
                ft.Container(expand=True), 
                self.btn_next
            ], alignment=ft.MainAxisAlignment.END)
        ]

    def _build_source_selector(self):
        return ft.SegmentedButton(
            selected=[self.state.source_type],
            allow_multiple_selection=False,
            on_change=self._on_source_type_change,
            segments=[
                ft.Segment(
                    value="local_file",
                    label=ft.Text("📊 Arquivo Local"),
                    icon=ft.Icon(ft.Icons.DESCRIPTION)
                ),
                ft.Segment(
                    value="sql_db",
                    label=ft.Text("🗄️ SQL Database"),
                    icon=ft.Icon(ft.Icons.STORAGE)
                ),
            ],
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            )
        )

    def _build_file_section(self):
        return ft.ResponsiveRow([
            self._create_drop_zone("Planilha de ORIGEM", "src"),
        ], spacing=20)

    def _create_drop_zone(self, label, mode):
        """Card de Seleção Platinum."""
        is_src = (mode == "src")
        info_text = self.src_info if is_src else self.tgt_info
        path_field = self.src_path_field if is_src else self.tgt_path_field
        
        return ft.Container(
            content=ft.Column([
                ft.Text(label, weight=ft.FontWeight.W_600, size=16, color=PlatinumTheme.PRIMARY()),
                ft.Row([
                    ft.ElevatedButton(
                        "Abrir Arquivo 📂", 
                        icon=ft.Icons.FOLDER_OPEN_OUTLINED,
                        on_click=lambda _: self._trigger_picker(mode),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        bgcolor=PlatinumTheme.SURFACE_DARK(),
                        color=PlatinumTheme.PRIMARY()
                    ),
                    ft.Text("ou arraste aqui", size=12, color=PlatinumTheme.TEXT_MUTED())
                ]),
                info_text,
                path_field,
                self.src_sheet_dropdown if is_src else self.tgt_sheet_dropdown
            ], spacing=10),
            expand=True,
            col={"sm": 12, "md": 12},
            **PlatinumTheme.card_style(),
            on_hover=self._on_card_hover
        )

    def _build_sql_section(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Configuração de Conexão SQL", weight=ft.FontWeight.BOLD, size=16),
                ft.TextField(
                    label="Conexão Expressa (URL/URI)", 
                    hint_text="Ex: sqlite:///test_genaja.db ou postgresql://user:pass@host/db",
                    tooltip="Use este campo para SQLite ou conexão personalizada. Se preenchido, ignora os campos abaixo.",
                    on_change=lambda e: self._on_sql_field_change("url", e.data),
                    text_size=12,
                    border_color=PlatinumTheme.PRIMARY(),
                    focused_border_color=PlatinumTheme.PRIMARY(),
                    label_style=ft.TextStyle(color=PlatinumTheme.PRIMARY(), weight=ft.FontWeight.BOLD)
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.ResponsiveRow([
                    ft.TextField(label="Host/IP", col=8, on_change=lambda e: self._on_sql_field_change("host", e.data)),
                    ft.TextField(label="Porta", col=4, value="5432", on_change=lambda e: self._on_sql_field_change("port", e.data)),
                    ft.TextField(label="Usuário", col=6, on_change=lambda e: self._on_sql_field_change("user", e.data)),
                    ft.TextField(label="Senha", col=6, password=True, can_reveal_password=True, on_change=lambda e: self._on_sql_field_change("password", e.data)),
                    ft.TextField(label="Database", col=12, on_change=lambda e: self._on_sql_field_change("database", e.data)),
                ], spacing=10),
                ft.Row([
                    ft.ElevatedButton(
                        "Testar Conexão 🔍", 
                        on_click=self._on_sql_test_click,
                        bgcolor=PlatinumTheme.SURFACE_DARK(),
                        color=PlatinumTheme.PRIMARY()
                    ),
                    self._build_connection_status()
                ]),
                self.src_sheet_dropdown
            ], spacing=15),
            **PlatinumTheme.card_style()
        )

    def _build_connection_status(self):
        self.sql_status_indicator = ft.Row([
            ft.Icon(ft.Icons.CANCEL, color=PlatinumTheme.DANGER()), 
            ft.Text("Desconectado", size=12, color=PlatinumTheme.TEXT_MUTED())
        ], alignment=ft.MainAxisAlignment.CENTER)
        return self.sql_status_indicator

    def _update_status_visual(self, connected: bool):
        if connected:
            self.sql_status_indicator.controls = [
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=PlatinumTheme.SUCCESS()), 
                ft.Text("Conectado", size=12, color=PlatinumTheme.SUCCESS())
            ]
        else:
            self.sql_status_indicator.controls = [
                ft.Icon(ft.Icons.CANCEL, color=PlatinumTheme.DANGER()), 
                ft.Text("Desconectado", size=12, color=PlatinumTheme.TEXT_MUTED())
            ]
        self.sql_status_indicator.update()

    def _on_source_type_change(self, e):
        new_type = list(e.data)[0] if isinstance(e.data, (set, list)) else e.data
        LoggerService().info(f"Fonte alterada: {new_type}")
        self.state.set_source_type(new_type)
        
        # Reset visual
        self.controls[3] = self._build_file_section() if new_type == "local_file" else self._build_sql_section()
        self.btn_next.disabled = True # Forçar bloqueio no switch
        self.update()

    def _on_sql_field_change(self, field, value):
        if field == "password":
            self.state.source_config_runtime["password"] = value
        else:
            self.state.source_config_safe[field] = value
        
        # Reset ao mudar campos
        self.state.is_source_valid = False
        self.state.is_connected = False
        self._validate_next_button()
        self.update()

    def _on_sql_test_click(self, e):
        try:
            # Fundir configs (Runtime + Safe) SEM logs sensíveis
            config = {**self.state.source_config_safe, **self.state.source_config_runtime}
            LoggerService().info(f"Testando conexão SQL (Host: {config.get('host')})")
            
            connector = ConnectorFactory.get_connector("sql_db", config)
            if connector.validate_connection():
                self.state.connector = connector
                self.state.is_connected = True
                
                # Discovery: Buscar tabelas
                tables = connector.fetch_metadata()
                self._update_status_visual(True)
                self._update_sheet_dropdown(self.src_sheet_dropdown, tables, None, "src")
                self.src_sheet_dropdown.label = "SELECIONAR TABELA (SQL)"
                
                sb = ft.SnackBar(ft.Text("✅ Conexão SQL estabelecida com sucesso!"), bgcolor=PlatinumTheme.SUCCESS())
                self.page.overlay.append(sb)
                sb.open = True
            else:
                self.state.is_connected = False
                self.state.is_source_valid = False
                self._update_status_visual(False)
                sb = ft.SnackBar(ft.Text("❌ Falha na conexão SQL. Verifique as credenciais."), bgcolor=PlatinumTheme.DANGER())
                self.page.overlay.append(sb)
                sb.open = True
            
            self._validate_next_button()
            self.page.update()
        except Exception as ex:
            # Sanitização: Remover detalhes de credenciais do erro
            error_msg = str(ex).replace(self.state.source_config_runtime.get("password", "###"), "***")
            LoggerService().error(f"Erro no teste SQL: {error_msg}")
            sb = ft.SnackBar(ft.Text(f"Erro: {error_msg[:100]}..."), bgcolor=PlatinumTheme.DANGER())
            self.page.overlay.append(sb)
            sb.open = True
            self.update()

    def _trigger_picker(self, mode):
        """Fallback Robusto: Usa Tkinter se o FilePicker do Flet falhar."""
        try:
            LoggerService().info(f"Abrindo seletor nativo (Tkinter) para: {mode}")
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True) # Garante que a janela fique na frente
            file_path = filedialog.askopenfilename(
                title=f"Selecionar Arquivo de {'ORIGEM' if mode == 'src' else 'DESTINO'}",
                filetypes=[("Arquivos Excel", "*.xlsx *.xls"), ("Todos os arquivos", "*.*")]
            )
            root.destroy()
            
            if file_path:
                self.update_file(mode, file_path)
        except Exception as e:
            LoggerService().error(f"Erro no seletor Tkinter: {e}")
            # Se até o Tkinter falhar, o usuário ainda tem o campo manual
            self.on_pick_file(mode) 

    def _on_suggest_click(self, e):
        src, tgt = self.suggester.suggest_files()
        if src: self.update_file("src", src)
        if tgt: self.update_file("tgt", tgt)
        
        if src or tgt:
            sb = ft.SnackBar(ft.Text("🤖 Arquivos sugeridos com sucesso!"), bgcolor=PlatinumTheme.SUCCESS())
            self.page.overlay.append(sb)
            sb.open = True
            self.page.update()

    def _on_manual_path(self, mode, value):
        LoggerService().info(f"Tentando carga manual: {mode} -> {value}")
        if os.path.exists(value):
            self.update_file(mode, value)
        else:
            LoggerService().error(f"Arquivo não encontrado: {value}")

    def update_file(self, mode, path):
        try:
            workbook, headers = self.loader.load_workbook(path)
            
            # Treinamento Passivo — LearningLogger aponta para brains/
            ll = LearningLogger(BRAINS_DIR)
            ll.log_workbook_structure(workbook)

            if mode == "src":
                self.state.workbook_src = workbook
                self.state.path_src = path
                self.state.selected_sheet_src = list(workbook.keys())[0]
                self.state.df_src = workbook[self.state.selected_sheet_src]
                
                self._update_sheet_dropdown(self.src_sheet_dropdown, list(workbook.keys()), self.state.selected_sheet_src, "src")
                
                self.src_info.value = f"✅ {os.path.basename(path)}\n{len(self.state.df_src)} linhas | Aba: {self.state.selected_sheet_src}"
                self.src_info.color = PlatinumTheme.SUCCESS()
                self.src_path_field.value = path
            else:
                self.state.workbook_tgt = workbook
                self.state.path_tgt = path
                self.state.selected_sheet_tgt = list(workbook.keys())[0]
                self.state.df_tgt = workbook[self.state.selected_sheet_tgt]
                
                # Configurar Dropdown
                self._update_sheet_dropdown(self.tgt_sheet_dropdown, list(workbook.keys()), self.state.selected_sheet_tgt, "tgt")
                
                self.tgt_info.value = f"✅ {os.path.basename(path)}\n{len(self.state.df_tgt)} linhas | Aba: {self.state.selected_sheet_tgt}"
                self.tgt_info.color = PlatinumTheme.SUCCESS()
                self.tgt_path_field.value = path
            
            LoggerService().info(f"Workbook {mode} carregado ({len(workbook)} abas).")
            
            self._validate_next_button()
            self.update()
        except Exception as e:
            LoggerService().error(f"Erro ao carregar {path}: {e}")
            sb = ft.SnackBar(ft.Text(f"Erro ao carregar arquivo: {e}"), bgcolor=PlatinumTheme.DANGER())
            self.page.overlay.append(sb)
            sb.open = True
            self.page.update()

    def _update_sheet_dropdown(self, dropdown, options, selected, mode):
        if options:
            dropdown.visible = True
            dropdown.options = [ft.dropdown.Option(opt) for opt in options]
            dropdown.value = selected
            dropdown.on_change = lambda e: self._on_sheet_change(mode, e.data)
        else:
            dropdown.visible = False
            self.state.is_source_valid = False
        
        self._validate_next_button()
        self.update()

    def _on_sheet_change(self, mode, sheet_name):
        LoggerService().info(f"Alterada aba ativa: {mode} -> {sheet_name}")
        if mode == "src":
            self.state.selected_sheet_src = sheet_name
            
            if self.state.source_type == "sql_db":
                # CARGA DE PREVIEW (Contrato Fase 3: Max 100 linhas)
                try:
                    self.state.sql_selection["table"] = sheet_name
                    df_preview = self.state.connector.preview(table=sheet_name, limit=100)
                    self.state.df_src = df_preview
                    self.src_info.value = f"✅ SQL: {sheet_name}\nPreview: {len(df_preview)} linhas carregadas"
                    self.src_info.color = PlatinumTheme.SUCCESS()
                    self.state.is_source_valid = True
                except Exception as e:
                    LoggerService().error(f"Erro ao carregar preview SQL: {str(e)[:50]}")
                    sb = ft.SnackBar(ft.Text(f"Erro no preview: {str(e)[:100]}"), bgcolor=PlatinumTheme.DANGER())
                    self.page.overlay.append(sb)
                    sb.open = True
            else:
                self.state.df_src = self.state.workbook_src[sheet_name]
                self.src_info.value = f"✅ {os.path.basename(self.state.path_src)}\n{len(self.state.df_src)} linhas | Aba: {sheet_name}"
        else:
            self.state.selected_sheet_tgt = sheet_name
            self.state.df_tgt = self.state.workbook_tgt[sheet_name]
            self.tgt_info.value = f"✅ {os.path.basename(self.state.path_tgt)}\n{len(self.state.df_tgt)} linhas | Aba: {sheet_name}"
        
        # 3. Validar avanço
        self._validate_next_button()
        self.update()

    def _validate_next_button(self):
        """Validação Unificada: Estritamente baseada no tipo de fonte."""
        if self.state.source_type == "sql_db":
            # SQL requer Conexão + Tabela (df_src) + Destino (df_tgt)
            can_proceed = (
                self.state.is_connected and 
                self.state.sql_selection["table"] is not None and
                self.state.df_tgt is not None
            )
        else:
            # Excel requer Origem e Destino carregados
            can_proceed = (
                self.state.df_src is not None and 
                self.state.df_tgt is not None
            )
            
        self.btn_next.disabled = not can_proceed
        self.state.is_source_valid = can_proceed

    def _intercept_next(self, e):
        """Interceptador: Validação dinâmica por Source Type."""
        # 0. Validação de Segurança
        if self.state.source_type == "sql_db":
            if not self.state.is_connected or self.state.df_src is None or self.state.df_tgt is None:
                sb = ft.SnackBar(ft.Text("SQL: Conexão, Tabela e DESTINO são obrigatórios!"), bgcolor=PlatinumTheme.DANGER())
                self.page.overlay.append(sb)
                sb.open = True
                self.page.update()
                return
        else:
            if self.state.df_src is None or self.state.df_tgt is None:
                sb = ft.SnackBar(ft.Text("Arquivos de origem e destino são obrigatórios!"), bgcolor=PlatinumTheme.DANGER())
                self.page.overlay.append(sb)
                sb.open = True
                self.page.update()
                return

        # Orquestração de Sugestões
        src_cols = list(self.state.df_src.columns)
        tgt_cols = list(self.state.df_tgt.columns)
        
        smart = self.history_engine.get_smart_suggestions(src_cols, tgt_cols)
        
        key_src, key_tgt = self.lookup.suggest_key_pair(self.state.df_src, self.state.df_tgt)
        
        # Se for histórico, pode vir com as chaves também
        if smart["source"] == "history":
            h_keys = smart.get("keys", (None, None))
            if h_keys[0] and h_keys[1]:
                key_src, key_tgt = h_keys
        
        # 3. Popular Estado Sugerido
        # DEBUG LOG (Hardening)
        ls = LoggerService()
        ls.info(f"DEBUG TRANSITION STEP 1 -> 2")
        ls.info(f" - smart type: {type(smart)}")
        ls.info(f" - smart content: {smart}")
        ls.info(f" - key_src: {key_src} (type: {type(key_src)})")
        ls.info(f" - key_tgt: {key_tgt} (type: {type(key_tgt)})")

        v_src = self.validator.audit_dataframe(self.state.df_src)
        v_tgt = self.validator.audit_dataframe(self.state.df_tgt)
        self.state.validation_summary = {"src": v_src, "tgt": v_tgt}
        self.state.suggested_mapping = smart.get("mapping", {}) if isinstance(smart, dict) else {}
        self.state.suggested_source = smart.get("source", "none") if isinstance(smart, dict) else "none"
        self.state.suggested_key_src = key_src
        self.state.suggested_key_tgt = key_tgt
        
        # 4. Abrir Dialog
        def apply_and_next():
            # Consolida as sugestões no estado real ANTES de avançar
            self.state.mapping = self.state.suggested_mapping.copy()
            self.state.key_src = self.state.suggested_key_src
            self.state.key_tgt = self.state.suggested_key_tgt
            dialog.open = False
            self.page.update()
            self.on_next()

        def manual_and_next():
            dialog.open = False
            self.page.update()
            self.on_next()

        dialog = FileIntelligenceDialog(
            self.state, 
            on_apply=apply_and_next, 
            on_manual=manual_and_next
        )
        
        # Remove instâncias anteriores se houver
        to_remove = [ctrl for ctrl in self.page.overlay if isinstance(ctrl, FileIntelligenceDialog)]
        for ctrl in to_remove:
            self.page.overlay.remove(ctrl)
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Interface Legada - Passo 1: Seleção de Fontes e Heurística de Cabeçalho")
