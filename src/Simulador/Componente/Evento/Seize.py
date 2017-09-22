#coding: utf-8
'''
Created on May 21, 2016

@author: cesar
'''
from .Evento import Evento
from ..Miscelanea.Fila import Fila

class Seize(Evento):
    '''
    Representante do evento 'seize' (obtenção de um recurso)
    @cvar _queue: Fila de entidades que estão a espera de um recurso
    @cvar _resource_name: Recurso a ser ocupado pelas entidades que executarem esse evento
    '''
    _queue = None
    _resource_name = None
    
    def __init__(self,
                 nome,
                 recurso,
                 next_event):
        '''
        Construtor de um evento 'seize'.
        @param recurso: recurso a ser obtido no evento
        @type recurso: Simulador.Componente.Entidade.Resource
        '''
        Evento.__init__(self, nome, next_event)
        self._queue = Fila()
        self._resource_name = recurso
        pass
    def __call__(self,
                 entity):
        '''
        Função de execução do evento 'seize'
        Tenta ocupar um recurso.
        Ao ocupar um recurso, coloca o próximo evento a ser executado pela entidade na lista de eventos
        @param entity: entidade a executar o evento
        @type entity: Simulador.Componente.Entidade.Entity
        '''
        self._queue.append(entity)
        def seized():
            self._queue.remove(entity)
            self.add_evento_futuro(0, entity, self._next_event)
            pass
        from ..Entidade.Resource import Resource
        Resource.get_resource(self._resource_name).seize(seized)
        pass
    pass
