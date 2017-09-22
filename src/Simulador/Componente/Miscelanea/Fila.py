#coding: utf-8
'''
Created on May 23, 2016

@author: cesar
'''
from .Estatistica import Estatistica

class Fila(list, Estatistica):
    '''
    Fila que calcula estatísticas de tamanho (mínimo,médio,máximo) e tempo (mínimo,médio,máximo) na fila
    @cvar _tamanho_da_fila: Lista das estatísticas do tamanho da fila
    @cvar _momento_de_entrada_na_fila: Dicionário com os momentos que entidades entraram na fila.
    '''
    _tamanho_da_fila = None
    _momento_de_entrada_na_fila = None
    
    def __init__(self, *args, **kwargs):
        '''
        Construtor
        '''
        list.__init__(self, *args, **kwargs)
        Estatistica.__init__(self, 'Tempo na Fila')
        self._tamanho_da_fila = {'Minimo':float('inf'),
                                 'Medio': None,
                                 'Maximo':-float('inf')}
        self._momento_de_entrada_na_fila = {}
        pass
    def append(self, objeto):
        '''
        Acrescenta mais um objeto à fila, e calcula novas estatísticas
        @param objeto: objeto a ser acrescido na fila
        @type objeto: object
        '''
        from ...Sistema import Sistema
        TNOW = Sistema.get_relogio()
        self._momento_de_entrada_na_fila[objeto] = TNOW
        list.append(self, objeto)
        if len(self) > self._tamanho_da_fila['Maximo']: self._tamanho_da_fila['Maximo'] = len(self)
        pass
    def remove(self, objeto):
        '''
        Remove um objeto da fila, e calcula novas estatísticas
        @param objeto: objeto a ser removido da fila
        @type objeto: object
        '''
        from ...Sistema import Sistema
        TNOW = Sistema.get_relogio()
        list.remove(self, objeto)
        if len(self) < self._tamanho_da_fila['Minimo']: self._tamanho_da_fila['Minimo'] = len(self)
        self.estatisticas('Tempo na Fila', TNOW - self._momento_de_entrada_na_fila[objeto])
        if not TNOW == 0:
            somatorio = self._estatistica['Tempo na Fila']['somatorio']
            self._tamanho_da_fila['Medio'] = somatorio / TNOW
            pass
        del self._momento_de_entrada_na_fila[objeto]
        pass
    pass
