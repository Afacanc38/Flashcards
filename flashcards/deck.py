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
    lbl_deck_name = Gtk.Template.Child('lbl_deck_name')
    btn_study = Gtk.Template.Child('btn_study')

    _deck_name = 'undefined'
    _card_num = 0

    @GObject.Property(type=str, default='undefined')
    def deck_name(self):
        return self._deck_name

    @deck_name.setter
    def deck_name(self, name):
        self._name = name
        self.lbl_deck_name.set_label(name)

    @GObject.Property(type=int, default=0)
    def card_num(self):
        return self._card_num

    @card_num.setter
    def card_num(self, card_num):
        self._card_num = card_num
        self.lbl_card_num.set_label(card_num)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)