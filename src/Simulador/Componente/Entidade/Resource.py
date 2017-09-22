#coding: utf-8
'''
Created on May 21, 2016

@author: cesar
'''
from .Entity import Entity

class Resource(object):
    '''
    Representa tipos de recursos no sistema
    @cvar _recursos: Lista dos recursos no sistema
    @type _recursos: list / []
    @ivar _numero_de_recursos: Quantidade de recursos existentes
    @type _numero_de_recursos: int
    @ivar _avaiable: Quantidade de recursos disponíveis
    @type _avaiable: int
    @ivar _queue: Fila de rotinas (as quais serão executadas após a obtenção de um recurso) de entidades a espera de um recurso.
    #@ivar _queue: Fila de tuplas (entity, next_event).
    @type _queue: list / []
    #@keyword entity: Entidade que está a espera do recurso
    #@type entity: Entidade
    #@keyword next_event: Evento a ser executado após a posse do recurso
    #@type next_event: string
    @ivar _somatorio_dos_tempos_livres: Somatório dos tempos livres dos recursos
    @type _somatorio_dos_tempos_livres: float
    @ivar _ultima_atualizacao: Momento da última atualização das estatísticas
    @type _ultima_atualizacao: float
    @ivar _taxa_media_de_utilizacao: Taxa média de utilização dos recursos
    @type _taxa_media_de_utilizacao: float
    @ivar _name: Nome do recurso
    @type _name: string
    '''
    _recursos = {}#static
    _numero_de_recursos = 0
    _avaiable = 0
    _queue = None
    _somatorio_dos_tempos_livres = 0
    _ultima_atualizacao = 0
    _taxa_media_de_utilizacao = None
    _name = None
    
    @staticmethod
    def get_resource(nome):
        '''
        @param nome: Nome do recurso
        @type nome: string
        '''
        return Resource._recursos[nome]
    def __init__(self,
                 nome,
                 quantos):
        '''
        Cria um novo tipo de recurso no sistema
        @param nome: Nome do recurso
        @type nome: string
        @param quantos: Quantos recursos haverão
        @type quantos: int
        '''
        Resource._recursos[nome] = self
        self._name = nome
        self._queue = []
        self._numero_de_recursos = quantos
        self._avaiable = quantos
        pass
    def __repr__(self):
        return self._name
    def release(self):
        '''
        Libera um recurso.
        Se houver alguém a espera pelo recurso, já atende-o
        '''
        self.atualiza_estatistica()
        if len(self._queue) > 0:
            after_seized = self._queue.pop(0)
            after_seized()
            pass
        else: self._avaiable += 1
        pass
    def seize(self, after_seized):
        '''
        Obtém um recurso.
        Se não houver recursos disponíveis, fica numa fila de espera
        @param after_seized: função a ser chamada após a obtenção do recurso
        '''
        self.atualiza_estatistica()
        if self._avaiable > 0:
            self._avaiable -= 1
            after_seized()
            pass
        else: self._queue.append(after_seized)
        pass
    def atualiza_estatistica(self):
        '''
        Atualiza as estatísticas
        '''
        from ...Sistema import Sistema
        TNOW = Sistema.get_relogio()
        self._somatorio_dos_tempos_livres += self._avaiable * (TNOW - self._ultima_atualizacao)
        self._ultima_atualizacao = TNOW
        if not TNOW == 0:
            self._taxa_media_de_utilizacao = self._numero_de_recursos - self._somatorio_dos_tempos_livres / TNOW
        pass
    pass