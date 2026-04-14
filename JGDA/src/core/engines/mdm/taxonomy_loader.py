import json
import os
from core.services.logger_service import LoggerService

class TaxonomyLoader:
    """
    Gerente de Configuração MDM. 
    Carrega e valida as regras de negócios do Genaja.
    """
    def __init__(self, config_path=None):
        self.ls = LoggerService()
        if config_path is None:
            # Caminho padrão baseado na estrutura do projeto
            self.config_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "config", "mdm_rules.json")
            self.config_path = os.path.abspath(self.config_path)
        else:
            self.config_path = config_path
            
        self.rules = {}
        self.load_rules()

    def load_rules(self):
        """Carrega o arquivo JSON de regras."""
        try:
            if not os.path.exists(self.config_path):
                self.ls.error(f"FALHA MDM: Arquivo de regras não encontrado em {self.config_path}")
                return False
                
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.rules = json.load(f)
                self.ls.info(f"MDM GOVERNANCE: Regras carregadas com sucesso (v{self.rules.get('rules_version')})")
                return True
        except Exception as e:
            self.ls.error(f"FALHA MDM: Erro ao ler regras JSON: {str(e)}")
            return False

    def get_settings(self):
        return self.rules.get("settings", {})

    def get_taxonomy(self):
        return self.rules.get("taxonomy", [])

    def get_exceptions(self):
        return self.rules.get("exceptions", {})

    def get_thresholds(self):
        return self.get_settings().get("thresholds", {})

    def get_weights(self):
        return self.get_settings().get("weights", {})
