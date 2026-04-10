import sys
import os
# Setup path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

import unittest
import pandas as pd
import tempfile
from sqlalchemy import create_engine, text
from core.connectors.database_connector import DatabaseConnector

class TestDatabaseConnector(unittest.TestCase):
    """
    Testes de Unidade para o DatabaseConnector (Genaja Stable).
    Valida o contrato BaseConnector usando SQLite temporário.
    """

    def setUp(self):
        # 1. Setup do banco SQLite em arquivo temporário (para persistência entre conexões)
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.db_url = f"sqlite:///{self.db_path}"
        self.engine = create_engine(self.db_url)
        
        # 2. Criar tabela dummy e popular dados
        with self.engine.begin() as conn:
            conn.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"))
            conn.execute(text("INSERT INTO users (name, email) VALUES ('User 1', 'user1@example.com')"))
            conn.execute(text("INSERT INTO users (name, email) VALUES ('User 2', 'user2@example.com')"))
            conn.execute(text("INSERT INTO users (name, email) VALUES ('User 3', 'user3@example.com')"))

        # 3. Configuração do conector
        self.config = {
            "url": self.db_url,
            "table": "users",
            "api_key": "secret_123" # Para testar o expurgo
        }
        self.connector = DatabaseConnector(self.config)

    def tearDown(self):
        if self.connector:
            self.connector.close()
        if self.engine:
            self.engine.dispose()
        # Cleanup do arquivo temporário
        if os.path.exists(self.db_path):
            os.close(self.db_fd)
            os.remove(self.db_path)

    def test_validate_connection(self):
        """Valida se o conector consegue se comunicar com o banco."""
        self.assertTrue(self.connector.validate_connection())
        self.assertTrue(self.connector._is_connected)

    def test_fetch_metadata(self):
        """Valida a extração do esquema de colunas."""
        metadata = self.connector.fetch_metadata()
        expected = ["id", "name", "email"]
        self.assertEqual(metadata, expected)

    def test_preview(self):
        """Valida o preview com limite controlado."""
        df_preview = self.connector.preview(limit=2)
        self.assertEqual(len(df_preview), 2)
        self.assertIsInstance(df_preview, pd.DataFrame)

    def test_fetch_all_standard(self):
        """Valida a carga completa sem chunking."""
        df_all = self.connector.fetch_all()
        self.assertEqual(len(df_all), 3)
        self.assertEqual(df_all.iloc[0]["name"], "User 1")

    def test_fetch_all_streaming(self):
        """Valida o modo de streaming (yield chunks)."""
        chunks = list(self.connector.fetch_all(chunksize=1))
        self.assertEqual(len(chunks), 3) # 3 linhas, chunksize 1 = 3 chunks
        self.assertEqual(len(chunks[0]), 1)
        self.assertIsInstance(chunks[0], pd.DataFrame)

    def test_close_and_sensitive_purge(self):
        """Valida se o close() limpa as credenciais da memória (Governança)."""
        self.assertEqual(self.connector.config["api_key"], "secret_123")
        self.connector.close()
        # O BaseConnector.close() deve setar chaves sensíveis como None
        self.assertIsNone(self.connector.config["api_key"])
        self.assertFalse(self.connector._is_connected)

if __name__ == '__main__':
    unittest.main()
