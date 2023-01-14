#!/usr/bin/env python3
import gi
import sys
from os.path import abspath, dirname, join
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib, Gio, Gdk, GObject
import flashcardapi

APP_DIR = '/'.join(abspath(dirname(__file__)).split('/')[:-1])

resource = Gio.Resource.load(APP_DIR + '/data/io.github.afacanc38.flashcards.gresource')
Gio.Resource._register(resource)

decks = [flashcardapi.Deck("İngilizce"), flashcardapi.Deck("Zort zort")]

from window import FlashcardsWindow
from deck import FlashcardsDeck
from study import FlashcardsStudyWindow
from flashcard import FlashcardsFlashcard
from editdeckdialog import FlashcardsEditDeckDialog

class Application(Adw.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        GLib.set_application_name('Flashcards')
        GLib.set_prgname('Flashcards')

        act = Gio.SimpleAction(name='about')
        act.connect('activate', self.on_about)
        self.add_action(act)

        act = Gio.SimpleAction(name='shortcuts')
        act.connect('activate', self.on_show_shortcuts)
        self.add_action(act)

        act = Gio.SimpleAction(name='study')
        act.connect('activate', self.on_study)
        self.add_action(act)

        act = Gio.SimpleAction(name='newdeck')
        act.connect('activate', self.on_newdeck)
        self.add_action(act)

        self.set_accels_for_action("window.close", ("<Ctrl>q","<Ctrl>w"))
        self.set_accels_for_action("app.shortcuts", ("<Ctrl>question",))

    def on_activate(self, app):
        theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        theme.add_resource_path("/io/github/afacanc38/flashcards/icons")

        self.win = self.props.active_window
        if not self.win:
            self.win = FlashcardsWindow()
            self.win.set_application(app)
            self.win.present()

    def on_about(self, action, param):
        about = Adw.AboutWindow()
        about.set_transient_for(self.get_active_window())
        about.set_modal(True)
        about.set_version("0.1-alpha")
        about.set_application_name("Flashcards")
        about.set_application_icon("io.github.afacanc38.Flashcards")
        about.set_developers(["Alperen İsa Nalbant"])
        about.set_comments("Memorizing Made Easy")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_copyright("Copyleft © 2022 Alperen İsa Nalbant")
        # Translators: Replace "translator-credits" with your names, one name per line
        about.set_translator_credits("Alperen İsa Nalbant")
        about.set_website("https://afacanc38.github.io")
        about.set_release_notes("<p>Initial release</p>")
        about.present()
        
    def on_study(self, action, param):
        fsw = FlashcardsStudyWindow()
        fsw.set_transient_for(self.get_active_window())
        fsw.set_modal(True)
        fsw.present()

    def on_show_shortcuts(self, action, param):
        builder = Gtk.Builder()
        builder.add_from_resource('/io/github/afacanc38/flashcards/ui/shortcuts.xml')
        help = builder.get_object('help_overlay')
        help.set_transient_for(self.get_active_window())
        help.present()

    def on_newdeck(self, action, param):
        ed = FlashcardsEditDeckDialog()
        ed.set_transient_for(self.get_active_window())
        ed.set_modal(True)
        ed.present()

if __name__ == '__main__':
    app = Application(application_id = 'io.io.github.afacanc38.flashcards')
    app.run()

