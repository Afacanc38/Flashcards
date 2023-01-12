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

@Gtk.Template(resource_path='/io/github/afacanc38/flashcards/ui/flashcard.xml')
class FlashcardsFlashcard(Gtk.Box):
    __gtype_name__ = 'FlashcardsFlashcard'

    rvl_answer = Gtk.Template.Child('rvl_answer')
    lbl_front = Gtk.Template.Child('lbl_front')
    lbl_back = Gtk.Template.Child('lbl_back')

    _show_answer = False

    @GObject.Property(type=bool, default=False)
    def show_answer(self):
        return self._show_answer

    @show_answer.setter
    def show_answer(self, value):
        self._show_answer = value

        if value:
            self.rvl_answer.set_reveal_child(True)
        else:
            self.rvl_answer.set_reveal_child(False)

    # Setup Flashcard
    _front_label = ""

    @GObject.Property(type=str, default="")
    def front_label(self):
        return self._front_label

    @front_label.setter
    def front_label(self, value):
        self._front_label = value
        self.lbl_front.set_label(value)

    def set_front_label(self, value):
        self._front_label = value
        self.lbl_front.set_label(value)

    _back_label = ""

    @GObject.Property(type=str, default="")
    def back_label(self):
        return self._back_label

    @back_label.setter
    def front_label(self, value):
        self._back_label = value
        self.lbl_back.set_label(value)

    def set_back_label(self, value):
        self._back_label = value
        self.lbl_back.set_label(value)