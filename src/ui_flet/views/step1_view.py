import flet as ft
import os
import tkinter as tk
from tkinter import filedialog
from ui_flet.theme import PlatinumTheme
from core.engines.loader_engine import LoaderEngine
from core.engines.suggestion_engine import SuggestionEngine
from services.logger_service import LoggerService
from core.validation_engine import ValidationEngine
from core.lookup_engine import LookupEngine
from core.learning.suggestion_engine import HistoricalSuggestionEngine
from ui_flet.dialogs.file_intelligence_dialog import FileIntelligenceDialog

class Step1View(ft.Column):
    """
    PASSO 1: Seleção de Fontes (v0.6.0).
    Focada em clareza visual e heurística de cabeçalho.
    """
    def _on_card_hover(self, e):
        """Efeito Visual Platinum: Altera a borda no hover (v0.6.0)."""
        e.control.border = ft.border.all(1, PlatinumTheme.PRIMARY() if e.data == "true" else PlatinumTheme.BORDER_DARK())
        e.control.update()

    def __init__(self, state, on_next, on_pick_file):
        super().__init__(expand=True, spacing=20)
        self.state = state
        self.on_next = on_next
        self.on_pick_file = on_pick_file
        self.loader = LoaderEngine()
        self.suggester = SuggestionEngine()
        self.validator = ValidationEngine()
        self.lookup = LookupEngine()
        self.history_engine = HistoricalSuggestionEngine(os.getcwd())
        
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
            ft.Text("Seleção de Arquivos", size=24, weight=ft.FontWeight.W_600, color=PlatinumTheme.PRIMARY()),
            ft.ResponsiveRow([
                self._create_drop_zone("Planilha de ORIGEM", "src"),
                self._create_drop_zone("Planilha de DESTINO", "tgt"),
            ], spacing=20),
            ft.Row([
                ft.ElevatedButton(
                    "🤖 Sugerir Arquivos Recentes (Smart-Pull)", 
                    icon=ft.Icons.AUTO_AWESOME,
                    on_click=self._on_suggest_click,
                    bgcolor=PlatinumTheme.SURFACE_DARK(),
                    color=PlatinumTheme.PRIMARY()
                ),
                ft.Container(expand=True), 
                self.btn_next
            ], alignment=ft.MainAxisAlignment.END)
        ]

    def _create_drop_zone(self, title, mode):
        return ft.Container(
            **PlatinumTheme.card_style(),
            col={"sm": 12, "md": 6},
            on_click=lambda _: self._trigger_picker(mode),
            on_hover=self._on_card_hover,
            content=ft.Column([
                ft.Text(title, weight=ft.FontWeight.BOLD, size=16, color=PlatinumTheme.TEXT_PRIMARY()),
                ft.Divider(color=PlatinumTheme.BORDER_DARK()),
                ft.Icon(PlatinumTheme.Icons.FILE_SOURCE if mode == "src" else PlatinumTheme.Icons.FILE_TARGET, size=50, color=PlatinumTheme.PRIMARY()),
                self.src_info if mode == "src" else self.tgt_info,
                ft.Text("Clique aqui ou arraste o arquivo", size=12, italic=True, color=PlatinumTheme.TEXT_MUTED()),
                ft.Container(height=10),
                ft.Row([
                    self.src_path_field if mode == "src" else self.tgt_path_field,
                    ft.IconButton(
                        PlatinumTheme.Icons.CHECK,
                        icon_color=PlatinumTheme.SUCCESS(),
                        on_click=lambda _: self._on_manual_path(mode, (self.src_path_field.value if mode == "src" else self.tgt_path_field.value)),
                        tooltip="Validar Caminho Manual"
                    )
                ])
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def _trigger_picker(self, mode):
        """Fallback Robusto v0.6.0: Usa Tkinter se o FilePicker do Flet falhar."""
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
            df, skip = self.loader.load_excel(path)
            if mode == "src":
                self.state.df_src = df
                self.state.path_src = path
                self.src_info.value = f"✅ {os.path.basename(path)}\n{len(df)} linhas | Cabeçalho: {skip}"
                self.src_info.color = PlatinumTheme.SUCCESS()
                self.src_path_field.value = path
            else:
                self.state.df_tgt = df
                self.state.path_tgt = path
                self.tgt_info.value = f"✅ {os.path.basename(path)}\n{len(df)} linhas | Cabeçalho: {skip}"
                self.tgt_info.color = PlatinumTheme.SUCCESS()
                self.tgt_path_field.value = path
            
            LoggerService().info(f"Arquivo {mode} carregado: {len(df)} linhas.")
            
            if self.state.df_src is not None and self.state.df_tgt is not None:
                LoggerService().info("Ambos os arquivos carregados. Habilitando botão 'Próximo'.")
                self.btn_next.disabled = False
            
            self.update()
        except Exception as e:
            sb = ft.SnackBar(ft.Text(f"Erro ao carregar arquivo: {e}"), bgcolor=PlatinumTheme.DANGER())
            self.page.overlay.append(sb)
            sb.open = True
            self.page.update()

    def _intercept_next(self, e):
        """Interceptador v0.6.3: Realiza pré-análise antes de avançar."""
        # 0. Guarda Defensiva (Hardening Patch 2)
        if self.state.df_src is None or self.state.df_tgt is None:
            LoggerService().error("Tentativa de avanço sem arquivos carregados.")
            sb = ft.SnackBar(ft.Text("Ambos os arquivos precisam ser carregados para análise!"), bgcolor=PlatinumTheme.DANGER())
            self.page.overlay.append(sb)
            sb.open = True
            self.page.update()
            return

        LoggerService().info("Iniciando pré-análise v0.6.3...")
        
        # 1. Executar Motores (Análise Leve)
        v_src = self.validator.audit_dataframe(self.state.df_src)
        v_tgt = self.validator.audit_dataframe(self.state.df_tgt)
        
        common_cols = self.lookup.find_common_columns(self.state.df_src, self.state.df_tgt)
        
        # 2. Orquestração de Sugestões (v0.6.3 Patch 4)
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
        self.state.validation_summary = {"src": v_src, "tgt": v_tgt}
        self.state.suggested_mapping = smart["mapping"] if smart["mapping"] else {col: col for col in common_cols}
        self.state.suggested_source = smart["source"]
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
