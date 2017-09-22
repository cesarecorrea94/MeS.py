#coding: utf-8
'''
Created on 15/10/2016

@author: cesar
'''
from .Evento import Evento

class Dispose(Evento):
    '''
    classdocs
    '''

    def __init__(self,
                 nome):
        '''
        Constructor
        @param nome: Nome do módulo
        @type nome: string
        '''
        Evento.__init__(self, nome, None)
        pass
    def __call__(self,
                 entity):
        '''
        Deixa de criar um novo evento que envolva a entidade, e assim ela está fora do sistema
        @param entity: entidade que está a sair do sistema
        @type entity: Entidade
        '''
        #del entity
        pass