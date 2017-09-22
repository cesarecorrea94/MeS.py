#coding: utf-8
'''
Created on May 22, 2016

@author: cesar
'''

class Evento(object):
    '''
    Representante de um evento
    @cvar _processos: Lista de processos no sistema
    @ivar _next_event: Evento a ser executado a seguir
    @ivar _name: Nome do módulo
    '''
    _processos = {}#static
    _name = None
    _next_event = None

    @staticmethod
    def get_TNOW():
        '''
        @return: O valor do relógio no sistema
        '''
        from ...Sistema import Sistema
        return Sistema.get_relogio()
    @staticmethod
    def add_evento_futuro(quando,
                          entidade,
                          evento):
        from ...Sistema import Sistema
        Sistema.get_system().add_event(quando, entidade, evento)
        pass
    def __init__(self,
                 nome,
                 next_event):
        '''
        @type nome: string
        @param nome: Nome do módulo
        @type next_event: string
        @param next_event: Nome do próximo módulo
        '''
        self._name = nome
        Evento._processos[nome] = self
        self._next_event = next_event
        pass
    def __call__(self,
                 entidade):
        '''
        Interface para os módulos que implementam esta classe
        @param entidade: Entidade que está a passar pelo módulo
        @type entidade: Entidade
        '''
        print 'Unimplemented'
        pass
    def set_next_event(self,
                       event):
        '''
        Define o evento a ser executado após este (self / si mesmo)
        @type event: Simulador.Componente.Evento.Evento
        @param event: Próximo evento a ser executado
        '''
        self._next_event = event
        pass
    def __repr__(self):
        return self._name
    pass
