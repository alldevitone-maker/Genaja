import json
import os

class ConfigService:
    """
    Serviço de Configuração (v0.6.0) - Governança v0.5.9.
    Gerencia persistência de preferências e estados do app.
    """
    DEFAULTS = {
        "general": {
            "app_name": "Genaja Flet",
            "operator_name": "Operador Genaja",
            "language": "pt-br",
            "theme": "dark"
        },
        "engine": {
            "auto_trim": True,
            "smart_mapping_threshold": 80
        },
        "export": {
            "default_format": ".xlsx",
            "include_timestamp": True
        }
    }

    def __init__(self, filename='genaja_config_flet.json'):
        self.filename = filename
        self.data_dir = os.path.join(os.getcwd(), "data")
        self.config_path = os.path.join(self.data_dir, self.filename)
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            return self.DEFAULTS.copy()
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                full = self.DEFAULTS.copy()
                for k, v in saved.items():
                    if k in full and isinstance(v, dict):
                        full[k].update(v)
                    else:
                        full[k] = v
                return full
        except Exception:
            return self.DEFAULTS.copy()

    def get(self, section, key):
        return self.config.get(section, {}).get(key, self.DEFAULTS[section][key])

    def save(self):
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)
