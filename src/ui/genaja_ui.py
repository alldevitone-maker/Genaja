import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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
                         background="#1E293B", foreground="#F8FAFC", relief=tk.SOLID, borderwidth=1,
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
        self.canvas = tk.Canvas(self, bg=kwargs.get('bg', '#F1F5F9'), highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=kwargs.get('bg', '#F1F5F9'))

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

class GenajaUI:
    def __init__(self, root, title, version, callbacks):
        self.root = root
        self.root.title(f"{title} - Inteligência de Sincronização (v{version}) - Hub Unificado Flex")
        self.root.geometry("1100x950")
        
        self.style = ttk.Style(self.root)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")
        
        self.bg_col = "#F1F5F9"  
        self.fg_col = "#0F172A"  
        self.root.configure(bg=self.bg_col)
        
        self.style.configure(".", background=self.bg_col, foreground=self.fg_col, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=self.bg_col)
        self.style.configure("TLabelframe", background=self.bg_col, foreground="#1E293B", font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabelframe.Label", background=self.bg_col, foreground="#1E293B", font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabel", background=self.bg_col, foreground=self.fg_col)
        
        self.style.configure("TButton", padding=6, relief="flat", background="#E2E8F0", foreground="#334155", font=("Segoe UI", 10, "bold"))
        self.style.map("TButton", background=[("active", "#CBD5E1")])
        self.style.configure("Action.TButton", background="#2563EB", foreground="white")
        self.style.map("Action.TButton", background=[("active", "#1D4ED8")])
        self.style.configure("Success.TButton", background="#059669", foreground="white")
        self.style.map("Success.TButton", background=[("active", "#047857")])
        self.style.configure("Warning.TButton", background="#D97706", foreground="white")
        self.style.map("Warning.TButton", background=[("active", "#B45309")])
        self.style.configure("Danger.TButton", background="#DC2626", foreground="white")
        self.style.map("Danger.TButton", background=[("active", "#B91C1C")])
        
        self.callbacks = callbacks
        self.watermark_text = "--- Selecione e Transfira para Cá ---"
        
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
        self.btn_toggle_tips = ttk.Button(self.top_nav, text="💡 Desativar Dicas", command=self.toggle_tooltips)
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
        f = ttk.LabelFrame(self.main_container, text=" 📂 Passo 1: Arraste e Solte suas Planilhas ou Clique no Botão ")
        f.pack(fill=tk.X, pady=(0, 10), ipadx=0, ipady=5)
        
        container = tk.Frame(f, bg=self.bg_col)
        container.pack(fill=tk.X, expand=True)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        
        c1 = tk.Frame(container, bg="#FFFFFF", highlightbackground="#CED4DA", highlightthickness=2)
        c1.grid(row=0, column=0, sticky="nsew", padx=10, pady=5, ipady=5)
        self.lbl_src_drop = tk.Label(c1, text="📁 Arraste a ORIGEM aqui\\nou clique para buscar", bg="#FFFFFF", fg="#6C757D", font=("Segoe UI", 11, "bold"))
        self.lbl_src_drop.pack(expand=True)
        self.lbl_src_drop.drop_target_register(DND_FILES)
        self.lbl_src_drop.dnd_bind('<<Drop>>', lambda e: self._on_drop(e, self.file_src, self.lbl_src_drop, "Origem"))
        self.lbl_src_drop.bind('<Button-1>', lambda e: self._ask_file(self.file_src, self.lbl_src_drop, "Origem"))
        
        c2 = tk.Frame(container, bg="#FFFFFF", highlightbackground="#CED4DA", highlightthickness=2)
        c2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10, ipady=15)
        self.lbl_tgt_drop = tk.Label(c2, text="📁 Arraste o DESTINO aqui\\nou clique para buscar", bg="#FFFFFF", fg="#6C757D", font=("Segoe UI", 11, "bold"))
        self.lbl_tgt_drop.pack(expand=True)
        self.lbl_tgt_drop.drop_target_register(DND_FILES)
        self.lbl_tgt_drop.dnd_bind('<<Drop>>', lambda e: self._on_drop(e, self.file_tgt, self.lbl_tgt_drop, "Destino"))
        self.lbl_tgt_drop.bind('<Button-1>', lambda e: self._ask_file(self.file_tgt, self.lbl_tgt_drop, "Destino"))
        
        self.lbl_meta = tk.Label(f, text="", font=("Segoe UI", 9, "italic"), fg="#6C757D", bg=self.bg_col)
        self.lbl_meta.pack(side=tk.BOTTOM, pady=(10, 0))

    def build_keys_layer(self):
        self.f_keys = ttk.LabelFrame(self.main_container, text=" 🧠 Passo 2: Intersecção Matemática & Protected Keys ")
        self.f_keys.pack(fill=tk.X, pady=(0, 10), ipadx=0, ipady=5)
        
        self.ai_status_lbl = tk.Label(self.f_keys, text="Aguardando planilhas para varredura I.A...", font=("Segoe UI", 10), bg=self.bg_col, fg="#6C757D", justify=tk.LEFT)
        self.ai_status_lbl.pack(anchor=tk.W, padx=10, pady=2)
        self.ai_status_lbl.bind('<Double-Button-1>', self.show_ai_matches)
        
        row = tk.Frame(self.f_keys, bg=self.bg_col)
        row.pack(fill=tk.X, padx=10, pady=5)
        
        # Perfect weight logic for full responsiveness
        row.columnconfigure(1, weight=1) # src combo stretches
        row.columnconfigure(4, weight=1) # tgt combo stretches
        row.columnconfigure(6, weight=1) # tgt_final combo stretches

        tk.Label(row, text="Chave na Origem:", bg=self.bg_col, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="e", padx=(0,5))
        self.combo_src = ttk.Combobox(row, textvariable=self.key_src, state="disabled")
        self.combo_src.grid(row=0, column=1, sticky="ew", padx=(0,10))
        
        tk.Label(row, text="🔗 cruza com", bg=self.bg_col, fg="#0b5ed7", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="ew", padx=2)
        
        tk.Label(row, text="Chave Destino:", bg=self.bg_col, font=("Segoe UI", 9, "bold")).grid(row=0, column=3, sticky="e", padx=(10,5))
        self.combo_tgt = ttk.Combobox(row, textvariable=self.key_tgt, state="disabled")
        self.combo_tgt.grid(row=0, column=4, sticky="ew", padx=(0,10))
        
        f_tgt_final = tk.Frame(row, bg=self.bg_col)
        f_tgt_final.grid(row=0, column=5, columnspan=2, sticky="ew", padx=(10,10))
        
        tk.Label(f_tgt_final, text="⭐ Fixar Chave\\n(Posição A1)", bg=self.bg_col, fg="#D97706", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        self.combo_tgt_final = ttk.Combobox(f_tgt_final, textvariable=self.key_tgt_final, state="disabled")
        self.combo_tgt_final.pack(fill=tk.X)
        self.key_tgt_final.set("Apenas se ativado")
        self.combo_tgt_final.config(foreground="#DC2626")
        
        self.chk_fix_key_var = tk.BooleanVar(value=False)
        self.chk_fix_key = tk.Checkbutton(f_tgt_final, text="Ativar", variable=self.chk_fix_key_var, bg=self.bg_col, fg="#DC2626", font=("Segoe UI", 9, "bold"), command=self.on_fix_key_toggle)
        self.chk_fix_key.pack(anchor=tk.W)
        
        self.btn_validate = ttk.Button(row, text="🔒 Validar", style="Warning.TButton", state="disabled", command=self.on_validate_clicked)
        self.btn_validate.grid(row=0, column=7, sticky="s", padx=(5, 0), pady=15)
        
        self.add_tooltip(self.combo_src, "Coluna de Identificação Principal na Planilha de Origem (Ex: ID, CPF, Codigo)")
        self.add_tooltip(self.combo_tgt, "Coluna Equivalente na Planilha Destino. As duas formam o Cruzamento principal.")
        self.add_tooltip(self.combo_tgt_final, "Força essa chave a sempre ser a Primeira Coluna (A1) no Relatório Excel Exportado.")
        self.add_tooltip(self.chk_fix_key, "Desativa a dependência da Chave Protegida A1. Marque para forçar a formatação.")

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
            self.ai_status_lbl.config(text=placar, fg="#0284c7", font=("Segoe UI", 9, "bold"), cursor="hand2")
        else:
            self.ai_status_lbl.config(text=":( A I.A não encontrou colunas com dados idênticos. Selecione manualmente.", fg="#DC2626", font=("Segoe UI", 9, "bold"), cursor="")

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

    # --- CAMADA 3: O HUB MULTI-MODULOS ---
    def build_hub_layer(self):
        # f_hub uses expand=True so it claims all remaining vertical space!
        self.f_hub = ttk.LabelFrame(self.main_container, text=" ⚙️ Passo 3: Módulos de Execução Integrados ")
        self.f_hub.pack(fill=tk.BOTH, expand=True, pady=(0, 10), ipadx=5, ipady=5)
        
        # Area dos Giant Buttons
        self.f_mod_select = tk.Frame(self.f_hub, bg=self.bg_col)
        self.f_mod_select.pack(fill=tk.X, pady=5)
        self.btn_mod_etl = ttk.Button(self.f_mod_select, text="🧹 Módulo Sincronização e Limpeza (ETL)", command=lambda: self.switch_module('etl'), state="disabled")
        self.btn_mod_etl.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(10, 5), ipady=5)
        self.btn_mod_cmp = ttk.Button(self.f_mod_select, text="⚖️ Módulo Comparador Púro (Auditoria)", command=lambda: self.switch_module('cmp'), state="disabled")
        self.btn_mod_cmp.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=(5, 10), ipady=5)
        
        # Containers Modulares Escondidos - They take full size when packed
        self.f_etl_module = tk.Frame(self.f_hub, bg=self.bg_col)
        self.f_cmp_module = tk.Frame(self.f_hub, bg=self.bg_col)
        
        self.build_etl_ui()
        self.build_cmp_ui()

    def switch_module(self, name):
        if name == 'etl':
            self.f_cmp_module.pack_forget()
            self.f_etl_module.pack(fill=tk.BOTH, expand=True, pady=10)
            self.btn_mod_etl.config(style="Action.TButton")
            self.btn_mod_cmp.config(style="TButton")
            self.current_hub_module = 'etl'
        else:
            self.f_etl_module.pack_forget()
            self.f_cmp_module.pack(fill=tk.BOTH, expand=True, pady=10)
            self.btn_mod_cmp.config(style="Action.TButton")
            self.btn_mod_etl.config(style="TButton")
            self.current_hub_module = 'cmp'

    # --- SUB-MODULO: ETL ---
    def build_etl_ui(self):
        # Define bottom container first, pack it to bottom so it's guaranteed visible
        bottom_container = tk.Frame(self.f_etl_module, bg=self.bg_col)
        bottom_container.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Responsiveness vertically
        maps_f = tk.Frame(self.f_etl_module, bg=self.bg_col)
        maps_f.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        
        maps_f.columnconfigure(0, weight=1)
        maps_f.columnconfigure(1, weight=0)
        maps_f.columnconfigure(2, weight=1)
        maps_f.rowconfigure(1, weight=1) # The listboxes row expands dynamically!
        
        tk.Label(maps_f, text="Colunas Disponíveis (Origem)", bg=self.bg_col, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky='w')
        tk.Label(maps_f, text="A Sincronizar (Destino Final)", bg=self.bg_col, font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky='w')
        
        f_left = tk.Frame(maps_f, bg=self.bg_col)
        f_left.grid(row=1, column=0, sticky="nsew", padx=5)
        self.lb_src = tk.Listbox(f_left, selectmode=tk.MULTIPLE, bg="#E9ECEF", fg="#6C757D", relief="solid", borderwidth=1)
        sb_src = ttk.Scrollbar(f_left, orient="vertical", command=self.lb_src.yview)
        self.lb_src.configure(yscrollcommand=sb_src.set)
        self.lb_src.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb_src.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb_src.bind('<Double-Button-1>', self._move_to_tgt)
        
        mid_btns = tk.Frame(maps_f, bg=self.bg_col)
        mid_btns.grid(row=1, column=1, padx=10, sticky="")
        self.btn_trasp_all = ttk.Button(mid_btns, text=">> Transpor Todas", command=self._move_all_to_tgt)
        self.btn_trasp_all.pack(pady=(0, 10))
        self.btn_trasp = ttk.Button(mid_btns, text="> Transpor Seção", command=self._move_to_tgt)
        self.btn_trasp.pack(pady=5)
        self.btn_remov = ttk.Button(mid_btns, text="< Remover Seção", command=self._remove_from_tgt)
        self.btn_remov.pack(pady=5)
        self.btn_remov_all = ttk.Button(mid_btns, text="<< Remover Todas", command=self._remove_all_from_tgt)
        self.btn_remov_all.pack(pady=(10, 0))
        
        f_right = tk.Frame(maps_f, bg=self.bg_col)
        f_right.grid(row=1, column=2, sticky="nsew", padx=5)
        self.lb_tgt = tk.Listbox(f_right, selectmode=tk.MULTIPLE, bg="#E9ECEF", fg="#6C757D", relief="solid", borderwidth=1)
        sb_tgt = ttk.Scrollbar(f_right, orient="vertical", command=self.lb_tgt.yview)
        self.lb_tgt.configure(yscrollcommand=sb_tgt.set)
        self.lb_tgt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb_tgt.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb_tgt.bind('<Double-Button-1>', self._remove_from_tgt)
        
        lbl_acc = tk.Label(bottom_container, text="Colunas Acumuladas Para Sincronização:", bg=self.bg_col, font=("Segoe UI", 9, "bold"))
        lbl_acc.pack(anchor=tk.W, pady=(5,0))
        
        self.txt_acc_cols = tk.Text(bottom_container, height=2, bg="#FFFFFF", fg="#0b5ed7", font=("Segoe UI", 9, "bold"))
        self.txt_acc_cols.pack(fill=tk.X, pady=(0,5))
        self.txt_acc_cols.insert(tk.END, "Nenhuma coluna selecionada no processo acima.")
        self.txt_acc_cols.config(state=tk.DISABLED)
        
        bot_f = tk.Frame(bottom_container, bg=self.bg_col)
        bot_f.pack(fill=tk.X, pady=5)
        bot_f.columnconfigure(0, weight=1)
        bot_f.columnconfigure(1, weight=1)

        f_regras_linha = ttk.LabelFrame(bot_f, text=" Regras de Linha ")
        f_regras_linha.grid(row=0, column=0, sticky="nsew", padx=(0,5))
        
        self.chk_zeros = tk.BooleanVar(value=False)
        tk.Checkbutton(f_regras_linha, text="Remover linhas com valor zero ou nulo nas colunas:", variable=self.chk_zeros, bg=self.bg_col).pack(anchor=tk.W, padx=5, pady=2)
        
        self.lb_zeros_cols = tk.Listbox(f_regras_linha, selectmode=tk.MULTIPLE, bg="#FFFFFF", fg="#1E293B", height=6, relief="solid", borderwidth=1)
        self.lb_zeros_cols.pack(fill=tk.X, padx=5, pady=5)
        
        f_regras_est = ttk.LabelFrame(bot_f, text=" Regras de Estrutura Estruturais ")
        f_regras_est.grid(row=0, column=1, sticky="nsew", padx=(5,0))

        self.chk_clean_out = tk.BooleanVar(value=True)
        self.chk_trim = tk.BooleanVar(value=True)
        self.chk_upper = tk.BooleanVar(value=True)
        
        tk.Checkbutton(f_regras_est, text="Manter APENAS as colunas selecionadas", variable=self.chk_clean_out, bg=self.bg_col).pack(anchor=tk.W, padx=5, pady=2)
        tk.Checkbutton(f_regras_est, text="Trim (limpar espaços extras no início/fim)", variable=self.chk_trim, bg=self.bg_col).pack(anchor=tk.W, padx=5, pady=2)
        tk.Checkbutton(f_regras_est, text="Maiúsculas (converter para Capslock)", variable=self.chk_upper, bg=self.bg_col).pack(anchor=tk.W, padx=5, pady=2)
        
        nav = ttk.Frame(bottom_container)
        nav.pack(fill=tk.X, pady=10)
        
        export_f = tk.Frame(nav, bg=self.bg_col)
        export_f.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(export_f, text="Opções de Saída:", bg=self.bg_col, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        
        excel_rb = tk.Radiobutton(export_f, text="Excel", variable=self.export_fmt, value=".xlsx", bg=self.bg_col, font=("Segoe UI", 9, "bold"))
        excel_rb.pack(side=tk.LEFT, padx=2)
        
        warn_f = tk.Frame(export_f, bg=self.bg_col, highlightbackground="#DC2626", highlightthickness=1)
        warn_f.pack(side=tk.LEFT, padx=10, fill=tk.Y, pady=2)
        tk.Label(warn_f, text="⚠️ Experimental (Testes)", bg=self.bg_col, fg="#DC2626", font=("Segoe UI", 8, "bold")).pack(side=tk.LEFT, padx=(4,2))
        
        csv_rb = tk.Radiobutton(warn_f, text="CSV", variable=self.export_fmt, value=".csv", bg=self.bg_col)
        csv_rb.pack(side=tk.LEFT, padx=2)
        sql_rb = tk.Radiobutton(warn_f, text="SQL", variable=self.export_fmt, value=".sql", bg=self.bg_col)
        sql_rb.pack(side=tk.LEFT, padx=2)
        json_rb = tk.Radiobutton(warn_f, text="JSON", variable=self.export_fmt, value=".json", bg=self.bg_col)
        json_rb.pack(side=tk.LEFT, padx=2)
        
        self.add_tooltip(excel_rb, "Planilha Excel (Estável). Demora mais para processar grandes volumes.")
        self.add_tooltip(warn_f, "Os motores O(1) de Big Data CSV, JSON e SQL estão em fase Experimental\\n(aprimoramento de estabilidade e design).")
        
        self.btn_run_etl = ttk.Button(nav, text="🚀 Executar Sincronização & Exportar Relatório", style="Success.TButton", command=self.on_process)
        self.btn_run_etl.pack(side=tk.RIGHT, ipadx=20)
        
        self.btn_reset_etl = ttk.Button(nav, text="🔄 Reiniciar App", style="Danger.TButton", command=self.callbacks.get('on_reset', lambda: None))
        self.btn_reset_etl.pack(side=tk.RIGHT, padx=(0, 10), ipadx=10)
        
    # --- SUB-MODULO: COMPARADOR (GAPS) ---
    def build_cmp_ui(self):
        f = tk.Frame(self.f_cmp_module, bg="#FFFFFF", highlightbackground="#CED4DA", highlightthickness=1)
        f.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, ipady=20)
        
        nav = ttk.Frame(f)
        nav.pack(side=tk.BOTTOM, fill=tk.X, pady=15)
        
        tk.Label(f, text="🔍 Modo Auditoria Habilitado", font=("Segoe UI", 14, "bold"), fg="#DC3545", bg="#FFFFFF").pack(pady=(15, 5))
        tk.Label(f, text="Neste modo, o algoritmo não transporá colunas, mas sim fará uma varredura extrema.\nO arquivo gerado conterá a linha BRUTA original do banco caso não exista correspondência mútua.\nIdeal para encontrar rapidamente o que existe no Legado que falta no Novo, e vice-versa.", font=("Segoe UI", 10), fg="#6C757D", bg="#FFFFFF", justify=tk.CENTER).pack()
        
        lbl_acc = tk.Label(f, text="Opções de Comparação de Arquivos:", bg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        lbl_acc.pack(anchor=tk.W, padx=10, pady=(15, 0))

        mod_f = ttk.LabelFrame(f, text=" Sentido da Busca e Exportação ")
        mod_f.pack(fill=tk.X, padx=10, pady=5)
        
        self.cmp_direction = tk.StringVar(value="Falta no Destino")
        tk.Radiobutton(mod_f, text="Falta no Destino (O que existe na Origem mas não no Destino)", variable=self.cmp_direction, value="Falta no Destino", bg="#FFFFFF", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=5)
        tk.Radiobutton(mod_f, text="Falta na Origem (O que existe no Destino mas não  na Origem)", variable=self.cmp_direction, value="Falta na Origem", bg="#FFFFFF", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=5)
        
        self.chk_cmp_clean = tk.BooleanVar(value=True)
        tk.Checkbutton(mod_f, text="Exportar relatório mantendo apenas as chaves e colunas mapeadas", variable=self.chk_cmp_clean, bg="#FFFFFF", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.txt_cmp_status = tk.Text(f, height=3, bg="#F0F0F0", fg="#6C757D", font=("Segoe UI", 9))
        self.txt_cmp_status.pack(fill=tk.X, padx=10, pady=(10, 0))
        self.txt_cmp_status.insert(tk.END, "")
        self.txt_cmp_status.config(state=tk.DISABLED)

        self.btn_run_cmp = ttk.Button(nav, text="⚖️ Auditar GAPS e Extrair Relatório Bruto", style="Danger.TButton", command=self.on_process)
        self.btn_run_cmp.pack(side=tk.RIGHT, ipadx=20)
        
        self.btn_reset_cmp = ttk.Button(nav, text="🔄 Reiniciar App", style="Danger.TButton", command=self.callbacks.get('on_reset', lambda: None))
        self.btn_reset_cmp.pack(side=tk.RIGHT, padx=(0, 10), ipadx=10)
        
        export_f = tk.Frame(nav, bg=self.bg_col)
        export_f.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(export_f, text="Opções de Saída:", bg=self.bg_col, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        
        excel_rb = tk.Radiobutton(export_f, text="Excel", variable=self.export_fmt, value=".xlsx", bg=self.bg_col, font=("Segoe UI", 9, "bold"))
        excel_rb.pack(side=tk.LEFT, padx=2)
        
        warn_f = tk.Frame(export_f, bg=self.bg_col, highlightbackground="#DC2626", highlightthickness=1)
        warn_f.pack(side=tk.LEFT, padx=10, fill=tk.Y, pady=2)
        tk.Label(warn_f, text="⚠️ Experimental (Testes)", bg=self.bg_col, fg="#DC2626", font=("Segoe UI", 8, "bold")).pack(side=tk.LEFT, padx=(4,2))
        
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
            self.txt_acc_cols.insert(tk.END, "Nenhuma coluna selecionada no processo acima.")
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
        self.switch_module('etl')
        
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
