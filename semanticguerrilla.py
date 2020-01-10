#!/usr/bin/env python2
'''
https://no-me.space/2029-semantic-guerriglia/
'''

from cartaro import BaseCard, create_images

class Carta(BaseCard):
    text1_size=70
    text1_margin_up = 7.5
    text1_margin_down = 0
    fontsize=40
    bordercolor='white'
    max_width=40 #mm
    max_heigth=20
    def __init__(self, parola, colore):
        self.text1 = parola
        self.bordercolor = colore
dizionario =  {
    'blue': [
        'firefox',
        'app',
    ],
    'red': [
        'saldatura',
        'ferro'
    ],
    'green': [
        'bucare',
        'injection',
        'scanner'
    ]
}

carte = []

for color, parole in dizionario.items():
    for parola in parole:
        carte.append(Carta(parola, color))

create_images(carte, directory='sg/')
