import os
import json
from typing import Dict, Optional, List
from datetime import datetime
from version import __version__

class CuratedStore:
    """
    Motor de Mapeamentos Curados.
    Gerencia as 'Regras de Ouro' que precedem as sugestões estatísticas.
    Localizado em learn/curated/master_rules.json.
    """
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.storage_path = os.path.join(root_dir, "learn", "curated", "master_rules.json")
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {
            "rules": {}, 
            "metadata": {
                "version": __version__, 
                "creator": "Master Agent Protocol",
                "last_sync": ""
            }
        }

    def promote_mapping(self, src: str, tgt: str, reason: str = "auto_promotion"):
        """Promove um mapeamento para o estado CURATED (Regra Master)."""
        key = src.strip().lower()
        tgt_val = tgt.strip() # Preservar case original
        
        self.data["rules"][key] = {
            "target": tgt_val,
            "reason": reason,
            "promoted_at": str(datetime.now())
        }

    def get_curated_match(self, src_col: str, possible_targets: List[str]) -> Optional[str]:
        """Tenta encontrar um match determinístico na base curada."""
        key = src_col.strip().lower()
        if key not in self.data["rules"]:
            return None
            
        rule = self.data["rules"][key]
        tgt_val = rule["target"]
        
        # Verificar se o alvo da regra existe nas colunas atuais
        if tgt_val.lower() in [pt.lower() for pt in possible_targets]:
            # Retornar o case exato presente no dataset
            for pt in possible_targets:
                if pt.lower() == tgt_val.lower():
                    return pt
        return None

    def save(self):
        self.data["metadata"]["last_sync"] = str(datetime.now())
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Gerenciador de regras curadas (Regras de Ouro) para mapeamento determinístico")
