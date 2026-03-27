import os
import sys
import pandas as pd
import unittest

# Setup paths
sys.path.append(os.path.join(os.getcwd(), "src"))

from core.services.lookup_engine import LookupEngine

class TestV063Lookup(unittest.TestCase):
    def test_find_common_columns(self):
        df1 = pd.DataFrame(columns=["A", "B", "C"])
        df2 = pd.DataFrame(columns=["B", "C", "D"])
        engine = LookupEngine()
        common = engine.find_common_columns(df1, df2)
        self.assertIn("B", common)
        self.assertIn("C", common)
        self.assertNotIn("A", common)

if __name__ == "__main__":
    unittest.main()
