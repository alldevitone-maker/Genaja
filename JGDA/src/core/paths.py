"""
paths.py — Âncora Central de Caminhos do Produto Genaja
-----------------------------------------------------------------
JGDA = motor ETL técnico   →  JGDA_DIR
Genaja = produto completo  →  PRODUCT_DIR
brains/ = inteligência     →  BRAINS_DIR
shared/ = saídas globais   →  SHARED_DIR

Este módulo resolve caminhos de forma absoluta, independente de 
os.getcwd() ou do diretório de execução do processo.
"""
import os

# --- Âncora: localização deste arquivo ---
_THIS_FILE = os.path.abspath(__file__)
_CORE_DIR  = os.path.dirname(_THIS_FILE)          # JGDA/src/core/
_SRC_DIR   = os.path.dirname(_CORE_DIR)           # JGDA/src/
JGDA_DIR   = os.path.dirname(_SRC_DIR)            # JGDA/
PRODUCT_DIR = os.path.dirname(JGDA_DIR)           # Genaja/

# --- Camada de Inteligência (desacoplada do motor) ---
BRAINS_DIR    = os.path.join(PRODUCT_DIR, "brains")
LEARN_DIR     = os.path.join(BRAINS_DIR, "learn")
AUDIT_DIR     = os.path.join(BRAINS_DIR, "audit")

# --- Saídas compartilhadas do produto ---
SHARED_DIR       = os.path.join(PRODUCT_DIR, "shared")
RESULTS_DIR      = os.path.join(SHARED_DIR, "results")
LOGS_SHARED_DIR  = os.path.join(SHARED_DIR, "logs")

# --- Logs do próprio motor JGDA ---
LOGS_MOTOR_DIR = os.path.join(JGDA_DIR, "logs")

# --- Workspace (temporários, fora do core) ---
WORKSPACE_DIR  = os.path.join(PRODUCT_DIR, "workspace")

# --- Config e Data do motor ---
JGDA_DATA_DIR  = os.path.join(JGDA_DIR, "data")


def ensure_dirs():
    """
    Cria todos os diretórios necessários da topologia do produto.
    Seguro para chamar múltiplas vezes (idempotente via exist_ok=True).
    """
    dirs = [
        LEARN_DIR,
        AUDIT_DIR,
        RESULTS_DIR,
        LOGS_SHARED_DIR,
        LOGS_MOTOR_DIR,
        WORKSPACE_DIR,
        JGDA_DATA_DIR,
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, "0.7.1", "Âncora de topologia de diretórios para o ecossistema Genaja (Brains, Shared, JGDA)")
