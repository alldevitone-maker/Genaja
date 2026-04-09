import asyncio
from app.wizard_state import WizardState
from core.services.logger_service import LoggerService

class FlowRouter:
    """
    Roteador de Intenção do App Shell.
    Decide qual tela instanciar/exibir baseado puramente no `WizardState`.
    """
    def __init__(self, view_container, state: WizardState, page):
        self.container = view_container
        self.state = state
        self.page = page
        self.views = {}  # Cache de instâncias ativas
        
    def register_view(self, key: str, view_instance):
        self.views[key] = view_instance
        
    def navigate(self, key: str):
        """
        Navegação limpa: remove views anteriores do container (evita memory leak Flet)
        e injeta a nova view com base na chave de roteamento.
        """
        if key not in self.views:
            LoggerService().error(f"Router Exception: View '{key}' não registrada.")
            return

        target_view = self.views[key]
        
        # Limpeza atômica do DOM
        self.container.content.controls.clear()
        self.container.content.controls.append(target_view)
        
        # Power-ups pós renderização e trigger de Engine
        try:
            if hasattr(target_view, "on_route_mounted"):
                result = target_view.on_route_mounted()
                # Suporte a on_route_mounted async (ex: SinglePrepView)
                if asyncio.iscoroutine(result):
                    asyncio.ensure_future(result)
        except Exception as e:
             LoggerService().error(f"Erro ao montar Rota {key}: {e}")
             
        self.page.update()

    def handle_intent_decision(self, mode: str):
        """
        O Acionador principal da Intenção do Operador.
        Altera o WizardState e dispara para a rota correspondente.
        """
        self.state.operation_mode = mode
        
        if mode == "convert_only":
            self.state.requires_target = False
            self.navigate("single_convert")
            
        elif mode == "prepare_single":
            self.state.requires_target = False
            self.navigate("single_prep")
            
        elif mode == "compare_sync":
            self.state.requires_target = True
            # Preserva fluxo legado mantendo compatibilidade (Step 1 permite escolher a fonte Destino e acionar a I.A)
            self.navigate("step1_legacy")
            
        else:
            LoggerService().error(f"Modo desconhecido: {mode}")


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, "0.7.1", "Roteador central que orquestra a transição entre telas Flet baseada em estado")
