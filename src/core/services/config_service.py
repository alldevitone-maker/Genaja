import json
import os

class ConfigService:
    # 🏁 SCHEMA PADRÃO (v0.5.8 Professional)
    DEFAULTS = {
        "general": {
            "app_name": "Genaja Pro",
            "operator_name": "Operador Genaja",
            "language": "pt-br",
            "default_export_dir": ""
        },
        "engine": {
            "auto_trim": True,
            "auto_upper": False,
            "case_sensitive_match": False,
            "smart_mapping_threshold": 80
        },
        "export": {
            "default_format": ".xlsx",
            "include_timestamp": True,
            "open_after_export": True
        },
        "security": {
            "lock_mapping_after_start": True,
            "detailed_logging": True
        }
    }

    def __init__(self, filename='genaja_config.json'):
        self.filename = filename
        self.data_dir = os.path.join(os.getcwd(), "data")
        self.config_path = os.path.join(self.data_dir, self.filename)
        self.config = self.load_config()

    def get_config(self, section=None, key=None):
        """Retorna configuração com fallbacks automáticos dos defaults."""
        if section and key:
            return self.config.get(section, {}).get(key, self.DEFAULTS.get(section, {}).get(key))
        if section:
            return self.config.get(section, self.DEFAULTS.get(section))
        return self.config

    def set_config(self, section, key, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

    def load_config(self, logger=None):
        if not os.path.exists(self.config_path):
            return self.DEFAULTS.copy()
            
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                # Merger recursivo simples (1 nível)
                full_config = self.DEFAULTS.copy()
                for section, values in saved.items():
                    if section in full_config:
                        full_config[section].update(values)
                    else:
                        full_config[section] = values
                return full_config
        except Exception as e:
            if logger: logger.error(f"Erro ao carregar config: {e}")
            return self.DEFAULTS.copy()

    def save_config(self, logger=None):
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            if logger: logger.info("Configurações persistidas com sucesso.")
            return True
        except Exception as e:
            if logger: logger.error(f"Falha ao salvar config: {e}")
            return False
