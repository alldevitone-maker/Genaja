class WizardState:
    """
    Gerenciador de Estado do Wizard (v0.6.0).
    Mantém os DataFrames e escolhas do usuário entre as páginas do Flet.
    A UI é efêmera, mas o estado é persistente durante a sessão.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.close_connections()
        self.path_src = None
        self.path_tgt = None
        
        self.df_src = None
        self.df_tgt = None
        
        self.workbook_src = {} # {sheet_name: df} (v0.6.6)
        self.workbook_tgt = {}
        self.selected_sheet_src = None
        self.selected_sheet_tgt = None
        
        self.key_src = None
        self.key_tgt = None
        self.key_tgt_final = None
        
        self.mapping = {} # {col_src: col_tgt}
        self.active_filters = []
        
        # --- v0.7.0 UNIVERSAL CONNECTORS ---
        self.source_type = "local_file" # "local_file", "sql_db"
        self.source_config_safe = {} # Públicos: host, database, user (Persistível)
        self.source_config_runtime = {} # Sensíveis: password, token (Efêmero)
        self.connector = None
        self.sql_selection = {"schema": None, "table": None}
        self.is_source_valid = False # Flag para habilitar o "Próximo"
        self.is_connected = False # Status visual da conexao

        self.current_step_index = 0
        
        # --- FLAGS v0.4.8 LEGACY PARITY ---
        self.protected_a1 = True
        self.shielding = False
        self.auto_trim = True
        self.auto_upper = False
        self.preserve_leading_zeros = True
        
        # --- FLAGS v0.4.6 RULES ---
        self.remove_nulls = False
        self.null_filter_cols = []
        self.keep_only_mapped = False
        
        # --- v0.6.3 DATA INTELLIGENCE (PRE-ANALYSIS) ---
        self.suggested_key_src = None
        self.suggested_key_tgt = None
        self.suggested_mapping = {}
        self.validation_summary = {}
        self.suggested_source = "none" # "history", "fuzzy", "exact"

    def set_source_type(self, new_type: str):
        """Alterna a fonte de dados e limpa estados irrelevantes."""
        if self.source_type == new_type:
            return
        
        self.source_type = new_type
        self.close_connections(is_switch=True)

    def close_connections(self, is_switch=False):
        """
        Limpa credenciais e fecha conexoes ativas (v0.7.0).
        is_switch: Se True, limpa também os dataframes de origem para evitar corrupção.
        """
        if self.connector:
            try:
                self.connector.close()
            except Exception:
                pass
            self.connector = None

        # Limpeza Sensível (Runtime)
        self.source_config_runtime = {}
        self.is_connected = False
        self.is_source_valid = False
        
        if is_switch:
            # Limpeza de Dados da Origem
            self.df_src = None
            self.path_src = None
            self.workbook_src = {}
            self.selected_sheet_src = None
            self.source_config_safe = {}
            self.sql_selection = {"schema": None, "table": None}

    @property
    def ready_for_sync(self):
        return all([
            self.df_src is not None,
            self.df_tgt is not None,
            self.key_src and self.key_tgt,
            self.mapping
        ])
