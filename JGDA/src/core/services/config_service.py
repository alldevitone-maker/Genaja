import json
import os
from core.paths import JGDA_DATA_DIR

class ConfigService:
    # 🏁 SCHEMA PADRÃO
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
        self.data_dir = JGDA_DATA_DIR
        self.config_path = os.path.join(self.data_dir, self.filename)
        # 🛡️ Garantia de inicialização
        self.config = self.DEFAULTS.copy()
        self.config = self.load_config()

    def get_config(self, section=None, key=None):
        """Retorna configuração com fallbacks automáticos dos defaults."""
        try:
            if section and key:
                # Tenta no config carregado, se falhar tenta no default
                val = self.config.get(section, {}).get(key)
                if val is None:
                    val = self.DEFAULTS.get(section, {}).get(key)
                return val
            if section:
                return self.config.get(section, self.DEFAULTS.get(section))
            return self.config
        except Exception:
            return self.DEFAULTS.get(section) if section else self.DEFAULTS

    def get(self, key, default=None):
        """Get inteligente que busca em seções se a chave for direta."""
        if not isinstance(self.config, dict):
            return self.DEFAULTS.get(key, default)
            
        # 1. Tenta acesso direto (raiz)
        val = self.config.get(key)
        
        # 2. Se nǜo achou na raiz OU se o que achou Ǹ um dicionário (seo)
        # mas quem chamou pode estar esperando um valor de dentro da seo
        if val is None or isinstance(val, dict):
            for section, content in self.config.items():
                if isinstance(content, dict) and key in content:
                    return content[key]
        
        # 3. Fallback para os DEFAULTS se ainda estiver nulo
        if val is None:
            for section, content in self.DEFAULTS.items():
                if isinstance(content, dict) and key in content:
                    return content[key]
            val = self.DEFAULTS.get(key, default)
            
        return val

    def set(self, *args):
        """
        Suporta chamadas flexveis:
        - set(key, value)
        - set(section, key, value)
        """
        if len(args) == 2:
            section, key, value = None, args[0], args[1]
        elif len(args) == 3:
            section, key, value = args[0], args[1], args[2]
        else:
            raise TypeError("set() espera 2 ou 3 argumentos")

        if not isinstance(self.config, dict):
            self.config = self.DEFAULTS.copy()
            
        # Tenta localizar a seo se nǜo informada
        if section is None:
            for s, content in self.DEFAULTS.items():
                if isinstance(content, dict) and key in content:
                    section = s
                    break
        
        if section:
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = value
        else:
            # Se nǜo for uma chave conhecida das sees, salva na raiz
            self.config[key] = value
            
        self.save_config()

    def set_config(self, section, key, value):
        if not isinstance(self.config, dict):
            self.config = self.DEFAULTS.copy()
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

    def load_config(self, logger=None):
        """Carregamento resiliente com fusão profunda de defaults."""
        if not os.path.exists(self.config_path):
            return self.DEFAULTS.copy()
            
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return self.DEFAULTS.copy()
                saved = json.loads(content)
                
                if not isinstance(saved, dict):
                    return self.DEFAULTS.copy()

                # Fusão inteligente: preserva defaults se chaves estiverem ausentes no arquivo
                full_config = self.DEFAULTS.copy()
                for section, values in saved.items():
                    if isinstance(values, dict) and section in full_config:
                        full_config[section].update(values)
                    else:
                        full_config[section] = values
                return full_config
        except (json.JSONDecodeError, Exception) as e:
            if logger: logger.error(f"Erro ao carregar config (Fallback para Defaults): {e}")
            return self.DEFAULTS.copy()

    def save_config(self, logger=None):
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                # Garante que estamos salvando um dicionário válido
                data_to_save = self.config if isinstance(self.config, dict) else self.DEFAULTS
                json.dump(data_to_save, f, indent=4)
            if logger: logger.info("Configurações persistidas com sucesso.")
            return True
        except Exception as e:
            if logger: logger.error(f"Falha ao salvar config: {e}")
            return False


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, "0.7.1", "Serviço de configuração resiliente com fusão de defaults e persistência JSON")
