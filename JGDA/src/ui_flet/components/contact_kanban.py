import flet as ft
from ui_flet.theme import PlatinumTheme

class ContactKanban(ft.Column):
    """
    Kanban Board para Curadoria Visual de Contatos.
    Gerencia o arrasto e classificação de domínios.
    """
    def __init__(self, contacts, on_change=None):
        super().__init__()
        self.contacts = contacts # Lista de dicts do mvf_detail_df
        self.on_change = on_change
        self.spacing = 20
        self.expand = True
        
        # 🔗 Sincronização com MDMEngine Taxonomia v0.7.2
        self.sectors = {
            "FINANCEIRO": {"label": "FINANCEIRO", "color": ft.Colors.BLUE_700, "code": "FINANCEIRO"},
            "FISCAL": {"label": "FISCAL", "color": ft.Colors.PURPLE_700, "code": "FISCAL"},
            "COMPRAS": {"label": "COMPRAS", "color": ft.Colors.GREEN_700, "code": "COMPRAS"},
            "RH": {"label": "RH", "color": ft.Colors.PINK_700, "code": "RH"},
            "ADMINISTRATIVO": {"label": "ADM", "color": ft.Colors.ORANGE_700, "code": "ADMINISTRATIVO"},
            "PENDENTE": {"label": "PENDENTES", "color": ft.Colors.GREY_700, "code": "PENDENTE"}
        }
        
        # Mapeamento Reverso (Fallback para códigos curtos se vierem do legado)
        self.legacy_map = {
            "FIN": "FINANCEIRO",
            "FISC": "FISCAL",
            "COMP": "COMPRAS"
        }
        
        self.build_kanban()

    def build_kanban(self):
        # Criar os buckets (DragTargets)
        self.buckets = {}
        row = ft.Row(alignment="start", vertical_alignment="start", scroll="auto", spacing=20)
        
        for code, info in self.sectors.items():
            bucket = ft.Column(
                [
                    ft.Text(info["label"], weight="bold", size=14, color=info["color"]),
                    ft.Divider(color=info["color"], height=2),
                    ft.Column(spacing=10, scroll="auto", expand=True) # Lista de cards
                ],
                width=240,
                spacing=10,
                horizontal_alignment="center"
            )
            
            dt = ft.DragTarget(
                group="contacts",
                content=ft.Container(
                    content=bucket,
                    padding=10,
                    border_radius=8,
                    bgcolor=ft.Colors.with_opacity(0.05, info["color"]),
                    height=440
                ),
                on_accept=lambda e, c=code: self._handle_accept(e, c)
            )
            self.buckets[code] = bucket.controls[2] # Referência para a lista interna
            row.controls.append(dt)
            
        self._populate_cards()
        self.controls = [row]

    def _populate_cards(self):
        for b in self.buckets.values():
            b.controls.clear()
            
        for idx, contact in enumerate(self.contacts):
            # Lógica de extração de setor resiliente
            status = contact.get("MDM_Status")
            raw_code = contact.get("category_code")
            
            # Se for legado (FIN), converte para Platinum (FINANCEIRO)
            if raw_code in self.legacy_map:
                raw_code = self.legacy_map[raw_code]
            
            sector = raw_code if status == "AUTO_CLASSIFIED" or status == "USER_VALIDATED" else "PENDENTE"
            if sector not in self.buckets: sector = "PENDENTE"
            
            card = self._create_card(contact, idx)
            self.buckets[sector].controls.append(card)

    def _create_card(self, contact, idx):
        # 🕵️ Detecção Universal de Valor (Email ou Telefone)
        # Tenta chaves conhecidas ou busca pela primeira string que não seja de metadado
        data = contact.get("E_Mail") or contact.get("E-mail") or contact.get("Phone") or contact.get("Telefone")
        if not data:
            # Fallback: Tenta pegar o primeiro valor que não seja chave MDM
            known_keys = ["MDM_Status", "MDM_Confidence", "category_code", "category_label", "_ID"]
            for k, v in contact.items():
                if k not in known_keys and v:
                    data = str(v)
                    break
        
        data = str(data or "DADO_NAO_IDENTIFICADO")
        label = contact.get("category_label") or "PENDENTE"
        conf = contact.get("MDM_Confidence") or 0.0
        
        content = ft.Container(
            content=ft.Column([
                ft.Text(data, size=11, weight="bold", overflow="ellipsis"),
                ft.Row([
                    ft.Text(label, size=9, italic=True, color=ft.Colors.GREY_500),
                    ft.Container(expand=True),
                    ft.Text(f"{int(float(conf)*100)}%", size=9, weight="bold", color="green" if float(conf) > 0.8 else "orange")
                ])
            ], spacing=2),
            padding=10,
            bgcolor="white",
            border_radius=6,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        return ft.Draggable(
            group="contacts",
            data=idx,
            content=content
        )

    def _handle_accept(self, e, new_sector_code):
        try:
            idx = int(e.src.data)
            contact = self.contacts[idx]
            
            sector_info = self.sectors.get(new_sector_code)
            contact["category_code"] = new_sector_code
            contact["category_label"] = sector_info["label"]
            contact["MDM_Status"] = "USER_VALIDATED"
            contact["MDM_Confidence"] = 1.0
            
            self._populate_cards()
            self.update()
            
            if self.on_change:
                self.on_change()
        except:
            pass

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version import __version__
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Componente Kanban de curadoria MDM com mapeamento flexível de taxonomia")
