import os
import sys
import pandas as pd
import unittest

# Setup paths
sys.path.append(os.path.join(os.getcwd(), "src"))

from migration.schema_mapper import SchemaMapper

class TestV063Patch3(unittest.TestCase):
    def test_fuzzy_matching(self):
        mapper = SchemaMapper(threshold=0.5)
        src = ["Cod. Prod", "Valor Unit.", "Nome Cliente"]
        tgt = ["Codigo Produto", "Vlr Unitario", "Cliente"]
        
        suggestions = mapper.suggest_matches(src, tgt)
        
        self.assertIn("Cod. Prod", suggestions)
        self.assertEqual(suggestions["Cod. Prod"]["target"], "Codigo Produto")
        self.assertGreater(suggestions["Cod. Prod"]["score"], 0.55)
        
        self.assertIn("Valor Unit.", suggestions)
        self.assertEqual(suggestions["Valor Unit."]["target"], "Vlr Unitario")

if __name__ == "__main__":
    unittest.main()
