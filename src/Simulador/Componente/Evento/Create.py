#coding: utf-8
'''
Created on May 22, 2016

@author: cesar
'''
from .Delay import Delay
from ..Entidade.Entity import Entity

class Create(Delay):
    '''
    Classe responsável por criar novas entidades.
    @cvar _nome_da_entidade: Nome da entidade a ser criada
    @cvar _quantos_por_vez: Quantas entidades serão criadas por evento
    @cvar _quantas_vezes: Quantas vezes o evento será executado
    '''
    _nome_da_entidade = None
    _quantos_por_vez = 1
    _quantas_vezes = float('inf')

    def __init__(self,
                 nome,
                 next_event,
                 fgva,
                 nome_entidade,
                 quantos_por_vez = 1,
                 quantas_vezes = float('infinity')):
        '''
        Construtor do evento 'create'
        @param nome: Nome do módulo
        @type nome: string
        @param fgva: Gerador de variáveis aleatórias para o delay entre criações de entidades.
        @type fgva: Simulador.FGVA
        @param nome_entidade: Nome da entidade a ser criada
        @type nome_entidade: string
        @param quantos_por_vez: Quantas entidades serão criadas por evento
        @type quantos_por_vez: int
        @param quantas_vezes: Até quantas vezes este módulo/evento será executado
        @type quantas_vezes: int
        '''
        Delay.__init__(self, nome, fgva, next_event)
        self._nome_da_entidade = nome_entidade
        self._quantos_por_vez = quantos_por_vez
        self._quantas_vezes = quantas_vezes
        #Adiciona create à LEF
        self.add_evento_futuro(0, None, nome)
        pass
    def __call__(self,
                 entity):
        '''
        Função de execução do evento
        Cria uma certa quantidade de entidades (passada no construtor),
        e, caso a cota de criações de entidades não esteja batida,
        coloca a si mesmo na lista de eventos futuros
        programado para um determinado tempo segundo seu FGVA
        @param entity: Por este módulo não passa nenhuma entidade (diferente dos outros módulos, onde é útil)
        '''
        for _ in range(self._quantos_por_vez):
            self.add_evento_futuro(0, Entity(self._nome_da_entidade), self._next_event)
            pass
        self._quantas_vezes -= 1
        if self._quantas_vezes > 0:
            self.add_evento_futuro(next(self._fgva), None, self._name) # updated
            pass
        pass
    pass