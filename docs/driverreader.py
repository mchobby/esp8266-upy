import json

class DriverRessource():
	""" Driver external ressource label->URL link """
	__slot__ = ['label', 'url']
	def __init__(self, res_dic ):
		self.label = res_dic['label']
		self.url   = res_dic['url']

class Description():
	""" Driver description in french and english """

	def __init__( self, descr_dic ):
		self.descr_dic = descr_dic

	@property
	def eng( self ):
		return self.descr_dic['ENG']

	@property
	def fr( self ):
		return self.descr_dic['FR']

	def get_lang( self, lang_code ):
		return self.descr_dic[ lang_code.upper() ]

class Driver():
	""" Facade object loaded with the driver folder data """
	def __init__( self, driver_json ):
		self.folder 	= driver_json['folder']
		self.components = driver_json['components']
		self.interfaces = driver_json['interfaces']
		self.manufacturers = driver_json['manufacturers']
		self.plateforms    = driver_json['plateforms']
		self.ressources    = []
		for res_dict in driver_json['ressources']:
			self.ressources.append( DriverRessource(res_dict) )
		self.descr        = Description( driver_json['descr'] )

class DriverList( list ):
	""" Just a result list composed of tuples (entry_label, driver_object ) """

	def append( self, label, driver_obj ):
		super().append( (label, driver_obj) )

class Manufacturer():
	""" Facade for Manufacturer data """
	__slot__ = ['code','name','url']

	def __init__( self, code, man_json ):
		self.code = code
		self.name = man_json['name']
		self.url  = man_json['url']

class Interface():
	""" Facade for the Interface data """
	__slot__ = ['code', 'descr']

	def __init__( self, code, intf_json ):
		self.code = code
		self.descr = Description( intf_json['descr'] )

class Plateform():
	""" Facade for the Plateform data """
	__slot__ = ['code','descr','url']
	def __init__( self, code, plt_json ):
		self.code = code
		self.descr = Description( plt_json['descr'] )
		self.url   = plt_json['url']

class DriverReader:
	""" class to read the drivers.json file """
	def __init__( self ):
		with open( 'drivers.json', "r") as f:
			self.data = json.load( f )
		self.folders = [ item['folder'] for item in self.data ]
		self.drivers = [ Driver(item) for item in self.data ]
		with open( 'manufacturers.json', "r") as f:
			data = json.load( f )
			self.manufacturers = [ Manufacturer(code=key, man_json=value ) for key,value in data.items() ]
		with open( 'interfaces.json', "r") as f:
			data = json.load( f )
			self.interfaces = [ Interface(code=key, intf_json=value ) for key,value in data.items() ]
		with open( 'plateforms.json', "r" ) as f:
			data = json.load( f )
			self.plateforms = [ Plateform(code=key, plt_json=value ) for key, value in data.items() ]

	def validate( self ):
		""" check that the driver data is fullfilling the manufacturer, interface and plateforms.

		Raise an assertion is case of problem """
		for driver in self.drivers:
			for manufacturer in driver.manufacturers:
				assert any( [manufacturer==man.code for man in self.manufacturers] ), "Invalid manufacturer '%s' for driver folder '%s'" % (manufacturer,driver.folder)
			for interface in driver.interfaces:
				assert any( [interface==intf.code for intf in self.interfaces] ), "Invalid interface '%s' for driver folder '%s'" % (interface,driver.folder)
			for plateform in driver.plateforms:
				assert any( [plateform==plt.code for plt in self.plateforms] ), "Invalid plateform '%s' for driver folder '%s'" % (plateform,driver.folder)

	def driver( self, folder ):
		""" return a Driver object for a given folder name """
		assert folder in self.folders
		for item in self.drivers:
			if item.folder == folder:
				return item
		return None

	def list_by_folder( self, filter = None ):
		""" List all the driver entries by folder name """
		_lst = DriverList()
		for driver in self.drivers:
			if filter:
				if filter(driver)==False:
					continue
			_lst.append( driver.folder, driver )
		return sorted( _lst, key=lambda entry:entry[0] )

	def interface( self, code ):
		return [ item for item in self.interfaces if item.code == code ][0]

	def manufacturer( self, code ):
		return [ item for item in self.manufacturers if item.code == code ][0]
