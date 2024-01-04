""" HUSKYLENS : Easy-to-use AI Machine Vision Sensor with MicroPython

  Library @ https://github.com/mchobby/esp8266-upy/tree/master/huskylens

Based on the following DFRobot [community article](https://community.dfrobot.com/makelog-311712.html).
Library credits to [RRoy](https://community.dfrobot.com/makelog-310469.html).

Buy HUSKYLENS at:
 * https://shop.mchobby.be/fr/imprimantes-et-camera/2421-huskylens-capteur-de-vision-ai-uart-i2c-interface-gravity-3232100024212-dfrobot.html
 * https://www.dfrobot.com/product-1922.html

History:
 * 2023-12-28 Portage to MicroPython, refactoring by [MCHobby](shop.mchobby.be)

Doc: https://github.com/HuskyLens/HUSKYLENSArduino/blob/master/HUSKYLENS%20Protocol.md

"""
from ubinascii import unhexlify # HexString -> bytes
import time

__version__ = '0.1.0'

HEADER = "55AA11" # Command Header and Address

# See https://github.com/HuskyLens/HUSKYLENSArduino/blob/master/HUSKYLENS%20Protocol.md#command_request_algorithm0x2d
# 0x2D COMMAND_REQUEST_ALGORITHM stored as number (sparing memory)
FACE_RECOGNITION   = const( 0x022d00003f )
OBJECT_TRACKING    = const( 0x022d010040 )
OBJECT_RECOGNITION = const( 0x022d020041 )
LINE_TRACKING      = const( 0x022d030042 )
COLOR_RECOGNITION  = const( 0x022d040043 )
TAG_RECOGNITION    = const( 0x022d050044 )
OBJECT_CLASSIFICATION = const( 0x022d060045 )

ALGORTHIM_NAMES = { FACE_RECOGNITION:"FACE_RECOGNITION", OBJECT_TRACKING:"OBJECT_TRACKING",
	OBJECT_RECOGNITION:"OBJECT_RECOGNITION",LINE_TRACKING:"LINE_TRACKING",
	COLOR_RECOGNITION:"COLOR_RECOGNITION", OBJECT_CLASSIFICATION:"OBJECT_CLASSIFICATION",
	None:"UNDEFINED" }

COMMAND_REQUEST_CUSTOMNAMES= 0x2f
COMMAND_REQUEST_TAKE_PHOTO_TO_SD_CARD = 0x30
COMMAND_REQUEST_SAVE_MODEL_TO_SD_CARD = 0x32
COMMAND_REQUEST_LOAD_MODEL_FROM_SD_CARD = 0x33
COMMAND_REQUEST_CUSTOM_TEXT = 0x34
COMMAND_REQUEST_CLEAR_TEXT = 0x35
COMMAND_REQUEST_LEARN_ONECE = 0x36
COMMAND_REQUEST_FORGET = 0x37
COMMAND_REQUEST_SCREENSHOT_TO_SD_CARD = 0x39
COMMAND_REQUEST_FIRMWARE_VERSION = 0x3C

class Point:
	__slots__ = ('x','y')
	def __init__( self ):
		self.x = 0
		self.y = 0

class GenericData( list ):
	""" Just store the list of values returned from _processData """
	@property
	def id( self ):
		return self[4]

class Box( GenericData ):
	__slot__ = ('_center')

	def __init__( self ):
		super( Box, self ).__init__()
		self._center = Point()

	def __repr__( self ):
		return "<%s ID%i center=%i,%i   width,height=%i,%i>" % (self.__class__.__name__, self.id, self[0], self[1], self.width, self.height )

	@property
	def center( self ):
		self._center.x = self[0]
		self._center.y = self[1]
		return self._center

	@property
	def width( self ):
		""" Box width """
		return self[2]

	@property
	def height( self ):
		""" Box Height """
		return self[3]

class Arrow( GenericData ):
	__slots__ = ('_origin','_target')
	def __init__( self ):
		super( Arrow, self ).__init__()
		self._origin = Point()
		self._target = Point()

	def __repr__( self ):
		return "<%s ID%i center(x,y)=%i,%i   target(x,y)=%i,%i>" % (self.__class__.__name__, self.id, self[0], self[1], self[2], self[3] )

	@property
	def origin( self ):
		self._origin.x = self[0]
		self._origin.y = self[1]
		return self._origin

	@property
	def target( self ):
		self._target.x = self[2]
		self._target.y = self[3]
		return self._target


class HuskyLens:
    def __init__(self, i2c=None, address=0x32, uart=None ):
        """ Create an instance with communication bus. The address is for I2C bus. """
        self.proto  = "I2C" if i2c!=None else "SERIAL"
        self._bus   = i2c if i2c!=None else uart
        self.address=address
        #if(self.proto=="SERIAL"):
        #    self._bus = UART(2,baudrate=9600,rx=33,tx=32,timeout=100)
        #else :
        #    self._bus = I2C(0, sda=Pin(8), scl=Pin(9), freq=10000) # sda=green(T)=gp8, scl=blue(R)=gp9
        #self.lastCmdSent = ""

        # Update by _processData
        self._count     = 0 # count of blocks and arrows
        self._learned   = 0 # count of LearnedIDs
        self._frame_nbr = 0 # Frame Number
        # Last algorithm set with the library
        self._algorithm = None


    def _write(self, cmd): # Send data to HuskyLens
        #self.lastCmdSent = cmd
        if(self.proto=="SERIAL"):
            self._bus.write(cmd)
        else :
            self._bus.writeto(self.address, cmd)

    def _checksum(self, hexStr): # Calculate the CRC of HexString
        total = 0
        for i in range(0, len(hexStr), 2):
            total += int(hexStr[i:i+2], 16)
        hexStr = hex(total)[-2:]
        return hexStr

    def _split_command(self, str): # Split a HuskyLens command request into parts
        headers = str[0:4]
        address = str[4:6]
        data_length = int(str[6:8], 16)
        command = str[8:10]
        if(data_length > 0):
            data = str[10:10+data_length*2]
        else:
            data = []
        checkSum = str[2*(6+data_length-1):2*(6+data_length-1)+2]
        # convert the command to its integer valye
        return [headers, address, data_length, int(command,16), data, checkSum]

    def _read_BoA(self): # Read Block OR Arrow data from HuskyLens
        if(self.proto=="SERIAL"):
            byteString = self._bus.read(5)
            byteString += self._bus.read(int(byteString[3]))
            byteString += self._bus.read(1)
        else:
            byteString  =self._bus.readfrom(self.address,5)
            byteString +=self._bus.readfrom(self.address,byteString[3]+1)
        commandSplit = self._split_command(''.join(['%02x' % b for b in byteString]))
        return commandSplit[3], commandSplit[4] # return (command,data)

    def _processData(self): # Process the returned Data
        try:
            if(self.proto=="SERIAL"):
                byteString = self._bus.read(5)
                byteString += self._bus.read(int(byteString[3]))
                byteString += self._bus.read(1)
            else:
                byteString  =self._bus.readfrom(self.address,5)
                byteString +=self._bus.readfrom(self.address,byteString[3]+1)

            #print( byteString ) # DEBUG: received data bytes
            commandSplit = self._split_command(''.join(['%02x' % b for b in byteString]))
            _cmd = commandSplit[3]
            if _cmd == 0x00: # Seems return by the "Change Algorithm"
                return False
            if _cmd == 0x2E: # OK RESULT (by knock or change algorithm)
                return True
            else: # We should have a 0x29 (general info)
                _r = [] # resyktubg kust
                self._count = int( commandSplit[4][2:4]+commandSplit[4][0:2], 16 ) # count of Blocks or Arrow
                self._Learned = int( commandSplit[4][6:8]+commandSplit[4][4:6], 16 ) # Count of learnedIDs
                self._frame_nbr = int( commandSplit[4][10:12]+commandSplit[4][8:10], 16 ) # FrameNumber
                for k in range(self._count):
                    # returnData.append(self._read_BoA())
                    _cmd,_data = self._read_BoA() # '8b0073007f0080000100'
                    # Which resulting object to create ?
                    if _cmd == 0x2A:
                        _tmp = Box() # derived from list()
                    elif _cmd == 0x2B:
                        _tmp = Arrow() # derived from list()
                    else:
                        _tmp = GenericData() # derived from list()

                    # transform data to list [139, 115, 127, 128, 1]
                    for q in range(0,len(_data),4):
                        _tmp.append( int(_data[q:q+2],16)+int(_data[q+2:q+4],16) )
                    # Add specialized object (to resulting list)
                    _r.append( _tmp )
                return _r
        except:
             print("Read error")
             raise
             return []

    @property
    def count( self ):
        """ count of Blocks or Arrows """
        return self._count

    @property
    def learned( self ):
        """ count of Learned IDs """
        return self._learned

    @property
    def frame_number( self ):
        return self._frame_nbr

    @property
    def algorithm( self ):
        """ Algorithm/mode as set with this library or None if not yet done. """
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value ):
        assert value != None, "None is an invalid algorithm!"
        assert value in ALGORTHIM_NAMES, "Invalid algorithm value! %s" % str(ALGORTHIM_NAMES.values()).replace("'","")
        self._algorithm = value
        h = "%010x" % value # as hexadecimal, 0 left padded over 10 position
        cmd = unhexlify(HEADER+h)
        self._write(cmd)
        return self._processData()

    def knock(self):
        cmd = unhexlify(HEADER+"002c3c")
        self._write(cmd)
        return self._processData()

    def get_all(self, learned=False ): # Tested OK
        cmd = unhexlify(HEADER+ ("002333" if learned else "002030") )
        self._write(cmd)
        return self._processData()

    def get_blocks(self, learned=False ): # Tested OK
        cmd = unhexlify(HEADER+ ("002434" if learned else "002131") )
        self._write(cmd)
        return self._processData()

    def get_arrows(self, learned=False ): # Tested OK
        cmd = unhexlify(HEADER+("002535" if learned else "002232") )
        self._write(cmd)
        return self._processData()

    def get_by_id(self, idVal, block=None, arrow=None ): # Tested OK
        # Note: block=None & arrow=None is the same as block=True & arrow=True
        #       => return any of the block/arrow having the ID=idVal
        if ((block==None) and (arrow==None)) or ((block==True) and (arrow==True)):
            cmd = "0226" # get any by ID
        elif block:
            cmd = "0227" # get Blocks by ID
        elif arrow:
            cmd = "0228" # get Arrows by ID
        idVal = "{:04x}".format(idVal)
        req = HEADER+cmd+idVal[2:]+idVal[0:2]
        req += self._checksum(req)
        self._write( unhexlify(req) )
        return self._processData()

    #---------------------  8.5 update new features
    def custom_text(self, x,y, msg ): # Tested OK
        # Place custom text (20 chars) at position x,y on HUSKYLENS UI
        #   https://github.com/HuskyLens/HUSKYLENSArduino/blob/master/HUSKYLENS%20Protocol.md#command_request_custom_text-0x34
        assert len(msg)<=20, "Max string len exceeded"
        cmd = HEADER
        cmd += "{:02x}".format( len(msg)+4 )   # data length [len(msg)+4 ]
        cmd += "{:02x}".format(COMMAND_REQUEST_CUSTOM_TEXT)
        # first 4 digits: length,cor_x1,cor_x2,cor_y
        cmd += "{:02x}".format( len(msg)+4 )
        # Coordinate X
        if x > 255:
            cmd += "{:02x}".format(0xff)
            cmd += "{:02x}".format(x%256)
        else:
            cmd += "{:02x}".format(0)
            cmd += "{:02x}".format(x)
        # Coordinate Y
        cmd += "{:02x}".format(y)
        # Text content
        for ch in msg:
            cmd += "{:02x}".format(ord(ch))
        cmd += self._checksum(cmd)
        self._write( unhexlify(cmd) )
        return self._processData()

    def clear_text(self): # Tested OK
        # Clear any custom text on HUSKYLENS UI
        cmd = HEADER + "00" # data length = 0
        cmd += "{:02x}".format(COMMAND_REQUEST_CLEAR_TEXT)
        cmd += self._checksum(cmd)
        self._write( unhexlify(cmd) )
        return self._processData()

    def forget(self): # Tested OK
        cmd = HEADER+"00" # data length = 0
        cmd += "{:02x}".format(COMMAND_REQUEST_FORGET)
        cmd += self._checksum(cmd)
        self._write( unhexlify(cmd) )
        return self._processData()

    def learn_once(self, id ): # Tested OK
        cmd = HEADER + "02"  # data length = 2
        cmd += "{:02x}".format(COMMAND_REQUEST_LEARN_ONECE)
        cmd += "{:02x}".format( id & 0xff )
        cmd += "{:02x}".format( (id >> 8) & 0xff )
        cmd += self._checksum(cmd)
        self._write( unhexlify(cmd) )
        return self._processData()

    def photo_to_sd(self): # Tested OK
        cmd = HEADER + "00" # data length = 0
        cmd += "{:02x}".format(COMMAND_REQUEST_TAKE_PHOTO_TO_SD_CARD)
        cmd += self._checksum(cmd)
        self._write( unhexlify(cmd) )
        return self._processData()

    def screen_to_sd(self): # Tested OK
        cmd = HEADER + "00" # data length = 0
        cmd += "{:02x}".format(COMMAND_REQUEST_SCREENSHOT_TO_SD_CARD)
        cmd += self._checksum(cmd)
        self._write( unhexlify(cmd) )
        return self._processData()

    def set_customnames(self, id, name): # not tested yet
        # Set a custom name for a learned object.
        # https://github.com/HuskyLens/HUSKYLENSArduino/blob/master/HUSKYLENS%20Protocol.md#command_request_custom_text-0x34
        assert len(name)<20 # Not specified in spec but should be reasonable
        assert id>0         # ID0 is un-learned
        cmd = HEADER+"{:02x}".format( len(name)+3 ) # data length = name length + 3
        cmd += "{:02x}".format(COMMAND_REQUEST_CUSTOMNAMES)
        cmd += "{:02x}".format(id)
        cmd += "{:02x}".format( len(name)+1 )
        for char in name:
            cmd += "{:02x}".format(ord(char))
        cmd += "00" # Null Terminaed
        cmd += self._checksum(cmd)
        self._write( unhexlify(cmd) )
        return self._processData()

    def save_model_to_sd(self,filenum): # Tested OK
        # Save the current algorithm/mode model to the SDCard with the following
        # filename <AlgorithmName>_Backup_<FileNum>.conf
        cmd = HEADER+"02" # data length = 2
        cmd += "{:02x}".format(COMMAND_REQUEST_SAVE_MODEL_TO_SD_CARD)
        cmd += "{:02x}".format( filenum & 0xff )
        cmd += "{:02x}".format( (filenum >> 8) & 0xff )
        cmd += self._checksum(cmd)
        self._write( unhexlify(cmd) )
        return self._processData()

    def load_model_from_sd(self, filenum): # Tested OK
        # Reload a saved model (see save_model_to_sd for details)
        cmd = HEADER+"02" # data length = 2
        cmd += "{:02x}".format(COMMAND_REQUEST_LOAD_MODEL_FROM_SD_CARD)
        cmd += "{:02x}".format( filenum & 0xff )
        cmd += "{:02x}".format( (filenum >> 8) & 0xff )
        cmd += self._checksum(cmd)
        self._write( unhexlify(cmd) )
        return self._processData()
