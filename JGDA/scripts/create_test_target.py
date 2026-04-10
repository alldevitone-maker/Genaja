import pandas as pd
import os
import sys

# --- ANCORAGEM PARA IMPORT DE VERSÃO ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from version import __version__

def create_test_target():
    # Caminho Resolvido Absoluto para evitar falhas de permissão (ex: System32)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(base_dir, "destino_vendedores.xlsx")
    print(f"--- CRIANDO PLANILHA DE DESTINO PARA WORKSHOP (v{__version__}) ---")
    print(f"📍 Destino: {target_path}")
    
    # Colunas que espelham o que queremos sincronizar ou manter
    # O SQL tem: id, nome, cpf, equipe, vendas
    # O Destino terá campos que aceitarão esses dados
    data = {
        'ID_Vendedor': [1, 2, 3, 4, 5],
        'NOME_VENDEDOR': ['LUCAS SILVA', 'MARIA SOUZA', 'JOSE OLIVEIRA', 'ANA COSTA', 'CARLOS PEREIRA'],
        'REGIAO_ATUAL': ['NOROESTE', 'SUL', 'NOROESTE', 'LITORAL', 'NOROESTE'],
        'META_ALCANCADA': [0.0, 0.0, 0.0, 0.0, 0.0], # Será preenchido pelo SQL 'vendas'
        'STATUS_COMPLIANCE': ['PENDENTE', 'PENDENTE', 'PENDENTE', 'PENDENTE', 'PENDENTE']
    }
    
    try:
        df = pd.DataFrame(data)
        df.to_excel(target_path, index=False)
        full_path = os.path.abspath(target_path)
        print(f"✅ SUCESSO! Planilha criada em: {full_path}")
        print("\nPróximo Passo no Genaja:")
        print("1. Origem: SQL Database (vendedores)")
        print(f"2. Destino: {target_path}")
        print("3. Passo 2: Chave na Origem (nome) <-> Chave no Destino (NOME_VENDEDOR)")
        print("4. Passo 3: Mapear 'vendas' -> 'META_ALCANCADA'")
    except Exception as e:
        print(f"❌ Erro ao criar planilha: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_test_target()
