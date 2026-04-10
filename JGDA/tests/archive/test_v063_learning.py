import os
import sys
import json
import unittest
import shutil

# Setup paths
sys.path.append(os.path.join(os.getcwd(), "src"))

from core.learning.learning_store import LearningStore
from core.learning.learning_logger import LearningLogger
from core.learning.suggestion_engine import HistoricalSuggestionEngine

class TestV063Learning(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = os.path.join(os.getcwd(), "tmp_test_genaja")
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
        os.makedirs(self.tmp_dir)

    def tearDown(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def test_learning_flow(self):
        logger = LearningLogger(self.tmp_dir)
        
        src = ["Cod", "Nome", "Preco"]
        tgt = ["Codigo", "Descricao", "Inativo"]
        mapping = {"Cod": "Codigo", "Nome": "Descricao"}
        keys = ("Cod", "Codigo")
        
        # 1. Gravar Execução
        logger.log_execution(src, tgt, mapping, keys, 100)
        
        # 2. Verificar Pasta e JSON
        store = LearningStore(self.tmp_dir)
        self.assertTrue(os.path.exists(store.log_path))
        
        log = store.load_log()
        self.assertEqual(log["log_version"], "1.0")
        self.assertEqual(len(log["executions"]), 1)
        self.assertEqual(log["executions"][0]["usage_count"], 1)

        # 3. Incrementar Usage Count (Segunda execução idêntica)
        logger.log_execution(src, tgt, mapping, keys, 200)
        log_v2 = store.load_log()
        self.assertEqual(len(log_v2["executions"]), 1)
        self.assertEqual(log_v2["executions"][0]["usage_count"], 2)

        # 4. Sugestão Histórica
        engine = HistoricalSuggestionEngine(self.tmp_dir)
        suggestion = engine.get_smart_suggestions(src, tgt)
        
        self.assertEqual(suggestion["source"], "history")
        self.assertEqual(suggestion["mapping"]["Cod"], "Codigo")
        self.assertEqual(suggestion["confidence"], 0.9)

if __name__ == "__main__":
    unittest.main()
