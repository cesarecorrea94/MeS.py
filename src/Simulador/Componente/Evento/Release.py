#coding: utf-8
'''
Created on May 21, 2016

@author: cesar
'''
from .Evento import Evento

class Release(Evento):
    '''
    Representante do evento 'release' (liberação de um recurso)
    @cvar _resource_name: Nome do recurso a ser liberado pelas entidades que executarem esse evento
    @type _resource_name: string
    '''
    _resource_name = None

    def __init__(self,
                 nome,
                 recurso,
                 next_event):
        '''
        Construtor de um módulo 'release'.
        @param nome: Nome do módulo
        @type nome: string
        @param recurso: Nome do recurso a ser liberado no evento
        @type recurso: string
        @param next_event: Nome do próximo módulo
        @type next_event: string
        '''
        Evento.__init__(self, nome, next_event)
        self._resource_name = recurso
        pass
    def __call__(self,
                 entity):
        '''
        Função de execução do evento 'release'
        Libera um recurso, e coloca o próximo evento a ser executado pela entidade na lista de eventos
        @param entity: entidade a executar o evento
        @type entity: Simulador.Componente.Entidade.Entity
        '''
        from ..Entidade.Resource import Resource
        Resource.get_resource(self._resource_name).release()
        self.add_evento_futuro(0, entity, self._next_event)
        pass
    pass
