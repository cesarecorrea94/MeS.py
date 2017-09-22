#coding: utf-8
'''
Created on May 22, 2016

@author: cesar
'''

class Entity(object):
    '''
    Representa uma entidade no sistema
    @ivar _name: Nome da entidade
    @cvar _id: ID para diferenciação de entidades
    '''
    _name = None
    _id = 0

    def __init__(self, name):
        '''
        Construtor de uma nova entidade
        @param name: Nome da entidade
        '''
        Entity._id += 1
        self._id = Entity._id
        self._name = name
        pass
    def __repr__(self):
        return self._name +' '+ str(self._id)
    pass