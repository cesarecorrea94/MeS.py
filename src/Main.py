#!/usr/bin/env python
#coding: utf-8
'''
Created on May 21, 2016

@author: cesar
'''
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib
from Simulador.GUI import GUI
from os import sys

def main():
    '''
    Habilita multithread para o Gtk, abri o arquivo com a interface do usuário, conecta os sinais
    do usuário (botões) a rotinas, e chama a rotina Gtk.main()
    '''
    #GObject.threads_init()
    #GLib.threads_init()
    #Gdk.threads_init() # deprecated
    
    #Gdk.threads_enter() # deprecated
    
    GUI._builder = Gtk.Builder()
    GUI._builder.add_from_file("myglade.glade")
    GUI._builder.connect_signals({
            "on_Velocidade_value_changed": GUI.Velocidade_value_changed,
            "on_Iniciar_clicked": GUI.Iniciar_clicked,
            "on_Play/Pause_toggled": GUI.Play_Pause_toggled,
            "on_Stop_clicked": GUI.Stop_clicked,
            "on_dialog1_destroy": GUI.Stop_clicked,
            "on_Salvar_clicked": GUI.Salvar_clicked,
            "on_window1_destroy": GUI.quit,
            })
    GUI._builder.get_object('window1').show_all()
    GLib.timeout_add(250, GUI.update_GUI) # new
    Gtk.main()
    
    #Gdk.threads_leave() # deprecated
    pass

if __name__ == '__main__':
    sys.exit(main())
    pass
