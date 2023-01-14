#!/usr/bin/env python3
import gi
import sys
from os.path import abspath, dirname, join
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, Gdk, GObject

APP_DIR = '/'.join(abspath(dirname(__file__)).split('/')[:-1])

resource = Gio.Resource.load(APP_DIR + '/data/io.github.afacanc38.flashcards.gresource')
Gio.Resource._register(resource)

@Gtk.Template(resource_path='/io/github/afacanc38/flashcards/ui/edit_deck.xml')
class FlashcardsEditDeckDialog(Adw.Window):
    __gtype_name__ = 'FlashcardsEditDeckDialog'

    row_deck_name = Gtk.Template.Child('row_deck_name')
    row_flashcard_front = Gtk.Template.Child('row_flashcard_front')
    row_flashcard_back = Gtk.Template.Child('row_flashcard_back')
    btn_apply_changes = Gtk.Template.Child('btn_apply_changes')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.row_deck_name.connect('changed', self.on_invaild)
        self.row_flashcard_front.connect('changed', self.on_invaild)
        self.row_flashcard_back.connect('changed', self.on_invaild)
        self.row_deck_name.connect_after('changed', self.on_invaild)
        self.row_flashcard_front.connect_after('changed', self.on_invaild)
        self.row_flashcard_back.connect_after('changed', self.on_invaild)

    def on_invaild(self, widget):
        if widget.get_text().isspace() == True or\
        widget.get_text() == '':
            widget.add_css_class('error')
        else:
            widget.remove_css_class('error')
    def activate_apply_button(self, widget):
        pass