#coding: utf-8
'''
Created on May 25, 2016

@author: cesar
'''

class Estatistica(object):
    '''
    Calcula estatísticas de valores (mínimo, médio, máximo)
    @cvar _estatistica: Lista das estatísticas que estão sendo calculadas
    '''
    _estatistica = None

    def __init__(self, *args):
        '''
        Construtor
        @param *args: lista de estatísticas que serão calculadas
        '''
        self._estatistica = {}
        for pos in args:
            self._estatistica[pos] = {'Minimo':float('inf'),
                                      'Medio': None,
                                      'Maximo':-float('inf'),
                                      'somatorio':0,
                                      'passagens':0}
        pass
    def estatisticas(self, pos, value):
        '''
        Insere mais um valor para a estatística
        @param pos: a estatística a ser calculada
        @param value: o novo valor que comporá a estatística
        '''
        self._estatistica[pos]['somatorio'] += value
        if value < self._estatistica[pos]['Minimo']:   self._estatistica[pos]['Minimo'] = value
        if value > self._estatistica[pos]['Maximo']:   self._estatistica[pos]['Maximo'] = value
        self._estatistica[pos]['passagens'] += 1
        self._estatistica[pos]['Medio'] = self._estatistica[pos]['somatorio'] / self._estatistica[pos]['passagens']
        pass
    pass
