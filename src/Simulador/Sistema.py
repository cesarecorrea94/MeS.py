#coding: utf-8
'''
Created on May 21, 2016

@author: cesar
'''
from operator import itemgetter, attrgetter
from time import sleep
from threading import Thread
import threading
from itertools import product
from .Componente.Entidade.Entity import Entity
from .Componente.Entidade.Resource import Resource
from .Componente.Evento.Delay import Delay
from .Componente.Evento.Create import Create
from .Componente.Evento.Assign import Assign
from .Componente.Evento.Record import Count
from .Componente.Evento.Seize import Seize
from .Componente.Evento.Release import Release
from .Componente.Evento.Decide import Chance, Condition
from .Componente.Evento.Dispose import Dispose
from Simulador.Componente.Evento.Record import Time_Interval, Get_In, Get_Out
from Simulador.Componente.Evento.Evento import Evento

class Sistema(Thread):
    '''
    Responsável pelo sistema. Carrega o relógio, a lista de eventos futuros, a lista de recursos,
    e a lista de processos.
    @cvar _system: O sistema em si
    @type _system: Sistema
    @cvar _relogio: Relógio do sistema
    @cvar _lista_eventos_futuros: Lista de eventos futuros do sistema
    @cvar _velocidade: Velocidade de execução do sistema
    @cvar _pause_flag: Sinalizador de "Pause" para o sistema
    @cvar _finish: Identifica se o sistema deve finalizar
    '''
    _system = None
    _relogio = 0
    _lista_eventos_futuros = []
    _velocidade = 0
    _pause_flag = threading.Event()
    _finish = False

    @staticmethod
    def get_relogio():  return Sistema._system._relogio
    @staticmethod
    def get_system():   return Sistema._system

    def __init__(self,
                 tempo_execucao=float('infinity')):
        '''
        Cria um novo sistema, inicializa todos os recursos e processos.
        @type tempo_execucao: number
        @param tempo_execucao: Tempo de execução do sistema
        '''
        from .GUI import GUI
        Thread.__init__(self)
        Sistema._system = self
        self._pause_flag.set()
        self.add_event(tempo_execucao, None, self)
        #Recursos
        for destino in ('L','R'):
            Resource(nome=      'Servidor Destino '+destino,
                     quantos=   GUI.get_id("n servidores destino "+destino)
                     )
            pass
        Resource(nome=      'Mensagens no Sistema',
                 quantos=   0)
        #Processos
        for origem in ('L','R'):
            Create(nome=            'Cria Origem '+origem,
                   fgva=            GUI.get_fgva("TEC "+origem),
                   nome_entidade=   'Origem '+origem,
                   next_event=      'Atribui Origem '+origem,
                   )
            Assign(nome=            'Atribui Origem '+origem,
                   atribuicoes=     [('Origem', origem)],
                   next_event=      'Decide Destino de Origem '+origem,
                   )
            Chance(nome=            'Decide Destino de Origem '+origem,
                   chances=         [(GUI.get_id("proporção "+origem+"L"),
                                      'Atribui Destino L')],
                   else_event=      'Atribui Destino R'
                   )
            pass
        for destino in ('L','R'):
            Assign(nome=            'Atribui Destino '+destino,
                   atribuicoes=     [('Destino', destino)],
                   next_event=      'Atribui Tempo de Chegada',
                   )
            pass
        Assign(nome=            'Atribui Tempo de Chegada',
               atribuicoes=     [('TChegada', 'TNOW')],
               next_event=      'Entra Mensagem',
               )
        Get_In(nome=            'Entra Mensagem',
               recurso=         'Mensagens no Sistema',
               next_event=      'Centro de Recepção')
        Delay(nome=             'Centro de Recepção',
              fgva=             GUI.get_fgva("recepção"),#FGVA.Triangular(0.10, 0.15, 0.20),
              next_event=       'Decide Centro de Serviço',
              )
        Condition(nome=             'Decide Centro de Serviço',
                  attr=             'Destino',
                  condicoes=        [('==', 'L',
                                      'Toma Servidor Destino L')],
                  else_event=       'Toma Servidor Destino R',
                  )
        for destino in ('L','R'):
            servidor = 'Servidor Destino '+destino
            Seize(nome=             'Toma '+servidor,
                  recurso=          servidor,
                  next_event=       'Verifica Origem de Destino '+destino)
            Condition(nome=         'Verifica Origem de Destino '+destino,
                      attr=         'Origem',
                      condicoes=    [('==', 'L',
                                      'Decide Resultado L'+destino)],
                      else_event=   'Decide Resultado R'+destino,
                      )
            for origem in ('L','R'):
                orig_dest = origem+destino
                chance = {}
                chance['S'] = GUI.get_id("proporção "+orig_dest+"S")
                chance['F'] = GUI.get_id("proporção "+orig_dest+"F") + chance['S']
                chance['A'] = GUI.get_id("proporção "+orig_dest+"A") + chance['F']
                nome = 'Decide Resultado '+orig_dest
                Chance(nome=            nome,
                       chances=         [(chance['S'],   orig_dest+'S'),
                                         (chance['F'],   orig_dest+'F'),
                                         (chance['A'],   orig_dest+'A'),
                                         ],
                       else_event=      nome,
                       )
                pass
        conta_resultado_goto = {'S': 'Calcula Tempo de Transito',
                                'F': 'Conta Despachadas',
                                'A': 'Decide Centro de Serviço',
                                };
        for resultado in ('S','F','A'):
            modulo_contador = 'Conta '+resultado
            for destino in ('L','R'):
                servidor = 'Servidor Destino '+destino
                modulo_libera = resultado+' Libera '+servidor
                for origem in ('L','R'):
                    nome = origem+destino+resultado
                    Delay(nome=         nome,
                          fgva=         GUI.get_fgva("tempo "+nome),
                          next_event=   modulo_libera,
                          )
                    pass
                Release(nome=           modulo_libera,
                        recurso=        servidor,
                        next_event=     modulo_contador,
                        )
                pass
            Count(nome=         modulo_contador,
                  next_event=   conta_resultado_goto[resultado]
                  )
            pass
        Time_Interval(nome=         'Calcula Tempo de Transito',
                      attr=         'TChegada',
                      next_event=   'Conta Despachadas')
        Count(nome=         'Conta Despachadas',
              next_event=   'Sai Mensagem')
        Get_Out(nome=       'Sai Mensagem',
                recurso=    'Mensagens no Sistema',
                next_event= 'Dispose')
        Dispose('Dispose')
        print "Sistema Iniciado"
        pass
    def __call__(self, entity):
        self.finish()
        pass
    def finish(self):
        '''
        Finaliza a simulação.
        '''
        del self._lista_eventos_futuros[:]
        Evento._processos.clear()
        Resource._recursos.clear()
        Entity._id = 0
        #sleep(float(GUI._intervalo.microseconds)/10**6) # deprecated
        #GUI.update_GUI() # deprecated
        Sistema._system = None
        pass
    def __repr__(self): return type(self).__name__
    def run(self):
        '''
        Realiza os eventos da lista de eventos futuros,
        e chama a classe GUI para atualizar as estatísticas.
        '''
        from GUI import GUI
        while len(self._lista_eventos_futuros) > 0:
            relogio, entidade, evento = self._lista_eventos_futuros.pop(0)
            self._relogio = relogio
            Evento._processos[evento](entidade)
            #GUI.update_GUI() # deprecated
            sleep(pow(2, -self._velocidade))
            self._pause_flag.wait()
            if self._finish: self(None)
            pass
        pass
    def add_event(self, daqui_a_quanto_tempo, entidade, evento):
        '''
        Adiciona um evento a lista de eventos futuros.
        @param daqui_a_quanto_tempo: o tempo de espera para realizar o evento.
        @param entidade: a entidade que realizará o evento.
        @type entidade: Simulador.Componente.Entidade.Entity
        @param evento: o evento em si.
        @type evento: Simulador.Componente.Evento.Evento
        '''
        if daqui_a_quanto_tempo < 0: daqui_a_quanto_tempo = 0
        tempo = self._relogio + daqui_a_quanto_tempo
        item = (tempo, entidade, evento)
        self._lista_eventos_futuros.append(item)
        self._lista_eventos_futuros.sort(key=itemgetter(0))
        pass
    pass
