import flet as ft
from ui_flet.theme import PlatinumTheme
import pandas as pd

class DeduplicatorMatrix(ft.Column):
    """
    HUD de Consolidação Power Query (v0.7.3).
    Permite visualizar e editar a unificação de roles em tempo real.
    """
    def __init__(self, contacts_df, on_confirm=None):
        super().__init__()
        self.contacts_df = contacts_df
        self.on_confirm = on_confirm
        self.spacing = 20
        self.expand = True
        self.scroll = ft.ScrollMode.ADAPTIVE
        
        # 🔍 Mapeamento Dinâmico de Colunas (Zero Hardcoding)
        cols = contacts_df.columns.tolist()
        self.col_name = next((c for c in cols if str(c).lower() in ["name", "nome", "razo social", "razão social"]), "Name")
        self.col_mail = next((c for c in cols if str(c).lower() in ["e_mail", "e-mail", "email", "contato"]), "E_Mail")
        
        self.groups_container = ft.ListView(spacing=15, expand=True, padding=10)
        self.lbl_stats = ft.Text("Analisando redundâncias...", size=13, weight="bold", color=PlatinumTheme.PRIMARY())
        
        # --- ESTADO DE CONTROLE (v0.7.3) ---
        self.threshold = 80
        self.show_all = False
        
        self.sld_sensitivity = ft.Slider(
            min=50, max=100, divisions=10, 
            label="{value}% Sensibilidade", value=self.threshold,
            on_change=self._on_sensitivity_change
        )
        
        self.chk_show_all = ft.Switch(label="Mapear Únicos", value=self.show_all, on_change=self._on_toggle_all)
        
        self.dashboard = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.AUTO_FIX_HIGH, color=PlatinumTheme.PRIMARY(), size=28),
                ft.Column([
                    ft.Text("CONSOLIDAÇÃO ANALÍTICA PLATINUM", weight="bold", size=16, color=PlatinumTheme.PRIMARY()),
                    self.lbl_stats
                ], spacing=2, expand=True),
                ft.Column([
                    ft.Text("ORDENAÇÃO", size=10, weight="bold", color=PlatinumTheme.TEXT_MUTED()),
                    ft.Dropdown(
                        options=[
                            ft.dropdown.Option("ID", "Ordem Original"),
                            ft.dropdown.Option("CONF", "Menor Confiança")
                        ],
                        value="ID",
                        height=40, width=150, text_size=12,
                        on_change=lambda _: self._analyze_and_build()
                    )
                ], spacing=0, horizontal_alignment="center"),
                ft.Column([
                    ft.Text("SENSIBILIDADE DO ROBÔ", size=10, weight="bold", color=PlatinumTheme.TEXT_MUTED()),
                    self.sld_sensitivity
                ], spacing=0, horizontal_alignment="center"),
                ft.VerticalDivider(width=1),
                self.chk_show_all
            ], vertical_alignment="center", spacing=20),
            padding=25,
            bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.15, PlatinumTheme.PRIMARY()))
        )
        
        self.controls = [
            self.dashboard,
            ft.Divider(height=1, color=ft.Colors.with_opacity(0.05, PlatinumTheme.TEXT_SECONDARY())),
            self.groups_container
        ]
        
        self._analyze_and_build()

    def _analyze_and_build(self):
        from core.engines.deduplication_engine import DeduplicationEngine
        engine = DeduplicationEngine()
        
        # 1. Executa Consolidação v0.7.3 com Sensibilidade Dinâmica e Mapeamento
        col_map = {"name": self.col_name, "mail": self.col_mail, "phone": "Phone"}
        self.consolidated_df, self.dedup_log = engine.consolidate(self.contacts_df, dynamic_threshold=self.threshold, col_mapping=col_map)
        
        # 2. Renderiza HUD
        self.groups_container.controls.clear()
        
        # Agrupa para exibição por ParentKey
        groups = self.consolidated_df.groupby('ParentKey')
        total_groups = len(groups)
        
        # Filtro de Saliência: Only show problematic groups by default
        conflict_groups = 0
        visible_groups = 0
        
        for pk, group_df in groups:
            has_merge = (group_df['MDM_Status'] == "CONSOLIDATED").any()
            if has_merge: conflict_groups += 1
            
            # Lógica de Visibilidade UX
            if not self.show_all and not has_merge:
                continue
            
            visible_groups += 1
            card = self._build_group_card(pk, group_df, has_merge)
            self.groups_container.controls.append(card)
        
        self.lbl_stats.value = f"Detectamos {conflict_groups} grupos críticos | Curando {visible_groups} de {total_groups} Entidades."
        
        try:
            self.update()
        except: pass

    def _on_sensitivity_change(self, e):
        self.threshold = e.control.value
        self._analyze_and_build()

    def _on_toggle_all(self, e):
        self.show_all = e.control.value
        self._analyze_and_build()

    def _build_group_card(self, pk, group_df, has_merge):
        rows = []
        for _, row in group_df.iterrows():
            is_consolidated = row.get('MDM_Status') == "CONSOLIDATED"
            score = row.get('_similarity_score', 100)
            is_phonetic = row.get('_is_phonetic', False)
            
            # Badge de Confiança Matemática
            score_color = PlatinumTheme.SUCCESS() if score > 85 else PlatinumTheme.WARNING()
            badge_text = f"{int(score)}%" if is_consolidated else "100%"
            if is_phonetic and is_consolidated: badge_text = "FONÉTICO"

            # Parse de Emails para Interactive Chips (Engenharia de Ejeção)
            email_val = str(row.get(self.col_mail, ""))
            emails = [e.strip() for e in email_val.split(';') if e.strip()]
            email_chips = []
            for m in emails:
                email_chips.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(m, size=11, color=PlatinumTheme.TEXT_SECONDARY()),
                            ft.Icon(ft.Icons.FILE_DOWNLOAD_OUTLINED, size=10, color=PlatinumTheme.PRIMARY())
                        ], spacing=4),
                        tooltip="Clique para ejetar (Split Manual)",
                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        border=ft.border.all(1, ft.Colors.with_opacity(0.1, PlatinumTheme.PRIMARY())),
                        border_radius=12,
                        on_click=lambda e, m=m, r=row: self._on_eject_email(m, r)
                    )
                )

            # Matriz X-Ray (Expandable) com Mudanças Visuais (Audit)
            xray_panel = ft.Column([
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.05, PlatinumTheme.TEXT_SECONDARY())),
                ft.Row([
                    ft.Text("AUDITORIA TÉCNICA:", size=9, weight="bold", color=PlatinumTheme.TEXT_MUTED()),
                    ft.Text(f"Diff: ", size=9, color=PlatinumTheme.TEXT_SECONDARY()),
                    ft.Text(spans=self._get_visual_diff(str(pk), str(row.get(self.col_name, "")))),
                    ft.Container(expand=True),
                    ft.Text("METAPHONE BR MATCH" if is_phonetic else "DIFERENÇA FONÉTICA", 
                            size=8, weight="bold", color=PlatinumTheme.SUCCESS() if is_phonetic else PlatinumTheme.WARNING())
                ])
            ], visible=False)

            # Campo de Nome Editável
            name_input = ft.TextField(
                value=str(row.get(self.col_name, "")),
                text_size=12, height=35, expand=True,
                border_color=score_color if is_consolidated else ft.Colors.with_opacity(0.1, PlatinumTheme.TEXT_SECONDARY()),
                border_width=2 if is_consolidated else 1,
                cursor_color=PlatinumTheme.PRIMARY(),
                on_change=lambda e, r=row: self._on_name_edit(e, r)
            )
            
            row_content = ft.Column([
                ft.Row([
                    ft.GestureDetector(
                        on_double_tap=lambda e, x=xray_panel: self._toggle_xray(x),
                        content=ft.Icon(ft.Icons.MERGE_TYPE if is_consolidated else ft.Icons.PERSON_ROUNDED, 
                                        size=18, color=score_color if is_consolidated else PlatinumTheme.TEXT_MUTED())
                    ),
                    name_input,
                    ft.Row(email_chips, spacing=5, wrap=True, expand=True),
                    ft.Container(
                        content=ft.Text(badge_text, size=9, weight="bold", color="white"),
                        bgcolor=score_color, padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        border_radius=12
                    )
                ], vertical_alignment="center"),
                xray_panel
            ], spacing=5)
            
            rows.append(ft.Container(content=row_content, padding=8, border_radius=8))

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.BUSINESS_ROUNDED, size=14, color=PlatinumTheme.PRIMARY() if has_merge else PlatinumTheme.TEXT_MUTED()),
                    ft.Text(f"ENTIDADE ID: {pk}", weight="bold", size=12, color=PlatinumTheme.PRIMARY() if has_merge else PlatinumTheme.TEXT_MUTED()),
                    ft.Container(expand=True),
                    ft.Text("CONFLITO DETECTADO" if has_merge else "IDENTIDADE ÚNICA", 
                            size=10, weight="bold", color=AlphaColor := PlatinumTheme.WARNING() if has_merge else PlatinumTheme.TEXT_MUTED())
                ]),
                ft.Column(rows, spacing=5)
            ], spacing=10),
            padding=20,
            bgcolor=ft.Colors.with_opacity(0.04, PlatinumTheme.PRIMARY()) if has_merge else ft.Colors.with_opacity(0.01, ft.Colors.BLACK),
            border=ft.border.all(1, PlatinumTheme.PRIMARY() if has_merge else ft.Colors.with_opacity(0.1, PlatinumTheme.BORDER_DARK())),
            border_radius=15,
            animate=ft.Animation(300, ft.AnimationCurve.DECELERATE)
        )

    def _on_name_edit(self, e, row_data):
        # Localizamos o registro exato no DataFrame consolidado e atualizamos o nome
        # (Usamos o índice do row_data que é preservado do DataFrame original de trabalho)
        self.consolidated_df.at[row_data.name, self.col_name] = e.control.value

    def _on_eject_email(self, email, row_data):
        """
        ENGENHARIA DE EJEÇÃO (Split Manual).
        Remove o email da linha consolidada e cria um novo registro mestre.
        """
        # 1. Remove da linha atual
        current_emails = [e.strip() for e in str(row_data.get(self.col_mail, "")).split(';') if e.strip()]
        if email in current_emails:
            current_emails.remove(email)
            self.consolidated_df.at[row_data.name, self.col_mail] = "; ".join(current_emails)
            
            # 2. Cria Nova Linha (Injeção de MDM Master)
            new_row = row_data.copy()
            new_row[self.col_name] = f"[EJETADO] {email.split('@')[0]}"
            new_row[self.col_mail] = email
            new_row['MDM_Status'] = "UNIQUE" # Deixa de ser mestre consolidado
            new_row['MDM_Reason'] = "Ejeção Manual (HUD Power Query)"
            
            # Adiciona ao DataFrame
            self.consolidated_df = pd.concat([self.consolidated_df, pd.DataFrame([new_row])], ignore_index=True)
            
            # 3. Reconstrói UI
            self._analyze_and_build()

    def _get_visual_diff(self, original, current):
        """Implementação de diff visual para auditoria de nomes."""
        import difflib
        s = difflib.SequenceMatcher(None, original.upper(), current.upper())
        spans = []
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            if tag == 'equal':
                spans.append(ft.TextSpan(current[j1:j2], style=ft.TextStyle(color=PlatinumTheme.TEXT_SECONDARY())))
            elif tag == 'replace':
                spans.append(ft.TextSpan(current[j1:j2], style=ft.TextStyle(color=PlatinumTheme.WARNING(), weight="bold", bgcolor=ft.Colors.with_opacity(0.1, PlatinumTheme.WARNING()))))
            elif tag == 'insert':
                spans.append(ft.TextSpan(current[j1:j2], style=ft.TextStyle(color=PlatinumTheme.SUCCESS(), weight="bold")))
        return spans

    def get_final_data(self):
        return self.consolidated_df

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version import __version__
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "HUD Power Query: Interface de Consolidação Responsiva e Editável")
