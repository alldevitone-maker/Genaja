import flet as ft
import asyncio
import os
import tkinter as tk
from tkinter import filedialog

from ui_flet.theme import PlatinumTheme
from ui_flet.views.base_view import RoutedViewMixin
from core.services.config_service import ConfigService


class PriceSyncView(ft.Container, RoutedViewMixin):

    def __init__(self, state, router):
        ft.Container.__init__(self)
        self.state = state
        self.router = router
        self._config = ConfigService()

        # Paths e metadados carregados
        self._path_origem = None
        self._path_destino = None
        self._wb_orig = {}     # {sheet_name: df}
        self._wb_dest = {}
        self._sheet_orig = None
        self._sheet_dest = None

        # Chaves alternativas (lista de tuplas adicionadas pelo operador)
        self._chaves_alternativas = []

        # ── ETAPA 1: Seletores de Arquivo ──────────────────────────────
        self.lbl_orig = ft.Text("Nenhum arquivo selecionado", size=12,
                                italic=True, color=PlatinumTheme.TEXT_MUTED())
        self.btn_orig = ft.ElevatedButton(
            "① Tabela de Preços (Origem)",
            icon=ft.Icons.TABLE_CHART_OUTLINED,
            on_click=self._pick_origem
        )
        self.drop_sheet_orig = ft.Dropdown(
            label="Aba da Origem", options=[], width=200,
            visible=False,
            border_color="#333333", focused_border_color=PlatinumTheme.PRIMARY()
        )
        self.drop_sheet_orig.on_change = self._on_sheet_orig_change

        self.lbl_dest = ft.Text("Nenhum arquivo selecionado", size=12,
                                italic=True, color=PlatinumTheme.TEXT_MUTED())
        self.btn_dest = ft.ElevatedButton(
            "② Arquivo Destino",
            icon=ft.Icons.UPLOAD_FILE_OUTLINED,
            on_click=self._pick_destino
        )
        self.drop_sheet_dest = ft.Dropdown(
            label="Aba do Destino", options=[], width=200,
            visible=False,
            border_color="#333333", focused_border_color=ft.Colors.AMBER_400
        )
        self.drop_sheet_dest.on_change = self._on_sheet_dest_change

        # ── ETAPA 2: Mapeamento de Colunas ─────────────────────────────
        self.drop_chave_orig = ft.Dropdown(
            label="Coluna Chave (Código)", options=[], width=260,
            visible=False, border_color="#333333",
            focused_border_color=PlatinumTheme.PRIMARY()
        )
        self.drop_valor_orig = ft.Dropdown(
            label="Coluna de Preço", options=[], width=260,
            visible=False, border_color="#333333",
            focused_border_color=PlatinumTheme.PRIMARY()
        )
        self.drop_chave_dest = ft.Dropdown(
            label="Coluna Chave (Código)", options=[], width=260,
            visible=False, border_color="#333333",
            focused_border_color=ft.Colors.AMBER_400
        )
        self.drop_col_preencher = ft.Dropdown(
            label="Coluna a Preencher (Preço)", options=[], width=260,
            visible=False, border_color="#333333",
            focused_border_color=ft.Colors.AMBER_400
        )

        self.lbl_validacao = ft.Text("", size=12, color=ft.Colors.ORANGE_400, visible=False)
        self.btn_add_chave = ft.TextButton(
            "+ Adicionar Chave Alternativa (fallback)",
            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
            on_click=self._add_chave_alt,
            visible=False
        )
        self.col_chaves_alt = ft.Column([], spacing=8, visible=False)

        # ── ETAPA 3: Live Preview ───────────────────────────────────────
        self.preview_orig_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("..."))],
            rows=[], heading_row_color=ft.Colors.with_opacity(0.1, PlatinumTheme.PRIMARY()),
            border=ft.border.all(1, PlatinumTheme.BORDER_DARK()),
        )
        self.preview_dest_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("..."))],
            rows=[], heading_row_color=ft.Colors.with_opacity(0.1, ft.Colors.AMBER_400),
            border=ft.border.all(1, PlatinumTheme.BORDER_DARK()),
        )
        self.card_preview = ft.Card(content=ft.Container(
            content=ft.Column([
                ft.Text("PREVIEW — Amostra (5 linhas)", weight="bold",
                        color=PlatinumTheme.PRIMARY(), size=12),
                ft.Row([
                    ft.Column([
                        ft.Text("ORIGEM", size=11, color=PlatinumTheme.PRIMARY()),
                        ft.Row([self.preview_orig_table], scroll=ft.ScrollMode.ADAPTIVE)
                    ], expand=True),
                    ft.VerticalDivider(width=1, color=PlatinumTheme.BORDER_DARK()),
                    ft.Column([
                        ft.Text("DESTINO", size=11, color=ft.Colors.AMBER_400),
                        ft.Row([self.preview_dest_table], scroll=ft.ScrollMode.ADAPTIVE)
                    ], expand=True),
                ], spacing=10),
            ], spacing=10),
            **PlatinumTheme.card_style()
        ), visible=False)

        # ── ETAPA 4: Execução e Resultado ──────────────────────────────
        self.lbl_status = ft.Text(
            "Selecione os arquivos e configure as colunas.",
            size=14, weight="bold"
        )
        self.progress = ft.ProgressBar(visible=False, color=PlatinumTheme.PRIMARY())
        self.col_passes = ft.Column([], spacing=6, visible=False)

        self.btn_executar = ft.ElevatedButton(
            "EXECUTAR PRICE SYNC",
            icon=ft.Icons.SYNC_ALT_ROUNDED,
            on_click=self._executar,
            disabled=True, height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
        self.btn_abrir_pasta = ft.ElevatedButton(
            "Abrir Pasta do Resultado",
            icon=ft.Icons.FOLDER_OPEN,
            visible=False, on_click=self._abrir_pasta
        )
        self.btn_back = ft.OutlinedButton(
            "Voltar", on_click=lambda _: self.router.navigate("intent_router")
        )

        # ── LAYOUT FINAL ───────────────────────────────────────────────
        self.content = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.CURRENCY_EXCHANGE, color=ft.Colors.AMBER_400, size=28),
                ft.Text("PRICE SYNC", size=26, weight="bold"),
                ft.Text("v0.7.1 — Multi-Chave · Live Preview · IEEE 754 Fix",
                        size=11, color=PlatinumTheme.TEXT_MUTED(), italic=True),
            ], alignment="center", spacing=12),

            # Card Origem
            ft.Card(content=ft.Container(content=ft.Column([
                ft.Text("① TABELA DE PREÇOS (Origem)", weight="bold",
                        color=PlatinumTheme.PRIMARY()),
                ft.Row([self.btn_orig, self.drop_sheet_orig], spacing=15, wrap=True),
                self.lbl_orig,
                ft.Row([self.drop_chave_orig, self.drop_valor_orig], spacing=15, wrap=True),
            ], spacing=10), **PlatinumTheme.card_style())),

            # Card Destino
            ft.Card(content=ft.Container(content=ft.Column([
                ft.Text("② ARQUIVO DESTINO", weight="bold", color=ft.Colors.AMBER_400),
                ft.Row([self.btn_dest, self.drop_sheet_dest], spacing=15, wrap=True),
                self.lbl_dest,
                ft.Row([self.drop_chave_dest, self.drop_col_preencher], spacing=15, wrap=True),
            ], spacing=10), **PlatinumTheme.card_style())),

            # Chaves alternativas
            ft.Card(content=ft.Container(content=ft.Column([
                ft.Text("Chaves de Fallback (opcional)", weight="bold",
                        color=PlatinumTheme.TEXT_MUTED(), size=12),
                self.lbl_validacao,
                self.col_chaves_alt,
                self.btn_add_chave,
            ], spacing=8), **PlatinumTheme.card_style()), visible=False,
            ref=ft.Ref()),

            # Live Preview
            self.card_preview,

            ft.Divider(height=1, color=PlatinumTheme.BORDER_DARK()),
            self.lbl_status,
            self.progress,
            self.col_passes,
            ft.Row([self.btn_executar, self.btn_abrir_pasta], spacing=15,
                   alignment="center", wrap=True),
            ft.Container(height=8),
            self.btn_back,
        ], horizontal_alignment="center", spacing=18,
           scroll=ft.ScrollMode.AUTO)

        self.padding = 40
        self.alignment = ft.Alignment(0, 0)
        self._card_alt = self.content.controls[3]

    # ── Contrato RoutedViewMixin ────────────────────────────────────────
    def on_route_mounted(self):
        """Ao montar: resetar estado e (futuro) pré-sugerir arquivos recentes."""
        pass

    # ── Seleção de Arquivo ──────────────────────────────────────────────
    def _pick_origem(self, e):
        path = self._abrir_dialogo("Tabela de Preços (Origem)")
        if not path:
            return
        self._path_origem = path
        self._carregar_workbook(path, lado="orig")

    def _pick_destino(self, e):
        path = self._abrir_dialogo("Arquivo Destino")
        if not path:
            return
        self._path_destino = path
        self._carregar_workbook(path, lado="dest")

    def _abrir_dialogo(self, titulo: str) -> str:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askopenfilename(
            title=f"Selecionar: {titulo}",
            filetypes=[("Planilhas", "*.xlsx;*.xls;*.csv"), ("Todos", "*.*")]
        )
        root.destroy()
        return path

    def _carregar_workbook(self, path: str, lado: str):
        """Carrega via LoaderEngine — multi-aba, multi-encoding, robusto."""
        from core.engines.loader_engine import LoaderEngine
        try:
            loader = LoaderEngine()
            wb, _ = loader.load_workbook(path)
        except Exception as ex:
            self._set_status(f"Erro ao carregar arquivo: {ex}", ft.Colors.RED_400)
            return

        abas = list(wb.keys())

        if lado == "orig":
            self._wb_orig = wb
            self._sheet_orig = abas[0]
            self.lbl_orig.value = os.path.basename(path)
            self.lbl_orig.color = ft.Colors.GREEN_400
            self._preencher_drop_abas(self.drop_sheet_orig, abas)
            self._popular_colunas_orig(abas[0])

        else:
            self._wb_dest = wb
            self._sheet_dest = abas[0]
            self.lbl_dest.value = os.path.basename(path)
            self.lbl_dest.color = ft.Colors.AMBER_400
            self._preencher_drop_abas(self.drop_sheet_dest, abas)
            self._popular_colunas_dest(abas[0])

        self._checar_pronto()
        self.update()

    def _preencher_drop_abas(self, drop: ft.Dropdown, abas: list):
        drop.options = [ft.dropdown.Option(a, a) for a in abas]
        drop.value = abas[0]
        drop.visible = len(abas) > 1  # Só aparece se há múltiplas abas

    def _on_sheet_orig_change(self, e):
        self._sheet_orig = e.control.value
        self._popular_colunas_orig(self._sheet_orig)
        self._checar_pronto()
        self.update()

    def _on_sheet_dest_change(self, e):
        self._sheet_dest = e.control.value
        self._popular_colunas_dest(self._sheet_dest)
        self._checar_pronto()
        self.update()

    def _popular_colunas_orig(self, sheet: str):
        df = self._wb_orig.get(sheet)
        if df is None:
            return
        cols = list(df.columns)
        self._preencher_dropdown(self.drop_chave_orig, cols)
        self._preencher_dropdown(self.drop_valor_orig, cols)
        self.drop_chave_orig.visible = True
        self.drop_valor_orig.visible = True
        # Auto-sugestão via MappingEngine (se destino já carregado)
        self._auto_sugerir()

    def _popular_colunas_dest(self, sheet: str):
        df = self._wb_dest.get(sheet)
        if df is None:
            return
        cols = list(df.columns)
        self._preencher_dropdown(self.drop_chave_dest, cols)
        self._preencher_dropdown(self.drop_col_preencher, cols)
        self.drop_chave_dest.visible = True
        self.drop_col_preencher.visible = True
        self._auto_sugerir()

    def _auto_sugerir(self):
        """Usa MappingEngine para sugerir o melhor par de chaves por dados."""
        df_o = self._wb_orig.get(self._sheet_orig)
        df_d = self._wb_dest.get(self._sheet_dest)
        if df_o is None or df_d is None:
            return
        try:
            from core.engines.mapping_engine import MappingEngine
            mg = MappingEngine()
            sugestoes = mg.suggest_primary_keys(df_o, df_d, sample_size=500)
            if sugestoes:
                melhor = sugestoes[0]
                if not self.drop_chave_orig.value:
                    self.drop_chave_orig.value = melhor["src"]
                if not self.drop_chave_dest.value:
                    self.drop_chave_dest.value = melhor["tgt"]
        except Exception:
            pass  # Sugestão opcional — falha silenciosa

    def _preencher_dropdown(self, drop: ft.Dropdown, cols: list):
        drop.options = [ft.dropdown.Option(c, c) for c in cols]
        drop.value = None

    # ── Chaves Alternativas ─────────────────────────────────────────────
    def _add_chave_alt(self, e):
        df_o = self._wb_orig.get(self._sheet_orig)
        df_d = self._wb_dest.get(self._sheet_dest)
        if df_o is None or df_d is None:
            return

        cols_o = list(df_o.columns)
        cols_d = list(df_d.columns)
        idx = len(self._chaves_alternativas)

        drop_d = ft.Dropdown(
            label=f"Chave Destino #{idx+1}", options=[ft.dropdown.Option(c, c) for c in cols_d],
            width=230, border_color="#333333"
        )
        drop_o = ft.Dropdown(
            label=f"Chave Origem #{idx+1}", options=[ft.dropdown.Option(c, c) for c in cols_o],
            width=230, border_color="#333333"
        )
        self._chaves_alternativas.append((drop_d, drop_o))
        self.col_chaves_alt.controls.append(
            ft.Row([drop_d, drop_o], spacing=12)
        )
        self.col_chaves_alt.visible = True
        if len(self._chaves_alternativas) >= 3:
            self.btn_add_chave.visible = False
        self.update()

    # ── Validação e Preview ─────────────────────────────────────────────
    def _checar_pronto(self):
        pronto = bool(self._wb_orig and self._wb_dest)
        self.btn_executar.disabled = not pronto
        self._card_alt.visible = pronto
        self.btn_add_chave.visible = pronto

        if pronto:
            self._set_status("Pronto! Configure as colunas e clique em Executar.",
                             ft.Colors.GREEN_400)
            self._validar_chaves()
            self._atualizar_preview()

    def _validar_chaves(self):
        """ValidationEngine: alerta se chave tem duplicatas (Shift-Left Validation)."""
        col_k_o = self.drop_chave_orig.value
        col_k_d = self.drop_chave_dest.value
        df_o = self._wb_orig.get(self._sheet_orig)
        df_d = self._wb_dest.get(self._sheet_dest)
        if not all([col_k_o, col_k_d, df_o is not None, df_d is not None]):
            return
        try:
            from core.engines.validation_engine import ValidationEngine
            ve = ValidationEngine()
            rep_o = ve.validate_keys(df_o, [col_k_o])
            rep_d = ve.validate_keys(df_d, [col_k_d])
            avisos = rep_o["errors"] + rep_d["errors"]
            if avisos:
                self.lbl_validacao.value = "⚠️ " + " | ".join(avisos)
                self.lbl_validacao.visible = True
            else:
                self.lbl_validacao.visible = False
        except Exception:
            pass

    def _atualizar_preview(self):
        """Mostra 5 linhas de cada arquivo para validação visual antes de executar."""
        df_o = self._wb_orig.get(self._sheet_orig)
        df_d = self._wb_dest.get(self._sheet_dest)
        if df_o is None or df_d is None:
            return
        try:
            self._preencher_preview_table(self.preview_orig_table, df_o.head(5))
            self._preencher_preview_table(self.preview_dest_table, df_d.head(5))
            self.card_preview.visible = True
        except Exception:
            pass

    def _preencher_preview_table(self, table: ft.DataTable, df):
        cols = list(df.columns)[:6]  # máx 6 colunas para não explodir o layout
        table.columns = [ft.DataColumn(ft.Text(str(c), size=10, weight="bold")) for c in cols]
        table.rows = []
        for _, row in df[cols].iterrows():
            cells = [ft.DataCell(ft.Text(str(row[c])[:30], size=10)) for c in cols]
            table.rows.append(ft.DataRow(cells=cells))

    # ── Execução ────────────────────────────────────────────────────────
    async def _executar(self, e):
        col_chave_orig = self.drop_chave_orig.value
        col_valor_orig = self.drop_valor_orig.value
        col_chave_dest = self.drop_chave_dest.value
        col_preencher = self.drop_col_preencher.value

        if not all([col_chave_orig, col_valor_orig, col_chave_dest, col_preencher]):
            self._set_status("⚠️ Configure todas as 4 colunas antes de executar.",
                             ft.Colors.ORANGE_400)
            self.update()
            return

        # Montar lista de chaves alternativas configuradas
        chaves_alt = []
        for (dr_d, dr_o) in self._chaves_alternativas:
            if dr_d.value and dr_o.value:
                chaves_alt.append((dr_d.value, dr_o.value))

        # Pasta de saída via ConfigService
        config_dir = self._config.get_config("general", "default_export_dir") or ""
        out_path = None
        if config_dir and os.path.isdir(config_dir):
            base = os.path.splitext(os.path.basename(self._path_destino))[0]
            out_path = os.path.join(config_dir, base + "_SYNC.xlsx")

        self.btn_executar.disabled = True
        self.progress.visible = True
        self.col_passes.visible = False
        self._set_status("Executando Price Sync...", ft.Colors.BLUE_400)
        self.update()

        from core.engines.transform_engine import TransformEngine
        operator = self._config.get_config("general", "operator_name") or "Genaja"

        try:
            res = await asyncio.to_thread(
                TransformEngine.price_sync_join,
                self._path_origem,
                self._path_destino,
                col_chave_orig,
                col_valor_orig,
                col_chave_dest,
                col_preencher,
                chaves_alt or None,
                self._sheet_orig or 0,
                self._sheet_dest or 0,
                out_path,
                operator,
            )
        except Exception as ex:
            res = {"success": False, "warnings": [str(ex)],
                   "matched_total": 0, "unmatched": 0, "passes": []}

        self.progress.visible = False
        self.btn_executar.disabled = False

        if res.get("success"):
            self._ultimo_out = res.get("output_path", "")
            matched = res.get("matched_total", 0)
            unmatched = res.get("unmatched", 0)
            total = matched + unmatched

            self._set_status(
                f"Concluído! {matched:,} preços sincronizados | "
                f"{unmatched:,} sem match | "
                f"{matched/total*100:.1f}% de cobertura",
                ft.Colors.GREEN_400
            )
            self.btn_abrir_pasta.visible = True

            # Relatório por passe
            self.col_passes.controls.clear()
            for p in res.get("passes", []):
                self.col_passes.controls.append(ft.Text(
                    f"  • {p['chave_dest']} ↔ {p['chave_orig']}: {p['matches']:,} matches",
                    size=12, color=PlatinumTheme.TEXT_MUTED()
                ))
            if self.col_passes.controls:
                self.col_passes.visible = True

            for w in res.get("warnings", []):
                self.col_passes.controls.append(
                    ft.Text(f"  ⚠️ {w}", size=11, color=ft.Colors.ORANGE_400)
                )
        else:
            erros = res.get("warnings", ["Erro desconhecido"])
            self._set_status(f"Falha: {erros[0]}", ft.Colors.RED_400)

        self.update()

    def _set_status(self, msg: str, color=None):
        self.lbl_status.value = msg
        if color:
            self.lbl_status.color = color

    def _abrir_pasta(self, e):
        import platform
        pasta = os.path.dirname(self._ultimo_out)
        if platform.system() == "Windows" and os.path.isdir(pasta):
            os.startfile(pasta)
