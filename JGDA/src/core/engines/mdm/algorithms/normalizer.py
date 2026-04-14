import unicodedata
import re

class Normalizer:
    """
    Higienizador de Dados MDM.
    Prepara a string para o casamento de padrões e similaridade.
    """
    
    @staticmethod
    def deep_clean(text):
        """
        Limpeza extrema:
        1. Remove acentos (Unicode Normalization)
        2. Lowercase
        3. Remove pontuação ruidosa
        4. Colapsa múltiplos espaços
        """
        if not text:
            return ""
            
        # Converter para string e lowercase
        val = str(text).lower().strip()
        
        # Isolar prefixo se for Email
        if "@" in val:
            val = val.split("@")[0]
            
        # Remover acentuação (ASCII Folding)
        val = "".join(
            c for c in unicodedata.normalize('NFD', val)
            if unicodedata.category(c) != 'Mn'
        )
        
        # Trocar separadores comuns por espaço para facilitar Tokenização
        val = re.sub(r'[\._\-/]', ' ', val)
        
        # Remover caracteres não alfanuméricos residuais (mantendo espaços)
        val = re.sub(r'[^a-z0-9\s]', '', val)
        
        # Colapsar múltiplos espaços
        val = re.sub(r'\s+', ' ', val).strip()
        
        return val

    @staticmethod
    def extract_identity(text):
        """Extrai apenas a parte significativa sem espaços para IDs."""
        return Normalizer.deep_clean(text).replace(" ", "")

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
from version import __version__
_vdeclare(__name__, __version__, "Módulo de higienização de strings e normalização Unicode")
