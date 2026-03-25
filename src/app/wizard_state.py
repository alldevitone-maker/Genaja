class WizardState:
    """
    Gerenciador de Estado do Wizard (v0.6.0).
    Mantém os DataFrames e escolhas do usuário entre as páginas do Flet.
    A UI é efêmera, mas o estado é persistente durante a sessão.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.path_src = None
        self.path_tgt = None
        
        self.df_src = None
        self.df_tgt = None
        
        self.key_src = None
        self.key_tgt = None
        self.key_tgt_final = None
        
        self.mapping = {} # {col_src: col_tgt}
        self.active_filters = []
        
        self.current_step_index = 0

    @property
    def ready_for_sync(self):
        return all([
            self.df_src is not None,
            self.df_tgt is not None,
            self.key_src and self.key_tgt,
            self.mapping
        ])
