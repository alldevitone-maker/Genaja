import pandas as pd

class LoaderEngine:
    """
    Motor de Carga Inteligente (v0.6.0) - Heurística v0.4.8.
    Detecta automaticamente a linha de cabeçalho em arquivos Excel bagunçados.
    """
    
    def find_best_header(self, path, search_rows=20):
        """
        Heurística: Encontra a linha com maior densidade de strings (títulos).
        """
        try:
            # Ler apenas o início do arquivo para inspeção
            df_temp = pd.read_excel(path, nrows=search_rows, header=None)
            best_row = 0
            best_score = -1
            
            for i, row in df_temp.iterrows():
                non_null_vals = row.dropna()
                if non_null_vals.empty:
                    continue
                
                # Cabeçalhos costumam ser textos (strings)
                str_count = sum(1 for x in non_null_vals if isinstance(x, str))
                
                # Se houver empate, preferimos a linha mais profunda (geralmente a técnica)
                if str_count >= best_score:
                    best_score = str_count
                    best_row = i
                    
            return best_row
        except Exception:
            return 0

    def find_best_header_from_df(self, df_temp):
        """Versão que aceita DataFrame já carregado (OTIMIZAÇÃO v0.6.6)."""
        try:
            best_row = 0
            best_score = -1
            
            for i, row in df_temp.iterrows():
                non_null_vals = row.dropna()
                if non_null_vals.empty: continue
                # Se houver empate, preferimos a primeira linha (v0.6.6 balanceamento)
                if str_count > best_score:
                    best_score = str_count
                    best_row = i
            return best_row
        except Exception:
            return 0

    def load_workbook(self, path):
        """Carrega todas as abas de um arquivo Excel (v0.6.6)."""
        # 1. Ler cabeçalhos crus para detectar header em cada aba
        # sheet_name=None retorna Dict[str, DataFrame]
        workbook_raw = pd.read_excel(path, sheet_name=None, header=None, nrows=20)
        
        final_workbook = {}
        sheet_headers = {}
        
        for sheet_name, df_raw in workbook_raw.items():
            skip = self.find_best_header_from_df(df_raw)
            # 2. Recarregar a aba com o header correto
            df = pd.read_excel(path, sheet_name=sheet_name, skiprows=skip)
            
            # Sanitização (Refatorada v0.6.6)
            df.columns = [str(c).strip() for c in df.columns]
            df = df.loc[:, ~df.columns.str.contains('^Unnamed|^nan', case=False)]
            
            if not df.empty:
                final_workbook[sheet_name] = df
                sheet_headers[sheet_name] = skip
        
        if not final_workbook:
            raise ValueError("O arquivo Excel não contém abas válidas ou dados.")
            
        return final_workbook, sheet_headers

    def load_excel(self, path, skip_rows=None):
        """Wrapper de compatibilidade (v0.6.0) - Retorna a primeira aba válida."""
        wb, headers = self.load_workbook(path)
        first_sheet = list(wb.keys())[0]
        return wb[first_sheet], headers[first_sheet]
