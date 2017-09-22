#coding: utf-8
'''
Created on May 23, 2016

@author: cesar
'''
from gi.repository import Gtk
from datetime import datetime, timedelta
from time import sleep
from .FGVA import FGVA
from .Sistema import Sistema
from Simulador.Componente.Evento.Evento import Evento
from Simulador.Componente.Entidade.Resource import Resource

class InitError(Exception): pass

class GUI(object):
    '''
    Responsável pela comunicação com o usuário. Obtém os dados passados pelo usuário para o
    Sistema, e informa as estatísticas alterando valores na interface usuário.
    @cvar _builder: Objeto que carrega os widgets da interface usuário
    @cvar _utlimo_update: Momento da último 'refresh' da interface usuário
    @cvar _intervalo: Intervalo que deve-se dar 'refresh' na interface usuário
    '''
    _builder = None
    _utlimo_update = datetime.now()
    _intervalo = timedelta(seconds=1.0/4)

    @staticmethod
    def quit(widget):
        '''
        Encerra a simulação e fecha o programa.
        @param widget: widget que enviou o sinal para a chamada da rotina (o botão fechar).
        '''
        GUI.Stop_clicked(widget)
        Gtk.main_quit()
    @staticmethod
    def Velocidade_value_changed(widget):
        '''
        Altera a velocidade da simulação.
        @param widget: widget que enviou o sinal para a chamada da rotina (Gtk.Scale).
        '''
        Sistema.get_system()._velocidade = GUI._builder.get_object('Velocidade').get_value()
        pass
    @staticmethod
    def Iniciar_clicked(widget):
        if not Sistema.get_system() is None: return
        #n_caminhoes = GUI._builder.get_object('n_caminhoes').get_value()
        try: Sistema()
        except InitError:
            if not Sistema.get_system() is None:
                Sistema.get_system().finish()
            return
        Sistema.get_system().start()
        Sistema.get_system()._pause_flag.set()
        GUI._builder.get_object("dialog1").show_all()
        pass
    @staticmethod
    def Play_Pause_toggled(widget):
        '''
        Inicia/pausa/continua uma simulação.
        @param widget: widget que enviou o sinal para a chamada da rotina (o botão "Play/Pause").
        '''
        if not widget.get_active():#Play
            Sistema.get_system()._pause_flag.set()
            #for ID in ('caminhoes_spin','TC','TP','TT'):
            #    GUI._builder.get_object(ID).set_editable(False)
            #    pass
            pass
        elif not Sistema.get_system() is None:
            Sistema.get_system()._pause_flag.clear()
            pass
        pass
    @staticmethod
    def Stop_clicked(widget):
        '''
        Para uma simulação. (As estatísticas da simulação permanecem visíveis).
        @param widget: widget que enviou o sinal para a chamada da rotina (o botão "Stop").
        '''
        GUI._builder.get_object("dialog1").hide()
        if Sistema.get_system() is None: return
        Sistema.get_system()._finish = True
        Sistema.get_system()._pause_flag.set()
        #for ID in ('caminhoes_spin','TC','TP','TT'):
        #    GUI._builder.get_object(ID).set_editable(True)
        #    pass
        pass
    @staticmethod
    def get_id(ID):
        '''
        '''
        objeto = GUI._builder.get_object(ID)
        try:
            if ID.startswith("proporção"):
                proporcao = float(objeto.get_text()) / 100
                return proporcao
            elif ID.startswith("n servidores destino"):
                n = int(objeto.get_text())
                return n
            else: return GUI.get_fgva(ID)
        except ValueError:
            objeto.set_text('ERROR: '+objeto.get_text())
            raise InitError
    @staticmethod
    def get_fgva(ID):
        '''
        Cria um gerador de variáveis aleatórias.
        @param ID: ID do campo de entrada na interface usuário o qual deseja-se obter o dado.
        “TC” para obter a função para o Tempo de Carga,
        “TP” para o Tempo de Pesagem, e
        “TT” para o tempo de transporte.
        @type ID: str
        @raise InitError: Erro lançado caso haja algum erro em alguma das funções de distribuição passadas pelo usuário
        '''
        original = GUI._builder.get_object(ID).get_text()
        text = original.replace(' ','')
        if len(text) > 4+2 and text[4] == '(' and text[-1] == ')':
            arg = [float(i) for i in text[5:-1].split(',')]
            if text[0:4].upper() == 'CONS':
                if len(arg) == 1: return FGVA.Constante(arg[0])
                pass
            elif text[0:4].upper() == 'NORM':
                if len(arg) == 2:   return FGVA.Normal(arg[0], arg[1])
                elif len(arg) == 3: return FGVA.Normal(arg[0], arg[1], int(arg[2]))
                pass
            elif text[0:4].upper() == 'EXPO':
                if len(arg) == 1:   return FGVA.Exponencial(arg[0])
                elif len(arg) == 2: return FGVA.Exponencial(arg[0], int(arg[1]))
                pass
            elif text[0:4].upper() == 'TRIA':
                if len(arg) == 3:   return FGVA.Triangular(arg[0], arg[1], arg[2])
                elif len(arg) == 4: return FGVA.Triangular(arg[0], arg[1], arg[2], int(arg[3]))
                pass
            elif text[0:4].upper() == 'UNIF':
                if len(arg) == 2:   return FGVA.Uniforme(arg[0], arg[1])
                elif len(arg) == 3: return FGVA.Uniforme(arg[0], arg[1], int(arg[2]))
                pass
            pass
        GUI._builder.get_object(ID).set_text('ERROR: '+original)
        raise InitError
    @staticmethod
    def update_GUI():
        '''
        Atualiza as estatísticas, o relógio, e a lista de eventos futuros na interface usuário.
        '''
        if Sistema.get_system() is None: return True # new
        if datetime.now() - GUI._utlimo_update < GUI._intervalo: return True # updated
        GUI._utlimo_update = datetime.now()
        #from gi.repository import Gdk # deprecated
        #Gdk.threads_enter() # deprecated
        GUI.show_estatisticas()
        GUI.show_LEF()
        #Gdk.threads_leave() # deprecated
        return True # new
    @staticmethod
    def show_estatisticas():
        '''
        Atualiza as estatísticas na interface usuário.
        '''
        for processo in ['Entra Mensagem']:
            for estatistica in ['Minimo','Medio','Maximo']:
                texto = Evento._processos[processo]._queue._tamanho_da_fila[estatistica]
                GUI._builder.get_object('Msg no Sistema '+estatistica).set_text(str(texto))
                pass
            pass
        for recurso in ['Servidor Destino L','Servidor Destino R']:
            utilizacao = Resource._recursos[recurso]._taxa_media_de_utilizacao
            GUI._builder.get_object(recurso).set_text(str(utilizacao))
            pass
        for processo in ['Calcula Tempo de Transito']:
            for estatistica in ['Minimo','Medio','Maximo']:
                text = Evento._processos[processo]._estatistica[processo][estatistica]
                GUI._builder.get_object('TTMS '+estatistica).set_text(str(text))
                pass
            pass
        text = Evento._processos['Conta Despachadas']._contador
        GUI._builder.get_object('Despachadas').set_text(str(text))
        for resultado in ['Sucesso','Fracasso','Adiamento']:
            text = Evento._processos['Conta '+resultado[0]]._contador
            GUI._builder.get_object(resultado).set_text(str(text))
            pass
        pass
    @staticmethod
    def show_LEF():
        '''
        Atualiza o relógio e a lista de eventos futuros na interface usuário.
        '''
        GUI._builder.get_object('Relogio').set_text(str(Sistema.get_relogio()))
        box_lef = GUI._builder.get_object('LEF')
        def callback(widget, _):
            box_lef.remove(widget)
            pass
        box_lef.foreach(callback, None)
        for evento in Sistema.get_system()._lista_eventos_futuros:
            entry = Gtk.Entry()
            entry.set_text(str(evento))
            entry.set_width_chars(entry.get_text_length())
            entry.set_editable(False)
            box_lef.pack_start(entry, True, True, 0)
            pass
        box_lef.set_homogeneous(False)
        box_lef.show_all()
        pass
    @staticmethod
    def Salvar_clicked(widget):
        '''
        Salva as estatísticas num arquivo. O arquivo é salvo na mesma pasta do arquivo de execução.
        Seu nome é “Output 'data'.txt”, sendo “ 'data' ” a data de criação do arquivo.
        @param widget: widget que enviou o sinal para a chamada da rotina (o botão "Salvar").
        '''
        espacamento = 30
        with open("Output "+str(datetime.now())+".txt", 'w+') as fp:
            fp.write("Número de Mensagens no Sistema:\n")
            for estatistica in ['Minimo','Medio','Maximo']:
                fp.write(estatistica.ljust(espacamento))
                pass
            fp.write('\n')
            for estatistica in ['Minimo','Medio','Maximo']:
                text = GUI._builder.get_object('Msg no Sistema '+estatistica).get_text()
                fp.write(text.ljust(espacamento))
                pass
            fp.write('\n\n')
            ##
            fp.write("Taxa Média de Ocupação dos Centros:\n")
            for estatistica in ['Centro 1','Centro 2']:
                fp.write(estatistica.ljust(espacamento))
                pass
            fp.write('\n')
            for recurso in ['Servidor Destino L','Servidor Destino R']:
                text = GUI._builder.get_object(recurso).get_text()
                fp.write(text.ljust(espacamento))
                pass
            fp.write('\n\n')
            ##
            fp.write("Tempo de Transito das Mensagens no Sistema:\n")
            for estatistica in ['Minimo','Medio','Maximo']:
                fp.write(estatistica.ljust(espacamento))
                pass
            fp.write('\n')
            for estatistica in ['Minimo','Medio','Maximo']:
                text = GUI._builder.get_object('TTMS '+estatistica).get_text()
                fp.write(text.ljust(espacamento))
                pass
            fp.write('\n\n')
            ##
            fp.write("Contador de Mensagens Despachadas:\n")
            text = GUI._builder.get_object('Despachadas').get_text()
            fp.write(text.ljust(espacamento))
            fp.write('\n\n')
            ##
            fp.write("Contador de Mensagens por Tipo:\n")
            for resultado in ['Sucesso','Fracasso','Adiamento']:
                fp.write(resultado.ljust(espacamento))
                pass
            fp.write('\n')
            for resultado in ['Sucesso','Fracasso','Adiamento']:
                text = GUI._builder.get_object(resultado).get_text()
                fp.write(text.ljust(espacamento))
                pass
            fp.write('\n')
            pass
        pass
    pass
