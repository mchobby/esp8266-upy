""" Based on the Radomir Dopieralski works.
    micropython-pca9685 available at https://bitbucket.org/thesheep/micropython-pca9685/src/c8dec836f7a4?at=default

    July 11, 2016 - I2C fixes, inheritance - DMeurisse (shop.mchobby.be)  """
from pca9685 import PCA9685
import math


class ServoCtrl( PCA9685 ):
    """ Servo Controleur - Allow you to control the servo 0 to 15 on the PCA9685 PWM Driver """
    def __init__(self, i2c, address=0x40, freq=50, min_us=600, max_us=2400,
                 degrees=180):
        PCA9685.__init__( self, i2c=i2c, address=address)
        
        self.period = 1000000 / freq
        self.min_duty = self._us2duty(min_us)
        self.max_duty = self._us2duty(max_us)
        self.degrees = degrees
        
        # Init the freq on PCA9685
        self.freq(freq)

    def _us2duty(self, value):
        return int(4095 * value / self.period)

    def position(self, index, degrees=None, radians=None, us=None, duty=None):
        span = self.max_duty - self.min_duty
        if degrees is not None:
            duty = self.min_duty + span * degrees / self.degrees
        elif radians is not None:
            duty = self.min_duty + span * radians / math.radians(self.degrees)
        elif us is not None:
            duty = self._us2duty(us)
        elif duty is not None:
            pass
        else:
            return self.duty(index)
        duty = min(self.max_duty, max(self.min_duty, int(duty)))
        self.duty(index, duty)

    def release(self, index=None ):
        if index==None:
            for i in range( 16 ):
                self.duty(i, 0)
        else:
            self.duty(index, 0)
