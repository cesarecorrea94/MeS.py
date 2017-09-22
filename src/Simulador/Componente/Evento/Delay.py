#coding: utf-8
'''
Created on May 21, 2016

@author: cesar
'''
from .Evento import Evento

class Delay(Evento):
    '''
    Representante do evento 'delay' (espera)
    @cvar _fgva: Gerador de variáveis aleatórias para o tempo despendido no 'delay'
    @type _fgva: FGVA
    '''
    _fgva = None
    
    def __init__(self,
                 nome,
                 fgva,
                 next_event):
        '''
        Construtor de um módulo 'delay'.
        @param nome: Nome do módulo
        @type nome: string
        @param fgva: Gerador de valores aleatórios para o tempo de espera
        @type fgva: Simulador.FGVA
        @param next_event: Nome do próximo módulo
        @type next_event: string
        '''
        Evento.__init__(self, nome, next_event)
        self._name = nome
        self._fgva = fgva
        pass
    def __call__(self,
                 entity):
        '''
        Função de execução do evento 'delay'
        Coloca um novo evento, programado para executar a um determinado tempo depois
        segundo seu FGVA, na lista de eventos.
        @param entity: entidade a executar o evento
        @type entity: Simulador.Componente.Entidade.Entity
        '''
        self.add_evento_futuro(next(self._fgva), entity, self._next_event) # updated
        pass
    pass
