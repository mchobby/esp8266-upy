from lcdmtrx import LcdMatrix

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

# === Support Europeen =================================================
CHAR_EGRAVE = 0 # è
CHAR_EACUTE = 1 # é
CHAR_ECIRC  = 2 # ê
CHAR_CEDIL  = 3 # ç
CHAR_AGRAVE = 4 # à
CHAR_EURO   = 5 # €

class EuropeLcdMatrix( LcdMatrix ):
	""" Dérivé de LcdMatrix pour ajouter le support des caractères
	    Accentués Europeen é è ê ç à  dans une bank de caractère
	    personnalisés
	"""

	# Déclaration du dictionnaire permettant le réencodage des caractères
	# par write_european()
	_translation_dic = { ord(u'è'): CHAR_EGRAVE, ord(u'é'): CHAR_EACUTE, ord(u'ê'): CHAR_ECIRC,
						 ord(u'ç'): CHAR_CEDIL , ord(u'à'): CHAR_AGRAVE, ord(u'€'): CHAR_EURO }

	def __init__( self, lcd_serial ):
		""" Initialise l'objet et initialize la communication série +
			la bank 4 avec les caractères Europeen
		"""
		super().__init__( lcd_serial )

	def create_european_charset(self):
		""" Génère et stocke une série de caractère européen dans la
		    bank de travail en vue de son utilisation directe
		"""
		self.create_custom_char( CHAR_EGRAVE, self._compose_egrave_char() ) # Pos 0 = è
		self.create_custom_char( CHAR_EACUTE, self._compose_eacute_char() ) # Pos 1 = é
		self.create_custom_char( CHAR_ECIRC , self._compose_ecirc_char()  ) # Pos 2 = ê
		self.create_custom_char( CHAR_CEDIL , self._compose_cedil_char()  ) # Pos 3 = ç
		self.create_custom_char( CHAR_AGRAVE, self._compose_agrave_char() ) # Pos 4 = à
		self.create_custom_char( CHAR_EURO  , self._compose_euro_char()   ) # Pos 5 = €

	def save_european_charset_to_bank( self, bank ):
		""" Génère et stocke une série de caractère européen dans la
		    bank mémoire en vue de son chargement ultérieur

		    Args:
				bank (int): Bank dans laquelle il faut stocker les caractères
		"""
		self.save_custom_char_to_bank( bank, CHAR_EGRAVE, self._compose_egrave_char() ) # Pos 0 = è
		self.save_custom_char_to_bank( bank, CHAR_EACUTE, self._compose_eacute_char() ) # Pos 1 = é
		self.save_custom_char_to_bank( bank, CHAR_ECIRC , self._compose_ecirc_char()  ) # Pos 2 = ê
		self.save_custom_char_to_bank( bank, CHAR_CEDIL , self._compose_cedil_char()  ) # Pos 3 = ç
		self.save_custom_char_to_bank( bank, CHAR_AGRAVE, self._compose_agrave_char() ) # Pos 4 = à
		self.save_custom_char_to_bank( bank, CHAR_EURO  , self._compose_euro_char()   ) # Pos 5 = €

	def _compose_egrave_char(self):
		""" Génère les données pour le Custom Char Europeen è """
		return compose_custom_char( [ '01000',
									  '00100',
									  '00000',
	                                  '01110',
	                                  '10001',
	                                  '11111',
	                                  '10000',
	                                  '01110' ] )

	def _compose_eacute_char(self):
		""" Génère les données pour le Custom Char Europeen é """
		return compose_custom_char( [ '00100',
									  '01000',
									  '00000',
	                                  '01110',
	                                  '10001',
	                                  '11111',
	                                  '10000',
	                                  '01110' ] )

	def _compose_ecirc_char(self):
		""" Génère les données pour le Custom Char Europeen ê """
		return compose_custom_char( [ '00100',
									  '01010',
									  '00000',
	                                  '01110',
	                                  '10001',
	                                  '11111',
	                                  '10000',
	                                  '01110' ] )

	def _compose_cedil_char(self):
		""" Génère les données pour le Custom Char Europeen ç """
		return compose_custom_char( [ '00000',
									  '01110',
									  '10000',
	                                  '10000',
	                                  '01110',
	                                  '00100',
	                                  '00010',
	                                  '01100' ] )

	def _compose_agrave_char(self):
		""" Génère les données pour le Custom Char Europeen à """
		return compose_custom_char( [ '01000',
									  '00100',
									  '00000',
	                                  '01110',
	                                  '00001',
	                                  '01111',
	                                  '10001',
	                                  '01111' ] )

	def _compose_euro_char(self):
		""" Génère les données pour le Custom Char Europeen € """
		return compose_custom_char( [ '00000',
									  '00111',
									  '01000',
									  '11110',
	                                  '01000',
	                                  '11110',
	                                  '01000',
	                                  '00111' ] )

	def write_european( self, str ):
		""" Ecrit une chaîne de caractère sur le LCD en faisant la
			translation des caractères européen definit dans la bank 4.

			Args:
				str (string): chaine de caractère UNICODE à envoyer sur la ligne courante du LCD.
							  \r Force le passage à la ligne suivante.
							  \n ignoré

			Remarks:
				ATTENTION - LA BANK EUROPEAN CHARSET DOIT ÊTRE CHARGEE!
		"""
		translatedStr = ''
		#DEBUG: for key in self._translation_dic:
		#DEBUG: 	print( "**** %i = pos %i" % (key, self._translation_dic[key]) )
		for c in str:
			#DEBUG: print ( "--- %s %i ---" % (c, ord(c)) )
			if ord(c) in self._translation_dic:
				#DEBUG: print( '  translated with %i ' % ( self._translation_dic[ord(c)] ) )
				translatedStr += chr( self._translation_dic[ord(c)] )
			else:
				#DEBUG: print( '  ajout origine %s ' % (c) )
				translatedStr += c
		# Fix: http://stackoverflow.com/questions/22275079/pyserial-write-wont-take-my-string
		# self.write( translatedStr )
		self.write( translatedStr.encode() )

	def write_european_pos( self, row, col, str ):
		""" Déplace le curseur sur l'écran à position ligne, colonne.
		    puis affiche la chaine de caractère.
		    AUTOSCROLL doit être désactivé!

			Args:
				row (int): Ligne à laquelle il faut placer le curseur (1..N)
				col (int): Colonne à laquelle il faut placer le curseur (1..N)
				Args:
				str (string): chaine de caractère UNICODE à envoyer sur la ligne courante du LCD.
							  \r Force le passage à la ligne suivante.
							  \n ignoré

			Remarks:
				ATTENTION - LA BANK EUROPEAN CHARSET DOIT ÊTRE CHARGEE!
		"""
		self.position( row, col )
		self.write_european( str )
