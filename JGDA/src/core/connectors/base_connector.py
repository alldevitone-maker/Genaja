from abc import ABC, abstractmethod
from pandas import DataFrame

class BaseConnector(ABC):
    """
    Contrato Universal de Conectividade.
    Define a interface obrigatoria para todos os adaptadores de dados.
    """
    
    # Política de expurgo de campos sensíveis (v0.7.1)
    SENSITIVE_KEYS = ["api_key", "token", "password", "secret"]

    def __init__(self, config: dict):
        self.config = config
        self._is_connected = False

    @abstractmethod
    def validate_connection(self) -> bool:
        """Valida credenciais/extensao sem carregar dados."""
        pass

    @abstractmethod
    def fetch_metadata(self) -> list:
        """Retorna lista de colunas/esquema da fonte."""
        pass

    @abstractmethod
    def preview(self, limit: int = 10) -> DataFrame:
        """Retorna amostra inicial (Suporte a Live Preview)."""
        pass

    @abstractmethod
    def fetch_all(self) -> DataFrame:
        """Retorna o dataset completo para processamento."""
        pass

    def close(self):
        """Interface para fechamento de conexões físicas."""
        pass

    def _cleanup_sensitive_data(self):
        """
        Libera recursos/conexoes e limpa credenciais efêmeras.
        Aplica política de expurgo apenas para chaves sensíveis.
        """
        self._is_connected = False
        for key in self.SENSITIVE_KEYS:
            if key in self.config:
                self.config[key] = None # Expurgo seguro sem destruir o objeto config


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, "0.7.1", "Classe base abstrata (Protocolo) para conectores Genaja")
