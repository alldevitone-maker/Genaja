import json
import os

class ConfigService:
    def __init__(self, filename='genaja_config.json'):
        self.filename = filename
        self.config_path = self._get_config_path()
        
    def _get_config_path(self):
        # Baseado na nova estrutura src/core/services/
        return os.path.join(os.getcwd(), "data", self.filename)

    def save_config(self, config, logger=None):
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            if logger: logger.info(f"Configuração salva em: {self.config_path}")
            return True
        except Exception as e:
            if logger: logger.error(f"Erro ao salvar configuração: {e}")
            return False

    def load_config(self, logger=None):
        try:
            if not os.path.exists(self.config_path):
                return None
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if logger: logger.info(f"Configuração carregada de: {self.config_path}")
                return config
        except Exception as e:
            if logger: logger.error(f"Erro ao carregar configuração: {e}")
            return None
