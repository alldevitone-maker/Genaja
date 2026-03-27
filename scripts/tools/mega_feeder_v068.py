import os
import pandas as pd
import random
import string

INBOX = "learn/inbox"
os.makedirs(INBOX, exist_ok=True)

def generate_random_dataset(i):
    # Simular diferentes nomes de colunas que devem ser mapeados
    cols = ["ID_PRODUTO", "NOME_ITEM", "VALOR_UNITARIA", "QTD_ESTOQUE", "CATEGORIA_X"]
    data = []
    for _ in range(10):
        data.append([
            random.randint(1000, 9999),
            ''.join(random.choices(string.ascii_uppercase, k=10)),
            round(random.uniform(10, 500), 2),
            random.randint(0, 100),
            "CAT_" + random.choice(["A", "B", "C"])
        ])
    
    df = pd.DataFrame(data, columns=cols)
    df.to_csv(os.path.join(INBOX, f"dirty_data_{i}.csv"), index=False)

print(f"Gerando 100 datasets em {INBOX}...")
for i in range(100):
    generate_random_dataset(i)
print("Pronto. Execute brain_feed.py para ingerir.")
