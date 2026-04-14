import pandas as pd
import os
from version import __version__

class LoaderEngine:
    """
    Motor de Carga Inteligente.
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
        """
        Sensoriamento de Cabeçalho Universal (Cognitivo).
        Não utiliza keywords fixas. Baseia-se em Unicidade, DNA de Dados e Taxonomia.
        """
        try:
            from core.engines.mdm.taxonomy_loader import TaxonomyLoader
            # 1. Carregar conhecimento dinâmico (O que o sistema já 'conhece' sobre dados)
            known_terms = set()
            try:
                taxonomy = TaxonomyLoader().load_all()
                for cat in taxonomy:
                    known_terms.update([t.upper() for t in cat.get("canonical_terms", [])])
                    known_terms.update([s.upper() for s in cat.get("business_synonyms", [])])
                    known_terms.update([a.upper() for a in cat.get("abbreviations", [])])
            except Exception: pass

            best_row, best_score = 0, -100.0
            
            # Padrões que definem "DADO" e não "CABEÇALHO" (DNA de Dados)
            re_is_data = [
                r'.*@.*\..*', # E-mail
                r'\d{2,3}[\.\/-]\d{3}[\.\/-]\d{3}', # CPF/CNPJ ou similar
                r'^\d+$', # Números puros
                r'^\d{5,}-\d+$' # CEP ou IDs formatados
            ]

            for i, row in df_temp.iterrows():
                # Limpeza e detecção de nulidade
                vals = row.dropna().astype(str).str.strip()
                if vals.empty: continue
                
                raw_count = len(vals)
                unique_vals = set(vals.str.upper())
                unique_count = len(unique_vals)
                
                # --- CAMADA 1: ENTROPIA DE UNICIDADE (Peso 10.0) ---
                # Headers tendem a ser nomes únicos de colunas. Dados tendem a se repetir.
                uniqueness_ratio = unique_count / raw_count
                score = uniqueness_ratio * 10.0
                
                # --- CAMADA 2: DNA DE DADOS (Penalidade Pesada) ---
                # Se a linha contém padrões que 'parecem' dados, reduzimos o score.
                for v in vals:
                    if any(re.match(p, v) for p in re_is_data):
                        score -= 4.0 # Penalidade por cada célula que parece dado
                    if len(v) > 60:
                        score -= 2.0 # Títulos de colunas dificilmente são strings imensas
                
                # --- CAMADA 3: TAXONOMIA DINÂMICA (Bônus de Especialista) ---
                # Se a linha contém termos que o sistema já conhece no MDM.
                matches_known = sum(1 for v in unique_vals if v in known_terms)
                score += (matches_known * 2.5)

                if score > best_score:
                    best_score, best_row = score, i
            
            return best_row
        except Exception:
            return 0

    def load_workbook(self, path):
        """
        Carrega arquivos Excel ou CSV.
        Implementa FALLBACK de codificação para evitar erros de 'charmap'.
        """
        try:
            # Detecção de extensão para compatibilidade
            ext = os.path.splitext(path)[1].lower()
            
            if ext == ".csv":
                df = self._robust_read_csv(path)
                skip = self.find_best_header_from_df(df.head(20))
                if skip > 0:
                    df = self._robust_read_csv(path, skiprows=skip)
                
                return {"Planilha1": self._sanitize_df(df)}, {"Planilha1": skip}
            
            # Fluxo Excel
            engine = "xlrd" if ext == ".xls" else "openpyxl"
            
            # 1. Ler cabeçalhos crus para detectar header em cada aba
            try:
                workbook_raw = pd.read_excel(path, sheet_name=None, header=None, nrows=20, engine=engine)
            except (UnicodeDecodeError, LookupError):
                # Caso o arquivo seja um verdadeiro arquivo texto/CSV disfarçado
                df = self._robust_read_csv(path)
                return {"Planilha1": self._sanitize_df(df)}, {"Planilha1": 0}

            final_workbook = {}
            sheet_headers = {}
            
            for sheet_name, df_raw in workbook_raw.items():
                skip = self.find_best_header_from_df(df_raw)
                # 2. Recarregar a aba com o header correto
                df = pd.read_excel(path, sheet_name=sheet_name, skiprows=skip, engine=engine)
                
                if not df.empty:
                    final_workbook[sheet_name] = self._sanitize_df(df)
                    sheet_headers[sheet_name] = skip
            
            if not final_workbook:
                raise ValueError("O arquivo não contém abas válidas ou dados.")
                
            return final_workbook, sheet_headers
        except (UnicodeDecodeError, LookupError) as ue:
            raise ValueError(f"Falha de codificação no arquivo: {str(ue)}")
        except Exception as e:
            raise e

    def _robust_read_csv(self, path, skiprows=0):
        """Tenta carregar CSV/texto em múltiplos encodings silenciosamente."""
        
        # 1. Tentativa para "Falso Excel SAP B1" (Tabelas HTML salvas como .xls)
        try:
            dfs = pd.read_html(path)
            if dfs:
                return dfs[0]
        except Exception:
            pass

        # 2. Tentativa Texto Plano / CSV / TSV
        encodings = ["utf-8", "latin-1", "cp1252", "utf-16", "utf-16-le"]
        last_err = None
        
        for enc in encodings:
            for sep in [None, '\t', ';', ',']:
                try:
                    df = pd.read_csv(
                        path, 
                        sep=sep, 
                        engine='python' if sep is None else 'c', 
                        encoding=enc, 
                        skiprows=skiprows,
                        on_bad_lines='skip'
                    )
                    if not df.empty and len(df.columns) > 1:
                        return df
                    # Se leu apenas 1 coluna inteira com sep específico fixo e não tentamos os outros, tenta de novo
                    if sep is None and not df.empty:
                        return df
                except Exception as e:
                    last_err = e
                    continue
        
        raise ValueError(f"Não foi possível decodificar o arquivo. SAP HTML falhou. CSV Último erro: {last_err}")

    def _sanitize_df(self, df):
        """Limpeza básica de colunas e nomes."""
        df.columns = [str(c).strip() for c in df.columns]
        df = df.loc[:, ~df.columns.str.contains('^Unnamed|^nan', case=False)]
        return df


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Motor de carga universal com sensoriamento cognitivo de cabeçalho e fallback robusto de codificação")
