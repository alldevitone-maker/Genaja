import tkinter as tk
from tkinter import ttk, filedialog
from services.excel_loader import load_excel_data_with_adjustment
from services.theme_service import ThemeService
from ui.ui_settings import SettingsWindow
import tkinter.messagebox as messagebox
from tkinterdnd2 import DND_FILES

class ModernTooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.enabled = True
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        if not self.enabled: return
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        if not self.enabled: return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#1E293B", foreground="white", relief=tk.SOLID, borderwidth=1,
                         font=("Segoe UI", 9, "normal"))
        label.pack(ipadx=4, ipady=2)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg="#E5E7EB", highlightthickness=0, cursor="hand2")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview, cursor="hand2")
        self.scrollable_frame = tk.Frame(self.canvas, bg="#E5E7EB")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)
        
    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# --- INTERNATIONALIZATION (i18n) ---
# Centralização de strings para fácil migração e tradução
I18N = {
    "app_title": "Inteligência de Sincronização - Hub Unificado Flex",
    "btn_tips_on": "💡 Desativar Dicas",
    "btn_tips_off": "💡 Ativar Dicas",
    "step1_title": " 📂 Passo 1: Arraste e Solte suas Planilhas ou Clique no Botão ",
    "lbl_src_idle": "📁 Arraste a ORIGEM aqui\nou clique para buscar",
    "lbl_tgt_idle": "📁 Arraste o DESTINO aqui\nou clique para buscar",
    "err_format": "Apenas planilhas Excel (.xlsx ou .xls) são aceitas.",
    "step2_title": " 🧠 Passo 2: Intersecção Matemática & Protected Keys ",
    "ai_waiting": "Aguardando planilhas para varredura I.A...",
    "lbl_key_src": "Chave na Origem:",
    "lbl_key_tgt": "Chave Destino:",
    "lbl_fix_key": "⭐ Fixar Chave\n(Posição A1)",
    "chk_activate": "Ativar",
    "btn_validate": "🔒 Validar",
    "btn_validated": "✅ Chaves Blindadas",
    "step3_title": " ⚙️ Passo 3: Módulos de Execução Integrados ",
    "mod_etl": "🧹 Módulo Sincronização e Limpeza (ETL)",
    "mod_cmp": "⚖️ Módulo Comparador Púro (Auditoria)",
    "watermark": "--- Selecione e Transfira para Cá ---",
    "lbl_av_cols": "Colunas Disponíveis (Origem)",
    "lbl_sync_cols": "A Sincronizar (Destino Final)",
    "btn_move_all": ">> Transpor Todas",
    "btn_move": "> Transpor Seção",
    "btn_remove": "< Remover Seção",
    "btn_remove_all": "<< Remover Todas",
    "lbl_acc_cols": "Colunas Acumuladas Para Sincronização:",
    "none_selected": "Nenhuma coluna selecionada no processo acima.",
    "rules_row": " Regras de Linha ",
    "rules_struct": " Regras de Estrutura ",
    "chk_zeros": "Remover linhas com valor zero ou nulo nas colunas:",
    "chk_only_mapped": "Manter APENAS as colunas selecionadas",
    "chk_trim": "Trim (limpar espaços extras no início/fim)",
    "chk_upper": "Maiúsculas (converter para Capslock)",
    "lbl_output": "Opções de Saída:",
    "lbl_experimental": "⚠️ Experimental (Testes)",
    "btn_run_etl": "🚀 Executar Sincronização & Exportar Relatório",
    "btn_reset": "🔄 Reiniciar App",
    "auditory_title": "🔍 Modo Auditoria Habilitado",
    "auditory_desc": "Neste modo, o algoritmo não transporá colunas, mas sim fará uma varredura extrema.\nO arquivo gerado conterá a linha BRUTA original do banco caso não exista correspondência mútua.",
    "lbl_comp_options": "Opções de Comparação de Arquivos:",
    "rules_direction": " Sentido da Busca e Exportação ",
    "opt_miss_tgt": "Falta no Destino (O que existe na Origem mas não no Destino)",
    "opt_miss_src": "Falta na Origem (O que existe no Destino mas não na Origem)",
    "chk_cmp_clean": "Exportar relatório mantendo apenas as chaves e colunas mapeadas",
    "btn_run_cmp": "⚖️ Auditar GAPS e Extrair Relatório Bruto",
    "tooltip_src": "Coluna de Identificação Principal na Planilha de Origem (Ex: ID, CPF, Codigo)",
    "tooltip_tgt": "Coluna Equivalente na Planilha Destino. As duas formam o Cruzamento principal.",
    "tooltip_fix": "Força essa chave a sempre ser a Primeira Coluna (A1) no Relatório Excel Exportado.",
    "tooltip_exp": "Os motores O(1) de Big Data CSV, JSON e SQL estão em fase Experimental\n(aprimoramento de estabilidade e design).",
    "ai_report_title": "Motor I.A de Intersecção (Detalhes)",
    "ai_no_matches": ":( A I.A não encontrou colunas com dados idênticos. Selecione manualmente.",
    "ai_matches_found": "🏆 Top Compatibilidades Matemáticas (Duplo clique para expandir):  ",
    "hud_search": "Busca Preditiva de Colunas...",
    "btn_next": "Próximo Passo (Módulos) ➡️",
    "btn_edit_mapping": "Editar Mapeamento de Colunas",
    "btn_back_selection": "Trocar Módulo",
    "step3_select_mod": "Módulo de Execução: Escolha sua Missão",
    "step3_config": "Configuração Final e Regras de Voo",
    "hint_scroll": "💡 Novos controles disponíveis abaixo! Role para continuar. ",
    "btn_help": "Ajuda"
}

class GenajaUI:
    def __init__(self, root, title, version, callbacks):
        self.root = root
        self.root.title(f"{title} - {I18N['app_title']} (v{version})")
        self.root.geometry("1100x950")
        
        self.theme_service = ThemeService()
        theme = self.theme_service.current_theme
        
        self.bg_col = theme["bg_col"]
        self.fg_col = theme["fg_col"]
        self.surface_col = theme["surface_col"]
        self.border_col = theme.get("border_col", "#FFFFFF")
        self.root.configure(bg=self.bg_col)
        
        self._apply_styles()
        self.drawer = SettingsWindow(self.root, self.theme_service, self.update_ui_theme)
        
        # --- MENU BAR (Top Level) ---
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Menu Settings
        self.menu_settings = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="⚙️ Settings", menu=self.menu_settings)
        self.menu_settings.add_command(label="🎨 Customizar Cores do App", command=self.drawer.toggle)
        self.menu_settings.add_separator()
        self.menu_settings.add_command(label="💡 Dicas de Interface", command=self.toggle_tooltips)
        self.menu_settings.add_separator()
        self.menu_settings.add_command(label="🚪 Sair", command=self.root.quit)
        
        self.callbacks = callbacks
        self.watermark_text = I18N["watermark"]
        
        self.file_src = tk.StringVar()
        self.file_tgt = tk.StringVar()
        self.key_src = tk.StringVar()
        self.key_tgt = tk.StringVar()
        self.key_tgt_final = tk.StringVar()
        self.export_fmt = tk.StringVar(value=".xlsx")
        self.cols_src = []
        self.cols_tgt = []
        self.current_hub_module = 'etl'
        
        self.tooltips_active = True
        self.tooltips_registry = []
        
        self.top_nav = tk.Frame(self.root, bg=self.bg_col)
        self.top_nav.pack(fill=tk.X, padx=20, pady=(10, 0))
        self.btn_toggle_tips = ttk.Button(self.top_nav, text=I18N["btn_tips_on"], command=self.toggle_tooltips)
        self.btn_toggle_tips.pack(side=tk.RIGHT)
        
        # --- CONTAINER PRINCIPAL ELÁSTICO COM SCROLL ---
        self.scroll_wrapper = ScrollableFrame(self.root, bg=self.bg_col)
        self.scroll_wrapper.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.main_container = self.scroll_wrapper.scrollable_frame
        
        # padding extra no container interno para respiro
        self.pack_frame = tk.Frame(self.main_container, bg=self.bg_col)
        self.pack_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        self.main_container = self.pack_frame
        
        self.build_upload_layer()
        self.build_keys_layer()
        self.build_hub_layer()
        
    def _apply_styles(self):
        self.style = ttk.Style(self.root)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")
        
        self.style.configure(".", background=self.bg_col, foreground=self.fg_col, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=self.bg_col)
        self.style.configure("TLabelframe", background=self.surface_col, foreground=self.fg_col, font=("Segoe UI", 10, "bold"), bordercolor=self.border_col)
        self.style.configure("TLabelframe.Label", background=self.surface_col, foreground="#0D6EFD", font=("Segoe UI", 10, "bold")) # Engine Blue
        self.style.configure("TLabel", background=self.surface_col, foreground=self.fg_col)
        
        # O ttk.Style para botões será usado apenas como fallback, pois trocamos para tk.Button Flat
        self.style.configure("TButton", padding=10, relief="flat", font=("Segoe UI", 9, "bold"))
        
    def _create_button(self, parent, text, style="TButton", command=None, tooltip=None, **kwargs):
        theme = self.theme_service.current_theme
        pack_keys = {'after', 'anchor', 'before', 'expand', 'fill', 'in', 'ipadx', 'ipady', 'padx', 'pady', 'side'}
        pack_opts = {k: v for k, v in kwargs.items() if k in pack_keys}
        widget_opts = {k: v for k, v in kwargs.items() if k not in pack_keys}
        
        # Mapeamento de Cores v0.4.8 (High Contrast) + Flat Design
        colors = {
            "Action.TButton": {"bg": theme.get("action_bg", "#0D6EFD"), "fg": theme.get("action_fg", "white"), "hover": "#0B5ED7"},
            "Success.TButton": {"bg": theme.get("success_bg", "#198754"), "fg": theme.get("success_fg", "white"), "hover": "#157347"},
            "Warning.TButton": {"bg": theme.get("warning_bg", "#0DCAF0"), "fg": theme.get("warning_fg", "white"), "hover": "#31D2F2"},
            "Danger.TButton": {"bg": theme.get("danger_bg", "#DC3545"), "fg": theme.get("danger_fg", "white"), "hover": "#BB2D3B"},
            "TButton": {"bg": theme.get("neutral_bg", "#6C757D"), "fg": theme.get("neutral_fg", "white"), "hover": "#5C636A"}
        }
        
        config = colors.get(style, colors["TButton"])
        
        # Criando botão Flat Puro (Tkinter nativo configurado)
        btn = tk.Button(parent, text=text, command=command, 
                        # Usando os valores do tema dinâmico para o estado inicial
                        bg=config["bg"], fg=config["fg"],
                        relief="flat", borderwidth=0, highlightthickness=1,
                        highlightbackground=theme.get("border_col", "#FFFFFF"),
                        disabledforeground="#ADB5BD", 
                        font=("Segoe UI", 9, "bold"), cursor="hand2",
                        activebackground=config["hover"], activeforeground=config["fg"],
                        **widget_opts)
        
        # Efeito de Hover Programático - SÓ SE ESTIVER ATIVO
        def on_enter(e): 
            if btn['state'] == 'normal': btn.config(bg=config["hover"])
        def on_leave(e): 
            if btn['state'] == 'normal': btn.config(bg=config["bg"])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        if not hasattr(self, '_custom_buttons'): self._custom_buttons = []
        self._custom_buttons.append((btn, style, config))
        
        if pack_opts:
            btn.pack(**pack_opts)
        
        if tooltip:
            self.add_tooltip(btn, tooltip)
        return btn

    def update_ui_theme(self, new_theme):
        """Atualiza a UI inteira em tempo real com COBERTURA ABSOLUTA"""
        self.bg_col = new_theme["bg_col"]
        self.fg_col = new_theme["fg_col"]
        self.surface_col = new_theme["surface_col"]
        self.border_col = new_theme.get("border_col", "#FFFFFF")
        self.root.config(bg=self.bg_col)
        
        self._apply_styles()
        
        def _refresh(parent):
            for child in parent.winfo_children():
                try:
                    cname = child.winfo_class()
                    # Frames e Canvas
                    if cname in ["Frame", "Canvas"]:
                        curr_bg = child.cget("bg")
                        # Verifica se é fundo ou surface e aplica
                        # Se tiver highlightthickness, aplica a border_col
                        if cname == "Frame" and child.cget("highlightthickness") > 0:
                            child.config(highlightbackground=self.border_col)
                            
                        if "surface" in str(child).lower() or curr_bg in ["#F9FAFB", "#FFFFFF"]:
                            child.config(bg=self.surface_col)
                        else:
                            child.config(bg=self.bg_col)
                    
                    # Labels (Incluindo títulos azuis que agora devem respeitar o tema se necessário)
                    elif cname == "Label":
                        # Títulos de passo costumam ter fg específico, mas labels comuns usam fg_col
                        curr_fg = child.cget("fg")
                        if curr_fg in ["#0F172A", "#111827", "#000000"]:
                            child.config(fg=self.fg_col)
                        child.config(bg=child.master.cget("bg"))
                    
                    # Entry/Text/Listbox
                    elif cname in ["Entry", "Text", "Listbox"]:
                        child.config(bg=self.surface_col, fg=self.fg_col, highlightcolor=self.border_col)
                        if cname == "Listbox":
                            child.config(selectbackground=new_theme.get("action_bg", "#0D6EFD"))
                except:
                    pass
                if cname not in ["Menu"]: # Não iterar menus internos recursivamente
                    _refresh(child)
        
        _refresh(self.root)
        
        # Atualiza botões customizados (engine Flat)
        colors_map = {
            "Action.TButton": "action",
            "Success.TButton": "success",
            "Warning.TButton": "warning",
            "Danger.TButton": "danger",
            "TButton": "neutral"
        }
        
        for btn, style, _ in self._custom_buttons:
            if btn.winfo_exists():
                role = colors_map.get(style, "neutral")
                bg = new_theme.get(f"{role}_bg")
                fg = new_theme.get(f"{role}_fg", "white")
                btn.config(bg=bg, fg=fg, highlightbackground=self.border_col)
        
        self.root.update_idletasks()

    def _create_labeled_combo(self, parent, label_text, variable, values=[], state="readonly", tooltip=None, font=("Segoe UI", 9, "bold")):
        container = tk.Frame(parent, bg=self.bg_col)
        tk.Label(container, text=label_text, bg=self.bg_col, fg=self.fg_col, font=font, cursor="hand2").pack(side=tk.LEFT, padx=(0,5))
        cb = ttk.Combobox(container, textvariable=variable, values=values, state=state, cursor="hand2")
        cb.pack(side=tk.LEFT, fill=tk.X, expand=True)
        if tooltip:
            self.add_tooltip(cb, tooltip)
        return container, cb

    def _create_checkbox(self, parent, text, variable, command=None, **kwargs):
        pack_keys = {'after', 'anchor', 'before', 'expand', 'fill', 'in', 'ipadx', 'ipady', 'padx', 'pady', 'side'}
        pack_opts = {k: v for k, v in kwargs.items() if k in pack_keys}
        widget_opts = {k: v for k, v in kwargs.items() if k not in pack_keys}
        
        # Override bg e add wraplength para evitar "div bug" (overflow)
        bg = widget_opts.pop('bg', self.bg_col) 
        chk = tk.Checkbutton(parent, text=text, variable=variable, command=command, bg=bg, cursor="hand2", wraplength=220, justify=tk.LEFT, fg=self.fg_col, selectcolor=self.surface_col, activebackground=self.surface_col, activeforeground="white", **widget_opts)
        if pack_opts:
            chk.pack(**pack_opts)
        return chk

    def _create_scrollable_listbox(self, parent, title=None, selectmode=tk.MULTIPLE, **pack_opts):
        frame = tk.Frame(parent, bg=self.bg_col)
        if title:
            tk.Label(frame, text=title, bg=self.bg_col, font=("Segoe UI", 9, "bold"), fg="#042F61").pack(anchor=tk.W)
            
        lb_frame = tk.Frame(frame, bg=self.surface_col, highlightbackground="#FFFFFF", highlightthickness=1)
        lb_frame.pack(fill=tk.BOTH, expand=True)
        
        lb = tk.Listbox(lb_frame, selectmode=selectmode, bg=self.surface_col, fg=self.fg_col, relief="flat", borderwidth=0, font=("Segoe UI", 10), cursor="hand2", selectbackground="#0D6EFD", selectforeground="white")
        sb = ttk.Scrollbar(lb_frame, orient="vertical", command=lb.yview, cursor="hand2")
        lb.configure(yscrollcommand=sb.set)
        
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        
        if pack_opts:
            frame.pack(**pack_opts)
            
        return frame, lb
        
    def toggle_tooltips(self):
        self.tooltips_active = not self.tooltips_active
        for tt in self.tooltips_registry:
            tt.enabled = self.tooltips_active
            if not self.tooltips_active:
                tt.hidetip()
        text = "💡 Desativar Dicas" if self.tooltips_active else "💡 Ativar Dicas"
        self.btn_toggle_tips.config(text=text)

    def add_tooltip(self, widget, text):
        tt = ModernTooltip(widget, text)
        self.tooltips_registry.append(tt)

    def _ask_file(self, var, lbl_widget, prefix):
        f = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if f: 
            var.set(f)
            short_name = f.split('/')[-1]
            lbl_widget.config(text=f"✅ {prefix}: {short_name}", fg="#198754", bg="#E8F5E9")
            self._check_auto_load()

    def _on_drop(self, event, var, lbl_widget, prefix):
        f = event.data.strip('{}')
        if f.endswith('.xlsx') or f.endswith('.xls'):
            var.set(f)
            short_name = f.split('\\\\')[-1].split('/')[-1]
            lbl_widget.config(text=f"✅ {prefix}: {short_name}", fg="#198754", bg="#E8F5E9")
            self._check_auto_load()
        else:
            messagebox.showerror("Erro de Formato", "Apenas planilhas Excel (.xlsx ou .xls) são aceitas.")
            
    def _check_auto_load(self):
        if self.file_src.get() and self.file_tgt.get():
            self.lbl_src_drop.dnd_bind('<<Drop>>', '')
            self.lbl_tgt_drop.dnd_bind('<<Drop>>', '')
            self.callbacks['on_files_selected'](self.file_src.get(), self.file_tgt.get())

    def build_upload_layer(self):
        f = ttk.LabelFrame(self.main_container, text=I18N["step1_title"])
        f.pack(fill=tk.X, pady=(0, 10), ipadx=0, ipady=5)
        
        container = tk.Frame(f, bg=self.bg_col)
        container.pack(fill=tk.X, expand=True)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        
        # Helper interno para os containers de drop para evitar repetição aqui
        def create_drop_zone(col, text, var, prefix):
            c = tk.Frame(container, bg="#FFFFFF", highlightbackground="#CED4DA", highlightthickness=2)
            c.grid(row=0, column=col, sticky="nsew", padx=10, pady=10, ipady=15)
            lbl = tk.Label(c, text=text, bg="#FFFFFF", fg="#6C757D", font=("Segoe UI", 11, "bold"), cursor="hand2")
            lbl.pack(expand=True, fill=tk.BOTH)
            lbl.drop_target_register(DND_FILES)
            lbl.dnd_bind('<<Drop>>', lambda e: self._on_drop(e, var, lbl, prefix))
            lbl.bind('<Button-1>', lambda e: self._ask_file(var, lbl, prefix))
            return lbl

        self.lbl_src_drop = create_drop_zone(0, I18N["lbl_src_idle"], self.file_src, "Origem")
        self.lbl_tgt_drop = create_drop_zone(1, I18N["lbl_tgt_idle"], self.file_tgt, "Destino")
        
        self.lbl_meta = tk.Label(f, text="", font=("Segoe UI", 9, "italic"), fg="#6C757D", bg=self.bg_col)
        self.lbl_meta.pack(side=tk.BOTTOM, pady=(10, 0))

    def build_keys_layer(self):
        self.f_keys = ttk.LabelFrame(self.main_container, text=I18N["step2_title"])
        self.f_keys.pack(fill=tk.X, pady=(0, 10), ipadx=0, ipady=5)
        
        self.ai_status_lbl = tk.Label(self.f_keys, text=I18N["ai_waiting"], font=("Segoe UI", 10), bg=self.bg_col, fg="#6C757D", justify=tk.LEFT)
        self.ai_status_lbl.pack(anchor=tk.W, padx=10, pady=2)
        self.ai_status_lbl.bind('<Double-Button-1>', self.show_ai_matches)
        
        row = tk.Frame(self.f_keys, bg=self.bg_col)
        row.pack(fill=tk.X, padx=10, pady=5)
        
        # Perfect weight logic for full responsiveness
        row.columnconfigure(1, weight=1) # src combo stretches
        row.columnconfigure(4, weight=1) # tgt combo stretches
        row.columnconfigure(6, weight=1) # tgt_final combo stretches

        # Col 0-1: Key Src
        _, self.combo_src = self._create_labeled_combo(row, I18N["lbl_key_src"], self.key_src, tooltip=I18N["tooltip_src"])
        self.combo_src.master.grid(row=0, column=0, columnspan=2, sticky="ew", padx=(0,10))
        self.combo_src.config(state="disabled")

        tk.Label(row, text="🔗 cruza com", bg=self.bg_col, fg="#2563EB", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="ew", padx=2)
        
        # Col 3-4: Key Tgt
        _, self.combo_tgt = self._create_labeled_combo(row, I18N["lbl_key_tgt"], self.key_tgt, tooltip=I18N["tooltip_tgt"])
        self.combo_tgt.master.grid(row=0, column=3, columnspan=2, sticky="ew", padx=(10,10))
        self.combo_tgt.config(state="disabled")
        
        f_tgt_final = tk.Frame(row, bg=self.bg_col)
        f_tgt_final.grid(row=0, column=5, columnspan=2, sticky="ew", padx=(10,10))
        
        tk.Label(f_tgt_final, text=I18N["lbl_fix_key"], bg=self.bg_col, fg="#FACC15", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        self.combo_tgt_final = ttk.Combobox(f_tgt_final, textvariable=self.key_tgt_final, state="disabled")
        self.combo_tgt_final.pack(fill=tk.X)
        self.key_tgt_final.set("Apenas se ativado")
        self.combo_tgt_final.config(foreground="#FACC15")
        self.add_tooltip(self.combo_tgt_final, I18N["tooltip_fix"])
        
        self.chk_fix_key_var = tk.BooleanVar(value=False)
        self.chk_fix_key = self._create_checkbox(f_tgt_final, I18N["chk_activate"], self.chk_fix_key_var, command=self.on_fix_key_toggle, anchor=tk.W)
        self.chk_fix_key.config(fg="#FACC15", font=("Segoe UI", 9, "bold"))
        
        self.btn_validate = self._create_button(row, I18N["btn_validate"], style="Warning.TButton", command=self.on_validate_clicked)
        self.btn_validate.grid(row=0, column=7, sticky="s", padx=(5, 0), pady=15)
        self.btn_validate.config(state="disabled")

    def on_fix_key_toggle(self):
        if self.chk_fix_key_var.get():
            self.combo_tgt_final.config(state="readonly" if self.cols_tgt else "normal", foreground=self.fg_col)
            if hasattr(self, 'last_tgt_final_val') and self.last_tgt_final_val != "Apenas se ativado": 
                self.key_tgt_final.set(self.last_tgt_final_val)
            else:
                self.key_tgt_final.set("")
        else:
            self.last_tgt_final_val = self.key_tgt_final.get()
            self.combo_tgt_final.config(state="disabled", foreground="#DC2626")
            self.key_tgt_final.set("Apenas se ativado")

    def set_keys_data(self, cols_src, cols_tgt, top_matches, len_src, len_tgt):
        self.cols_src = cols_src
        self.cols_tgt = cols_tgt
        self.top_matches = top_matches
        self.combo_src.config(state="readonly")
        self.combo_tgt.config(state="readonly")
        
        if self.chk_fix_key_var.get():
            self.combo_tgt_final.config(state="readonly")
        
        self.combo_src['values'] = cols_src
        self.combo_tgt['values'] = cols_tgt
        self.combo_tgt_final['values'] = cols_tgt
        self.btn_validate.config(state="normal")
        
        self.lbl_meta.config(text=f"📊 Analytics: Arquivo Origem possui {len_src:,} linhas | Arquivo Destino possui {len_tgt:,} linhas.".replace(',','.'))
        
        if top_matches:
            best = top_matches[0]
            self.key_src.set(best['src'])
            self.key_tgt.set(best['tgt'])
            
            if self.chk_fix_key_var.get():
                self.key_tgt_final.set(best['tgt'])
            else:
                self.last_tgt_final_val = best['tgt']
            
            placar = "🏆 Top Compatibilidades Matemáticas (Duplo clique para expandir):  "
            medals = ["🥇 1º", "🥈 2º", "🥉 3º"]
            for idx, m in enumerate(top_matches):
                if idx < 3: placar += f"| {medals[idx]}: '{m['src']}' 🔗 '{m['tgt']}' ({m['score']:,} matches) ".replace(',', '.')
            self.ai_status_lbl.config(text=placar, fg="#2563EB", font=("Segoe UI", 9, "bold"), cursor="hand2")
        else:
            self.ai_status_lbl.config(text="⚠️ A I.A não encontrou colunas compatíveis. Por favor, selecione as chaves manualmente abaixo.", fg="#EF4444", font=("Segoe UI", 9, "bold"), cursor="")
        
        self.root.update_idletasks() # Forçar atualização visual

    def show_ai_matches(self, event=None):
        if not hasattr(self, 'top_matches') or not self.top_matches:
            return
        msg = "💡 Relatório Completo do Scanner Lexical I.A\n\n"
        medals = ["🥇 1º Lugar", "🥈 2º Lugar", "🥉 3º Lugar", "🏅 4º Lugar", "🏅 5º Lugar", "🏅 6º Lugar"]
        for idx, m in enumerate(self.top_matches):
            medal = medals[idx] if idx < len(medals) else f"{idx+1}º Lugar"
            msg += f"{medal}:\nOrigem: '{m['src']}'\nDestino: '{m['tgt']}'\nForça: {m['score']:,} intersecções exatas\n\n".replace(',', '.')
        messagebox.showinfo("Motor I.A de Intersecção (Detalhes)", msg)

    def on_validate_clicked(self):
        if not self.key_src.get() or not self.key_tgt.get():
            messagebox.showwarning("Incompleto", "Selecione as chaves Origem e Destino Primária para cruzamento principal.")
            return

        if self.chk_fix_key_var.get():
            val = self.key_tgt_final.get()
            if not val or val == "Apenas se ativado" or val == "Escolha a chave protegida":
                messagebox.showwarning("Incompleto", "A Chave Protegida (A1) foi ativada. Por favor selecione a coluna correspondente.")
                return

        # Main validation only cares about src vs tgt intersections
        is_valid = self.callbacks.get('on_validate_keys', lambda a,b,c: True)(self.key_src.get(), self.key_tgt.get())
        if is_valid:
            if not self.chk_fix_key_var.get():
                self.key_tgt_final.set("") # Clear so backend skips it
                
            self.combo_src.config(state="disabled")
            self.combo_tgt.config(state="disabled")
            self.combo_tgt_final.config(state="disabled")
            self.chk_fix_key.config(state="disabled")
            self.btn_validate.config(text="✅ Chaves Blindadas", state="disabled")
            self.unlock_hub()

    def build_hub_layer(self):
        # f_hub uses expand=True so it claims all remaining vertical space
        self.f_hub = ttk.LabelFrame(self.main_container, text=I18N["step3_title"])
        self.f_hub.pack(fill=tk.BOTH, expand=True, pady=(0, 10), ipadx=5, ipady=5)
        
        # --- PERSPECTIVA 1: HUD & MAPPING AREA ---
        self.f_step3_hud = tk.Frame(self.f_hub, bg=self.bg_col)
        self.f_step3_hud.pack(fill=tk.X, pady=5)
        
        # HUD: Busca Preditiva I.A
        hud_c = tk.Frame(self.f_step3_hud, bg=self.bg_col)
        hud_c.pack(anchor=tk.N, pady=5)
        tk.Label(hud_c, text="🔍 " + I18N["hud_search"], bg=self.bg_col, fg="#0D6EFD", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=5)
        self.ent_search = tk.Entry(hud_c, width=40, font=("Segoe UI", 10), bg=self.surface_col, fg=self.fg_col, insertbackground="#0D6EFD", relief="solid", borderwidth=1, highlightthickness=0)
        self.ent_search.pack(side=tk.LEFT, padx=5)
        self.ent_search.bind("<KeyRelease>", self._on_search_keypress)
        
        self.btn_ai_map = self._create_button(hud_c, "🪄 Auto-Map I.A", style="Action.TButton", command=self._auto_map_ia, side=tk.LEFT, padx=10)
        
        self.btn_help = self._create_button(hud_c, "💡 " + I18N["btn_help"], style="TButton", command=self.toggle_tooltips, side=tk.RIGHT, padx=5)

        self.f_step3_mapping = tk.Frame(self.f_hub, bg=self.bg_col)
        self._build_mapping_area()
        
        # Status Bar (Collapsed Mapping)
        self.f_step3_status = tk.Frame(self.f_hub, bg=self.bg_col, highlightbackground="#FFFFFF", highlightthickness=1)
        self.lbl_status_msg = tk.Label(self.f_step3_status, text="", bg=self.bg_col, fg="#198754", font=("Segoe UI", 9, "bold italic"))
        self.lbl_status_msg.pack(side=tk.LEFT, padx=10, pady=2)
        self._create_button(self.f_step3_status, "✏️ " + I18N["btn_edit_mapping"], style="TButton", command=lambda: self.set_perspective("mapping"), side=tk.RIGHT, padx=5)

        # --- PERSPECTIVA 2: MODULE SELECTION (HUB) ---
        self.f_step3_selection = tk.Frame(self.f_hub, bg=self.bg_col)
        self._build_selection_area()

        # --- PERSPECTIVA 3: PROCESSING CONFIG (RULES) ---
        self.f_step3_processing = tk.Frame(self.f_hub, bg=self.bg_col)
        # ETL & CMP views are internal to processing
        self.f_etl_view = tk.Frame(self.f_step3_processing, bg=self.bg_col)
        self.f_cmp_view = tk.Frame(self.f_step3_processing, bg=self.bg_col)
        self.build_etl_ui()
        self.build_cmp_ui()

        # Initial State
        self.set_perspective("mapping")

    def set_perspective(self, name):
        """Gerencia as transições dinâmicas (Phoenix Architecture)"""
        # Limpa tudo
        self.f_step3_hud.pack_forget()
        self.f_step3_mapping.pack_forget()
        self.f_step3_status.pack_forget()
        self.f_step3_selection.pack_forget()
        self.f_step3_processing.pack_forget()
        
        if name == "mapping":
            self.f_step3_hud.pack(fill=tk.X)
            self.f_step3_mapping.pack(fill=tk.BOTH, expand=True)
            self.f_hub.config(text=I18N["step3_title"])
            
        elif name == "selection":
            # Quando selecionando módulo, encolhe o mapeamento para uma barra de status
            self.f_step3_status.pack(fill=tk.X, pady=5)
            self._update_status_bar()
            self.f_step3_selection.pack(fill=tk.X, expand=True, pady=20)
            self.f_hub.config(text="🏁 " + I18N["step3_select_mod"])
            
        elif name == "processing":
            self.f_step3_status.pack(fill=tk.X, pady=5)
            self.f_step3_processing.pack(fill=tk.BOTH, expand=True)
            self.f_hub.config(text="⚙️ " + I18N["step3_config"])
            
        # Smart Auto-Scroll para Laptop
        self.root.after(100, lambda: self.scroll_wrapper.canvas.yview_moveto(1.0))
        self._show_floating_hint(I18N["hint_scroll"])

    def _show_floating_hint(self, message):
        """Cria uma notificação flutuante sutil (Steel Cyber Bubble)"""
        if hasattr(self, 'f_hint') and self.f_hint.winfo_exists():
            self.f_hint.destroy()
            
        # Design ultra-minimalista arredondado Slate
        self.f_hint = tk.Frame(self.root, bg=self.surface_col, highlightbackground="#60A5FA", highlightthickness=1)
        self.f_hint.place(relx=0.5, rely=0.92, anchor=tk.CENTER)
        
        msg_l = tk.Label(self.f_hint, text=message, bg=self.surface_col, fg=self.fg_col, font=("Segoe UI", 9, "bold"), cursor="hand2")
        msg_l.pack(side=tk.LEFT, padx=(12, 4), pady=5)
        msg_l.bind("<Button-1>", lambda e: self.f_hint.destroy())
        
        btn_close = tk.Button(self.f_hint, text="✕", command=self.f_hint.destroy, bg=self.surface_col, fg="#60A5FA", relief="flat", font=("Segoe UI", 8, "bold"), cursor="hand2", activebackground="#34D399")
        btn_close.pack(side=tk.LEFT, padx=(4, 10), pady=5)
        
        self.root.after(4500, lambda: self.f_hint.destroy() if self.f_hint.winfo_exists() else None)

    def _update_status_bar(self):
        target_cols = [c for c in self.lb_tgt.get(0, tk.END) if c != self.watermark_text]
        if not target_cols:
            self.lbl_status_msg.config(text="⚠️ Nenhum mapeamento definido. As colunas originais serão mantidas como backup.", fg="#DC2626")
        else:
            txt = f"📦 {len(target_cols)} colunas mapeadas comercialmente: " + ", ".join(target_cols[:3])
            if len(target_cols) > 3:
                txt += f" (+{len(target_cols)-3})"
            self.lbl_status_msg.config(text=txt, fg="#1E293B")

    def _build_mapping_area(self):
        f = self.f_step3_mapping
        f.columnconfigure(0, weight=1)
        f.columnconfigure(1, weight=0)
        f.columnconfigure(2, weight=1)
        f.rowconfigure(0, weight=1)
        
        # Listbox Esquerda
        _, self.lb_src = self._create_scrollable_listbox(f, title=I18N["lbl_av_cols"])
        self.lb_src.master.master.grid(row=0, column=0, sticky="nsew", padx=5)
        self.lb_src.bind('<Double-Button-1>', self._move_to_tgt)
        
        # Botões Meio
        mid_btns = tk.Frame(f, bg=self.bg_col)
        mid_btns.grid(row=0, column=1, padx=10, sticky="")
        self._create_button(mid_btns, "⏩", command=self._move_all_to_tgt, pady=5, tooltip=I18N["btn_move_all"])
        self._create_button(mid_btns, "▶️", command=self._move_to_tgt, pady=5, tooltip=I18N["btn_move"])
        self._create_button(mid_btns, "◀️", command=self._remove_from_tgt, pady=5, tooltip=I18N["btn_remove"])
        self._create_button(mid_btns, "⏪", command=self._remove_all_from_tgt, pady=5, tooltip=I18N["btn_remove_all"])
        
        # Listbox Direita
        _, self.lb_tgt = self._create_scrollable_listbox(f, title=I18N["lbl_sync_cols"])
        self.lb_tgt.master.master.grid(row=0, column=2, sticky="nsew", padx=5)
        self.lb_tgt.config(bg="#E9ECEF", fg="#6C757D") 
        self.lb_tgt.bind('<Double-Button-1>', self._remove_from_tgt)
        
        # Botão Próximo (Fixado na área de mapeamento)
        mapping_footer = tk.Frame(f, bg=self.bg_col)
        mapping_footer.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10,0))
        self.btn_next_passo = self._create_button(mapping_footer, "🚀 " + I18N["btn_next"], style="Success.TButton", command=lambda: self.set_perspective("selection"))
        self.btn_next_passo.pack(side=tk.RIGHT, padx=20, pady=10)
        self.btn_next_passo.config(state="disabled")

    def _build_selection_area(self):
        f = self.f_step3_selection
        self.btn_mod_etl = self._create_button(f, I18N["mod_etl"], command=lambda: self.switch_module('etl'), side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(20, 10), ipady=15)
        self.btn_mod_cmp = self._create_button(f, I18N["mod_cmp"], command=lambda: self.switch_module('cmp'), side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=(10, 20), ipady=15)
        
    def _on_search_keypress(self, event=None):
        query = self.ent_search.get().lower().strip()
        self.lb_src.delete(0, tk.END)
        
        # Filtragem Inteligente: Prioriza começos, depois contenções
        exact_matches = [c for c in self.cols_src if c.lower().startswith(query)]
        substring_matches = [c for c in self.cols_src if query in c.lower() and c not in exact_matches]
        
        for col in exact_matches + substring_matches:
            # Não mostra o que já foi movido para o TGT
            if col not in self.lb_tgt.get(0, tk.END):
                self.lb_src.insert(tk.END, col)

    def _auto_map_ia(self):
        """Mapeamento automatizado inteligente (Exact Match & Best Guesses)"""
        self._remove_watermark_if_exists()
        matched_count = 0
        
        # 1. Tentar encontrar colunas que existam no destino com o mesmo nome
        for i in reversed(range(self.lb_src.size())):
            src_col = self.lb_src.get(i)
            # Se a coluna existe no destino e ainda não foi mapeada
            if src_col in self.cols_tgt:
                self.lb_tgt.insert(tk.END, src_col)
                self.lb_src.delete(i)
                matched_count += 1
                
        self._update_sync_summary()
        self._update_status_bar()
        
        if matched_count > 0:
            messagebox.showinfo("I.A Sync", f"🪄 Sucesso! {matched_count} colunas foram sincronizadas automaticamente por equivalência de nome.")
        else:
            messagebox.showinfo("I.A Sync", "A I.A não encontrou nomes idênticos automáticos. Por favor, use a busca preditiva.")

    def switch_module(self, name):
        self.set_perspective("processing")
        if name == 'etl':
            self.f_cmp_view.pack_forget()
            self.f_etl_view.pack(fill=tk.BOTH, expand=True, pady=10)
            self.btn_mod_etl.config(style="Action.TButton")
            self.btn_mod_cmp.config(style="TButton")
            self.current_hub_module = 'etl'
        else:
            self.f_etl_view.pack_forget()
            self.f_cmp_view.pack(fill=tk.BOTH, expand=True, pady=10)
            self.btn_mod_cmp.config(style="Action.TButton")
            self.btn_mod_etl.config(style="TButton")
            self.current_hub_module = 'cmp'

    # --- SUB-MODULO: ETL ---
    def build_etl_ui(self):
        # Define bottom container first, pack it to bottom so it's guaranteed visible
        bottom_container = tk.Frame(self.f_etl_view, bg=self.bg_col)
        bottom_container.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Navigation bar (Phoenix Style)
        nav_top = tk.Frame(self.f_etl_view, bg=self.bg_col)
        nav_top.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        self._create_button(nav_top, "⬅️ " + I18N["btn_back_selection"], command=lambda: self.set_perspective("selection"), side=tk.LEFT)
        tk.Label(nav_top, text=I18N["mod_etl"], font=("Segoe UI", 12, "bold"), fg="#2563EB", bg=self.bg_col).pack(side=tk.LEFT, padx=20)
        
        
        lbl_acc = tk.Label(bottom_container, text=I18N["lbl_acc_cols"], bg=self.bg_col, fg="#0DCAF0", font=("Segoe UI", 9, "bold"))
        lbl_acc.pack(anchor=tk.W, pady=(5,0))
        
        self.txt_acc_cols = tk.Text(bottom_container, height=2, bg=self.surface_col, fg="#0D6EFD", font=("Segoe UI", 9, "bold"), relief="solid", borderwidth=1, padx=10, pady=5)
        self.txt_acc_cols.pack(fill=tk.X, pady=(0,5))
        self.txt_acc_cols.insert(tk.END, I18N["none_selected"])
        self.txt_acc_cols.config(state=tk.DISABLED)
        
        bot_f = tk.Frame(bottom_container, bg=self.bg_col)
        bot_f.pack(fill=tk.X, pady=5)
        bot_f.columnconfigure(0, weight=1)
        bot_f.columnconfigure(1, weight=1)

        f_regras_linha = ttk.LabelFrame(bot_f, text=I18N["rules_row"])
        f_regras_linha.grid(row=0, column=0, sticky="nsew", padx=(0,5))
        
        self.chk_zeros = tk.BooleanVar(value=False)
        self._create_checkbox(f_regras_linha, text=I18N["chk_zeros"], variable=self.chk_zeros, anchor=tk.W, padx=5, pady=2)
        
        self.lb_zeros_cols = tk.Listbox(f_regras_linha, selectmode=tk.MULTIPLE, bg=self.surface_col, fg=self.fg_col, height=6, relief="flat", borderwidth=0, highlightthickness=1, highlightbackground="#334155", cursor="hand2")
        self.lb_zeros_cols.pack(fill=tk.X, padx=5, pady=5)
        
        f_regras_est = ttk.LabelFrame(bot_f, text=I18N["rules_struct"])
        f_regras_est.grid(row=0, column=1, sticky="nsew", padx=(5,0))

        self.chk_clean_out = tk.BooleanVar(value=True)
        self.chk_trim = tk.BooleanVar(value=True)
        self.chk_upper = tk.BooleanVar(value=True)
        
        self._create_checkbox(f_regras_est, I18N["chk_only_mapped"], self.chk_clean_out)
        self._create_checkbox(f_regras_est, I18N["chk_trim"], self.chk_trim)
        self._create_checkbox(f_regras_est, I18N["chk_upper"], self.chk_upper)
        
        nav = ttk.Frame(bottom_container)
        nav.pack(fill=tk.X, pady=10)
        
        export_f = tk.Frame(nav, bg=self.bg_col)
        export_f.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(export_f, text=I18N["lbl_output"], bg=self.bg_col, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        
        excel_rb = tk.Radiobutton(export_f, text="Excel", variable=self.export_fmt, value=".xlsx", bg=self.bg_col, font=("Segoe UI", 9, "bold"))
        excel_rb.pack(side=tk.LEFT, padx=2)
        
        warn_f = tk.Frame(export_f, bg=self.bg_col, highlightbackground="#DC2626", highlightthickness=1)
        warn_f.pack(side=tk.LEFT, padx=10, fill=tk.Y, pady=2)
        tk.Label(warn_f, text=I18N["lbl_experimental"], bg=self.bg_col, fg="#DC2626", font=("Segoe UI", 8, "bold")).pack(side=tk.LEFT, padx=(4,2))
        
        csv_rb = tk.Radiobutton(warn_f, text="CSV", variable=self.export_fmt, value=".csv", bg=self.bg_col)
        csv_rb.pack(side=tk.LEFT, padx=2)
        sql_rb = tk.Radiobutton(warn_f, text="SQL", variable=self.export_fmt, value=".sql", bg=self.bg_col)
        sql_rb.pack(side=tk.LEFT, padx=2)
        json_rb = tk.Radiobutton(warn_f, text="JSON", variable=self.export_fmt, value=".json", bg=self.bg_col)
        json_rb.pack(side=tk.LEFT, padx=2)
        
        self.add_tooltip(excel_rb, "Planilha Excel (Estável). Demora mais para processar grandes volumes.")
        self.add_tooltip(warn_f, I18N["tooltip_exp"])
        
        self.btn_run_etl = self._create_button(nav, I18N["btn_run_etl"], style="Success.TButton", command=self.on_process, side=tk.RIGHT, ipadx=20)
        self.btn_reset_etl = self._create_button(nav, I18N["btn_reset"], style="Danger.TButton", command=self.callbacks.get('on_reset', lambda: None), side=tk.RIGHT, padx=(0, 10), ipadx=10)
        
    # --- SUB-MODULO: COMPARADOR (GAPS) ---
    def build_cmp_ui(self):
        f = tk.Frame(self.f_cmp_view, bg="#FFFFFF", highlightbackground="#CED4DA", highlightthickness=1)
        f.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, ipady=20)
        
        # Navigation bar (Phoenix Style)
        nav_top = tk.Frame(f, bg="#FFFFFF")
        nav_top.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        self._create_button(nav_top, "⬅️ " + I18N["btn_back_selection"], command=lambda: self.set_perspective("selection"), side=tk.LEFT, padx=10)
        
        cmp_footer = tk.Frame(f, bg="#FFFFFF")
        cmp_footer.pack(side=tk.BOTTOM, fill=tk.X, pady=15)
        
        tk.Label(f, text=I18N["auditory_title"], font=("Segoe UI", 14, "bold"), fg="#DC3545", bg="#FFFFFF").pack(pady=(15, 5))
        tk.Label(f, text=I18N["auditory_desc"], font=("Segoe UI", 10), fg="#6C757D", bg="#FFFFFF", justify=tk.CENTER).pack()
        
        lbl_acc = tk.Label(f, text="Opções de Comparação de Arquivos:", bg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        lbl_acc.pack(anchor=tk.W, padx=10, pady=(15, 0))

        mod_f = ttk.LabelFrame(f, text=I18N["rules_direction"])
        mod_f.pack(fill=tk.X, padx=10, pady=5)
        
        self.cmp_direction = tk.StringVar(value="Falta no Destino")
        tk.Radiobutton(mod_f, text=I18N["opt_miss_tgt"], variable=self.cmp_direction, value="Falta no Destino", bg="#FFFFFF", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=5)
        tk.Radiobutton(mod_f, text=I18N["opt_miss_src"], variable=self.cmp_direction, value="Falta na Origem", bg="#FFFFFF", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=5)
        
        self.chk_cmp_clean = tk.BooleanVar(value=True)
        self._create_checkbox(mod_f, I18N["chk_cmp_clean"], self.chk_cmp_clean, bg="#FFFFFF", font=("Segoe UI", 10, "bold"), padx=10, pady=(10, 5))
        
        self.txt_cmp_status = tk.Text(f, height=3, bg="#F0F0F0", fg="#6C757D", font=("Segoe UI", 9))
        self.txt_cmp_status.pack(fill=tk.X, padx=10, pady=(10, 0))
        self.txt_cmp_status.insert(tk.END, "")
        self.txt_cmp_status.config(state=tk.DISABLED)

        self.btn_next_cmp = self._create_button(cmp_footer, "🚀 " + I18N["btn_run_cmp"], style="Success.TButton", command=self.on_process)
        self.btn_next_cmp.pack(side=tk.RIGHT, padx=20, pady=10)
        self.btn_reset_cmp = self._create_button(cmp_footer, I18N["btn_reset"], style="Danger.TButton", command=self.callbacks.get('on_reset', lambda: None), side=tk.RIGHT, padx=(0, 10), ipadx=10)
        
        export_f = tk.Frame(cmp_footer, bg=self.bg_col)
        export_f.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(export_f, text=I18N["lbl_output"], bg=self.bg_col, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        
        excel_rb = tk.Radiobutton(export_f, text="Excel", variable=self.export_fmt, value=".xlsx", bg=self.bg_col, font=("Segoe UI", 9, "bold"))
        excel_rb.pack(side=tk.LEFT, padx=2)
        
        warn_f = tk.Frame(export_f, bg=self.bg_col, highlightbackground="#DC2626", highlightthickness=1)
        warn_f.pack(side=tk.LEFT, padx=10, fill=tk.Y, pady=2)
        tk.Label(warn_f, text=I18N["lbl_experimental"], bg=self.bg_col, fg="#DC2626", font=("Segoe UI", 8, "bold")).pack(side=tk.LEFT, padx=(4,2))
        
        csv_rb = tk.Radiobutton(warn_f, text="CSV", variable=self.export_fmt, value=".csv", bg=self.bg_col)
        csv_rb.pack(side=tk.LEFT, padx=2)
        sql_rb = tk.Radiobutton(warn_f, text="SQL", variable=self.export_fmt, value=".sql", bg=self.bg_col)
        sql_rb.pack(side=tk.LEFT, padx=2)
        json_rb = tk.Radiobutton(warn_f, text="JSON", variable=self.export_fmt, value=".json", bg=self.bg_col)
        json_rb.pack(side=tk.LEFT, padx=2)


    def _update_sync_summary(self):
        target_cols = list(self.lb_tgt.get(0, tk.END))
        if self.watermark_text in target_cols:
            target_cols.remove(self.watermark_text)
            
        self.txt_acc_cols.config(state=tk.NORMAL)
        self.txt_acc_cols.delete(1.0, tk.END)
        
        self.lb_zeros_cols.delete(0, tk.END)
        
        if not target_cols:
            self.txt_acc_cols.insert(tk.END, I18N["none_selected"])
            self.txt_acc_cols.config(fg="#6C757D")
        else:
            self.txt_acc_cols.insert(tk.END, ", ".join(target_cols))
            self.txt_acc_cols.config(fg="#0b5ed7")
            for c in target_cols:
                self.lb_zeros_cols.insert(tk.END, c)
                
        self.txt_acc_cols.config(state=tk.DISABLED)

    def unlock_hub(self):
        self.btn_mod_etl.config(state="normal")
        self.btn_mod_cmp.config(state="normal")
        self.btn_next_mapping.config(state="normal")
        # Go to mapping first
        self.set_perspective("mapping")
        
        self.lb_src.config(bg="#FFFFFF", fg="#212529")
        self.lb_tgt.config(bg="#E8F5E9", fg="#212529")
        
        self.lb_src.delete(0, tk.END)
        for c in self.cols_src: self.lb_src.insert(tk.END, c)
        
        self.lb_tgt.delete(0, tk.END)
        self.lb_tgt.insert(tk.END, self.watermark_text)
        self._update_sync_summary()

    def _remove_watermark_if_exists(self):
        try:
            if self.lb_tgt.get(0) == self.watermark_text:
                self.lb_tgt.delete(0)
        except: pass

    def _add_watermark_if_empty(self):
        if self.lb_tgt.size() == 0:
            self.lb_tgt.insert(tk.END, self.watermark_text)

    def _move_to_tgt(self, event=None):
        self._remove_watermark_if_exists()
        sel = self.lb_src.curselection()
        for i in reversed(sel):
            val = self.lb_src.get(i)
            self.lb_tgt.insert(tk.END, val)
            self.lb_src.delete(i)
        self._update_sync_summary()
            
    def _move_all_to_tgt(self):
        self._remove_watermark_if_exists()
        for i in reversed(range(self.lb_src.size())):
            val = self.lb_src.get(i)
            self.lb_tgt.insert(tk.END, val)
            self.lb_src.delete(i)
        self._update_sync_summary()

    def _remove_from_tgt(self, event=None):
        sel = self.lb_tgt.curselection()
        for i in reversed(sel):
            val = self.lb_tgt.get(i)
            if val == self.watermark_text: continue
            self.lb_src.insert(tk.END, val)
            self.lb_tgt.delete(i)
        self._add_watermark_if_empty()
        self._update_sync_summary()
            
    def _remove_all_from_tgt(self):
        for i in reversed(range(self.lb_tgt.size())):
            val = self.lb_tgt.get(i)
            if val == self.watermark_text: continue
            self.lb_src.insert(tk.END, val)
            self.lb_tgt.delete(i)
        self._add_watermark_if_empty()
        self._update_sync_summary()

    def get_final_inputs(self):
        target_cols = list(self.lb_tgt.get(0, tk.END))
        if self.watermark_text in target_cols:
            target_cols.remove(self.watermark_text)
            
        zero_cols = []
        if self.chk_zeros.get():
            sel = self.lb_zeros_cols.curselection()
            if sel:
                zero_cols = [self.lb_zeros_cols.get(i) for i in sel]
            
        clean_out = self.chk_clean_out.get() if self.current_hub_module == "etl" else self.chk_cmp_clean.get()
            
        return {
            "current_mode": self.current_hub_module,  # 'etl' or 'cmp'
            "cols_mapped": target_cols,
            "export_fmt": self.export_fmt.get(),
            "chk_upper": self.chk_upper.get(),
            "chk_trim": self.chk_trim.get(),
            "chk_zeros": self.chk_zeros.get(),
            "zero_cols": zero_cols,
            "module": "Limpar" if self.current_hub_module == "etl" else self.cmp_direction.get(),
            "clean_output": clean_out,
            "key_src": self.key_src.get(),
            "key_tgt": self.key_tgt.get(),
            "key_tgt_final": self.key_tgt_final.get(),
            "file_src": self.file_src.get(),
            "file_tgt": self.file_tgt.get()
        }

    def on_process(self):
        inputs = self.get_final_inputs()
        if inputs["current_mode"] == "etl" and not inputs["cols_mapped"]:
            messagebox.showwarning("Aviso", "A lista de colunas para migrar (lado direito) está vazia.")
            return
            
        self.btn_run_etl.config(state="disabled")
        self.btn_run_cmp.config(state="disabled")
        self.callbacks['on_process'](inputs)
        
    def unlock_ui(self):
        self.btn_run_etl.config(state="normal")
        self.btn_run_cmp.config(state="normal")
