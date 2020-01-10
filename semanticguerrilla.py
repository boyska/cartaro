#!/usr/bin/env python2
"""
https://no-me.space/2029-semantic-guerriglia/
"""

from cartaro import BaseCard, create_pdf, create_images


class Carta(BaseCard):
    text1_size = 100
    text1_margin_up = 12
    text1_margin_down = 0
    fontsize = 40
    bordercolor = "white"
    max_width = 70  # mm
    max_heigth = 30

    def __init__(self, parola, colore):
        self.text1 = parola
        self.bordercolor = colore
        self.file_prefix = colore


dizionario = {
    "blue": ["firefox", "app", "smartphone", "startup"],
    "red": ["saldatura", "ferro", "bruciare", "squagliare"],
    "green": ["bucare", "injection", "scanner", "offuscamento", "log"],
    "yellow": ["stallman", "ada lovelace"],
}

carte = []

for color, parole in dizionario.items():
    for parola in parole:
        carte.append(Carta(parola, color))
        carte.append(Carta(parola, color))

create_images(carte, directory="sg/")
create_pdf(carte)
