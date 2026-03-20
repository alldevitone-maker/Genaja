import pandas as pd
import os

def create_dummy():
    # 1. Cria a pasta data se não existir
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    # 2. Arquivo de Origem (Simplesweb)
    # Tem o código e o valor que queremos atualizar
    df_origem = pd.DataFrame({
        'CODIGO': [101, 102, 103],
        'VALOR_NOVO': [500.00, 750.00, 1000.00],
        'DESC_ORIGEM': ['Prod A', 'Prod B', 'Prod C']
    })
    
    # 3. Arquivo de Destino (SAP)
    # Tem colunas extras (LIXO_*) que DEVEM SUMIR se o checkbox funcionar
    df_destino = pd.DataFrame({
        'SAP_KEY': [101, 102, 104],         # 104 não existe na origem
        'SAP_VALOR': [10.0, 10.0, 10.0],    # Será atualizado
        'LIXO_1': ['Dado inútil', 'X', 'Y'], # Deve sumir
        'LIXO_2': [999, 888, 777]            # Deve sumir
    })

    df_origem.to_excel(os.path.join(data_dir, 'origem_teste.xlsx'), index=False)
    df_destino.to_excel(os.path.join(data_dir, 'destino_teste.xlsx'), index=False)
    print(f"✅ Arquivos de teste gerados em: {data_dir}")

if __name__ == "__main__":
    create_dummy()