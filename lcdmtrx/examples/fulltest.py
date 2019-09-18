"""
TEST COMPLET de la classe Python LcdMatrix servant à gérer le
backpack Adafruit USB+Série LCD disponible chez MCHobby.be

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby

Basé sur les travaux de Limor Freid qui se trouve ici:
https://github.com/adafruit/Adafruit-USB-Serial-RGB-Character-Backpack

BSD license - identique à celle d'AdaFruit
------------------------------------------------------------------------
History:
  18 sept 2019 - portage to MicroPython
"""

from pyb import UART
from lcdmtrx import *
import time

uart = UART(3, 9600) # RX = Y10, TX = Y9

LCD_COLS = 16 # Taille du LCD 16 caractères x 2 lignes
LCD_ROWS = 2

lcd = LcdMatrix( uart )

# Initialiser la taille du LCD (et sauver dans l'EEPROM)
lcd.set_lcd_size( LCD_COLS, LCD_ROWS )
lcd.clear_screen()

# Activer/désactiver le rétro-éclairage
lcd.activate_lcd( True )
time.sleep( 1 )
lcd.activate_lcd( False )
time.sleep( 1 );
lcd.activate_lcd( True )

# Modifier le contrast
for i in range( 150, 256, 5 ):
	lcd.home()
	lcd.contrast( i )
	lcd.write( "Contrast %i" % (i) )
	time.sleep( 0.3 )
time.sleep(1)

# Constrat par défaut
lcd.contrast()

# Créer un custom char (avec donnée brute)
lcd.create_custom_char( 0, [0x00, 0xA, 0x15, 0x11, 0x11, 0xA, 0x4, 0x00] )
lcd.clear_screen()
for i in range( 1, 10 ):
	lcd.write( chr(0) )

# Créer un custom char (avec une fonction d'aide à la composition)
lcd.create_custom_char( 1, compose_custom_char( [ '01110',
												  '01010',
												  '11111',
												  '00000',
												  '01010',
												  '00000',
												  '10001',
												  '01110' ] ) )
lcd.write( '\r'+chr(1)+'  '+chr(1) )

# Luminosité max + couleur RGB
lcd.brightness( 255 )
for r in range(0, 256, 5): # de 0 à 256 par pas de 5
	lcd.color( r, 0, 0 )
for g in range(0, 256, 5):
	lcd.color( 255-g, g, 0 )
for b in range(0, 256, 5):
	lcd.color( 0, 255-b, b )
for r in range(0, 256, 5):
	lcd.color( r, 0, 255-r )
for r in range(255, 0, 5):
	lcd.color( r, 0, 0)

# Repasser en couleur blanche
lcd.color( 255, 255, 255 )

# tester la luminosité
for i in range( 0, 256, 5 ):
	lcd.brightness( i )
	time.sleep( 0.3 )

# Repasser en couleur blanche
lcd.color( 255, 255, 255 )

# Position d'origine
lcd.home()
lcd.write( "Home" )
time.sleep( 0.5 )

# Effacer l'écran
lcd.clear_screen()
lcd.write( "Clear" )
time.sleep( 0.5 )

# Creation des caractères de barre horizontale dans les positions
# 0 à 7 sauvé dans la "bank 1"
#
#  voir aussi la fonction compose_custom_char() pour créer la liste
#  de donnée plus facilement
bank = 1
lcd.save_custom_char_to_bank( bank, 0, [0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10])
lcd.save_custom_char_to_bank( bank, 1, [0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18])
lcd.save_custom_char_to_bank( bank, 2, [0x1C,0x1C,0x1C,0x1C,0x1C,0x1C,0x1C,0x1C])
lcd.save_custom_char_to_bank( bank, 3, [0x1E,0x1E,0x1E,0x1E,0x1E,0x1E,0x1E,0x1E])
lcd.save_custom_char_to_bank( bank, 4, [0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF])
lcd.save_custom_char_to_bank( bank, 5, [0x7,0x7,0x7,0x7,0x7,0x7,0x7,0x7])
lcd.save_custom_char_to_bank( bank, 6, [0x3,0x3,0x3,0x3,0x3,0x3,0x3,0x3])
lcd.save_custom_char_to_bank( bank, 7, [0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x1])
# Recharger la bank 1 en mémoire
lcd.load_custom_char_from_bank( bank )
# Afficher les barres horizontales (les 7 positions définies dans
# la bank chargée)
lcd.clear_screen()
lcd.write(chr(0))
lcd.write(chr(1))
lcd.write(chr(2))
lcd.write(chr(3))
lcd.write(chr(4))
lcd.write(chr(5))
lcd.write(chr(6))
lcd.write(chr(7))
time.sleep(1)

# Creation des caractères de barre verticales dans les positions
# 0 à 7 sauvé dans la "bank 2"
bank = 2
lcd.save_custom_char_to_bank( bank, 0, [0,0,0,0,0,0,0,0x1F])
lcd.save_custom_char_to_bank( bank, 1, [0,0,0,0,0,0,0x1F,0x1F])
lcd.save_custom_char_to_bank( bank, 2, [0,0,0,0,0,0x1F,0x1F,0x1F])
lcd.save_custom_char_to_bank( bank, 3, [0,0,0,0,0x1F,0x1F,0x1F,0x1F])
lcd.save_custom_char_to_bank( bank, 4, [0,0,0,0x1F,0x1F,0x1F,0x1F,0x1F])
lcd.save_custom_char_to_bank( bank, 5, [0,0,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])
lcd.save_custom_char_to_bank( bank, 6, [0,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])
lcd.save_custom_char_to_bank( bank, 7, [0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])
# Recharger la bank 2 en mémoire
lcd.load_custom_char_from_bank( bank )
	# Afficher les barres verticales (les 7 positions définies dans
# la bank chargée)
lcd.clear_screen()
lcd.write(chr(0))
lcd.write(chr(1))
lcd.write(chr(2))
lcd.write(chr(3))
lcd.write(chr(4))
lcd.write(chr(5))
lcd.write(chr(6))
lcd.write(chr(7))
time.sleep(1)


# Creation des caractères "Bords Epais" dans les positions
# 0 à 7 sauvé dans la "bank 3"
bank = 3
lcd.save_custom_char_to_bank( bank, 0, [0x1f,0x1f,0x03,0x03,0x03,0x03,0x03,0x03])
lcd.save_custom_char_to_bank( bank, 1, [0x1f,0x1f,0x18,0x18,0x18,0x18,0x18,0x18])
lcd.save_custom_char_to_bank( bank, 2, [0x03,0x03,0x03,0x03,0x03,0x03,0x1F,0x1F])
lcd.save_custom_char_to_bank( bank, 3, [0x18,0x18,0x18,0x18,0x18,0x18,0x1F,0x1F])
lcd.save_custom_char_to_bank( bank, 4, [0x00,0x00,0x00,0x00,0x00,0x00,0x1F,0x1F])
lcd.save_custom_char_to_bank( bank, 5, [0x1F,0x1F,0x00,0x00,0x00,0x00,0x00,0x00])
lcd.save_custom_char_to_bank( bank, 6, [0x1F,0x1F,0x03,0x03,0x03,0x03,0x1F,0x1F])
lcd.save_custom_char_to_bank( bank, 7, [0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])
# Recharger la bank 3 en mémoire
lcd.load_custom_char_from_bank( bank )
	# Afficher les barres verticales (les 7 positions définies dans
# la bank chargée)
lcd.clear_screen()
lcd.write(chr(0))
lcd.write(chr(1))
lcd.write(chr(2))
lcd.write(chr(3))
lcd.write(chr(4))
lcd.write(chr(5))
lcd.write(chr(6))
lcd.write(chr(7))
time.sleep(1)

# Note MCHobby: Alpha version - code instable
# Ecriture de "medium num #0"
#lcd.clear_screen()
#lcd.place_medium_digit( 0, 0, 0)
#lcd.place_medium_digit( 2, 0, 1)
#lcd.place_medium_digit( 4, 0, 2)
#lcd.place_medium_digit( 6, 0, 3)


# Tester le défilement automatique

lcd.autoscroll( True)
lcd.clear_screen()
lcd.write( "AutoScroll=on" )
time.sleep( 1 )
lcd.clear_screen()
if (LCD_ROWS == 4):
	lcd.write("Voici une longue longue ligne de texte  ");
	time.sleep(1)
	lcd.write("Ajoutons du texte.. ");
	time.sleep(1)
	lcd.write("Et encore plus....!");
	time.sleep(1)
	lcd.write(" Et ca scroll! :-)");
if (LCD_ROWS == 2):
	lcd.write("Voici du texte..");
	time.sleep(1)
	lcd.write("Un peu plus....");
	time.sleep(1)
	lcd.write(" Et ca scroll:-)");
time.sleep(1)


# Tester sans défilement automatique
lcd.autoscroll( False )
lcd.clear_screen()
lcd.write( "AutoScroll=off" )
time.sleep( 1 )

lcd.clear_screen()
lcd.write( "Voici un long.... texte en haut a gauche :-/    " )
time.sleep( 1 )

# Ecriture de caractères directement
lcd.clear_screen()
for i in range( 0, 10 ):
	lcd.write( chr(64+i) )
lcd.write( chr(13)+chr(75) ) # Chr(13) = \r (retour à la ligne)
time.sleep( 1 )

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

# Affichage du curseur souligné (ne clignote pas)
lcd.cursor_underline( True )
time.sleep( 3 )
lcd.cursor_underline( False )
time.sleep( 1 )

# Affichage du curseur en BLOCK (clignote)
lcd.cursor_block( True )
time.sleep( 3 )
lcd.cursor_block( False )
time.sleep( 1 )

# Déplace le curseur (à gauche... en arrière)
lcd.cursor_block( True )
lcd.cursor_back()
lcd.cursor_back()
time.sleep( 3 )
lcd.cursor_forward()
time.sleep( 3 )
lcd.cursor_block( False )

# Splashscreen change
if (LCD_ROWS == 4):
	lcd.set_splashscreen( 'Hello World!        '+
	                      'Testing 20x4 LCD    '+
	                      'USB+Serial avec     '+
	                      'Retroeclairage RGB  ' )
if (LCD_ROWS == 2):
	lcd.set_splashscreen( 'Hello World!    Testing 16x2 LCD' )

lcd.autoscroll( True )
lcd.clear_screen()
lcd.write( 'Splash modifie,' )
time.sleep( 1 )
lcd.write( '\rfaire un on/off' )
time.sleep( 1 )
lcd.write( '\rpour voir le' )
time.sleep( 1 )
lcd.write( '\rnouvel accueil' )
time.sleep( 2 )

# ---- General Purpose Output ----
lcd.clear_screen()
lcd.write( 'GPO test...' )
# Activer les GPIO externes
lcd.gpio_output( GPO_PB0, True )
time.sleep( 0.5 )
lcd.gpio_output( GPO_PC2, True )
time.sleep( 0.5 )
lcd.gpio_output( GPO_PC4, True )
time.sleep( 0.5 )
lcd.gpio_output( GPO_PC7, True )
time.sleep( 2 )
# Désactiver les GPIO externes
lcd.gpio_output( GPO_PB0, False )
time.sleep( 0.5 )
lcd.gpio_output( GPO_PC2, False)
time.sleep( 0.5 )
lcd.gpio_output( GPO_PC4, False )
time.sleep( 0.5 )
lcd.gpio_output( GPO_PC7, False )

# --- Serial Link BaudRate ---
# Configurer le débit de la liaison série TTL.
# A reconfigurer via USB (parce que c'est plus facile)
lcd.clear_screen()
lcd.write( 'Force 9600 Bauds' )
lcd.serial_baudrate( SERIAL_BAUDRATE_9600 )
time.sleep( 2 )

lcd.clear_screen()
lcd.write( 'C\'est fini' )
