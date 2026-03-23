import sys
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.genaja_ui import GenajaUI
from utils.logger_setup import configure_logging
from version import __version__
from services.excel_loader import load_excel_data_with_adjustment
from services.etl_service import (
    suggest_primary_keys, 
    process_data_synchronization, 
    clean_empty_quantities_multi, 
    process_data_comparison,
    apply_numeric_filter
)

class GenajaApp:
    ENGINE_NAME = "JGDA AI Engine"
    PRODUCT_NAME = "Genaja Pro"

    def __init__(self):
        self.root = tk.Tk()
        
        callbacks = {
            'on_files_selected': self.on_files_selected,
            'on_process': self.on_process
        }
        self.ui = GenajaUI(self.root, self.PRODUCT_NAME, __version__, callbacks)
        configure_logging()
        
        # Memory caches
        self.df_src = None
        self.df_tgt = None

    def on_files_selected(self, file_src, file_tgt):
        self.root.config(cursor="wait")
        self.root.update()
        
        try:
            # Fake logger for loader
            def dummy_log(msg, lvl="INFO"): print(msg)
            
            # Load DataFrames
            self.df_src = load_excel_data_with_adjustment(file_src, "ORIGEM", self.root, dummy_log)
            self.df_tgt = load_excel_data_with_adjustment(file_tgt, "DESTINO", self.root, dummy_log)
            
            if self.df_src is None or self.df_tgt is None:
                self.root.config(cursor="")
                return
            
            # Run AI Matcher
            best_s, best_t, score = suggest_primary_keys(self.df_src, self.df_tgt)
            cols_src = list(self.df_src.columns)
            cols_tgt = list(self.df_tgt.columns)
            
            self.ui.set_step2_data(cols_src, cols_tgt, best_s, best_t, score)
            
        except Exception as e:
            messagebox.showerror("Erro de Leitura", str(e))
        finally:
            self.root.config(cursor="")

    def on_process(self, inputs):
        self.root.config(cursor="wait")
        self.root.update()
        try:
            df_s = self.df_src.copy()
            df_t = self.df_tgt.copy()
            mapping = {col: col for col in inputs["cols_mapped"]}
            
            # Executa a limpeza Global (Zeros)
            if inputs["chk_zeros"]:
                # Pega as colunas numericas e aplica clear
                num_cols_t = df_t.select_dtypes(include='number').columns.tolist()
                df_t = apply_numeric_filter(df_t, num_cols_t)
            
            # Executa o Mapeamento/Limpeza (Action Module)
            module = inputs["module"]
            if module == "Limpar":
                df_final = process_data_synchronization(df_s, df_t, inputs["key_src"], inputs["key_tgt"], mapping)
            elif module == "Falta na Origem":
                df_final = process_data_comparison(df_s, df_t, inputs["key_src"], inputs["key_tgt"], "origem")
            elif module == "Falta no Destino":
                df_final = process_data_comparison(df_s, df_t, inputs["key_src"], inputs["key_tgt"], "destino")
                
            # Filters
            if inputs["chk_trim"]:
                df_final = df_final.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            if inputs["chk_upper"]:
                df_final = df_final.apply(lambda x: x.str.upper() if x.dtype == "object" else x)

            # --- EXPORT ---
            self.root.config(cursor="")
            filepath = filedialog.asksaveasfilename(
                title="Salvar Arquivo Mapeado",
                defaultextension=".csv",
                filetypes=[
                    ("Arquivo CSV (Super Rápido - Big Data)", "*.csv"), 
                    ("Planilha Excel Tradicional", "*.xlsx"),
                    ("Banco de Dados SQL Dump", "*.sql")
                ]
            )
            
            if not filepath:
                self.ui.unlock_ui()
                return
                
            self.root.config(cursor="wait")
            self.root.update()
            
            ext = os.path.splitext(filepath)[1].lower()
            if ext == '.csv':
                df_final.to_csv(filepath, index=False, sep=';', encoding='utf-8-sig')
            elif ext == '.sql':
                table_name = "genaja_exportacao"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"-- Genaja Universal SQL EXPORT (v0.4.6)\\n")
                    cols = df_final.columns.tolist()
                    cols_str = ", ".join([f"`{c}`" for c in cols])
                    
                    # Mass Insert optimization
                    for row in df_final.itertuples(index=False):
                        vals = []
                        for v in row:
                            if pd.isna(v): vals.append("NULL")
                            elif isinstance(v, str): 
                                clean_v = v.replace("'", "''")
                                vals.append(f"'{clean_v}'")
                            else: vals.append(str(v))
                        
                        vals_str = ", ".join(vals)
                        f.write(f"INSERT INTO {table_name} ({cols_str}) VALUES ({vals_str});\\n")
            else:
                df_final.to_excel(filepath, index=False)
                
            messagebox.showinfo("Sucesso", f"Processamento concluído com perfeição!\\nArquivo salvo em:\\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Erro Crítico", str(e))
        finally:
            self.root.config(cursor="")
            self.ui.unlock_ui()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GenajaApp()
    app.run()
