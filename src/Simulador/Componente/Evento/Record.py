#coding: utf-8
'''
Created on 15/10/2016

@author: cesar
'''
from .Evento import Evento
from ..Miscelanea.Estatistica import Estatistica
from Simulador.Componente.Evento.Seize import Seize
from Simulador.Componente.Evento.Release import Release

class Count(Evento):
    '''
    Classe representante de um evento contador de entidades que passam por ele
    @ivar _contador: Contador de entidades que passaram
    @type _contador: int
    '''
    _contador = 0

    def __init__(self,
                 nome,
                 next_event):
        '''
        Construtor do contador
        @param nome: Nome do contador
        @type nome: string
        @param next_event: Nome do próximo módulo
        @type next_event: string 
        '''
        Evento.__init__(self, nome, next_event)
        pass
    def __call__(self,
                 entity):
        '''
        Função de execução do evento 'contador'.
        Incrementa o número de entidades que passaram por ele
        @param entity: entidade que está a passar pelo contador
        @type entity: Simulador.Componente.Entidade.Entity
        '''
        self._contador += 1
        self.add_evento_futuro(0, entity, self._next_event)
        pass
    pass

class Time_Interval(Evento, Estatistica):
    '''
    @ivar _attr: Nome do atributo em que está o tempo para o cálculo do intervalo
    @type _attr: string
    '''
    _attr = None

    def __init__(self,
                 nome,
                 next_event,
                 attr):
        '''
        @param nome: Nome do módulo
        @type nome: string
        @param next_event: Nome do próximo módulo
        @type next_event: string
        @param attr: Nome do atributo em que está o tempo para o cálculo do intervalo
        @type attr: string
        '''
        Evento.__init__(self, nome, next_event)
        Estatistica.__init__(self, nome)
        self._attr = attr
        pass
    def __call__(self,
                 entity):
        '''
        @param entity: Entidade que está a passar pelo módulo
        @type entity: Simulador.Componente.Entidade.Entity
        '''
        TNOW = self.get_TNOW()
        interval = TNOW - getattr(entity, self._attr)
        self.estatisticas(self._name, interval)
        #next event
        self.add_evento_futuro(0, entity, self._next_event)
        pass
    pass

class Time_Between(Evento, Estatistica):
    '''
    @ivar _ultima_passagem: Momento da última passagem de uma entidade por esse módulo
    @type _ultima_passagem: int
    '''
    _ultima_passagem = 0

    def __init__(self,
                 nome,
                 next_event):
        '''
        @param nome: Nome do módulo
        @type nome: string
        @param next_event: Nome do próximo módulo
        @type next_event: string
        '''
        Evento.__init__(self, nome, next_event)
        Estatistica.__init__(self, nome)
        pass
    def __call__(self,
                 entity):
        '''
        @param entity: entidade que está a passar pelo módulo
        @type entity: Simulador.Componente.Entidade.Entity
        '''
        TNOW = self.get_TNOW()
        interval = TNOW - self._ultima_passagem
        self.estatisticas(self._name, interval)
        self._ultima_passagem = TNOW
        #next event
        self.add_evento_futuro(0, entity, self._next_event)
        pass
    pass

class Get_In(Seize):
    def __init__(self,
                 nome,
                 recurso,
                 next_event):
        '''
        Construtor de um evento 'seize'.
        @param recurso: recurso a ser obtido no evento
        @type recurso: Simulador.Componente.Entidade.Resource
        '''
        Seize.__init__(self, nome, recurso, next_event)
        pass
    def __call__(self,
                 entity):
        '''
        Função de execução do evento 'seize'
        Tenta ocupar um recurso.
        Ao ocupar um recurso, coloca o próximo evento a ser executado pela entidade na lista de eventos
        @param entity: entidade a executar o evento
        @type entity: Simulador.Componente.Entidade.Entity
        '''
        self._queue.append(entity)
        def seized():
            self._queue.remove(entity)
            pass
        from ..Entidade.Resource import Resource
        Resource.get_resource(self._resource_name).seize(seized)
        self.add_evento_futuro(0, entity, self._next_event)
        pass
    pass

class Get_Out(Release):
    def __init__(self,
                 nome,
                 recurso,
                 next_event):
        '''
        Construtor de um módulo 'release'.
        @param nome: Nome do módulo
        @type nome: string
        @param recurso: Nome do recurso a ser liberado no evento
        @type recurso: string
        @param next_event: Nome do próximo módulo
        @type next_event: string
        '''
        Release.__init__(self, nome, recurso, next_event)
        pass
    def __call__(self,
                 entity):
        '''
        Função de execução do evento 'release'
        Libera um recurso, e coloca o próximo evento a ser executado pela entidade na lista de eventos
        @param entity: entidade a executar o evento
        @type entity: Simulador.Componente.Entidade.Entity
        '''
        from ..Entidade.Resource import Resource
        Resource.get_resource(self._resource_name).release()
        self.add_evento_futuro(0, entity, self._next_event)
        pass
    pass
