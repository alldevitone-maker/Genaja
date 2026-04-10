import sys

class AppBootstrap:
    """
    Orquestrador de Inicialização (Platinum Architecture).
    Focado estritamente no disparo da UI Flet e serviços acoplados.
    """
    def __init__(self):
        # Os serviços são agora inicializados sob demanda pela UI ou Injeção de Dependência.
        pass
        
    def run(self):
        # O Genaja agora é estritamente Flet.
        # Fallback para Qt removido para garantir pureza da nova arquitetura.
        return self._run_flet()

    def _run_flet(self):
        try:
            import flet as ft
            from ui_flet.main import main as flet_main
            
            # Inicialização Platinum (Pure Flet)
            ft.app(target=flet_main)
            
        except ImportError as e:
            print(f"ERROR: Arquitetura Flet nao encontrada: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: ERRO DE INICIALIZACAO FLET: {e}")
            sys.exit(1)
