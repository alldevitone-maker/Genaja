class WizardState:
    """
    Gerenciador de Estado do Wizard.
    Mantém os DataFrames e escolhas do usuário entre as páginas do Flet.
    A UI é efêmera, mas o estado é persistente durante a sessão.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        # --- INTENT ADAPTIVE ROUTING ---
        self.operation_mode = None  # "convert_only", "prepare_single", "compare_sync"
        self.operation_plan = {
            "mode": None,
            "source_a": None,
            "source_b": None,
            "inspection": {},
            "conversion": {},
            "transforms": {},
            "mapping": {},
            "output": {}
        }
        self.requires_target = False
        self.source_ready = False
        self.target_ready = False
        self.inspection_report = {}
        self.conversion_report = {}
        self.sample_data = [] # preview da base (limit 10)
        self.temp_out_folder = None # Destino customizado do Modo A
        
        self.connector = None
        self.close_connections()
        self.path_src = None
        self.path_tgt = None
        
        self.df_src = None
        self.df_tgt = None
        
        self.workbook_src = {} # {sheet_name: df} 
        self.workbook_tgt = {}
        self.selected_sheet_src = None
        self.selected_sheet_tgt = None
        
        self.key_src = None
        self.key_tgt = None
        self.key_tgt_final = None
        
        self.mapping = {} # {col_src: col_tgt}
        self.active_filters = []
        
        # --- UNIVERSAL CONNECTORS ---
        self.source_type = "local_file" # "local_file", "sql_db"
        self.source_config_safe = {} # Públicos: host, database, user (Persistível)
        self.source_config_runtime = {} # Sensíveis: password, token (Efêmero)
        self.connector = None
        self.sql_selection = {"schema": None, "table": None}
        self.is_source_valid = False # Flag para habilitar o "Próximo"
        self.is_connected = False # Status visual da conexao

        self.current_step_index = 0
        
        # --- FLAGS LEGACY PARITY ---
        self.protected_a1 = True
        self.shielding = False
        self.auto_trim = True
        self.auto_upper = False
        self.preserve_leading_zeros = True
        
        # --- FLAGS RULES ---
        self.remove_nulls = False
        self.null_filter_cols = []
        self.keep_only_mapped = False
        
        # --- DATA INTELLIGENCE (PRE-ANALYSIS) ---
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
        Limpa credenciais e fecha conexões ativas.
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

    def can_advance(self) -> bool:
        """Regra de Navegação por Intenção (Adaptive Router)"""
        if self.operation_mode in ["convert_only", "prepare_single", "price_sync"]:
            return self.source_ready
        elif self.operation_mode == "compare_sync":
            return self.source_ready and self.target_ready
        return False


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, "0.7.1", "Gerenciador de estado global da sessão com suporte a múltiplos modos de operação")
