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

@Gtk.Template(resource_path='/io/github/afacanc38/flashcards/ui/study.xml')
class FlashcardsStudyWindow(Adw.Window):
    __gtype_name__ = 'FlashcardsStudyWindow'

    lbl_remaining_card_num = Gtk.Template.Child('lbl_remaining_card_num')
    carousel = Gtk.Template.Child('carousel')
    btn_show_answer = Gtk.Template.Child('btn_show_answer')

    btn_next_flashcard = Gtk.Template.Child('btn_next_flashcard')
    btn_add_to_repeat = Gtk.Template.Child('btn_add_to_repeat')
    stk_study_buttons = Gtk.Template.Child('stk_study_buttons')
    stk_pg_study_buttons = Gtk.Template.Child('stk_pg_study_buttons')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.card_num = self.carousel.get_n_pages()
        self.position = int(self.carousel.get_position())

        self.connect_signals()

        self.set_card_num(self.position, self.card_num)

        self.btn_show_answer.connect('clicked', self.on_btn_show_answer_clicked)

    def connect_signals(self):
        self.carousel.connect('page-changed', self.set_position)
        self.btn_next_flashcard.connect('clicked',
                                        self.on_btn_next_flashcard_clicked)

    def set_card_num(self, position, card_num):
        self.lbl_remaining_card_num.set_label(f'Card {position}/{card_num}')

    def set_position(self, widget, event):
        self.position = int(self.carousel.get_position())
        self.lbl_remaining_card_num.set_label(f'Card {self.position + 1}/{self.card_num}')
        if self.position == self.card_num -1:
            self.btn_next_flashcard.set_label("Close")
            self.btn_add_to_repeat.set_visible(False)

    def on_btn_next_flashcard_clicked(self, button):
        if self.position != self.card_num -1:
            next_page = self.carousel.get_nth_page(self.position + 1)
            self.carousel.scroll_to(next_page, animate=True)
            self.stk_study_buttons.set_visible_child(self.btn_show_answer)
        else:
            self.close()

    def on_btn_show_answer_clicked(self, button):
        current_page_widget = self.carousel.get_nth_page(self.position)
        self.stk_study_buttons.set_visible_child(self.stk_pg_study_buttons)
        current_page_widget.show_answer = True

@Gtk.Template(resource_path='/io/github/afacanc38/flashcards/ui/flashcard.xml')
class FlashcardsFlashcard(Gtk.Box):
    __gtype_name__ = 'FlashcardsFlashcard'

    rvl_answer = Gtk.Template.Child('rvl_answer')
    lbl_front = Gtk.Template.Child('lbl_front')

    _show_answer = False
    GObject.Property(type=bool, default=False)

    @property
    def show_answer(self):
        return self._show_answer

    @show_answer.setter
    def show_answer(self, value):
        self._show_answer = value

        if value:
            self.rvl_answer.set_reveal_child(True)
        else:
            self.rvl_answer.set_reveal_child(False)

class Application(Adw.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        GLib.set_application_name('Flashcards')
        GLib.set_prgname('Flashcards')

        act_show_about = Gio.SimpleAction(name='about')
        act_show_about.connect('activate', self.on_about)
        self.add_action(act_show_about)

        act_show_shortcuts = Gio.SimpleAction(name='shortcuts')
        act_show_shortcuts.connect('activate', self.on_show_shortcuts)
        self.add_action(act_show_shortcuts)

        act_study = Gio.SimpleAction(name='study')
        act_study.connect('activate', self.on_study)
        self.add_action(act_study)

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


if __name__ == '__main__':
    app = Application(application_id = 'io.io.github.afacanc38.flashcards')
    app.run()
