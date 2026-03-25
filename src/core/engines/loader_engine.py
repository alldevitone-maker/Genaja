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

    def load_excel(self, path, skip_rows=None):
        """Carga robusta com sanitização de nomes de colunas."""
        if skip_rows is None:
            skip_rows = self.find_best_header(path)
            
        df = pd.read_excel(path, skiprows=skip_rows)
        
        # Limpar nomes de colunas (V0.4.8 Standard)
        df.columns = [str(c).strip() for c in df.columns]
        
        # Remover colunas fantasmas (Unnamed/NaN)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed|^nan', case=False)]
        
        if df.empty:
            raise ValueError("O arquivo Excel carregado está vazio.")
            
        return df, skip_rows
