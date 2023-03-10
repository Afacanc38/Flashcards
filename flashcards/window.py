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

@Gtk.Template(resource_path='/io/github/afacanc38/flashcards/ui/mainwindow.xml')
class FlashcardsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'FlashcardsWindow'

    btn_quickstart_new_deck = Gtk.Template.Child()
    stk_main = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stk_main.set_visible_child_name('decks')