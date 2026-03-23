import pandas as pd

def gerar_massa_teste():
    print("Gerando arquivos de teste no formato Excel...")
    
    # Arquivo de Origem
    data_src = {
        "ID_CLIENTE": [1, 2, 3, 4, 5, 6, 7],
        "NOME_CLIENTE": ["Alice Silva", "Bruno Costa", "Carlos Dias", "Daniela Souza", "Eduardo Melo", "Fernanda Lima", "Gabriel Santos"],
        "IDADE": [25, 30, 22, 28, 35, 29, 41],
        "STATUS_SISTEMA": ["Ativo", "Inativo", "Ativo", "Ativo", "Pendente", "Ativo", "Inativo"],
        "UF": ["SP", "RJ", "MG", "SP", "PR", "SC", "RS"]
    }
    df_src = pd.DataFrame(data_src)
    df_src.to_excel("origem_teste.xlsx", index=False)
    
    # Arquivo de Destino (Novo Sistema / BD)
    # Tem algumas colunas com nomes iguais (para testar o drop do sufixo _x _y do pandas)
    data_tgt = {
        "CODIGO_EXTERNO": [3, 4, 5, 8, 9, 1, 2],
        "NOME_CLIENTE": ["Carlos Dias", "Daniela Souza", "Eduardo Melo", "Helena Gomes", "Igor Barros", "Alice S.", "Bruno C."],
        "SALDO_CONTA": [150.0, 0.0, 300.5, 50.0, 0.0, 1000.0, 250.0],
        "DATA_CADASTRO": ["2023-01-01", "2023-02-15", "2023-03-10", "2023-04-20", "2023-05-05", "2022-10-10", "2022-11-11"],
        "ATIVO": [True, True, False, True, False, True, False]
    }
    df_tgt = pd.DataFrame(data_tgt)
    df_tgt.to_excel("destino_teste.xlsx", index=False)
    
    print("Sucesso! Os arquivos 'origem_teste.xlsx' e 'destino_teste.xlsx' foram criados na pasta JGDA.")

if __name__ == "__main__":
    gerar_massa_teste()
