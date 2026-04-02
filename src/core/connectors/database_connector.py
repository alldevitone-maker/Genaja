import pandas as pd
from core.connectors.base_connector import BaseConnector


class DatabaseConnector(BaseConnector):
    """
    Conector Universal de Banco de Dados (v0.7.0 Patch).
    Utiliza SQLAlchemy para suportar múltiplos drivers (Postgres, MySQL, SQLite).
    Implementa modo de Streaming para grandes volumes de dados.
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.engine = None
        self._connection = None
        self._build_engine()

    def _build_engine(self):
        """Constrói o engine SQLAlchemy a partir da config ou URL bruta."""
        try:
            from sqlalchemy import create_engine as _create_engine
            self._create_engine = _create_engine
        except ImportError:
            raise ImportError(
                "SQLAlchemy nao encontrado. Execute: pip install sqlalchemy"
            )
        url = self.config.get("url")
        if not url:
            driver = self.config.get("driver", "postgresql")
            user = self.config.get("user")
            password = self.config.get("password")
            host = self.config.get("host", "localhost")
            port = self.config.get("port", 5432)
            database = self.config.get("database")
            url = f"{driver}://{user}:{password}@{host}:{port}/{database}"
        
        self.engine = self._create_engine(url, pool_pre_ping=True)

    def validate_connection(self) -> bool:
        try:
            with self.engine.connect() as conn:
                self._is_connected = True
                return True
        except Exception as e:
            print(f"Erro de Conexão: {e}")
            return False

    def fetch_metadata(self) -> list:
        """Extrai esquema das colunas executando uma query vazia."""
        df = self.preview(limit=0)
        return list(df.columns)

    def preview(self, limit: int = 100) -> pd.DataFrame:
        """Retorna amostra controlada. Default 100, Max 1000."""
        safe_limit = min(max(limit, 0), 1000)
        query = self.config.get("query")
        if not query:
            table = self.config.get("table")
            query = f"SELECT * FROM {table}"
        
        preview_query = f"SELECT * FROM ({query}) AS sub limit {safe_limit}"
        
        with self.engine.connect() as conn:
            from sqlalchemy import text
            return pd.read_sql_query(text(preview_query), conn)

    def fetch_all(self, chunksize: int = None):
        """
        Executa a carga de dados.
        Se chunksize for definido, retorna um generator de chunks (Streaming).
        Caso contrário, retorna o DataFrame completo.
        """
        query = self.config.get("query")
        if not query:
            table = self.config.get("table")
            query = f"SELECT * FROM {table}"

        if chunksize:
            from sqlalchemy import text
            return pd.read_sql_query(text(query), self.engine, chunksize=chunksize)
        
        with self.engine.connect() as conn:
            from sqlalchemy import text
            return pd.read_sql_query(text(query), conn)

    def close(self):
        """Fecha o pool de conexões e limpa credenciais."""
        if self.engine:
            self.engine.dispose()
        super().close()
