import pandas as pd
from src.services.etl_service import clean_empty_quantities_multi

def test_0001414():
    # Simulando o dado carregado pelo pandas
    df = pd.DataFrame({
        'Local Estoque': ['0001414', '0.0', '0'],
        'Quantidade': [0, 0, 0]
    })
    
    # As colunas de exclusão que o usuário possa ter passado
    cols_to_check = ['Local Estoque', 'Quantidade']
    
    print("DataFrame original:")
    print(df)
    
    # Simula a limpeza
    df_cleaned = clean_empty_quantities_multi(df, cols_to_check)
    
    print("\nDataFrame apos limpeza:")
    print(df_cleaned)

if __name__ == "__main__":
    test_0001414()
