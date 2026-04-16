from ui_flet.theme import PlatinumTheme
from core.math.phonetic_engine import PhoneticEngine

class SmartContractCard(ft.Container):
    def __init__(self, parent_key, items, sectors_dict, on_move_action, on_edit_action=None, zoom_level=100):
        super().__init__()
        self.parent_key = parent_key
        self.items = items
        self.sectors_dict = sectors_dict
        self.on_move_action = on_move_action
        self.on_edit_action = on_edit_action
        self.zoom_level = zoom_level
        self.expanded = False

        self.padding = 10 if zoom_level == 100 else 6
        self.border_radius = 12
        self.animate = ft.Animation(300, ft.AnimationCurve.DECELERATE)
        self.animate_scale = ft.Animation(300, ft.AnimationCurve.DECELERATE)
        self.animate_size = ft.Animation(300, ft.AnimationCurve.DECELERATE)
        self.on_click = self.toggle_expand
        self.ink = True
        
        self._sync_visual_state()
        self._update_content()

    def _sync_visual_state(self):
        base_bg = PlatinumTheme.SURFACE_DARK()
        hover_bg = ft.Colors.with_opacity(0.8, PlatinumTheme.BG_DARK())
        
        self.bgcolor = base_bg if not self.expanded else hover_bg
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.1, PlatinumTheme.BORDER_DARK())) if not self.expanded else ft.border.all(1, PlatinumTheme.PRIMARY())
        
        shadow_col = ft.Colors.with_opacity(0.05 if not self.expanded else 0.2, "black")
        self.shadow = ft.BoxShadow(blur_radius=5 if not self.expanded else 14, color=shadow_col)
        self.scale = 1.0 if not self.expanded else 1.02
        if self.expanded:
            self.blur = ft.Blur(10, 10, ft.BlurTileMode.MIRROR)
        else:
            self.blur = None

    def _update_content(self):
        header = ft.Row([
            ft.Icon(ft.Icons.BUSINESS_ROUNDED, size=14, color=ft.Colors.BLUE_GREY_400),
            ft.Text(str(self.parent_key), size=12, weight="bold", overflow="ellipsis", expand=True),
            ft.Container(
                content=ft.Text(f"{len(self.items)}", size=10, weight="bold", color="white"),
                bgcolor=PlatinumTheme.PRIMARY(),
                border_radius=12,
                padding=ft.padding.symmetric(horizontal=6, vertical=2)
            )
        ])

        if not self.expanded:
            self.content = header
        else:
            children = [header, ft.Divider(color=PlatinumTheme.BORDER_DARK(), height=1)]
            for item in self.items:
                data = str(item.get("E_Mail") or item.get("E-mail") or item.get("Phone") or item.get("Telefone", "DADO"))
                
                contact_name_str = item.get("Name") or item.get("Nome") or ""
                if str(contact_name_str).lower() == "none" or str(contact_name_str) == "NaN":
                    contact_name_str = ""
                display_text = f"{str(contact_name_str).strip()} • {data}" if str(contact_name_str).strip() else data
                
                raw_conf = item.get("MDM_Confidence", 0.0)
                try:
                    conf = float(raw_conf)
                    if str(conf).lower() == 'nan': conf = 0.0
                except:
                    conf = 0.0
                    
                reason = item.get("MDM_Reason", "Classificação Manual")
                
                pills = []
                for s_code, s_info in self.sectors_dict.items():
                    if s_code == "PENDENTE": continue
                    pill = ft.Container(
                        content=ft.Text(s_info["label"][:3].upper(), size=8, weight="bold", color="white"),
                        bgcolor=ft.Colors.with_opacity(0.8, s_info["color"]),
                        padding=ft.padding.symmetric(horizontal=6, vertical=2),
                        border_radius=12,
                        ink=True,
                        on_click=lambda e, idx=item['_global_idx'], c=s_code: self.trigger_move(e, idx, c)
                    )
                    pills.append(pill)
                
                edit_btn = ft.IconButton(
                    icon=ft.Icons.EDIT_ROUNDED,
                    icon_size=12,
                    icon_color=PlatinumTheme.TEXT_MUTED(),
                    padding=0,
                    width=24, height=24,
                    tooltip="Editar valor do Contato",
                    on_click=lambda e, i=item: self._click_edit(e, i)
                )

                if self.zoom_level == 50:
                    item_row = ft.Row([
                        ft.Row(pills, wrap=True, spacing=2),
                        ft.Container(expand=True),
                        ft.Text(f"{int(conf*100)}%", size=8, weight="bold", tooltip=f"MDM: {reason}", color=PlatinumTheme.SUCCESS() if conf > 0.8 else PlatinumTheme.WARNING())
                    ], spacing=2)
                else:
                    item_row = ft.Column([
                        ft.Row([
                            ft.Text(display_text, size=11, weight="bold", color=PlatinumTheme.TEXT_SECONDARY(), overflow="ellipsis", tooltip=display_text),
                            edit_btn,
                            ft.Container(expand=True),
                            ft.Text(f"{int(conf*100)}%", size=9, weight="bold", tooltip=f"MDM Engine: {reason}", color=PlatinumTheme.SUCCESS() if conf > 0.8 else PlatinumTheme.WARNING())
                        ]),
                        ft.Row(pills, wrap=True, spacing=4)
                    ], spacing=4)
                
                item_bg = ft.Colors.with_opacity(0.5, PlatinumTheme.SURFACE_DARK()) if PlatinumTheme.SURFACE_DARK() else "transparent"
                children.append(ft.Container(content=item_row, padding=4, bgcolor=item_bg, border_radius=6, border=ft.border.all(1, ft.Colors.with_opacity(0.05, PlatinumTheme.TEXT_PRIMARY()))))

            self.content = ft.Column(children, spacing=4 if self.zoom_level == 50 else 8)
            
    def toggle_expand(self, e):
        self.expanded = not self.expanded
        self._sync_visual_state()
        self._update_content()
        self.update()

    def trigger_move(self, e, global_idx, new_sector):
        e.control.page.update()
        if self.on_move_action:
            self.on_move_action(global_idx, new_sector)

    def _click_edit(self, e, item):
        if self.on_edit_action:
            self.on_edit_action(item)

class ContactKanban(ft.Column):
    """
    Kanban Board para Curadoria Visual de Contatos.
    Gerencia o agrupamento de Contratos Pai e movimentação híbrida.
    """
    def __init__(self, contacts, on_change=None):
        super().__init__()
        self.contacts = contacts
        self.visible_contacts = contacts[:] # Cópia para filtragem
        self.on_change = on_change
        self.spacing = 10
        self.expand = False
        self.zoom_level = 100
        
        self.sectors = {
            "FIN": {"label": "FINANCEIRO", "color": ft.Colors.BLUE_700, "code": "FIN"},
            "FISC": {"label": "FISCAL", "color": ft.Colors.PURPLE_700, "code": "FISC"},
            "COMP": {"label": "COMPRAS", "color": ft.Colors.GREEN_700, "code": "COMP"},
            "ADM": {"label": "ADM", "color": ft.Colors.ORANGE_700, "code": "ADM"},
            "RH": {"label": "RH", "color": ft.Colors.PINK_700, "code": "RH"},
            "CONT": {"label": "CONTATO", "color": ft.Colors.TEAL_700, "code": "CONT"},
            "XX": {"label": "SUSPEITOS", "color": ft.Colors.ORANGE_800, "code": "XX"},
            "PENDENTE": {"label": "PENDENTES", "color": ft.Colors.GREY_700, "code": "PENDENTE"}
        }
        
        self.build_ui_shell()

    def build_ui_shell(self):
        def on_zoom(e):
            self.zoom_level = int(e.control.value)
            self._populate_cards()
            if self.page:
                self.update()
            
        zoom_slider = ft.CupertinoSlider(
            min=50, max=100, divisions=1, value=100,
            active_color=PlatinumTheme.PRIMARY(),
            on_change=on_zoom
        )
        
        self.txt_search = ft.TextField(
            label="Busca Semântica (Soa como...)",
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            width=350, height=45, text_size=12,
            border_radius=10,
            on_change=self._handle_search
        )
        
        toolbar = ft.Row([
            ft.Icon(ft.Icons.ZOOM_IN_MAP_OUTLINED, color=PlatinumTheme.TEXT_SECONDARY(), size=16),
            ft.Text("Semantic Zoom:", weight="bold", size=12, color=PlatinumTheme.TEXT_SECONDARY()),
            zoom_slider,
            ft.Container(expand=True),
            self.txt_search
        ], alignment="start")
        
        self.kanban_row = ft.Row(alignment="start", vertical_alignment="start", scroll=ft.ScrollMode.ALWAYS, spacing=15)
        self.build_kanban()
        
        self.controls = [toolbar, self.kanban_row]

    def did_mount(self):
        """Hook sagrado do Flet: Chamado quando o controle entra na página real."""
        self._populate_cards()
        self.update()

    def _trigger_rename_col(self, e, code):
        curr_label = self.sectors[code]["label"]
        tf = ft.TextField(value=curr_label, label="Novo Nome Roteador", border_color=PlatinumTheme.PRIMARY())
        
        def save(evt):
            new_label = str(tf.value).strip().upper()
            if new_label:
                self.sectors[code]["label"] = new_label
                for contact in self.contacts:
                    if contact.get("category_code") == code:
                        contact["category_label"] = new_label
                        
                self.page.dialog.open = False
                self.page.update()
                self.build_kanban()
                if self.on_change: self.on_change()
                
        def close(evt):
            self.page.dialog.open = False
            self.page.update()
            
        dlg = ft.AlertDialog(
            title=ft.Text(f"Renomear Coluna: {curr_label}"),
            content=tf,
            actions=[ft.TextButton("Cancelar", on_click=close), ft.ElevatedButton("Salvar", on_click=save, bgcolor=PlatinumTheme.PRIMARY(), color="white")]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def build_kanban(self):
        self.buckets = {}
        self.headers = {}
        self.kanban_row.controls.clear()
        
        for code, info in self.sectors.items():
            header_text = ft.Text(f'{info["label"]} (0)', weight="bold", size=13, color=info["color"])
            self.headers[code] = header_text
            
            header_row = ft.Row([
                header_text,
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.SETTINGS_OUTLINED, icon_size=12, tooltip="Renomear Categoria de Curadoria", opacity=0.5, on_click=lambda e, c=code: self._trigger_rename_col(e, c))
            ])
            
            bucket = ft.Column(
                [
                    header_row,
                    ft.Divider(color=info["color"], height=2),
                    ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, height=400)
                ],
                width=240 if self.zoom_level == 100 else 180,
                spacing=8,
                horizontal_alignment="center"
            )
            
            bg_col = ft.Colors.with_opacity(0.08, info["color"])
            dt = ft.DragTarget(
                group="contacts",
                content=ft.Container(
                    content=bucket,
                    padding=10,
                    border_radius=12,
                    bgcolor=bg_col,
                    blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.1, info["color"])),
                    height=500
                ),
                on_accept=lambda e, c=code: self._handle_accept(e, c)
            )
            self.buckets[code] = bucket.controls[2]
            self.kanban_row.controls.append(dt)
            
        self._populate_cards()

    def _update_headers(self):
        for code, header in self.headers.items():
            count = 0
            for c in self.buckets[code].controls:
                if hasattr(c, 'content') and hasattr(c.content, 'items'):
                    count += len(c.content.items)
            
            label = self.sectors[code]["label"]
            header.value = f"{label} ({count})"

    def _populate_cards(self):
        for b in self.buckets.values():
            b.controls.clear()
            
        grouped_by_sector_and_pk = {s: {} for s in self.sectors.keys()}
        MAX_CARDS = 50
        rendered_count = 0
            
        for idx, contact in enumerate(self.visible_contacts):
            if rendered_count >= MAX_CARDS:
                if "PENDENTE" in self.buckets:
                    self.buckets["PENDENTE"].controls.append(
                        ft.Text(f"+ {len(self.contacts) - MAX_CARDS} itens soltos (use export)...", color="red", size=10, italic=True)
                    )
                break

            status = contact.get("MDM_Status")
            raw_code = contact.get("category_code")
            
            # 🧠 Roteirização Inteligente: mesmo "REVIEW_CANDIDATE" vai pra coluna sugerida pra facilitar a vida do humano.
            sector = raw_code if raw_code and raw_code in self.sectors.keys() else "PENDENTE"
            
            pk = contact.get("ParentKey", "UNKNOWN")
            if not pk or str(pk).strip() == '': pk = "UNKNOWN"
            contact['_global_idx'] = idx

            if pk not in grouped_by_sector_and_pk[sector]:
                grouped_by_sector_and_pk[sector][pk] = []
                
            grouped_by_sector_and_pk[sector][pk].append(contact)
            rendered_count += 1
            
        for sector_code, pks in grouped_by_sector_and_pk.items():
            for pk, items in pks.items():
                card = SmartContractCard(
                    parent_key=pk,
                    items=items,
                    sectors_dict=self.sectors,
                    on_move_action=self._handle_quick_move,
                    on_edit_action=self._handle_edit_click,
                    zoom_level=self.zoom_level
                )
                
                
                import json
                payload = json.dumps({"pk": pk, "source_sector": sector_code, "idxs": [i['_global_idx'] for i in items]})
                
                drag_wrapper = ft.Draggable(
                    group="contacts",
                    data=payload,
                    content=card
                )
                self.buckets[sector_code].controls.append(drag_wrapper)
                
        self._update_headers()

    def _handle_edit_click(self, item):
        data_key = next((k for k in ["E_Mail", "E-mail", "Phone", "Telefone"] if k in item and item[k]), None)
        current_val = str(item.get(data_key, "DADO")) if data_key else ""
        
        tf = ft.TextField(value=current_val, label="Corrigir Informação", border_color=ft.Colors.TEAL_700)
        
        def save(e):
            if data_key:
                item[data_key] = tf.value
            else:
                item["E_Mail"] = tf.value
                
            item["MDM_Status"] = "USER_VALIDATED"
            item["MDM_Confidence"] = 1.0
            
            dlg.open = False
            self.page.update()
            self._populate_cards()
            if self.on_change: self.on_change()
            
        def close(e):
            dlg.open = False
            self.page.update()
            
        dlg = ft.AlertDialog(
            title=ft.Row([ft.Icon(ft.Icons.EDIT_ROUNDED), ft.Text("Editar Dado Bruto")]),
            content=ft.Container(content=tf, padding=10),
            actions=[
                ft.TextButton("Cancelar", on_click=close),
                ft.ElevatedButton("Salvar Alteração", on_click=save, bgcolor=ft.Colors.TEAL_700, color="white"),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def _handle_quick_move(self, global_idx, new_sector_code):
        contact = self.contacts[global_idx]
        sector_info = self.sectors.get(new_sector_code)
        
        contact["category_code"] = new_sector_code
        contact["category_label"] = sector_info["label"]
        contact["MDM_Status"] = "USER_VALIDATED"
        contact["MDM_Confidence"] = 1.0
        
        self._populate_cards()
        self.update()
        if self.on_change: self.on_change()

    def _handle_search(self, e):
        query = str(self.txt_search.value).strip().upper()
        if not query:
            self.visible_contacts = self.contacts[:]
        else:
            q_code = PhoneticEngine.get_phonetic_code(query)
            
            def is_match(c):
                name = str(c.get("Name", "")).upper()
                pk = str(c.get("ParentKey", "")).upper()
                # Match Fonético Primário
                if q_code and (q_code in PhoneticEngine.get_phonetic_code(name) or q_code in PhoneticEngine.get_phonetic_code(pk)):
                    return True
                # Match Texto Básico (Fallback)
                if query in name or query in pk:
                    return True
                return False
                
            self.visible_contacts = [c for c in self.contacts if is_match(c)]
            
        self._populate_cards()
        self.update()

    def _handle_accept(self, e, new_sector_code):
        try:
            import json
            raw_data = str(e.src.data)
            data = json.loads(raw_data) if "{" in raw_data else {"idxs": [int(raw_data)]}
            idxs = data.get("idxs", [])
            sector_info = self.sectors.get(new_sector_code)
            
            for idx in idxs:
                contact = self.contacts[idx]
                contact["category_code"] = new_sector_code
                contact["category_label"] = sector_info["label"]
                contact["MDM_Status"] = "USER_VALIDATED"
                contact["MDM_Confidence"] = 1.0
            
            self._populate_cards()
            self.update()
            if self.on_change: self.on_change()
        except:
            pass

from version import __version__
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Componente Smart Kanban com Semantic UI e O(1) Hook")
