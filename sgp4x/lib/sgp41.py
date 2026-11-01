""" SGP41 MicroPython Library 

  The SGP41 is an air quality sensor measuring VoC and NOx (MOX).
  MOX sensor use a hotplate as sensitive element. 
  The hotplate requires conditionning period of 10 sec.
  Data is captured over I2C bus.


* Author(s): Meurisse D.
* See https://github.com/mchobby/esp8266-upy/sgp4x 

Based on https://github.com/Sensirion/arduino-i2c-sgp41 for Arduino.

Producing driver is a tedeous work made available to you as free software!
Help us to produce more code and purchase your products from shop.mchobby.be
"""
from micropython import const
import time, struct

class SGP41:
  def __init__( self, i2c, address=0x59 ):
    self._i2c = i2c
    self._address = address
    self.buf9 = bytearray(9)    
    self.buf2 = bytearray(2)
    self.buf3 = bytearray(3)
    self.buf6 = bytearray(6)

  def calc_crc( self, buf2 ):
    crc = 0xFF
    for i in range(2):
      crc = crc ^ buf2[i]
      for bitnr in range( 8 ):
        if (crc & 0x80)==0x80 :
          crc = ((crc << 1) & 0xFF) ^ 0x31
        else:
          crc = (crc << 1) & 0xFF
    return crc 

  def check_crc_from( self, abuf ):
    # There is a CRC every 2 bytes of the buffer (data_len=2).    
    mv = memoryview( abuf )
    for ipos in range( len(abuf)//3 ):
        data = mv[ipos*3:(ipos*3)+2]
        crc  = mv[(ipos*3)+2]
        if self.calc_crc( data ) != crc:
          raise ValueError( 'Invalid CRC %i for data %i %i' % (crc, data[0], data[1]) )


  def exec_cmd_into( self, cmd, abuf, ms ):
    # Send a 16 bit command and read results into the abuf buffer.
    # ms is the measurement duration required by the command.
    # data_len specify the number of bytes in a Data+CRC block 
    self.buf2[0] = (cmd >> 8)
    self.buf2[1] = (cmd & 0xFF)
    self._i2c.writeto( self._address, self.buf2 )
    time.sleep_ms( ms )
    if abuf!=None:
      self._i2c.readfrom_into( self._address, abuf )
      self.check_crc_from( abuf ) # will raise exception is case of error

  def exec_cmd_param_into( self, cmd, params, abuf, ms ):    
    buf = bytearray( 2+len(params)*3 )
    # Send a 16 bit with a list of parameters. Each if tghe parameters MUST be a buffer of 2 bytes
    # Then it reads the response into abuf
    buf[0] = (cmd >> 8)
    buf[1] = (cmd & 0xFF)
    for idx,pbuf in enumerate(params):
      assert isinstance(pbuf,bytes) or isinstance(pbuf,bytearray), "params %r is not a buffer!" % pbuf
      base_offset = (idx*3)+2
      buf[base_offset+0] = pbuf[0]
      buf[base_offset+1] = pbuf[1]
      buf[base_offset+2] = self.calc_crc(pbuf)
    self._i2c.writeto( self._address, buf, False ) # Last param is "stop" state

    time.sleep_ms( ms )
    if abuf!=None:
      # Wait the read to be acknowledge
      iretry = 10
      while iretry>0:
        try:
          # self._i2c.readfrom_into( self._address, abuf )
          self._i2c.readfrom_into( self._address, abuf )
          self.check_crc_from( abuf ) # will raise exception is case of error
          return # It's OK boss
        except OSError as err:
          if not("EIO" in str(err)):
            raise
          iretry -= 1
          time.sleep_ms( 1000 )
      raise OSError('Cmd %s read error for %i bytes' % (hex(cmd),len(abuf)) )      


  @property
  def serial_number( self ):
    # Returns 48bits serial number as integer
    self.exec_cmd_into( 0x3682, self.buf9, 1 ) # 1ms of pause
    v = self.buf9[0]
    v = ( v<<8 ) + self.buf9[1]
    v = ( v<<8 ) + self.buf9[3]
    v = ( v<<8 ) + self.buf9[4]
    v = ( v<<8 ) + self.buf9[6]
    v = ( v<<8 ) + self.buf9[7]
    return v


  def self_test( self ):
    # This command triggers the built-in self-test checking 
    # for integrity of both hotplate and MOX material and returns the result of
    # this test as 2 bytes
    #
    # Returns test result 0xXX 0xYY: ignore most significant byte 0xXX. The four
    # least significant bits of the least significant byte 0xYY provide
    # information if the self-test has or has not passed for each individual
    # pixel. All zero mean all tests passed successfully. Check the datasheet for more detailed information.
    #
    # May raise exception
    self.exec_cmd_into( 0x280E, self.buf3, 320 ) # requires 320ms to execute
    if self.buf3[1]!=0x00:
      raise Exception( "Self test failed with code %i = pixels %s" % (self.buf3[1], bin(self.buf3[1] & 0x0F)) )

     
  def heater_off( self ): # return uint16_t
    # This command turns the hotplate off and stops the measurement. 
    # Subsequently, the sensor enters the idle mode (so we do not expect any response)
    self.exec_cmd_into( 0x3615, None, 1 )


  def conditioning( self, default_rh, default_t ): # uint16_t defaultRh, uint16_t defaultT, uint16_t& srawVoc
    # This command starts the conditioning, i.e., the VOC pixel will be operated at the same temperature as it is by calling
    # the sgp41_measure_raw command while the NOx pixel will be operated at a different temperature for conditioning. 
    # This command returns only the measured raw signal of the VOC pixel SRAW_VOC as 2 bytes (+ 1 CRC byte).
    #
    # WARNING: To avoid damage to the sensing material the conditioning must not exceed 10s!
    #
    # default_rh Default conditions for relative humidty (uint16, big endian)
    # default_t  Default conditions for temperature (uint16, big endian)
    #
    # returns: srawVoc u16 unsigned integer directly provides the raw signal SRAW_VOC in ticks which is proportional 
    # to the logarithm of the resistance of the sensing element.
    #
    # May raise exception in case of error
    assert 0<=default_rh<=100, "rh must be in the range 0..100"
    assert -45<=default_t<=130, "t must be in the range -45..130"    
    rh = (65535*default_rh)//100 # convert value for SGP41
    t =  int((default_t+45)*(65535/175))
    params = [ struct.pack('>H', rh), 
               struct.pack('>H', t) ]
    self.exec_cmd_param_into( 0x2612, params, self.buf3, 100 ) # 50ms delay
    return (self.buf3[0]<<8) + self.buf3[1] # srawVoc is an uint16


  def measure_raw( self, rh, t ):
    # Read the raw sensor values after the conditioning.
    # returns a (srawVoc, srawNox) tuple with raw signal value which are both uint16
    # 
    assert 0<=rh<=100, "rh must be in the range 0..100"
    assert -45<=t<=130, "t must be in the range -45..130"
    
    rh = (65535*rh)//100 # convert value for SGP41
    t =  int((t+45)*(65535/175))
    
    params = [ struct.pack('>H',rh), 
               struct.pack('>H',t ) ]
    self.exec_cmd_param_into( 0x2619, params, self.buf6, 50 ) # 50ms delay

    mv = memoryview(self.buf6)
    raw_voc = struct.unpack( '>H', mv[0:2] )[0] # decode Uint16
    raw_nox = struct.unpack( '>H', mv[3:5] )[0] # decode Uint16
    return (raw_voc, raw_nox)
