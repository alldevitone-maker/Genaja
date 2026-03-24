import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import logging
from tkinterdnd2 import TkinterDnD

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.bootstrap import AppBootstrap
from ui_tk.genaja_tk_window import GenajaUI
from core.services.config_service import ConfigService
from services.excel_loader import load_excel_data_with_adjustment
from core.services.etl_service import ETLService
from core.services.mapping_engine import MappingEngine
from core.services.validation_engine import ValidationEngine
from utils.logger_setup import setup_logger, get_logger
from services.theme_service import ThemeService
from services.export_service import ExportService

class GenajaApp:
    ENGINE_NAME = "JGDA AI Engine"
    PRODUCT_NAME = "Genaja Pro"

    def __init__(self):
        # Inicia logger
        setup_logger()
        self.logger = get_logger()
        self.logger.info("Genaja v0.5.0 Gold - Hybrid Synchronization Engine Initiated")

        # Inicialização Híbrida via Bootstrap
        self.bootstrap = AppBootstrap()
        
        # Inicia serviços neutros
        self.theme_service = self.bootstrap.theme_service
        self.config_service = self.bootstrap.config_service
        
        # Se for Qt, o bootstrap já lida com o loop de eventos e bloqueia aqui
        ui_mode = self.bootstrap.run()
        if ui_mode == "qt":
            return

        # --- FLUXO TKINTER (LEGADO) ---
        from version import __version__
        
        # Ativa DND (Drag & Drop) se disponível
        try:
            from tkinterdnd2 import TkinterDnD
            self.root = TkinterDnD.Tk()
        except Exception as e:
            self.root = tk.Tk()
            self.logger.warning(f"Falha ao carregar TkinterDnD: {e}")

        # Configurações de Janela
        self.root.title(f"Genaja Pro - Inteligência de Sincronização - Hub Unificado (v{__version__} Gold)")
        self.root.geometry("1100x750")

        # Inicia Motores de Negócio
        self.mapping_engine = MappingEngine()
        self.validation_engine = ValidationEngine()
        self.etl_service = ETLService(self.mapping_engine, self.validation_engine)
        self.export_service = ExportService()

        # Callbacks para o Step 3 (Lógica de Negócio)
        callbacks = {
            "on_files_selected": self.on_files_selected,
            "on_validate_keys": self.on_validate_keys,
            "on_start_sync": self.on_process, # Mantendo nome interno on_process por enquanto
            "on_export_data": self.on_process, # Reutiliza fluxo por enquanto
            "on_ia_map": self.on_ia_map,
            "on_reset": self.on_reset_app
        }

        # UI (Injeta Serviços e Callbacks)
        self.ui = GenajaUI(self.root, self.theme_service, callbacks)
        
    def run(self):
        self.root.mainloop()
        
        self.df_src = None
        self.df_tgt = None
        self.loader_win = None

    def on_reset_app(self):
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
            top_matches = self.validation_engine.suggest_primary_keys(self.df_src, self.df_tgt)
            
            cols_src = list(self.df_src.columns)
            cols_tgt = list(self.df_tgt.columns)
            
            # Aqui no v0.5.0, top_matches já vem pronto do engine
            # Se for uma lista de dicts (formato esperado pela UI), passamos direto
            formatted_matches = []
            if isinstance(top_matches, tuple):
                # Legacy compatibility: (src, tgt, score)
                formatted_matches = [{'src': top_matches[0], 'tgt': top_matches[1], 'score': int(top_matches[2]*100)}]

            self.ui.set_keys_data(cols_src, cols_tgt, formatted_matches, len(self.df_src), len(self.df_tgt))
            
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
            messagebox.showwarning(":( Ops! Chave errada?", f"A coluna '{k_src}' não compartilha NENHUM dado em comum com '{k_tgt}'.\n\nCruzá-las iria destruir seu relatório. Por favor, escolha outra Chave Primária compatível que faz sentido!")
            return False
            
        return True

    def on_process(self, inputs):
        self.root.config(cursor="wait")
        self.show_loader("Isolando colunas e preparando Motor Mapeador...")
        try:
            df_s = self.df_src.copy()
            df_t = self.df_tgt.copy()
            mapping = {col: col for col in inputs["cols_mapped"]}
            
            module = inputs["module"]
            self.show_loader(f"Aplicando {module}. Realizando as junções complexas...")
            
            if module == "Limpar":
                df_final = self.etl_service.execute_sync(df_s, df_t, mapping, inputs["key_src"], inputs["key_tgt"], inputs["key_tgt_final"], inputs["clean_output"])
            elif module == "Falta na Origem":
                df_final = self.etl_service.execute_comparison(df_s, df_t, inputs["key_src"], inputs["key_tgt"], "falta_origem", inputs["clean_output"], mapping, inputs["key_tgt_final"])[0]
            elif module == "Falta no Destino":
                df_final = self.etl_service.execute_comparison(df_s, df_t, inputs["key_src"], inputs["key_tgt"], "falta_destino", inputs["clean_output"], mapping, inputs["key_tgt_final"])[0]

            # Post-processing filters (on df_final)
            if inputs["chk_zeros"]:
                self.show_loader("I.A filtrando linhas zero/nulas (Cross-check)...")
                cols_to_filter = inputs.get("zero_cols", [])
                df_final = self.validation_engine.apply_numeric_filter(df_final, cols_to_filter)
                
            # Data Sanitization via Service
            if inputs["chk_trim"] or inputs["chk_upper"]:
                self.show_loader("Higienizando dados (Trim/Upper)...")
                df_final = apply_text_transformations(df_final, trim=inputs["chk_trim"], upper=inputs["chk_upper"])

            self.hide_loader()
            self.root.config(cursor="")
            export_fmt = inputs.get("export_fmt", ".xlsx")
            
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
            
            # Export via Service Class
            export_success = self.export_service.export(df_final, filepath, export_fmt)
                
            self.hide_loader()
            
            if export_success:
                resp = messagebox.askyesno("Sucesso Expresso 🎉", f"Processamento Corporativo concluído e gravado!\n\nSalvo em:\n{filepath}\n\nDeseja disparar a abertura do arquivo gerado agora?")
                if resp:
                    try:
                        os.startfile(filepath)
                    except Exception as e:
                        messagebox.showwarning("Aviso do Sistema", f"Não foi possível acionar o sistema operacional para abrir o arquivo automaticamente.\nRecorrendo à verificação manual.\nErro: {e}")
            else:
                messagebox.showerror("Erro de Exportação", "O motor de exportação não reconheceu o formato ou falhou ao gravar o arquivo.")
            
        except Exception as e:
            self.hide_loader()
            messagebox.showerror("Erro Crítico", str(e))
        finally:
            self.root.config(cursor="")
            self.ui.unlock_ui()

    def on_ia_map(self):
        """Callback para o botão 'Auto-Map I.A'"""
        if self.df_src is not None and self.df_tgt is not None:
            return self.mapping_engine.suggest_mapping(self.df_src.columns, self.df_tgt.columns)
        return {}

    def run(self):
        self.root.mainloop()

    # O on_reset_app duplicado foi removido.

if __name__ == "__main__":
    app = GenajaApp()
    app.run()
