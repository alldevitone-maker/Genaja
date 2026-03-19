import json, os
from tkinter import messagebox

def get_config_path(filename):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), filename)

def save_config_service(config, root, log_callback, filename='genaja_config.json'):
    try:
        path = get_config_path(filename)
        with open(path, 'w', encoding='utf-8') as f: json.dump(config, f, indent=4)
        log_callback(f"Configuração salva: {path}", "SUCCESS")
    except Exception as e:
        log_callback(f"Erro ao salvar: {e}", "ERROR")

def load_config_service(root, log_callback, filename='genaja_config.json'):
    try:
        path = get_config_path(filename)
        if not os.path.exists(path): return None
        with open(path, 'r', encoding='utf-8') as f:
            log_callback(f"Configuração carregada: {path}", "SUCCESS")
            return json.load(f)
    except Exception as e:
        log_callback(f"Erro ao carregar: {e}", "ERROR"); return None
