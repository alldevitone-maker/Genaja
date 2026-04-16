import flet as ft
from ui_flet.theme import PlatinumTheme

class ParityAuditCard(ft.Container):
    """
    Componente Platinum O(1) para demonstrar a balança dimensional de dados pre/pós limpeza (ETL Audit).
    """
    def __init__(self, metrics: dict):
        super().__init__()
        self.metrics = metrics or {}
        self.padding = 15
        self.border_radius = 12
        self.bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.BLACK) if not PlatinumTheme.BG_DARK() else ft.Colors.with_opacity(0.2, PlatinumTheme.SURFACE_DARK())
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.1, PlatinumTheme.TEXT_SECONDARY()))
        self.build_ui()
        
    def build_ui(self):
        before = self.metrics.get("before", {"rows": 0, "cols": 0, "cells": 0})
        after = self.metrics.get("after", {"rows": 0, "cols": 0, "cells": 0})
        
        has_loss = before["cells"] != after["cells"]
        
        icon_color = PlatinumTheme.WARNING() if has_loss else PlatinumTheme.SUCCESS()
        icon_state = ft.Icons.WARNING_ROUNDED if has_loss else ft.Icons.CHECK_CIRCLE_ROUNDED
        title_text = "AUDITORIA: Mutilação Detectada" if has_loss else "AUDITORIA: Match 100%"
        
        def render_metric_block(title, rows, cols, cells, is_before=True):
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, size=11, weight="bold", color=PlatinumTheme.TEXT_MUTED()),
                    ft.Row([
                        ft.Icon(ft.Icons.TABLE_ROWS_ROUNDED, size=14, color=PlatinumTheme.TEXT_SECONDARY()),
                        ft.Text(f"{rows:,}".replace(",", "."), size=13, weight="bold")
                    ], spacing=5),
                    ft.Row([
                        ft.Icon(ft.Icons.VIEW_COLUMN_ROUNDED, size=14, color=PlatinumTheme.TEXT_SECONDARY()),
                        ft.Text(f"{cols:,}".replace(",", "."), size=13, weight="bold")
                    ], spacing=5),
                    ft.Divider(height=1),
                    ft.Text(f"{cells:,} Células".replace(",", "."), size=11, italic=True)
                ], spacing=4),
                padding=10,
                border_radius=8,
                bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.WHITE) if is_before else ft.Colors.with_opacity(0.05, PlatinumTheme.PRIMARY()),
                expand=True
            )
            
        block_before = render_metric_block("ORIGEM CRUA (Passo 0)", before.get("rows",0), before.get("cols",0), before.get("cells",0), True)
        block_after = render_metric_block("SANEADO (Passo 1)", after.get("rows",0), after.get("cols",0), after.get("cells",0), False)
        
        loss_text = None
        if has_loss:
            gap = before["cells"] - after["cells"]
            loss_text = ft.Text(f"Perda Tática: {gap:,} células limpas.".replace(",", "."), size=11, color=PlatinumTheme.WARNING(), italic=True)
        else:
            loss_text = ft.Text("Preservação geométrica absoluta mantida.", size=11, color=PlatinumTheme.SUCCESS(), italic=True)

        self.content = ft.Column([
            ft.Row([
                ft.Icon(icon_state, color=icon_color, size=18),
                ft.Text(title_text, weight="bold", size=13, color=icon_color),
            ], spacing=10),
            ft.Row([block_before, ft.Icon(ft.Icons.ARROW_RIGHT_ALT_ROUNDED, color=PlatinumTheme.TEXT_MUTED()), block_after], alignment="spaceBetween"),
            loss_text
        ], spacing=10)
