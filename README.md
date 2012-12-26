Sorry, this is italian only atm
The code, instead, is english, and it should speak by itself.
Especially, have a look, at `bang.py`, that is the only example I did

Scopo
======

Creare mazzi di carte in fretta.
Configurazione semplice.
Crea tante immagini singole.
Poi forse crea pure i pdf in cui cerca di metterne tante insieme

Uso
====

Si configurano le carte e i mazzi, quindi si richiede una stampa.
La modalità di stampa più semplice è generare tante png, una per immagine.
(quindi ci sono i duplicati).

Disegnare
==========

In tutti i casi l'allineamento degli oggetti sta a noi!

PIL
----

Con PIL lo strumento principale è ImageDraw.text
Centrare orizzontalmente si può con
http://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil

ImageMagick
------------

Interfaccia più oscura, ma, almeno a linea di comando, il supporto per il testo
è più esteso: ( http://www.imagemagick.org/Usage/text/ )

    convert -background lightblue -fill blue  -font Candice \
            -size 165x70  -pointsize 24  -gravity center \
            label:Anthony     label_gravity.gif


Configurazione
===============

Si definisce una carta. Ha vari parametri (bgcolor, bordercolor, borderstyle)
tra cui i testi.

Si possono ereditare carte, e crearne di nuove. In questo modo si può creare
una carta "base" e varie altre modifiche.

Si definisce poi quante stampare di ogni carta.

Testi
------

I testi sono speciali, perché sono attributi di tipo `text\d+` con relativi
`text\d+_font` In questo modo le funzioni di stampa ci possono iterare sopra e
trasformare tutto in "stringhe ricche" che hanno un font

Attributi
---------

Per semplicità si devono poter mischiare attributi di classe e d'istanza.
Non deve essere necessario definire un costruttore, se non si vogliono gestire
parametri.
Può essere utile una funzione `.set(**kwargs)` con cui settare tanti parametri
insieme.

Esempio (bang)!
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
