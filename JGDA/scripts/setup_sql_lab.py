import sqlite3
import sys
import os

# --- ANCORAGEM PARA IMPORT DE VERSÃO ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from version import __version__

def setup_sql_lab():
    # Caminho Resolvido Absoluto para evitar falhas de contexto (ex: System32)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "test_genaja.db")
    print(f"--- CRIANDO LABORATÓRIO SQL GENAJA (v{__version__}) ---")
    print(f"📍 Destino do Banco: {db_path}")
    
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Limpando banco anterior...")
        except Exception as e:
            print(f"Erro ao remover banco anterior: {e}")
            sys.exit(1)

    print(f"Criando novo banco...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Criar tabela de Vendedores (Estrutura de Teste)
    print("Criando tabela 'vendedores'...")
    cursor.execute('''
        CREATE TABLE vendedores (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            cpf TEXT,
            equipe TEXT,
            vendas REAL
        )
    ''')

    # Dados fake para cruzar no ETL
    vendedores = [
        (1, 'LUCAS SILVA', '111.222.333-44', 'NOROESTE', 15700.50),
        (2, 'MARIA SOUZA', '555.666.777-88', 'SUL', 24300.00),
        (3, 'JOSE OLIVEIRA', '999.000.111-22', 'NOROESTE', 8900.20),
        (4, 'ANA COSTA', '444.333.222-11', 'LITORAL', 31000.00),
        (5, 'CARLOS PEREIRA', '888.777.666-55', 'NOROESTE', 12500.75)
    ]

    cursor.executemany('INSERT INTO vendedores VALUES (?,?,?,?,?)', vendedores)
    
    conn.commit()
    conn.close()

    full_path = os.path.abspath(db_path)
    print("\n✅ LABORATÓRIO SQL PRONTO!")
    print(f"📍 Caminho: {full_path}")
    print(f"🔗 URL para Colar no Genaja: sqlite:///{db_path}")
    print("\nPróximo Passo: No Genaja, selecione 'SQL Database' e use a URL acima.")

if __name__ == "__main__":
    setup_sql_lab()
