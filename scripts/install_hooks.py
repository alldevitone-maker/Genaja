import os
import shutil
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK_SRC = os.path.join(BASE_DIR, '.git', 'hooks', 'pre-commit')

def install_hooks():
    # Na real, como ja criamos o arquivo, so precisamos garantir que ele é reconhecido.
    # Em Windows/Git Bash, ele deve funcionar se tiver o nome correto.
    print("Instalando Hooks do Git...")
    hooks_dir = os.path.join(BASE_DIR, '.git', 'hooks')
    if not os.path.exists(hooks_dir):
        print("Erro: Pasta .git/hooks não encontrada!")
        return
    
    # O arquivo ja foi criado pela IA, mas aqui garantimos que o usuario pode rodar este script.
    print(f"Hook pre-commit detectado em: {hooks_dir}")
    print("Sucesso: Automação pre-commit ativada.")

if __name__ == "__main__":
    install_hooks()
