#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author Lander Usategui San Juan, lander.usategui@gmail.com, creado para Open Gasteiz

import pygtk
pygtk.require('2.0')

import gtk
import urllib2
import os

class Application():

    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("Open Gasteiz")

        self.create_widgets()
        self.connect_signals()

        self.window.show_all()
        gtk.main()

    def create_widgets(self):
        self.vbox = gtk.VBox(spacing=10)

        self.hbox_1 = gtk.HBox(spacing=10)
        self.label = gtk.Label("URL Youtube:")
        self.hbox_1.pack_start(self.label)
        self.entry = gtk.Entry()
        self.hbox_1.pack_start(self.entry)

        self.hbox_2 = gtk.HBox(spacing=10)
        self.button_ok = gtk.Button("OK")
        self.hbox_2.pack_start(self.button_ok)
        self.button_exit = gtk.Button("Exit")
        self.hbox_2.pack_start(self.button_exit)

        self.vbox.pack_start(self.hbox_1)
        self.vbox.pack_start(self.hbox_2)

        self.window.add(self.vbox)

    def connect_signals(self):
        self.button_ok.connect("clicked", self.callback_ok)
        self.button_exit.connect("clicked", self.callback_exit)

    def error_dialog(self,mensaje):
        dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"%s" %(mensaje))
        dialog.run()
        dialog.destroy()

    def callback_ok(self, widget, callback_data=None):
        youtubeURL = self.entry.get_text()
        if len(youtubeURL) != 0:
            if check_internet():
                #Comenzamos el streaming
                caputureVideo(youtubeURL)
            else:
                no_internet="Compruebe su acceso a internet"
                self.error_dialog(no_internet)
        else:
            bad_URL = "La URL no puede estar vacía"
            #print(bad_URL)
            self.error_dialog(bad_URL)
            gtk.main_quit()

    def callback_exit(self, widget, callback_data=None):
        gtk.main_quit()

def check_internet():
    # http://stackoverflow.com/questions/3764291/checking-network-connection
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err:
        return False

def caputureVideo(url):
    os.system("raspivid -o - -t 0 -vf -hf -fps 30 -b 6000000 | avconv -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv %s
" % (url))

if __name__ == "__main__":
    app = Application()
