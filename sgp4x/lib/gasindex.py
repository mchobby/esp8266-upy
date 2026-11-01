""" Sensirion Gaz Index Algorithm Library for MicroPython


* Author(s): Meurisse D.
* See https://github.com/mchobby/esp8266-upy/sgp4x 

Ported from arduino-gas-index-algorithm 
https://github.com/Sensirion/arduino-gas-index-algorithm/tree/master

Producing driver is a tedeous work made available to you as free software!
Help us to produce more code and purchase your products from shop.mchobby.be
"""

class BaseIndexAlgorithm:
  def __init__( self ):
    # All int32
    self.index_offset = None
    self.learning_time_offset_hours = None
    self.learning_time_gain_hours = None
    self.gating_max_duration_minutes = None
    self.std_initial = None
    self.gain_factor = None


  def get_tuning_parameters( self ):
    return { 'index_offset' : self.index_offset, 'learning_time_offset_hours' : self.learning_time_offset_hours, \
            'learning_time_gain_hours' : self.learning_time_gain_hours, 'gating_max_duration_minutes' : self.gating_max_duration_minutes, \
            'std_initial' : self.std_initial, 'gain_factor' : self.gain_factor }

class VocIndexAlgorithm( BaseIndexAlgorithm ):
  def __init__( self ):
    super( BaseGazIndex , self ).__init()

class NoxIndexAlgorithm( BaseIndexAlgorithm ):
  def __init__( self ):
    super( BaseGazIndex , self ).__init()
