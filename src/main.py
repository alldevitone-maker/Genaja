import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import pandas as pd
from tkinterdnd2 import TkinterDnD

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.genaja_ui import GenajaUI
from utils.logger_setup import configure_logging
from version import __version__
import logging
from services.excel_loader import load_excel_data_with_adjustment
from services.etl_service import (
    suggest_primary_keys, 
    process_data_synchronization, 
    apply_numeric_filter,
    process_data_comparison
)

class GenajaApp:
    ENGINE_NAME = "JGDA AI Engine"
    PRODUCT_NAME = "Genaja Pro"

    def __init__(self):
        self.root = TkinterDnD.Tk()
        
        callbacks = {
            'on_files_selected': self.on_files_selected,
            'on_process': self.on_process,
            'on_validate_keys': self.on_validate_keys,
            'on_reset': self.on_reset
        }
        self.ui = GenajaUI(self.root, self.PRODUCT_NAME, __version__, callbacks)
        configure_logging()
        
        self.df_src = None
        self.df_tgt = None
        self.loader_win = None

    def on_reset(self):
        import sys, os
        resp = messagebox.askyesno("Reiniciar Aplicação", "Atenção: Todo o mapeamento atual será perdido.\nTem certeza que deseja reiniciar o Genaja e começar uma nova sessão?")
        if resp:
            os.execl(sys.executable, sys.executable, *sys.argv)

    def show_loader(self, msg="Processando..."):
        if not self.loader_win or not self.loader_win.winfo_exists():
            self.loader_win = tk.Toplevel(self.root)
            self.loader_win.overrideredirect(True)
            w, h = 350, 130
            x = self.root.winfo_x() + (self.root.winfo_width()//2) - (w//2)
            y = self.root.winfo_y() + (self.root.winfo_height()//2) - (h//2)
            self.loader_win.geometry(f"{w}x{h}+{x}+{y}")
            self.loader_win.config(bg="#FFFFFF")
            self.loader_win.attributes("-topmost", True)
            
            f = tk.Frame(self.loader_win, bg="#0D6EFD", bd=3)
            f.pack(fill=tk.BOTH, expand=True)

            self.lbl_loader = tk.Label(f, text=msg, bg="#FFFFFF", fg="#212529", font=("Segoe UI", 11, "bold"), pady=20)
            self.lbl_loader.pack(fill=tk.BOTH, expand=True)

            self.pb = ttk.Progressbar(f, mode="indeterminate")
            self.pb.pack(fill=tk.X, padx=30, pady=15)
            self.pb.start(10)
        else:
            self.lbl_loader.config(text=msg)
        self.root.update()

    def hide_loader(self):
        if self.loader_win and self.loader_win.winfo_exists():
            self.loader_win.destroy()

    def log_msg(self, msg, lvl="INFO"):
        level = getattr(logging, lvl.upper(), logging.INFO)
        logging.log(level, msg)

    def on_files_selected(self, file_src, file_tgt):
        self.root.config(cursor="wait")
        self.show_loader("Extraindo Headers do Arquivo de Origem...")
        
        try:
            self.df_src = load_excel_data_with_adjustment(file_src, "ORIGEM", self.root, self.log_msg)
            
            self.show_loader("Extraindo Headers da Base Histórica...")
            self.df_tgt = load_excel_data_with_adjustment(file_tgt, "DESTINO", self.root, self.log_msg)
            
            if self.df_src is None or self.df_tgt is None:
                self.hide_loader()
                self.root.config(cursor="")
                return
            
            self.show_loader("Calculando Placar de Intersecção I.A (Semantic Engine)...")
            top_matches = suggest_primary_keys(self.df_src, self.df_tgt)
            
            cols_src = list(self.df_src.columns)
            cols_tgt = list(self.df_tgt.columns)
            
            self.ui.set_keys_data(cols_src, cols_tgt, top_matches, len(self.df_src), len(self.df_tgt))
            
        except Exception as e:
            messagebox.showerror("Erro de Leitura", str(e))
        finally:
            self.hide_loader()
            self.root.config(cursor="")

    def on_validate_keys(self, k_src, k_tgt):
        if not k_src or not k_tgt:
            messagebox.showwarning("Aviso", "Selecione as chaves antes de continuar!")
            return False
            
        self.show_loader("Cruzamento em O(1): Verificando se as chaves fazem sentido...")
        
        s1 = set(self.df_src[k_src].astype(str).dropna())
        s2 = set(self.df_tgt[k_tgt].astype(str).dropna())
        intersection = len(s1 & s2)
        
        self.hide_loader()
        
        if intersection == 0:
            messagebox.showwarning(":( Ops! Chave errada?", f"A coluna '{k_src}' não compartilha NENHUM dado em comum com '{k_tgt}'.\\n\\nCruzá-las iria destruir seu relatório. Por favor, escolha outra Chave Primária compatível que faz sentido!")
            return False
            
        return True

    def on_process(self, inputs):
        self.root.config(cursor="wait")
        self.show_loader("Isolando colunas e preparando Motor Mapeador...")
        try:
            df_s = self.df_src.copy()
            df_t = self.df_tgt.copy()
            mapping = {col: col for col in inputs["cols_mapped"]}
            
            if inputs["chk_zeros"]:
                self.show_loader("I.A limpando falsos-positivos (Shielding zeros)...")
                cols_to_filter = inputs.get("zero_cols", [])
                if not cols_to_filter:
                    num_cols_t = df_t.select_dtypes(include='number').columns.tolist()
                    cols_to_filter = [c for c in inputs["cols_mapped"] if c in num_cols_t] if inputs["cols_mapped"] else num_cols_t
                df_t = apply_numeric_filter(df_t, cols_to_filter)
            
            module = inputs["module"]
            self.show_loader(f"Aplicando {module}. Realizando as junções complexas...")
            
            if module == "Limpar":
                df_final = process_data_synchronization(df_s, df_t, inputs["key_src"], inputs["key_tgt"], inputs["key_tgt_final"], mapping, inputs["clean_output"])
            elif module == "Falta na Origem":
                df_final = process_data_comparison(df_s, df_t, inputs["key_src"], inputs["key_tgt"], "falta_origem", inputs["clean_output"], mapping, inputs["key_tgt_final"])[0]
            elif module == "Falta no Destino":
                df_final = process_data_comparison(df_s, df_t, inputs["key_src"], inputs["key_tgt"], "falta_destino", inputs["clean_output"], mapping, inputs["key_tgt_final"])[0]
                
            if inputs["chk_trim"]:
                self.show_loader("Removendo micro-espaços falsos em textos...")
                df_final = df_final.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            if inputs["chk_upper"]:
                self.show_loader("Forçando CAIXA ALTA (Upper Case)...")
                df_final = df_final.apply(lambda x: x.str.upper() if x.dtype == "object" else x)

            self.hide_loader()
            self.root.config(cursor="")
            export_fmt = inputs.get("export_fmt", ".csv")
            
            filetypes_map = {
                ".csv": [("Arquivo CSV Rápido", "*.csv")],
                ".xlsx": [("Planilha Excel Pesada", "*.xlsx")],
                ".sql": [("Script SQL (Dumps Database)", "*.sql")],
                ".json": [("Notação de Objeto JSON", "*.json")]
            }
            
            filepath = filedialog.asksaveasfilename(
                title="Salvar Arquivo Final",
                defaultextension=export_fmt,
                filetypes=filetypes_map.get(export_fmt, [("Todos", "*.*")])
            )
            
            if not filepath:
                self.ui.unlock_ui()
                return
                
            self.root.config(cursor="wait")
            self.show_loader("Acelerando IO para Gravação no Disco...")
            
            ext = os.path.splitext(filepath)[1].lower()
            if ext == '.csv':
                df_final.to_csv(filepath, index=False, sep=';', encoding='utf-8-sig')
            elif ext == '.sql':
                table_name = "genaja_exportacao_v046"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"-- Genaja Enterprise Universal SQL EXPORT\n")
                    f.write(f"-- Auto-generated cross tables.\n\n")
                    cols = df_final.columns.tolist()
                    cols_str = ", ".join([f"`{c}`" for c in cols])
                    
                    for row in df_final.itertuples(index=False):
                        vals = []
                        for v in row:
                            if pd.isna(v): vals.append("NULL")
                            elif isinstance(v, str): 
                                clean_v = v.replace("'", "''")
                                vals.append(f"'{clean_v}'")
                            else: vals.append(str(v))
                        vals_str = ", ".join(vals)
                        f.write(f"INSERT INTO {table_name} ({cols_str}) VALUES ({vals_str});\n")
            elif ext == '.json':
                self.show_loader("Achatando dicionários para Array JSON Nativo...")
                df_final.to_json(filepath, orient='records', force_ascii=False, indent=4)
            else:
                self.show_loader("Renderizando Binários do Excel (Pode demorar vários minutos)...")
                df_final.to_excel(filepath, index=False)
                
            self.hide_loader()
            
            resp = messagebox.askyesno("Sucesso Expresso 🎉", f"Processamento Corporativo concluído e gravado!\n\nSalvo em:\n{filepath}\n\nDeseja disparar a abertura do arquivo gerado agora?")
            if resp:
                try:
                    os.startfile(filepath)
                except Exception as e:
                    messagebox.showwarning("Aviso do Sistema", f"Não foi possível acionar o sistema operacional para abrir o arquivo automaticamente.\nRecorrendo à verificação manual.\nErro: {e}")
            
        except Exception as e:
            self.hide_loader()
            messagebox.showerror("Erro Crítico", str(e))
        finally:
            self.root.config(cursor="")
            self.ui.unlock_ui()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GenajaApp()
    app.run()
