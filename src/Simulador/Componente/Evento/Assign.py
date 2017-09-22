#coding: utf-8
'''
Created on May 24, 2016

@author: cesar
'''
from .Evento import Evento

class Assign(Evento):
    '''
    @ivar _atribuicoes: Lista de tuplas (attr, value). 'value' será atribuido ao atributo 'attr' da entidade 
    @type _atribuicoes: list / []
    '''
    _atribuicoes = []

    def __init__(self,
                 nome,
                 next_event,
                 atribuicoes):
        '''
        @param nome: Nome do módulo
        @type nome: string
        @param next_event: Nome do próximo módulo
        @type next_event: string
        @param atribuicoes: Lista de tuplas (attr, value). 'value' será atribuido ao atributo 'attr' da entidade 
        @type atribuicoes: list / []
        '''
        Evento.__init__(self, nome, next_event)
        self._atribuicoes = atribuicoes
        pass
    def __call__(self,
                 entidade):
        '''
        @param entidade: Entidade que está a passar pelo módulo
        @type entidade: Entidade
        '''
        for attr,value in self._atribuicoes:
            if value == 'TNOW': value = self.get_TNOW()
            setattr(entidade, attr, value)
            pass
        self.add_evento_futuro(0, entidade, self._next_event)
        pass
    pass
