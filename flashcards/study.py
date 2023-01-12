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

    def connect_signals(self):
        self.carousel.connect('page-changed', self.set_position)
        self.btn_next_flashcard.connect('clicked',
                                        self.on_btn_next_flashcard_clicked)
        self.btn_add_to_repeat.connect('clicked',
                                        self.on_btn_add_to_repeat_clicked)
        self.btn_show_answer.connect('clicked', self.on_btn_show_answer_clicked)

    def switch_to_next_page(self):
        if self.position != self.card_num -1:
            next_page = self.carousel.get_nth_page(self.position + 1)
            self.carousel.scroll_to(next_page, animate=True)
            self.stk_study_buttons.set_visible_child(self.btn_show_answer)
        else:
            self.close()

    def set_card_num(self, position, card_num):
        self.lbl_remaining_card_num.set_label(f'Card {self.position + 1}/{card_num}')

    def set_position(self, widget, event):
        self.position = int(self.carousel.get_position())
        self.lbl_remaining_card_num.set_label(f'Card {self.position + 1}/{self.card_num}')
        if self.position == self.card_num -1:
            self.btn_next_flashcard.set_label("Close")

    def on_btn_next_flashcard_clicked(self, button):
        self.switch_to_next_page()

    def on_btn_show_answer_clicked(self, button):
        current_page_widget = self.carousel.get_nth_page(self.position)
        self.stk_study_buttons.set_visible_child(self.stk_pg_study_buttons)
        current_page_widget.show_answer = True

    def on_btn_add_to_repeat_clicked(self, button):
        self.switch_to_next_page()