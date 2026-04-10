from core.connectors.base_connector import BaseConnector
from version import __version__
from core.adapters.pandas_adapter import PandasAdapter

class ConnectorFactory:
    """
    Fábrica de Conectores.
    Desacopla a UI da instanciacao fisica dos adaptadores.
    Usa Registry Pattern para extensibilidade.
    DatabaseConnector usa import lazy para nao exigir SQLAlchemy no boot.
    """
    
    _registry = {
        "local_file": PandasAdapter,
        "sql_db": "core.connectors.database_connector.DatabaseConnector"  # lazy ref
    }
    
    @classmethod
    def register_connector(cls, source_type: str, connector_class):
        """Registra um novo tipo de conector no sistema."""
        cls._registry[source_type] = connector_class

    @classmethod
    def get_connector(cls, source_type: str, config: dict) -> BaseConnector:
        """
        Instancia o conector correto baseado no tipo registrado.
        Suporta refs lazy (string) para imports opcionais.
        """
        if source_type not in cls._registry:
            if source_type == "rest_api":
                raise NotImplementedError("REST API Connector em desenvolvimento.")
            raise ValueError(f"Tipo de conector desconhecido: {source_type}")
        
        connector_class = cls._registry[source_type]
        
        # Resolver import lazy (string ref)
        if isinstance(connector_class, str):
            import importlib
            module_path, class_name = connector_class.rsplit(".", 1)
            module = importlib.import_module(module_path)
            connector_class = getattr(module, class_name)
            cls._registry[source_type] = connector_class  # cache
        
        return connector_class(config)


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Fábrica de adaptadores para suporte a arquivos locais e bancos SQL (SQLAlchemy lazy load)")
