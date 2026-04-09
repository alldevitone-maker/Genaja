import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Adicionar src ao path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from app.wizard_state import WizardState
from ui_flet.views.step1_view import Step1View
import pandas as pd
import flet as ft

class MockEvent:
    def __init__(self, data=None, control=None):
        self.data = data
        self.control = control

class TestStep1Logic(unittest.TestCase):
    def setUp(self):
        self.state = WizardState()
        # Mocking callbacks
        self.on_next = MagicMock()
        self.on_pick_file = MagicMock()
        
        # Mocking Flet Page
        self.page = MagicMock(spec=ft.Page)
        self.page.overlay = []
        
        # Instanciar View com Mocks
        with patch('flet.Column.__init__', return_value=None):
            self.view = Step1View(self.state, self.on_next, self.on_pick_file)
            # Re-init controls as we patched __init__
            self.view.page = self.page
            self.view.controls = [None] * 10
            self.view.src_info = MagicMock(spec=ft.Text)
            self.view.tgt_info = MagicMock(spec=ft.Text)
            self.view.src_sheet_dropdown = MagicMock(spec=ft.Dropdown)
            self.view.btn_next = MagicMock(spec=ft.ElevatedButton)
            self.view.update = MagicMock()

    def test_scenario_1_local_file_to_target(self):
        """Cenário 1: Local File -> Destino válido libera avanço."""
        self.state.source_type = "local_file"
        self.state.df_src = pd.DataFrame({"A": [1]})
        self.state.df_tgt = pd.DataFrame({"B": [2]})
        
        # Simular seleção de aba (dispara validação de botão)
        self.view._on_sheet_change("tgt", "Aba1")
        
        self.assertFalse(self.view.btn_next.disabled)

    def test_scenario_2_sql_invalid_sanitization(self):
        """Cenário 2: SQL inválido com sanitização de senha."""
        self.state.source_type = "sql_db"
        self.state.source_config_runtime["password"] = "SECRET_123"
        
        with patch('core.services.connector_factory.ConnectorFactory.get_connector') as mock_factory:
            mock_conn = MagicMock()
            mock_conn.validate_connection.side_effect = Exception("Falha: SECRET_123 em host local")
            mock_factory.return_value = mock_conn
            
            # Tentar conexão
            self.view._on_sql_test_click(None)
            
            # Verificar SnackBar (Overlay)
            snackbar = self.page.overlay[0]
            self.assertIn("***", snackbar.content.value)
            self.assertNotIn("SECRET_123", snackbar.content.value)

    def test_scenario_3_sql_valid_flow(self):
        """Cenário 3: SQL válido + tabela + destino libera avanço."""
        self.state.source_type = "sql_db"
        self.state.df_tgt = pd.DataFrame({"B": [2]})
        
        with patch('core.services.connector_factory.ConnectorFactory.get_connector') as mock_factory:
            mock_conn = MagicMock()
            mock_conn.validate_connection.return_value = True
            mock_conn.fetch_metadata.return_value = ["table1"]
            mock_conn.preview.return_value = pd.DataFrame({"A": [1]})
            mock_factory.return_value = mock_conn
            
            # Testar Conexão
            self.view._on_sql_test_click(None)
            self.assertTrue(self.state.is_connected)
            
            # Selecionar Tabela
            self.view._on_sheet_change("src", "table1")
            
            # Verificações
            self.assertEqual(self.state.sql_selection["table"], "table1")
            self.assertIsNotNone(self.state.df_src)
            self.assertFalse(self.view.btn_next.disabled)

    def test_scenario_4_switch_local_to_sql(self):
        """Cenário 4: Troca Local -> SQL limpa df_src e origem anterior."""
        self.state.source_type = "local_file"
        self.state.df_src = pd.DataFrame({"A": [1]})
        self.state.path_src = "c:/test.xlsx"
        
        # Simular troca via UI
        e = MockEvent(data={"sql_db"})
        self.view._on_source_type_change(e)
        
        self.assertEqual(self.state.source_type, "sql_db")
        self.assertIsNone(self.state.df_src)
        self.assertIsNone(self.state.path_src)

    def test_scenario_5_switch_sql_to_local(self):
        """Cenário 5: Troca SQL -> Local limpa config SQL e seleção."""
        self.state.source_type = "sql_db"
        self.state.source_config_safe = {"host": "127.0.0.1"}
        self.state.source_config_runtime = {"password": "pwd"}
        
        # Simular troca via UI
        e = MockEvent(data={"local_file"})
        self.view._on_source_type_change(e)
        
        self.assertEqual(self.state.source_type, "local_file")
        self.assertEqual(self.state.source_config_safe, {})
        self.assertEqual(self.state.source_config_runtime, {})

    def test_scenario_6_dropdown_sql_visibility(self):
        """Cenário 6: Banco com 1 tabela mantém dropdown visível em modo SQL."""
        self.state.source_type = "sql_db"
        tables = ["only_one_table"]
        
        # Mock do dropdown UI
        dd = ft.Dropdown()
        self.view._update_sheet_dropdown(dd, tables, None)
        
        self.assertTrue(dd.visible)

    def test_scenario_7_is_connected_flag(self):
        """Cenário 7: Status de conexão ativa flag corretamente no estado."""
        with patch('core.services.connector_factory.ConnectorFactory.get_connector') as mock_factory:
            mock_conn = MagicMock()
            mock_conn.validate_connection.return_value = True
            mock_factory.return_value = mock_conn
            
            self.view._on_sql_test_click(None)
            self.assertTrue(self.state.is_connected)

    def test_scenario_8_log_hygiene(self):
        """Cenário 8: Log hygiene - Não expor senha em logs de erro."""
        self.state.source_type = "sql_db"
        self.state.source_config_runtime["password"] = "PRIVATE_KEY"
        
        with patch('core.services.logger_service.LoggerService.error') as mock_log:
            with patch('core.services.connector_factory.ConnectorFactory.get_connector') as mock_factory:
                mock_conn = MagicMock()
                mock_conn.validate_connection.side_effect = Exception("SECRET: PRIVATE_KEY")
                mock_factory.return_value = mock_conn
                
                self.view._on_sql_test_click(None)
                
                # O log capturado deve estar sanitizado
                log_call = mock_log.call_args[0][0]
                self.assertIn("***", log_call)
                self.assertNotIn("PRIVATE_KEY", log_call)

if __name__ == '__main__':
    # Relatório Compacto
    print("\n🏁 INICIANDO VALIDAÇÃO EXECUTÁVEL DA LÓGICA DA UI v0.7.0")
    print("-" * 50)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStep1Logic)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    
    print("\n📦 RESULTADO POR CENÁRIO:")
    print(f"✅ Cenários Sucesso: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas técnicas: {len(result.failures) + len(result.errors)}")
    sys.exit(0 if result.wasSuccessful() else 1)
