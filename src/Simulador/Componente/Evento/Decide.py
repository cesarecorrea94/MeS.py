#coding: utf-8
'''
Created on 09/10/2016

@author: cesar
'''
from .Evento import Evento
from Simulador.GNA import GNA

class Condition(Evento):
    '''
    @type _attr: string
    @ivar _attr: Nome do atributo da entidade
    @type _condicoes: list / []
    @ivar _condicoes: Lista de tuplas (signal, value, event).\n
    signal (string): sinal da comparação;\n
    value (*): valor a ser comparado;\n
    event (string): nome do próximo módulo caso a condição seja satisfeita;\n
    '''
    _attr = None
    _condicoes = None

    def __init__(self,
                 nome,
                 attr,
                 condicoes,
                 else_event):
        '''
        @type nome: string
        @param nome: Nome do módulo
        @type attr: string
        @param attr: Nome do atributo da entidade
        @type condicoes: list / []
        @param condicoes: Lista de tuplas (signal, value, event).\n
        signal (string): sinal da comparação;\n
        value (*): valor a ser comparado;\n
        event (string): nome do próximo módulo caso a condição seja satisfeita;\n
        @type else_event: string
        @param else_event: Nome do próximo módulo caso nenhuma das condições sejam satisfeitas
        '''
        Evento.__init__(self, nome, else_event)
        self._attr = attr
        self._condicoes = condicoes
        pass
    def __call__(self,
                 entity):
        '''
        @type entity: Entidade
        @param entity: Entidade que está a passar pelo módulo
        '''
        attr = getattr(entity, self._attr)
        next_event = self._next_event# else event
        for signal, value, event in self._condicoes:
            if signal == '>':
                if attr > value:    next_event = event
                pass
            elif signal == '>=':
                if attr >= value:   next_event = event
                pass
            elif signal == '==':
                if attr == value:   next_event = event
                pass
            elif signal == '<=':
                if attr <= value:   next_event = event
                pass
            elif signal == '<':
                if attr < value:    next_event = event
                pass
            elif signal in ('!=','<>','><'):
                if attr != value:   next_event = event
                pass
            else: continue
            break
        self.add_evento_futuro(0, entity, next_event)
        pass
    pass

class Chance(Evento):
    '''
    @type _chances: list / []
    @param _chances: Lista de tuplas (acumulado, evento).\n
    acumulado (float in interval '(0,1]'): chance acumulada;\n
    evento (string): nome do próximo evento caso a chance acumulada seja batida;\n
    '''
    _chances = None
    _random_generator = None

    def __init__(self,
                 nome,
                 chances,
                 else_event):
        '''
        @type nome: string
        @param nome: Nome do módulo
        @type chances: list / []
        @param chances: Lista de tuplas (acumulado, evento).\n
        acumulado (float in interval '(0,1]'): chance acumulada;\n
        evento (string): nome do próximo evento caso a chance acumulada seja batida;\n
        @type else_event: string
        @param else_event: Nome do próximo módulo caso nenhuma das chances acumuladas sejam batidas (equivale a acumulado=100)
        '''
        Evento.__init__(self, nome, else_event)
        self._chances = chances
        self._random_generator = GNA.LinearCongruentialGenerator()
        pass
    def __call__(self,
                 entity):
        '''
        @type entity: Entidade
        @param entity: Entidade que está a passar pelo módulo
        '''
        chance = next(self._random_generator)
        next_event = self._next_event# else_event
        for acumulado, event in self._chances:
            if chance < acumulado:
                next_event = event
                break;
            pass
        self.add_evento_futuro(0, entity, next_event)
        pass
    pass
