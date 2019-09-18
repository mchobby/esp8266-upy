
"""
Classe Python pour gérer le backpack Adafruit USB+Série LCD disponible
chez MCHobby.be

Fiche produit:
---> http://shop.mchobby.be/product.php?id_product=475
Voir notre tutoriel:
---> http://wiki.mchobby.be/index.php?title=LCD-USB-TTL

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby

Basé sur les travaux de Limor Freid qui se trouve ici:
https://github.com/adafruit/Adafruit-USB-Serial-RGB-Character-Backpack

BSD license - identique à celle d'AdaFruit
------------------------------------------------------------------------
History:
  18 sept 2019 - Dominique - portage to MicroPython

========================================================================
=  Here under the original message bloc from AdaFruit                  =
=  The orignal code upon which this class has been written.            =
========================================================================
Test python sketch for Adafruit USB+Serial LCD backpack
---> http://www.adafruit.com/category/63_96

Adafruit invests time and resources providing this open source code,
please support Adafruit and open-source hardware by purchasing
products from Adafruit!

Written by Limor Fried/Ladyada  for Adafruit Industries.
BSD license, check license.txt for more information
All text above must be included in any redistribution
------------------------------------------------------------------------
"""
import time

CMD_START_COMMAND = 0xFE

# --- Commandes de base ---
CMD_DISPLAY_ON = 0x42 # active le rétro-éclairage.
CMD_DISPLAY_OFF             = 0x46 # Désactive le rétro-éclairage.
CMD_SET_BRIGHTNESS          = 0x99 # fixe la luminosité du du rétro-éclairage
CMD_SET_AND_SAVE_BRIGHTNESS = 0x98 # Identique à la commande ci-dessous
CMD_SET_CONTRAST            = 0x50 # configure le contraste de l'afficheur. En générale, une valeur entre 180 et 220 fonctionne correctement. Ce paramètre est sauvé dans l'EEPROM.
CMD_SET_AND_CONTRAST        = 0x91 # Identique à la commande ci-dessus.

CMD_AUTOSCROLL_ON        = 0x51 # Défilement automatique. Le défilement automatique est activé lorsqu'il y a plus de texte reçu que de place sur l'écran. Dans ce cas, le texte défile (scroll) automatiquement et, par conséquent, la deuxième ligne devient la première ligne, etc. Le nouveau texte est toujours affiché en bas de l'écran.
CMD_AUTOSCROLL_OFF       = 0x52 # Désactive de défilement automatique. Quand l'afficheur reçoit du texte et s'il n'y a plus de place à l'écran alors l'afficheur recommence en haut à gauche de l'écran pour poursuivre l'affichage.
CMD_CLEAR_SCREEN         = 0x58 # efface le contenu de l'écran LCD
CMD_CHANGE_SPLASH_SCREEN = 0x40 # Change le message au démarrage du LCD (le splash screen). Après l'envoi de cette commande, vous devez envoyer 32 caractères (pour un LCD 16x2) ou jusqu'a 80 caractères (pour un LCD 20x4). Si vous ne voulez pas de splash screen, écrivez une série d'espace

# --- Cuseur et Déplacement du curseur ---
CMD_SET_CURSOR_POS       = 0x47 # Déplace la position du curseur. Le numéro de colonne (column) et ligne (row) commencent à 1. La première position en haut à gauche est 1, 1
CMD_GO_HOME              = 0x48 # Retourné à l'emplacement d'origine. La position (1, 1)
CMD_CURSOR_BACK          = 0x4C # Déplace le curseur d'un caractère en arrière. Si la position est déjà (1,1) le curseur est déplacé à la dernière position de l'écran.
CMD_CURSOR_FORWARD       = 0x4D # Déplace le curseur d'un caractère en avant. Si le curseur est à la dernière position, il est déplacé l'emplacement d'origine (1,1).
CMD_CURSOR_UNDERLINE_ON  = 0x4A # Affiche le curseur souligné (dit underline)
CMD_CURSOR_UNDERLINE_OFF = 0x4B # Désactive le curseur souligné.
CMD_CURSOR_BLOCK_ON      = 0x53 # Active le curseur "bloc clignotant".
CMD_CURSOR_BLOCK_OFF     = 0x54 # Désactive le curseur "bloc clignotant".

# --- Retro-éclairage RGB & Taille écran ---
CMD_SET_RGB_BACKLIGHT_COLOR = 0xD0 # initialise les composantes rouge (red), vert (green) et bleu (blue) du rétro-éclairage. Les valeurs des couleurs doivent évoluer entre 0 et 255 (un octet/byte). La couleur est sauvée dans l'EEPROM. Chacune des couleurs R, G et B est représenté dans un byte/octet juste après la commande. Pour fiixer le rétro-éclairage à rouge, il faut envoyer la commande 0xFE 0xD0 0xFF 0x0 0x0. En bleu c'est 0xFE 0xD0 0x0 0x0 0xFF. En blanc c'est 0xFE 0xD0 0xFF 0xFF 0xFF.
CMD_SET_LCD_SIZE            = 0xD1 # Cette commande permet d'indiquer au backpack la taille de l'écran qui lui est attaché. Cette valeur est sauvé dans l'EEPROM et par conséquent, cette opération ne doit être réalisé qu'une seule fois.

# --- Caractère personalisés ---
CMD_CREATE_CUSTOM_CHAR         = 0x4E # Crée un caractère personnalisé dans un emplacement de stockage donné (une position). Cette position doit être entre 0 et 7 (8 il y a 8 emplacements mémoire pour stocker des caractères personnalisés). 8 octets.bytes sont envoyés pour indiquer au backpack comment il doit être affiché.
CMD_SAVE_CUSTOM_CHAR_TO_BANK   = 0xC1 # Sauver le caractère personnalisé dans une bank de l'EEPROM pour pouvoir les réutiliser plus tard. Il y a 4 bank' de stockage et 8 positions par bank.
CMD_LOAD_CUSTOM_CHAR_FROM_BANK = 0xC0

# --- Autre ---
CMD_PLACE_MEDIUM_DIGIT         = 0x6F # Medium Digit Placement
CMD_SET_GPO_ON				   = 0x57 # Turn On the General Purpose Output (5 Volts logic)
CMD_SET_GPO_OFF				   = 0x57 # Turn Off the General Purpose Output (5 Volts logic)
CMD_SET_BAUDRATE			   = 0x39 # Change the baud rate of serial interface

# --- Nom et Numéro ddes GPO ---
GPO_1 = 1
GPO_2 = 2
GPO_3 = 3
GPO_4 = 4

GPO_PB0 = GPO_1
GPO_PC2 = GPO_2
GPO_PC4 = GPO_3
GPO_PC7 = GPO_4

# --- Baud Rates ---
SERIAL_BAUDRATE_2400 = 0x29
SERIAL_BAUDRATE_4800 = 0xCF
SERIAL_BAUDRATE_9600 = 0x67
SERIAL_BAUDRATE_19200 = 0x33
SERIAL_BAUDRATE_28800 = 0x22
SERIAL_BAUDRATE_38400 = 0x19
SERIAL_BAUDRATE_57600 = 0x10


class LcdMatrix( object ):
	""" MicroPython class to manage the Adafruit USB/Serial LCD backpack """

	__serial = None # Serial object to send data to LCD

	def __init__( self, lcd_serial ):
		self.__serial = lcd_serial

	def __write_command(self, commandlist):
		""" Envoi une commande + paramètres vers le LCD

			Args:
				commandlist (list): liste contenant la commande et les paramètres (octets/bytes) qui seront envoyés au LCD
		"""
		commandlist.insert(0, CMD_START_COMMAND )

		for i in range(0, len(commandlist)):
			self.__serial.writechar(commandlist[i])
		time.sleep( 0.05 ) # toujours attendre un peu après une commande

	def __isValidByte( self, i ):
		""" Verifie que l'entier contient une valeur valide pouvant servir de byte """
		return isinstance( i, int ) and (0<= i <=255)

	def write( self, str ):
		""" Ecrire une chaine de caractère sur le LCD.

			Args:
				str (string): chaine de caractère à envoyer sur la ligne courante du LCD.
							  \r Force le passage à la ligne suivante.
							  \n ignoré

			Remarks:
				Plusieurs appels à write() avec autoscroll = True insère
				des saut de lignes entre les appels :-)
		"""
		self.__serial.write( str )


	def writepos( self, row, col, str ):
		""" Déplace le curseur sur l'écran à position ligne, colonne.
		    puis affiche la chaine de caractère.
		    AUTOSCROLL doit être désactivé!

			Args:
				row (int): Ligne à laquelle il faut placer le curseur (1..N)
				col (int): Colonne à laquelle il faut placer le curseur (1..N)
				str (string): La chaine de caractere à afficher
		"""
		self.position( row, col )
		self.write( str )

	def clear_screen(self):
		""" Efface l'écran """
		self.__write_command( [CMD_CLEAR_SCREEN] )

	def set_lcd_size( self, cols, rows ):
		""" Définir la taille de l'écran et sauver paramètre dans l'EEPROM

			Args:
				cols (byte) : Nombre de colonnes
				rows (byte) : Nombre de lignes
		"""
		self.__write_command( [CMD_SET_LCD_SIZE, cols, rows] )

	def activate_lcd( self, activated ):
		""" Active ou désactive le retro-éclairage du LCD (turn on/turn off)

			Args:
				activated (boolean): True pour activer le rétro-éclairage.
		"""
		if activated:
			# AdaFruit backpack does not handle automatic off after a delay.
			# So, just send 0 minutes to fulfil MatrixOrbital specs.... but
			# that time will be ignored by the backpack.
			self.__write_command( [CMD_DISPLAY_ON, 0] )
		else:
			self.__write_command( [CMD_DISPLAY_OFF] )

	def contrast( self, contrast = 200 ):
		""" Definir le contrast de l'écran et le sauver dans l'EEPROM

			Args:
				constrast (byte): la valeur du contrast entre 0 et 255. Les valeurs optimales sont sitées entre 180 et 220.
		"""
		if not( self.__isValidByte( contrast ) ):
			raise EValueError( 'Invalid value for contrast' )
		self.__write_command( [CMD_SET_CONTRAST, contrast] )

	def brightness( self, brightness = 255 ):
		""" Définir la luminosité de l'écran et la sauver dans l'EEPROM

			Args:
				brightness (byte): la valeur du contrast entre 0 et 255.
		"""
		if not( self.__isValidByte( brightness ) ):
			raise EValueError( 'invalid value for brightness' )
		self.__write_command( [CMD_SET_BRIGHTNESS, brightness] )

	def home( self ):
		""" Place le curseur dans le coin en haut à gauche du LCD """
		self.__write_command( [CMD_GO_HOME] )

	def create_custom_char( self, position, hexdatalist ):
		""" crée un caractère personnalisé stocké à position

			Args:
				position (byte): position du caractère de 1 à 7
				hexdatalist (list): liste de 8 valeurs hexa, chacune de 0x00 à 0xFF.
								 Une valeur par ligne dans le caractère en commencant
								 par le haut.
		"""
		if not( 0<= position <= 7):
			raise ValueError( 'Invalid value for position' )
		if not( isinstance( hexdatalist, list ) ):
			raise TypeError( 'hexdatalist must be a list!' )
		if len( hexdatalist ) != 8:
			raise ValueError( 'hexdatalist must have 8 entries' )
		for i in hexdatalist:
			if not( self.__isValidByte( i ) ):
				raise ValueError( 'The hexdatalist contains an invalid byte value!' )

		self.__write_command( [CMD_CREATE_CUSTOM_CHAR, position]+hexdatalist )

	def save_custom_char_to_bank( self, bank, position, hexdatalist ):
		""" crée un caractère personnalisé directement stocké à la "position"
		    dans une bank déterminée

			Args:
				bank (byte): Bank dans laquelle il faut stocker le
							 caractère personalisé
				position (byte): position du caractère de 1 à 7
				hexdatalist (list): liste de 8 valeurs hexa, chacune de 0x00 à 0xFF.
								 Une valeur par ligne dans le caractère en commencant
								 par le haut.
		"""
		if not( 1<= bank <= 4):
			raise ValueError( 'Invalid value for bank' )
		if not( 0<= position <= 7):
			raise ValueError( 'Invalid value for position' )
		if not( isinstance( hexdatalist, list ) ):
			raise TypeError( 'hexdatalist must be a list!' )
		if len( hexdatalist ) != 8:
			raise ValueError( 'hexdatalist must have 8 entries' )
		for i in hexdatalist:
			if not( self.__isValidByte( i ) ):
				raise ValueError( 'The hexdatalist contains an invalid byte value!' )

		self.__write_command( [CMD_SAVE_CUSTOM_CHAR_TO_BANK, bank, position]+hexdatalist )

	def load_custom_char_from_bank( self, bank ):
		""" Recharger une bank de caractère prédéfini dans la mémoire """
		if not( 1<= bank <= 4):
			raise ValueError( 'Invalid value for bank' )

		self.__write_command( [CMD_LOAD_CUSTOM_CHAR_FROM_BANK, bank] )

	def color( self, red, green, blue ):
		""" Définir la couleur du retro éclairage et le sauver dans l'EEPROM

			Args:
				red (int): quantité de rouge (de 0 à 255)
				green (int): quantité de vert (de 0 à 255)
				blue (int): quantité de bleu (de 0 à 255)
		"""
		if not( self.__isValidByte( red ) ):
			raise EValueError( 'Invalid value for the red color' )
		if not( self.__isValidByte( green ) ):
			raise EValueError( 'Invalid value for the green color' )
		if not( self.__isValidByte( blue ) ):
			raise EValueError( 'Invalid value for the blue color' )

		self.__write_command( [CMD_SET_RGB_BACKLIGHT_COLOR, red, green, blue] )

	def place_medium_digit(self, medium_digit, row, col):
		''' placer un "medium size" digit _medium_digit à une ligne position donnée

		    Note MCHobby: Alpha version - code instable!!!

			Args:
				medium_digit (int): le digit à afficher (ex: 1)
				row (int): la ligne à laquelle il faut afficher (1 ou 2)
				col (int): la colonne à laquelle il faut afficher (1 à 16)

			Note:
				Voici l'exemple fourni par AdaFruit.
					matrixwritecommand([0x6F, 0, 0, 0])
					matrixwritecommand([0x6F, 2, 0, 1])
					matrixwritecommand([0x6F, 4, 0, 2])
					matrixwritecommand([0x6F, 6, 0, 3])
				qui se traduit par le code
					lcd.place_medium_digit( 0, 0, 0)
					lcd.place_medium_digit( 2, 0, 1)
					lcd.place_medium_digit( 4, 0, 2)
					lcd.place_medium_digit( 6, 0, 3)
				Mais ni l'un, ni l'autre ne fournit quelque-chose
				de compréhensible sur le LCD Backpack!
		'''
		if not( self.__isValidByte( medium_digit ) ):
			raise EValueError( 'Invalid value for the medium_digit' )
		if not( self.__isValidByte( row ) ):
			raise EValueError( 'Invalid value for row' )
		if not( self.__isValidByte( col ) ):
			raise EValueError( 'Invalid value for col' )

		self.__write_command( [ CMD_PLACE_MEDIUM_DIGIT, medium_digit, row, col ] )

	def autoscroll( self, is_active ):
		""" Active ou désactive le défilement automatique (autoscroll)

			Args:
				is_activate (boolean): indique s'il faut activer l'auto-scrolling
		"""
		if not( isinstance( is_active, bool ) ):
			raise ETypeError( 'is_active must be boolean' )

		if( is_active ):
			self.__write_command( [CMD_AUTOSCROLL_ON] )
		else:
			self.__write_command( [CMD_AUTOSCROLL_OFF] )

	def position( self, row, col ):
		""" Déplace le curseur sur l'écran à position ligne, colonne.
			Ne fonctionne correctement que si AUTOSCROLL est désactivé!

			Args:
				row (int): Ligne à laquelle il faut placer le curseur (1..N)
				col (int): Colonne à laquelle il faut placer le curseur (1..N)
		"""
		self.__write_command( [CMD_SET_CURSOR_POS, col, row] )

	def cursor_underline( self, is_active ):
		""" Active ou désactive le curseur souligné

			Args:
				is_active (bool): active/désactive le curseur souligné
		"""
		if not( isinstance( is_active, bool ) ):
			raise ETypeError( 'is_active must be boolean' )

		if is_active:
			self.__write_command( [CMD_CURSOR_UNDERLINE_ON] )
		else:
			self.__write_command( [CMD_CURSOR_UNDERLINE_OFF] )

	def cursor_block( self, is_active ):
		""" Active ou désactive le curseur en BLOCK

			Args:
				is_active (bool): active/désactive le curseur en BLOCK
		"""
		if not( isinstance( is_active, bool ) ):
			raise ETypeError( 'is_active must be boolean' )

		if is_active:
			self.__write_command( [CMD_CURSOR_BLOCK_ON] )
		else:
			self.__write_command( [CMD_CURSOR_BLOCK_OFF] )

	def cursor_back( self ):
		""" Déplace le curseur en arrière (donc à gauche) """
		self.__write_command( [CMD_CURSOR_BACK] )

	def cursor_forward( self ):
		""" Déplace le curseur vers l'avant (donc à droite) """
		self.__write_command( [CMD_CURSOR_FORWARD] )

	def set_splashscreen( self, newSplash ):
		""" Enregistre un nouveau splashscreen / acceuil dans le LCD

			Args:
				Le nouveau message d'acceuil. Il doit soit avoir 16x2 ou
				20x4 caractères en fonction de l'afficheur utilisé!
		"""

		if ( len( newSplash )!=32 ) and ( len( newSplash )!=80 ):
			raise EValueError( 'newSplash must have 32 or 80 char len depending on the LCD!' )

		arrData = [CMD_CHANGE_SPLASH_SCREEN]
		for c in newSplash:
			arrData.append( ord(c) )

		self.__write_command( arrData )

	def gpio_output( self, gpioNr, is_active ):
		""" Activer/désactiver l'un des GPO (General Purpose Output).
			Le GPO est en logique 5 Volts.

			Args:
				gpioNr (int): Numéro de GPO de 1 à 4 où l'une des constantes
							  GPO_xx correspondant à la sérigraphie du backpack
				is_active (bool): Indique si la sortie est en niveau haut/bas
		"""

		if not( 1<=gpioNr<=4 ):
			raise EValueError( 'gpioNr must be between 1 and 4' )
		if not( isinstance( is_active, bool ) ):
			raise EValueError( 'is_active must be a boolean' )


		if is_active:
			self.__write_command( [CMD_SET_GPO_ON, gpioNr] )
		else:
			self.__write_command( [CMD_SET_GPO_OFF, gpioNr] )

	def serial_baudrate( self, bauds ):
		""" Fixer la vitesse de la liaison série TTL.

			Args:
				bauds (int): Une des constantes SERIAL_BAUDRATE_x definissant le
							 débit.

			Remarks:
				Etant donné que la connexion USB ignore la configuration du débit
				il est plus facile de reconfigurer le début de la liaison série
				via une connexion USB.
		"""
		self.__write_command( [CMD_SET_BAUDRATE, bauds] )


def compose_custom_char( bitStrList ):
	""" Transforme une liste de bit 1/0 décrivant le caractère en une
	    liste de valeur numérique pour la méthode LcdMatrix.create_custom_char()

		Args:
			bitStrList (list): Liste de 8 lignes.Chaque ligne ayant 5 caractères 1/0

		Remarks:
			Voir exemple dans la classe
	"""
	if not( isinstance( bitStrList, list ) ):
		raise ETypeError( 'bitStrList must be a list' )
	if len( bitStrList )!=8:
		raise EValueError( 'bitStrList must have 8 entries' )

	result = []

	for line in bitStrList:
		if len( line )!= 5:
			raise EValueError( 'bitStrList must have 5 chars strings. \'%s\' is invalid!' % (line) )
		lineResult = 0
		for i in range( 0, 5 ): # 0 à 4 (5 exclus)
			if line[i] == '1':
				lineResult += (2**(4-i))
		result.append( lineResult )
	return result
