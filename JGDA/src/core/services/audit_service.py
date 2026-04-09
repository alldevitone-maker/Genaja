import os
import datetime
import json
from core.paths import AUDIT_DIR

class AuditService:
    """
    Serviço de Auditoria — Exclusivo Reconstrução.
    Registra eventos de negócio críticos (quem, quando, o quê).
    """
    def __init__(self, operator="N/A"):
        self.operator = operator
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.audit_dir = AUDIT_DIR
        os.makedirs(self.audit_dir, exist_ok=True)
        
    def log_event(self, event_type, details):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "operator": self.operator,
            "event": event_type,
            "details": details
        }
        
        audit_file = os.path.join(self.audit_dir, f"audit_{self.session_id}.jsonl")
        with open(audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
    def record_sync(self, src_file, tgt_file, rows_affected):
        self.log_event("SYNC_EXECUTION", {
            "src": os.path.basename(src_file),
            "tgt": os.path.basename(tgt_file),
            "rows": rows_affected
        })

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, "0.7.1", "Audit Service para conformidade LGPD (Art. 37) — Rastreabilidade total")
