'''
Created on 19/10/2016

@author: cesar
'''

class Expression(object):
    '''
    classdocs
    '''
    _expression = None

    def __init__(self, expression):
        '''
        Constructor
        '''
        self._expression = expression
        pass
    def __call__(self):
        self._expression()
        pass