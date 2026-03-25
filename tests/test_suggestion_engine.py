import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Setup path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from core.engines.suggestion_engine import SuggestionEngine

class TestSuggestionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SuggestionEngine()

    @patch('glob.glob')
    @patch('os.path.getmtime')
    @patch('os.path.exists')
    def test_suggestion_logic(self, mock_exists, mock_mtime, mock_glob):
        mock_exists.return_value = True
        mock_mtime.return_value = 1000
        mock_glob.side_effect = [
            ['/mock/downloads/sap_export.xlsx'],
            ['/mock/docs/master_base.xlsx'],
            []
        ]
        
        src, tgt = self.engine.suggest_files()
        
        self.assertIn('sap_export.xlsx', src)
        self.assertIn('master_base.xlsx', tgt)
        print(f"Suggestion Logic PASS: SRC={src}, TGT={tgt}")

if __name__ == "__main__":
    unittest.main()
