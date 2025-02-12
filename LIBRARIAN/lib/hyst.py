# Implementation of Hysteresis to implement Thermostat behavior
#
# Author: DMeurisse
#
# See project source at: https://github.com/mchobby/esp8266-upy/tree/master/LIBRARIAN

__version__ = '0.0.1'

class Hysteresis():
	def __init__( self, setpoint, hysteresis ):
		self.setpoint = setpoint
		self.hysteresis = hysteresis
		self.state = None # Output state 

	def update( self, value ):
		pass 

class HeaterTh(Hysteresis):
	""" Heater Thermostat """
	def __init__( self, setpoint, hysteresis, value=None ):
		super().__init__( setpoint, hysteresis )
		if value != None:
			self.state = value < (self.setpoint + self.hysteresis/2)


	def update( self, value ):
		if self.state==None:
			self.state = value < (self.setpoint + self.hysteresis/2)
		elif (self.state==True) and (value >= self.setpoint+(self.hysteresis/2)):
			self.state = False
		elif (self.state==False) and (value <= self.setpoint-(self.hysteresis/2)):
			self.state = True

		return self.state


class CoolerTh(Hysteresis):
	""" Cooler Thermostat """
	def __init__( self, setpoint, hysteresis, value=None ):
		super().__init__( setpoint, hysteresis )
		if value != None:
			self.state = value >= (self.setpoint + self.hysteresis/2)


	def update( self, value ):
		if self.state==None:
			self.state = value >= (self.setpoint + self.hysteresis/2)
		elif (self.state==True) and (value <= self.setpoint-(self.hysteresis/2)):
			self.state = False
		elif (self.state==False) and (value >= self.setpoint+(self.hysteresis/2)):
			self.state = True

		return self.state

