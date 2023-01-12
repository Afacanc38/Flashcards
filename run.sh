#!/bin/bash
cd /home/alperen/Projeler/Flashcards/data/
glib-compile-resources io.github.afacanc38.flashcards.gresource.xml
python3 ../flashcards/main.py
cd /home/alperen/Projeler/Flashcards