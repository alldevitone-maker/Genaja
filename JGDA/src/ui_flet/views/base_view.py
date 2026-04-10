from abc import ABC, abstractmethod

class RoutedViewMixin(ABC):
    """
    Genaja Stable - Padrão Arquitetural 'Big Tech' (Contrato de View)
    Garante que todas as instâncias injetadas no FlowRouter sigam a mesma 
    assinatura de ciclo de vida. Impede erros na instanciação e padroniza o offloading.
    """
    
    @abstractmethod
    def on_route_mounted(self):
        """
        Gatilho disparado em background pelo FlowRouter assim que o layout 
        físico da tela é inserido na DOM principal.
        
        Permite que a interface do usuário seja pintada imediatamente (Skeleton loading)
        enquanto processamentos pesados rodam em background.
        Pode ser implementado como 'def' corriqueiro ou 'async def' para tarefas assíncronas.
        """
        pass
