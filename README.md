
Scopo
======

Create card decks quickly.
Configuration is easy (for me): it's Python language, but you don't need to
understand it or to know how to program to be able to use it.

Especially, have a look, at `bang.py`, if you want to see how easy it is

Uso
====

After the configuration (see below), you'll find yourself with a bunch of
`.jpeg`s. They are optimized for easiness of print, so if you need to print the
same card 4 time, you'll have four identical JPEGs.

Configurazione
===============

You can defina a card. A card has lot of parameters (bgcolor, bordercolor) and
texts. Texts are special parameters, see below

You can "inherit" cards, and create new ones. This resembles how cards are
defined in games, and make it easy to create new ones

Finally, you define how many cards you should "print" for each one.

Testi
------

Texts are special attributes: they are like `text1`, `text2`...
for each one you can have `text1_size` or `text2_bgcolor`. They define
attributes for texts

Attributi
---------

You can mix class attributes and instance ones.
There's no need to define a constructor, if you don't feel so.

Example (bang)!
-------

	class Carta(BaseCard):
		text1_font="Arial 32"
		max_width="30" #30mm
		max_heigth="40" #40mm

	class Blu(Carta):
		bordercolor='blue'

	class Arma(Blu):
		text2="E' un arma. Puoi avere una sola arma per volta"

	class ArmaSemplice(Arma):
		def __init__(self, nome, punteggio):
			self.text1=nome
			self.text3="Spara a distanza %d" % punteggio

	barile=Blu()
	barile.text1="barile"
	barile.text2="Se ti sparano peschi dal tallone. Se è cuori, mancato!"

	carte=[]
	carte.append(ArmaSemplice('schofield', 2) * 4)
	carte.append(barile*3) #ritorna una lista di 3 barili!
	create_images(carte)

così stampa 4 schofield e 3 barili, tutti in immagini separate


# vim: set ft=markdown:
