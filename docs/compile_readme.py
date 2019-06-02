#!/usr/bin/python3
# coding: utf8

""" Compile the various readme files from the docs/_static/ templates to inject
    the driver list. """

from driverreader import *

def generate_table( entries, lang_code ):
	sFolderTitle = 'Répertoire' if lang_code=='fr' else 'Folder'
	sDescTitle   = 'Description' if lang_code=='fr' else 'Description'
	sCompTitle   = 'Composants' if lang_code=='fr' else 'Components'
	sIntfTitle   = 'Interfaces' if lang_code=='fr' else 'Interfaces'
	sPlateformTitle = 'Testé avec' if lang_code=='fr' else 'Tested with'
	sSeeTitle    = 'Voir' if lang_code=='fr' else 'See'
	_lst = [] # List of string
	_lst.append( '<table>' )
	_lst.append( '<thead>' )
	_lst.append( '  <th>%s</th><th>%s</th>' % (sFolderTitle, sDescTitle) )
	_lst.append( '</thead>' )
	_lst.append( '<tbody>'  )

	for label, driver in entries:
		_lst.append( '  <tr><td>%s</td>' % label )
		_lst.append( '      <td><strong>%s</strong> : %s<br />' % (sCompTitle, ', '.join(driver.components) ) )
		_lst.append( '      <strong>%s</strong> : %s<br />' % (sIntfTitle, ', '.join(driver.interfaces) ) )
		_lst.append( '      <strong>%s</strong> : %s<br />' % (sPlateformTitle, ', '.join(driver.plateforms) ) )
		_lst.append( '<small>%s</small>' % driver.descr.get_lang(lang_code))
		if len( driver.ressources )>0:
			_lst.append( '<br /><ul>' )
			for res in driver.ressources:
				_lst.append( '<li>%s <a href="%s">%s</a></li>' % (sSeeTitle,res.url, res.label) )
			_lst.append( '</ul>' )
		_lst.append( '      </td>' )
		_lst.append( '  </tr>' )
	_lst.append( '</tbody>' )
	_lst.append( '</table>' )
	_lst.append( '' ) # HTML table must be followed by an empty line into the Markdown file

	return "\n".join( _lst )

#-------------------------------------------------------------------------------
#         Function available to readme compiler
#-------------------------------------------------------------------------------
# Must generate a string as reply
#
def __driver_table( drivers, lang_code, filter ):
	return generate_table( drivers.list_by_folder(filter), lang_code )

def __interface_list( drivers, lang_code, str, filter ): # List per interface
	_interfaces = [ item.code for item in drivers.interfaces ]
	_interfaces = sorted( _interfaces )
	return ', '.join( [str.replace('%code%',code) for code in _interfaces]  )

def __interface_text( drivers, lang_code, code, filter ): # Identification of the interface codes
	return drivers.interface( code ).descr.get_lang( lang_code )

def __manufacturer_list( drivers, lang_code, str, filter ): # List per manufacturer
	_mans = [ item.code for item in drivers.manufacturers ]
	_mans = sorted( _mans )
	return ', '.join( [str.replace('%code%',code) for code in _mans]  )


#-------------------------------------------------------------------------------
#         Readme Compiler
#-------------------------------------------------------------------------------

def evaluate_and_write( line, destin_file, drivers, filter ):
	"""  evaluate a line containing @@ and call the function appropriate function + parameter

		 drivers is the list of drivers provided by the drivers.json

	 	 @@driver_table:{'lang_code':'fr'} # Insert the driver table  """
	# Strip the commentary if any
	if '#' in line:
		line = line[ line.index('@@')+2:line.index('#') ].strip()
	else:
		line = line[ line.index('@@')+2: ].strip()

	# Locate parameters
	if ':' in line:
		fname  = line[:line.index(':')].strip()
		# retreive the parameters as a real Python dictionnary
		params = eval( line[line.index(':')+1:].strip() )
	else:
		fname  = line
		params = {}
	params['drivers'] = drivers
	params['filter' ] = filter

	# Calling the function
	try:
		to_call = globals()['__'+fname]
		strings = to_call( **params )
	except:
		print( 'Exception when calling %s with params %s' % ('__'+fname,params) )
		raise

	# write the content to the file
	destin_file.write( strings )

def compile_file( drivers, **kwargs ): #source_file, destin_file, lang_code, filter ):
	""" Copy the content of the source_file to the destination file and substitue the content.
	    Drivers is the collection of drivers read from the drivers.json. """
	source_file = kwargs['source']
	destin_file = kwargs['destin']
	lang_code   = kwargs['lang_code']
	filter      = kwargs['filter'] if 'filter' in kwargs else None

	with open( source_file, 'r' ) as fsource:
		lines = fsource.readlines()
	with open( destin_file, 'w' ) as fdestin:
		for line in lines:
			for key,value in kwargs.items():
				line = line.replace( '%'+key+'%', '%s'%value)
			try:
				idx = line.index( '@@')
			except:
				idx = -1
			if idx==0: # we have to evaluate the line like --> @@driver_table:{'lang_code':'fr'} # Insert the driver table
				evaluate_and_write( line, fdestin, drivers, filter )
			else:
				fdestin.write( line )

def compile_all():
	""" Compile all the readme files """
	drivers = DriverReader()

	#for item in drivers.drivers:
	#	print( "%s : %s" % (item.folder, item.descr.fr)  )
	#for item in drivers.manufacturers:
	#	print( "%s : %s " % (item.code, item.name) )
	#for item in drivers.interfaces:
	#	print( "%s : %s" % (item.code, item.descr.fr) )
	#for item in drivers.plateforms:
	#	print( "%s : %s" %(item.code, item.descr.fr) )

	drivers.validate() # ensure that everything is properly encoded

	files = [
		{'source' : '_static/_readme.md', 'destin' : '../readme.md', 'lang_code': 'fr', 'filter': None},
		{'source' : '_static/_readme_ENG.md', 'destin' : '../readme_ENG.md', 'lang_code': 'fr', 'filter' : None },

 		{'source' : '_static/_drv_by_intf.md', 'destin' : 'drv_by_intf_GPIO.md', 'lang_code': 'fr', 'code' : 'GPIO', 'filter' : lambda driver : any(['GPIO'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf.md', 'destin' : 'drv_by_intf_I2C.md', 'lang_code': 'fr', 'code' : 'I2C', 'filter' : lambda driver : any(['I2C'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf.md', 'destin' : 'drv_by_intf_SPI.md', 'lang_code': 'fr', 'code' : 'SPI', 'filter' : lambda driver : any(['SPI'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf.md', 'destin' : 'drv_by_intf_ONEWIRE.md', 'lang_code': 'fr', 'code' : 'ONEWIRE', 'filter' : lambda driver : any(['ONEWIRE'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf.md', 'destin' : 'drv_by_intf_UART.md', 'lang_code': 'fr', 'code' : 'UART', 'filter' : lambda driver : any(['UART'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf.md', 'destin' : 'drv_by_intf_NCD.md', 'lang_code': 'fr', 'code' : 'NCD', 'filter' : lambda driver : any(['NCD'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf.md', 'destin' : 'drv_by_intf_UEXT.md', 'lang_code': 'fr', 'code' : 'UEXT', 'filter' : lambda driver : any(['UEXT'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf.md', 'destin' : 'drv_by_intf_QWIIC.md', 'lang_code': 'fr', 'code' : 'QWIIC', 'filter' : lambda driver : any(['QWIIC'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf.md', 'destin' : 'drv_by_intf_FEATHERWING.md', 'lang_code': 'fr', 'code' : 'FEATHERWING', 'filter' : lambda driver : any(['FEATHERWING'==intf for intf in driver.interfaces]) },

 		{'source' : '_static/_drv_by_intf_ENG.md', 'destin' : 'drv_by_intf_GPIO_ENG.md', 'lang_code': 'eng', 'code' : 'GPIO', 'filter' : lambda driver : any(['GPIO'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf_ENG.md', 'destin' : 'drv_by_intf_I2C_ENG.md', 'lang_code': 'eng', 'code' : 'I2C', 'filter' : lambda driver : any(['I2C'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf_ENG.md', 'destin' : 'drv_by_intf_SPI_ENG.md', 'lang_code': 'eng', 'code' : 'SPI', 'filter' : lambda driver : any(['SPI'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf_ENG.md', 'destin' : 'drv_by_intf_ONEWIRE_ENG.md', 'lang_code': 'eng', 'code' : 'ONEWIRE', 'filter' : lambda driver : any(['ONEWIRE'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf_ENG.md', 'destin' : 'drv_by_intf_UART_ENG.md', 'lang_code': 'eng', 'code' : 'UART', 'filter' : lambda driver : any(['UART'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf_ENG.md', 'destin' : 'drv_by_intf_NCD_ENG.md', 'lang_code': 'eng', 'code' : 'NCD', 'filter' : lambda driver : any(['NCD'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf_ENG.md', 'destin' : 'drv_by_intf_UEXT_ENG.md', 'lang_code': 'eng', 'code' : 'UEXT', 'filter' : lambda driver : any(['UEXT'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf_ENG.md', 'destin' : 'drv_by_intf_QWIIC_ENG.md', 'lang_code': 'eng', 'code' : 'QWIIC', 'filter' : lambda driver : any(['QWIIC'==intf for intf in driver.interfaces]) },
 		{'source' : '_static/_drv_by_intf_ENG.md', 'destin' : 'drv_by_intf_FEATHERWING_ENG.md', 'lang_code': 'eng', 'code' : 'FEATHERWING', 'filter' : lambda driver : any(['FEATHERWING'==intf for intf in driver.interfaces]) }

	]

	#for lang in ['fr','eng']:
	#	for interface_code in [ item.code for item in drivers.interfaces ]:
	#		# {'source' : '_static/_drv_by_intf.md', 'destin' : 'drv_by_intf_I2C.md', 'lang_code': 'fr', 'code' : 'I2C', 'filter' : lambda driver : any(['I2C'==intf for intf in driver.interfaces]) }
	#		files.append(
	#			{ 'source' : '_static/_drv_by_intf.md',
	#			  'destin' : 'drv_by_intf_%s.md' % interface_code ,
	#			  'lang_code': lang,
	#			  'code' : interface_code,
	#			  'filter' : lambda driver : any([interface_code==intf for intf in driver.interfaces])
	#			} )

	for entry in files:
		print( 'compile file: %s' % entry['source'] )
		compile_file( drivers, **entry ) # entry['source'], entry['destin'], entry['lang'], entry['filter'] )
		print( '    %s written!' % entry['destin'])

	# sHtml = generate_table( drivers.list_by_folder(), 'fr' )
	# print( sHtml )

if __name__ == '__main__':
	compile_all()
