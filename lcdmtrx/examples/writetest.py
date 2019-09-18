#!/usr/bin/python
#-*- coding: utf8 -*-
"""
TEST RESTREIND - AFFICHAGE DE TEXTE de la classe Python LcdMatrix
servant à gérer le backpack Adafruit USB+Série LCD disponible
chez MCHobby.be

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby

Basé sur les travaux de Limor Freid qui se trouve ici:
https://github.com/adafruit/Adafruit-USB-Serial-RGB-Character-Backpack

BSD license - identique à celle d'AdaFruit
------------------------------------------------------------------------
History:
  18 sept 2019 - Dominique - Version 0.1
"""

from pyb import UART
from lcdmtrx import LcdMatrix
import time

uart = UART(3, 9600) # RX = Y10, TX = Y9

LCD_COLS = 16 # Taille du LCD 16 caractères x 2 lignes
LCD_ROWS = 2


lcd = LcdMatrix( uart )

# Initialiser la taille du LCD (et sauver dans l'EEPROM)
lcd.set_lcd_size( LCD_COLS, LCD_ROWS )
lcd.clear_screen()


# Activer/désactiver le rétro-éclairage
lcd.activate_lcd( True );

# Constrat par défaut
lcd.contrast()
lcd.contrast(250)

# Luminosité max + couleur RGB
lcd.brightness( 255 )

# Couleur RBG
#lcd.color( 255, 17, 30 )
lcd.color( 0, 255, 0 )

# Position d'origine
lcd.clear_screen()

# Auto Scroll
lcd.clear_screen()
lcd.autoscroll( True )
if (LCD_ROWS == 4):
	lcd.write("Voici une longue longue ligne de texte  ")
	time.sleep(1)
	lcd.write("Ajoutons du texte.. ")
	time.sleep(1)
	lcd.write("Et encore plus....!")
	time.sleep(1)
	lcd.write(" Et ca scroll! :-)")
if (LCD_ROWS == 2):
	lcd.write("Voici du texte..")
	time.sleep(1)
	lcd.write("Un peu plus....")
	time.sleep(1)
	lcd.write(" Et ca scroll:-)")
time.sleep(1)

# Tester avec le retour à la ligne
# \r fait un retour à ligne et est insensible à la valeur de autoscroll.
lcd.autoscroll( False )
lcd.clear_screen()
lcd.write( "Ligne 1\rLigne 2" )
time.sleep(1)

# Si on ecrit une longue ligne de texte, seul les "x" derniers
# caractères seront affichés sur la ligne du LCD... SANS SAT DE
# LIGNE. Les "y" premiers caractères sont simplement ignorés!
lcd.autoscroll( True )
if (LCD_ROWS == 4):
	lcd.write("Voici une longue longue ligne de texte  ")
else:
	lcd.write("Voici une longue ligne...")
time.sleep(1)

# Déplacement du curseur
lcd.clear_screen()
lcd.autoscroll( False )
lcd.position( 1, 1 )
lcd.write( 'a' )
lcd.position( 1, LCD_COLS )
lcd.write( 'b' )
lcd.position( LCD_ROWS, 1 )
lcd.write( 'c' )
lcd.position( LCD_ROWS, LCD_COLS )
lcd.write( 'd' )

lcd.writepos( 1, 7, ':-)' ) # Déplacement de curseur + affichage
