#coding: utf-8
'''
Created on May 22, 2016

@author: cesar
'''
import math
from .GNA import GNA

class FGVA(object):
    '''
    Classe responsável pela geração de variáveis aleatórias.
    '''
    @staticmethod
    def Constante(c):
        '''
        Criador de um gerador de valores constante.
        @param c: valor constante a ser retornada pelo gerador.
        @return: um gerador de valores constantes
        '''
        while True: yield c
        pass
    @staticmethod
    def Normal(media, desvio_padrao, Z1 = True, seed = 0):
        '''
        Criador de um gerador de valores seguindo uma distribuição normal
        @param media: média da função normal
        @param desvio_padrao: desvio padrão da função normal
        @param Z1: identifica se será utilizada a função Z1 do método de Box-Muller (default: True)
        @param seed: semente para o gerador de variáveis aleatórias (default: 0)
        @return: um gerador de variáveis aleatórios seguindo uma distribuição normal
        '''
        gna = GNA.LinearCongruentialGenerator(seed = seed)
        while True:
            u1 = gna.next()
            u2 = gna.next()
            Z = math.sqrt(-2 * math.log(u1))
            if Z1:  Z *= math.cos(2 * math.pi * u2)
            else:   Z *= math.sin(2 * math.pi * u2)
            yield media + desvio_padrao * Z
            pass
        pass
    @staticmethod
    def Exponencial(taxa_decaimento, seed = 0):
        '''
        Criador de um gerador de valores seguindo uma distribuição exponencial
        @param taxa_decaimento: taxa de decaimento da função exponencial
        @param seed: semente para o gerador de variáveis aleatórias (default: 0)
        @return: um gerador de variáveis aleatórios seguindo uma distribuição exponencial
        '''
        gna = GNA.LinearCongruentialGenerator(seed = seed)
        while True:
            u = gna.next()
            yield - math.log(1 - u) / taxa_decaimento
            pass
        pass
    @staticmethod
    def Triangular(a, b, c, seed = 0):
        '''
        Criador de um gerador de valores seguindo uma distribuição triangular
        @param a: valor mínimo retornado pelo gerador
        @param b: moda dos valores retornados pelo gerador
        @param c: valor máximo retornado pelo gerador
        @param seed: semente para o gerador de variáveis aleatórias (default: 0)
        @return: um gerador de variáveis aleatórios seguindo uma distribuição triangular
        '''
        gna = GNA.LinearCongruentialGenerator(seed = seed)
        while True:
            u = gna.next()
            if u < (b - a) / (c - a):
                    yield a + math.sqrt(u * (b - a) * (c - a))
            else:   yield c - math.sqrt((1 - u) * (c - b) * (c - a))
            pass
        pass
    @staticmethod
    def Uniforme(a, b, seed = 0):
        '''
        Criador de um gerador de valores seguindo uma distribuição uniforme
        @param a: valor mínimo retornado pelo gerador
        @param c: valor máximo retornado pelo gerador
        @param seed: semente para o gerador de variáveis aleatórias (default: 0)
        @return: um gerador de variáveis aleatórios seguindo uma distribuição uniforme
        '''
        gna = GNA.LinearCongruentialGenerator(seed = seed)
        while True:
            u = gna.next()
            yield a + u * (b - a)
            pass
        pass 
    pass
