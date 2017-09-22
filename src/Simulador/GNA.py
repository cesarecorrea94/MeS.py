#coding: utf-8
'''
Created on May 23, 2016

@author: cesar
'''
import math
import fractions

class GNA(object):
    '''
    Classe responsável pela geração de números aleatórios.
    '''
    @staticmethod
    def LinearCongruentialGenerator(n_bits = 4*8, seed = 0):
        '''
        Gerador de números aleatórios
        @param n_bits: número de bits que comporá o número (default: 4*8 = 4 bytes).
        O número gerado estará no intervalo [0, 2^'n_bits'[.
        @param seed: semente para o gerador de números aleatórios (default: 0)
        @return: um gerador de números aleatórios.
        '''
        assert isinstance(n_bits, (int, long))
        m = pow(2, n_bits)
        x = seed
        a = round(math.log(m) * math.e)
        a = a * 4 + 1
        #todo fator primo de 'm' (i.e. 2), tambem e um fator primo de 'a-1'
        #'a-1' e multiplo de 4, se 'm' e multiplo de 4
        b = m / 4 - 1
        b /= fractions.gcd(b, m)
        #'m' e 'b' sao primos entre si
        while True:
            x = (x * a + b) % m
            yield 1.0 * x / m
            pass
        pass
    pass
