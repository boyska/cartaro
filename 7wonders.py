#!/usr/bin/env python2
"""
https://no-me.space/2029-semantic-guerriglia/
"""
import logging
import sys
import re
from collections import defaultdict

from PIL import ImageFont

from cartaro import BaseCard, create_pdf, create_images

try:
    from jinja2 import Template
except:
    logging.warning("Cannot load jinja; html rendering not available")
else:
    card_template = Template(open('7wonders.html').read())
logging.basicConfig(level=logging.DEBUG)

class Carta(BaseCard):
    text1_size = 110
    text1_margin_up = 12
    text1_margin_down = 0
    fontsize = 40
    # bordercolor = "black"
    max_width = 65  # mm
    max_heigth = 95

    def __init__(self, titolo):
        self.text2 = titolo

tipo_colore = {
        "militare": "red",
        "commerciale": "yellow",
        "civile": "blue",
        "risorsa": "brown",
        "manufatti": "gray",
        "scienza": "green",
        "gilda": "purple"
        }

COSTO = re.compile(r'^([0-9])([$A-z]*)$')
SYMBOL_MAP = {'L': '🌲', 'M': '⚔️'
        }
class CartaFase(Carta):
    fase: int = 0
    effetto: str = ""

    abilita: list = []
    gratiscon: list = []

    costo: list = []
    tipo: str = ""
    giocatori: int = 0

    @property
    def bordercolor(self):
        return tipo_colore[self.tipo]

    @property
    def text1(self):
        # TODO: metti icone giuste (unicode?)
        if self.effetto:
            return str(self.effetto)
        return ""

    def get_font_rich(self, num, rich):
        if num == 2:
            return ImageFont.truetype("dejavu/DejaVuSerif-Bold.ttf", 90)

        if num in (3,4, 5):
            return ImageFont.truetype("dejavu/DejaVuSans.ttf", 50)

        return super().get_font_rich(num, rich)

    @property
    def text3(self):
        if self.costo:
            return "Costo: " + ",".join(self.costo)
        return ""


    @property
    def text4(self):
        if self.abilita:
            return "Permette: " + ",".join(self.abilita)
        return ""

    @property
    def text5(self):
        if self.gratiscon:
            return "Gratis con: " + ",".join(self.gratiscon)
        return ""


    def __init__(self, fase, titolo, **kwargs):
        super().__init__(titolo)
        self.fase = fase
        for attr in kwargs:
            if not hasattr(self, attr):
                raise ValueError("invalid attribute `%s`" % attr)
            setattr(self, attr, kwargs[attr])
        if type(self.costo) is str:
            self.costo = [self.costo]
        self.costo = self.summarize_costo(self.costo)

    def summarize_costo_single(self, item):
        m = COSTO.match(item)
        if not m:
            return 1, item
        symbol = m.group(2)[0].upper()
        # symbol = SYMBOL_MAP.get(symbol, symbol)
        return int(m.group(1)), symbol

    def summarize_costo(self, l):
        result = []
        for item in sorted(l, reverse=True):
            howmany, symbol = self.summarize_costo_single(item)
            for _ in range(howmany):
                result.append(symbol)
        return result


    def render_html(self):
        return card_template.render(self.__dict__)

import json

carte = []

carteraw = json.load(open('7wonders.json'))
logging.debug("json loaded")
for fase in carteraw['fase']:
    for carta in carteraw['fase'][fase]:
        if not carta:
            continue
        howmany = int(carta.pop('#', 1))
        giocatori = carta.pop('giocatori', [])
        if not giocatori:
            # FIXME: this should be an error
            logging.error("Giocatori missing for %s (%s)", carta["titolo"], fase)
            continue
        if len(giocatori) != howmany:
            raise Exception("Giocatori missing for %s (%s)" % (carta["titolo"], fase))
        for i in range(howmany):
            obj = CartaFase(fase=int(fase), giocatori=giocatori[i], **carta)
            carte.append(obj)
    print('alla fine della fase', fase, 'siamo a', len(carte))
logging.debug("generated")

def check_numgioc(carte):
    for numgioc in range(3,8):
        contacarte = defaultdict(int)
        for c in carte:
            if numgioc >= c.giocatori:
                contacarte[c.fase] += 1
        print('Per %d giocatori: %d, %d, %d' % (numgioc, contacarte[1], contacarte[2], contacarte[3]))
        for fase in (1,2):
            if contacarte[fase] % numgioc != 0:
                print("  Forse errore in fase %d" % fase)
        if contacarte[3] % numgioc == 0:
            print("  Forse errore in fase 3")

def check_abilita(carte):
    cartefase = {}
    for fase in (1,2,3):
        cartefase[fase] = {c.text2: c for c in carte if c.fase == fase}
    for fase in (1,2):
        for nome, c in cartefase[fase].items():
            for altra in c.abilita:
                if altra not in cartefase[fase+1]:
                    print("Errore: %s abilita -/-> %s" % (nome, altra))
                elif nome not in cartefase[fase+1][altra].gratiscon:
                    print("Errore: %s abilita -> %s ma non ricambiato" % (nome, altra))
    for fase in (2,3):
        for nome, c in cartefase[fase].items():
            for altra in c.gratiscon:
                if altra not in cartefase[fase-1]:
                    print("Errore: %s gratis -/-> %s" % (nome, altra))
                elif nome not in cartefase[fase-1][altra].abilita:
                    print("Errore: %s gratis -> %s ma non ricambiato" % (nome, altra))


check_numgioc(carte)
check_abilita(carte)

with open(sys.argv[1], 'w') as buf:
    buf.write('''
<!doctype html>
<html>
    <head>
    <meta charset="utf-8" />
        <title>Cards</title>
        <link href="7wonders.css" rel="stylesheet" />
    </head>
    <body>
        <div class="container">
        ''')
    for carta in carte:
        buf.write(carta.render_html())
    buf.write('</div></body')

#create_images(carte, directory="7wonders/")
# create_pdf(carte)
