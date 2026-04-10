import unittest
import pandas as pd
import os
import sys

# Adicionar src ao path
sys.path.append(os.path.abspath("src"))

from core.engines.loader_engine import LoaderEngine
from core.learning.learning_logger import LearningLogger
from app.wizard_state import WizardState

class TestMultiSheet(unittest.TestCase):
    def setUp(self):
        self.loader = LoaderEngine()
        self.root_dir = os.getcwd()
        self.test_xlsx = "tests/test_multi.xlsx"
        
        # Criar Excel de teste com 2 abas
        with pd.ExcelWriter(self.test_xlsx) as writer:
            pd.DataFrame({"A": [1, 2], "B": [3, 4]}).to_excel(writer, sheet_name="Aba1", index=False)
            pd.DataFrame({"X": ["val1"], "Y": ["val2"]}).to_excel(writer, sheet_name="Aba2", index=False)

    def tearDown(self):
        if os.path.exists(self.test_xlsx):
            os.remove(self.test_xlsx)

    def test_load_workbook(self):
        """Valida se o LoaderEngine lê todas as abas."""
        wb, headers = self.loader.load_workbook(self.test_xlsx)
        self.assertEqual(len(wb), 2)
        self.assertIn("Aba1", wb)
        self.assertIn("Aba2", wb)
        self.assertListEqual(list(wb["Aba1"].columns), ["A", "B"])
        self.assertListEqual(list(wb["Aba2"].columns), ["X", "Y"])

    def test_learning_logger_multi(self):
        """Valida se o logger registra o contexto de aba."""
        logger = LearningLogger(self.root_dir)
        wb, _ = self.loader.load_workbook(self.test_xlsx)
        
        # Simular aprendizado passivo
        logger.log_workbook_structure(wb)
        
        log = logger.store.load_log()
        # Verificar se as abas foram registradas
        sheets_logged = [ex.get("sheet") for ex in log["executions"] if ex.get("is_passive_learning")]
        self.assertIn("Aba1", sheets_logged)
        self.assertIn("Aba2", sheets_logged)

    def test_wizard_state_integration(self):
        """Valida o armazenamento de workbooks no estado."""
        state = WizardState()
        wb, _ = self.loader.load_workbook(self.test_xlsx)
        state.workbook_src = wb
        state.selected_sheet_src = "Aba2"
        state.df_src = wb["Aba2"]
        
        self.assertEqual(len(state.df_src.columns), 2)
        self.assertEqual(state.df_src.columns[0], "X")

if __name__ == "__main__":
    unittest.main()
