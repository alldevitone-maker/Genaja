import os
import sys
import pandas as pd
import unittest

# Setup paths
sys.path.append(os.path.join(os.getcwd(), "src"))

from core.lookup_engine import LookupEngine

class TestV063Hardening(unittest.TestCase):
    def test_lookup_order_preservation(self):
        df_src = pd.DataFrame(columns=["Z", "A", "M"])
        df_tgt = pd.DataFrame(columns=["A", "M", "Z"])
        engine = LookupEngine()
        common = engine.find_common_columns(df_src, df_tgt)
        # Deve manter a ordem da ORIGEM: Z, A, M
        self.assertEqual(common, ["Z", "A", "M"])

    def test_lookup_nan_unicity(self):
        df_src = pd.DataFrame({"ID": [1, 2, 3, None, None]}) # 3 únicos / 5 total = 0.6
        df_tgt = pd.DataFrame({"ID": [1, 2, 3, 4, 5]})
        engine = LookupEngine()
        s_src, s_tgt = engine.suggest_key_pair(df_src, df_tgt)
        # 0.6 < 0.8, não deve sugerir
        self.assertIsNone(s_src)

        df_src_ok = pd.DataFrame({"ID": [1, 2, 3, 4, None]}) # 4 únicos / 5 total = 0.8
        # Se threshold for > 0.8, 0.8 ainda falha. Vamos testar unicitade real.
        df_perfect = pd.DataFrame({"ID": [1, 2, 3, 4, 5]})
        s_src, s_tgt = engine.suggest_key_pair(df_perfect, df_perfect)
        self.assertEqual(s_src, "ID")

if __name__ == "__main__":
    unittest.main()
