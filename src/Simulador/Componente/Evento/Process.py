#coding: utf-8
'''
Created on May 22, 2016

@author: cesar
'''
from .Seize import Seize
from .Delay import Delay
from .Release import Release
from .Evento import Evento

class Process(Evento):
    '''
    Representante de um processo no sistema
    @cvar _seize: Evento 'seize' integrado a esse processo
    @cvar _delay: Evento 'delay' integrado a esse processo
    @cvar _release: Evento 'release' integrado a esse processo
    @cvar _name: Nome do processo
    '''
    _seize = _delay = _release = None
    _name = None
    
    def __init__(self, nome, recurso, fgva):
        '''
        Construtor de um processo
        @param nome: Nome do processo
        @param recurso: Recurso a ser utilizado no processo
        @type recurso: Simulador.Componente.Entidade.Resource
        @param fgva: Gerador de valores para o tempo de espera
        @type fgva: Simulador.FGVA
        '''
        self._seize = Seize(recurso)
        self._delay = Delay(nome, fgva)
        self._release = Release(recurso)
        self._name = self._seize._name
        #next event
        self._seize.set_next_event(self._delay)
        self._delay.set_next_event(self._release)
        pass
    def __call__(self, entity):
        '''
        Função de execução do evento
        Ocupa um recurso, despende um tempo com o recurso, e libera-o.
        Após liberar o recurso, coloca o próximo evento a ser executado pela entidade na lista de eventos
        @param entity: entidade a executar o evento
        @type entity: Simulador.Componente.Entidade.Entity
        '''
        self._seize(entity)
        pass
    def set_next_event(self, event):
        '''
        Define o próximo evento a ser executado
        @param event: Evento a ser executado a seguir
        @type event: Simulador.Componente.Evento.Evento
        '''
        self._release.set_next_event(event)
        pass
    def tamanho_da_fila(self, estatistica):
        '''
        Retorna uma estatística (mínimo,médio,máximo) do tamanho da fila de espera
        pelo recurso utilizado nesse processo
        @param estatistica: Estatística a ser retornada ("Minimo","Medio","Maximo")
        @return: a estatística selecionada
        '''
        return self._seize._queue._tamanho_da_fila[estatistica]
    def tempo_na_fila(self, estatistica):
        '''
        Retorna uma estatística (mínimo,médio,máximo) do tempo na fila de espera
        pelo recurso utilizado nesse processo
        @param estatistica: Estatística a ser retornada ("Minimo","Medio","Maximo")
        @return: a estatística selecionada
        '''
        return self._seize._queue._estatistica['Tempo na Fila'][estatistica]
    pass
