import flet as ft
from ui_flet.theme import PlatinumTheme
from version import __version__

class ResultCard(ft.Container):
    """
    Card de Resultado Inteligente (v0.7.3).
    Representa uma sessão de extração única e consolidada.
    """
    def __init__(self, col_id, col_mvf, count, on_curadoria, on_export_primary, on_export_contacts, on_consolidar=None, metrics=None):
        super().__init__()
        self.col_id = col_id
        self.col_mvf = col_mvf
        self.count = count
        self.metrics = metrics
        
        # Estilização Platinum
        self.padding = 15
        self.border_radius = 12
        self.bgcolor = ft.Colors.with_opacity(0.03, PlatinumTheme.PRIMARY())
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.1, PlatinumTheme.BORDER_DARK()))
        
        # Referências de Botões (v0.7.2 Resiliente)
        self.btn_curadoria = ft.ElevatedButton(
            "Curadoria Visual", 
            icon=ft.Icons.DRAG_INDICATOR, 
            on_click=on_curadoria, 
            bgcolor=ft.Colors.ORANGE_900, 
            color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
        )
        
        self.btn_mestre = ft.ElevatedButton(
            "Mestre (1:1)", 
            icon=ft.Icons.SAVE_ALT, 
            on_click=on_export_primary, 
            bgcolor=ft.Colors.GREEN_900, 
            color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
        )
        
        self.btn_contatos = ft.ElevatedButton(
            "Contatos (1:N)", 
            icon=ft.Icons.CONTACT_PAGE, 
            on_click=on_export_contacts, 
            bgcolor=ft.Colors.BLUE_900, 
            color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
        )
        
        # 💎 Consolidador Power Query HUD (v0.7.3)
        self.btn_consolidar = ft.ElevatedButton(
            "Consolidar Roles",
            icon=ft.Icons.SUBDIRECTORY_ARROW_RIGHT_ROUNDED,
            on_click=on_consolidar,
            bgcolor=PlatinumTheme.PRIMARY(),
            color="white",
            disabled=(on_consolidar is None),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
        )
        
        self.content = self._build()

    def update_count(self, new_count):
        """Atualiza o contador quando o mesmo split é reprocessado."""
        self.count = new_count
        self.lbl_count.value = f"📊 {new_count} registros extraídos"
        self.update()

    def update_actions(self, on_curadoria, on_export_primary, on_export_contacts, on_consolidar=None, metrics=None):
        """Atualiza os callbacks de clique fisicamente nos botões."""
        self.btn_curadoria.on_click = on_curadoria
        self.btn_mestre.on_click = on_export_primary
        self.btn_contatos.on_click = on_export_contacts
        if on_consolidar:
            self.btn_consolidar.on_click = on_consolidar
            self.btn_consolidar.disabled = False
        if metrics:
            self.metrics = metrics
            self.content = self._build()
        self.update()

    def _build(self):
        self.lbl_count = ft.Text(f"📊 {self.count} registros extraídos", size=12, color=PlatinumTheme.TEXT_SECONDARY())
        
        layout = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.GREEN_400, size=20),
                ft.Column([
                    ft.Text(f"Sessão: {self.col_id} ➔ {self.col_mvf}", weight="bold", size=14, color=PlatinumTheme.PRIMARY()),
                    self.lbl_count
                ], spacing=2, expand=True),
                ft.IconButton(ft.Icons.AUTO_FIX_HIGH, tooltip="Purificar com MDM Intelligent", icon_color=PlatinumTheme.PRIMARY())
            ], alignment="spaceBetween"),
            
            ft.Divider(height=1, color=ft.Colors.with_opacity(0.05, PlatinumTheme.BORDER_DARK())),
            
            ft.Row([
                self.btn_curadoria,
                self.btn_mestre,
                self.btn_contatos,
                self.btn_consolidar
            ], alignment="start", spacing=10)
        ], spacing=12)
        
        if self.metrics:
            b_rows = self.metrics.get("before", {}).get("rows", 0)
            a_rows = self.metrics.get("after", {}).get("rows", 0)
            c_count = self.metrics.get("contacts", {}).get("count", 0)
            deep = self.metrics.get("deep_audit", {})
            
            s_tokens = deep.get("source_tokens", 0)
            d_tokens = deep.get("dest_tokens", 0)
            dirty = deep.get("dirty_tokens", 0)
            null_hooks = deep.get("nulls", 0)
            samples = deep.get("samples", {})
            g_samples = samples.get("genuino", [])
            s_samples = samples.get("suspeito", [])
            
            loss = b_rows - a_rows
            
            is_perfect = loss == 0
            is_clean = dirty == 0
            
            icon_pres = ft.Icons.SHIELD_ROUNDED if is_perfect else ft.Icons.WARNING_AMBER_ROUNDED
            color_pres = PlatinumTheme.SUCCESS() if is_perfect else PlatinumTheme.WARNING()
            
            icon_token = ft.Icons.CHECK_CIRCLE_OUTLINE if is_clean else ft.Icons.FLAKY_ROUNDED
            color_token = PlatinumTheme.SUCCESS() if is_clean else PlatinumTheme.WARNING()

            audit_panel = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Row([
                                ft.Text("📊 DEEP AUDIT & RAIO-X DE INTEGRIDADE (1:N)", size=11, weight="bold", color=PlatinumTheme.TEXT_MUTED(), expand=True),
                            ]),
                            
                            # Linha 1: PK x PK
                            ft.Row([
                                ft.Icon(icon_pres, color=color_pres, size=16),
                                ft.Text(f"PK x PK: {b_rows} Origem ➔ {a_rows} Mestre (100% Match)", size=12, color=color_pres) if is_perfect else \
                                ft.Text(f"HEMORRAGIA PK: {loss} Registros sumiram!", size=12, color=color_pres)
                            ], spacing=10),
                            
                            # Linha 2: Fragmentos vs Destino
                            ft.Row([
                                ft.Icon(icon_token, color=color_token, size=16),
                                ft.Text(f"Genuínos: {d_tokens} (Verificados)", size=12, color=PlatinumTheme.SUCCESS()),
                                ft.Text(f" | ", color=PlatinumTheme.BORDER_DARK()),
                                ft.Text(f"Suspeitos: {dirty} (Erros/Lixo)", size=12, color=PlatinumTheme.WARNING())
                            ], spacing=10),
                            
                            # Linha 3: Total e Hooks
                            ft.Row([
                                ft.Icon(ft.Icons.ANCHOR_ROUNDED, color=ft.Colors.PURPLE_400, size=16),
                                ft.Text(f"Total Fragmentos: {s_tokens} | Hooks Nulos: {null_hooks}", size=12, color=ft.Colors.PURPLE_400)
                            ], spacing=10),
                        ], spacing=8, expand=True),

                        # Botão Lupa - Inspecionar Profundidade
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.SUBDIRECTORY_ARROW_RIGHT_ROUNDED,
                                tooltip="Inspecionar Amostras Reais (CTO Vision)",
                                icon_color=PlatinumTheme.PRIMARY(),
                                icon_size=28,
                                on_click=lambda _: self._show_inspector_dialog(self.metrics)
                            ),
                            alignment=ft.Alignment(0, 0),
                            padding=ft.padding.only(left=20)
                        )
                    ], vertical_alignment="center")
                ], spacing=8),
                padding=15,
                bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
                border=ft.border.all(1, ft.Colors.with_opacity(0.1, PlatinumTheme.BORDER_DARK())),
                border_radius=10,
                margin=ft.margin.only(top=5, bottom=5)
            )
            layout.controls.insert(2, audit_panel)
            
        return layout

    def _show_inspector_dialog(self, metrics):
        """Abre o painel BottomSheet para inspeção detalhada de paridade."""
        if not self.page: return

        deep = metrics.get("deep_audit", {})
        samples = deep.get("samples", {})
        g_samples = samples.get("genuino", [])
        s_samples = samples.get("suspeito", [])
        raw_samples = samples.get("source", [])
        exp_factor = metrics.get("expansion_factor", 0)

        def close_sheet(e):
            self.page.bottom_sheet.open = False
            self.page.update()

        sheet_content = ft.Container(
            padding=30,
            bgcolor=PlatinumTheme.BG_DARK(),
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ANALYTICS_OUTLINED, color=PlatinumTheme.PRIMARY(), size=32),
                    ft.Column([
                        ft.Text("AUDITORIA DE VERDADE 1:N", size=18, weight="bold", color=PlatinumTheme.PRIMARY()),
                        ft.Text(f"Fator de Expansão: {exp_factor:+} linhas geradas no arquivo final.", size=13, color=PlatinumTheme.SUCCESS() if exp_factor >= 0 else PlatinumTheme.WARNING()),
                    ], spacing=2, expand=True),
                    ft.IconButton(ft.Icons.CLOSE, on_click=close_sheet)
                ], alignment="spaceBetween"),
                
                ft.Divider(height=40, color=ft.Colors.with_opacity(0.1, PlatinumTheme.BORDER_DARK())),
                
                ft.Row([
                    # Coluna 1: Brutos
                    ft.Column([
                        ft.Text("ORIGEM (BRUTO)", weight="bold", size=12, color=ft.Colors.GREY_400),
                        ft.Container(
                            content=ft.Column([
                                *[ft.Text(f"• {x}", size=11, color=ft.Colors.GREY_500, no_wrap=True) for x in raw_samples]
                            ], spacing=5, scroll=ft.ScrollMode.AUTO),
                            height=250, padding=10, border=ft.border.all(1, ft.Colors.with_opacity(0.1, PlatinumTheme.BORDER_DARK())), border_radius=8
                        )
                    ], expand=1),
                    
                    # Coluna 2: Genuinos
                    ft.Column([
                        ft.Text("DESTINO (SALVO)", weight="bold", size=12, color=PlatinumTheme.SUCCESS()),
                        ft.Container(
                            content=ft.Column([
                                *[ft.Text(f"• {x}", size=11, color=PlatinumTheme.SUCCESS(), no_wrap=True) for x in g_samples]
                            ], spacing=5, scroll=ft.ScrollMode.AUTO),
                            height=250, padding=10, border=ft.border.all(1, ft.Colors.with_opacity(0.1, PlatinumTheme.BORDER_DARK())), border_radius=8
                        )
                    ], expand=1),

                    # Coluna 3: Suspeitos
                    ft.Column([
                        ft.Text("CRÍTICOS (ERROS)", weight="bold", size=12, color=PlatinumTheme.WARNING()),
                        ft.Container(
                            content=ft.Column([
                                *[ft.Text(f"• {x}", size=11, color=PlatinumTheme.WARNING(), no_wrap=True) for x in s_samples]
                            ], spacing=5, scroll=ft.ScrollMode.AUTO),
                            height=250, padding=10, border=ft.border.all(1, ft.Colors.with_opacity(0.1, PlatinumTheme.BORDER_DARK())), border_radius=8
                        )
                    ], expand=1),
                ], alignment="start", spacing=15),
                
                ft.Text("Inspeção amostral de 10 fragmentos randômicos capturados pela Engine.", size=10, italic=True, color=PlatinumTheme.TEXT_MUTED())
            ], spacing=20, tight=True),
            border_radius=ft.border_radius.only(top_left=24, top_right=24)
        )

        self.page.bottom_sheet = ft.BottomSheet(sheet_content, open=True)
        self.page.update()

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Componente visual para gestão de sessões de extração MDM v0.7.2")
