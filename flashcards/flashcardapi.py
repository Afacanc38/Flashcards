import yaml
import os
from os.path import abspath, dirname, join
from random import randint

APP_DIR = '/'.join(abspath(dirname(__file__)).split('/')[:-1])
USER_DATA_DIR = f'/home/{os.getenv("LOGNAME")}/.local/share/'

class Deck():
  def __init__(self, name):
    self.name = name
    self.cards = []

  def append_card(self, card):
    self.cards.append(card)

  def remove_card(self, card):
    self.cards.remove(card)

  def get_card_by_front_label(self, label):
    for i in range(len(self.cards)):
      if label == self.cards[i].info['front']:
        card = self.cards[i]
        return card
      else:
        raise NameError(f'The flashcard labeled by {label} not found in {self.name}')

  def get_card_by_back_label(self, label):
    for i in range(len(self.cards)):
      if label == self.cards[i].info['back']:
        card = self.cards[i]
        return card
  
  def get_card_number(self):
    return len(self.cards)

class Flashcard():
  def __init__(self, deck, front, back):
    self.info = {
      'deck_name': deck,
      'front': front,
      'back': back
    }

    self.info['deck_name'].append_card(self)

  def __str__(self):
      return str(self.info)