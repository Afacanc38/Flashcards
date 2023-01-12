#!/usr/bin/env python3
import gi
import sys
from os.path import abspath, dirname, join
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib, Gio, Gdk, GObject

APP_DIR = '/'.join(abspath(dirname(__file__)).split('/')[:-1])

resource = Gio.Resource.load(APP_DIR + '/data/io.github.afacanc38.flashcards.gresource')
Gio.Resource._register(resource)

@Gtk.Template(resource_path='/io/github/afacanc38/flashcards/ui/flashcardsdeck.xml')
class FlashcardsDeck(Gtk.Box):
    __gtype_name__ = 'FlashcardsDeck'

    lbl_card_num = Gtk.Template.Child('lbl_card_num')
    btn_study = Gtk.Template.Child('btn_study')

    def __init__(self, **kwargs):
        self.card_num = 0
        self.set_card_num("5")

    def set_card_num(self, card_num):
        self.lbl_card_num.set_label(f'{card_num} cards')
        self.card_num = card_num

    def get_card_num(self):
        return self.lbl_card_num.get_label()