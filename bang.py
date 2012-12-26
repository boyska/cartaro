'''An example implementation for the Bang! card game'''

from cartaro import *

class Carta(BaseCard):
    text1_size=75
    fontsize=40
    bordercolor='white'
    max_width=30 #30mm
    max_heigth=40 #40mm
                                                                       
class Blu(Carta):
    bordercolor='blue'
                                                                       
class Arma(Blu):
    text2="E' un arma. Puoi avere una sola arma per volta"
                                                                       
class ArmaSemplice(Arma):
    def __init__(self, nome, punteggio):
        self.text1=nome
        self.text3="Spara a distanza %d" % punteggio

RichText.default_margin_down = 3
RichText.default_margin_up = 0
RichText.default_interspacing = 0.2

mustang = Arma()
mustang.text1='Mustang'
mustang.text3 = "Tutti ti vedono a distanza aumentata di 1"
                                                                       
barile=Blu()
barile.text1="Barile"
barile.text2="Se ti sparano peschi dal tallone. Se e' cuori, mancato! \nAltrimenti, puoi comunque estrarre un mancato!\n\n"

birra = Carta()
birra.text1="Birra"
birra.text2="Guadagni una vita"
                                                                       
carte=[]
carte.extend(ArmaSemplice('schofield', 2)*2)
carte.append(barile) #ritorna una lista di 3 barili!
carte.append(birra)
carte.append(mustang)
create_images(carte, directory='images/')
class Carta(BaseCard):
    text1_size=75
    fontsize=40
    bordercolor='white'
    max_width=30 #30mm
    max_heigth=40 #40mm
                                                                       
class Blu(Carta):
    bordercolor='blue'
                                                                       
class Arma(Blu):
    text2="E' un arma. Puoi avere una sola arma per volta"
                                                                       
class ArmaSemplice(Arma):
    def __init__(self, nome, punteggio):
        self.text1=nome
        self.text3="Spara a distanza %d" % punteggio

mustang = Arma()
mustang.text1='Mustang'
mustang.text3 = "Tutti ti vedono a distanza aumentata di 1"
                                                                       
barile=Blu()
barile.text1="Barile"
barile.text2="Se ti sparano peschi dal tallone. Se e' cuori, mancato! \nAltrimenti, puoi comunque estrarre un mancato!\n\n"

birra = Carta()
birra.text1="Birra"
birra.text2="Guadagni una vita"
                                                                       
carte=[]
carte.extend(ArmaSemplice('schofield', 2)*2)
carte.append(barile) #ritorna una lista di 3 barili!
carte.append(birra)
carte.append(mustang)
create_images(carte, directory='images/')

