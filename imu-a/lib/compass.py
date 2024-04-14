""" compass.py - compass helper for 9DOF IMU library

* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

14 Apr 2024 - domeu - extraction for compass.py
15 jun 2022 - domeu - initial portage from ZumoIMU.cpp

Based on project source @ https://github.com/mchobby/micropython-zumo-robot
"""

__version__ = "0.0.2"
__repo__ = "https://github.com/esp8266-upy/imu-a/lib/imu_a.py"

from imu_a import Vector
import time
import math

CALIBRATION_SAMPLES = 70

class Compass( object ):
	""" Compass IMU offers some COMPAS utility method over the IMU """
	DEVIATION_THRESHOLD = 5

	def __init__( self, imu, samples=CALIBRATION_SAMPLES ):
		self._imu = imu
		self._imu.config_for_compass_heading()
		self._samples = samples
		self._avg = Vector(0,0,0)
		self.m_min = Vector(32767,32767,32767)    # Used to calibrate min & max on magnetic sensor
		self.m_max = Vector(-32767,-32767,-32767)

	@property
	def min( self ):
		""" Calibration minima """
		return self.m_min

	@property
	def max( self ):
		""" Calibration maxima """
		return self.m_max

	def calibrate( self ):
		""" Magnetic sensor must turn on himself while performing  min & max values sampling """
		self.m_min = Vector(32767,32767,32767)
		self.m_max = Vector(-32767,-32767,-32767)

		for x in range( self._samples):
			self._imu.read_mag()
			self.m_min.x = min(self.m_min.x, self._imu.m.x)
			self.m_min.y = min(self.m_min.y, self._imu.m.y)

			self.m_max.x = max(self.m_max.x, self._imu.m.x)
			self.m_max.y = max(self.m_max.y, self._imu.m.y)
			print("COMPTEUR: %s | Running_max: %s | Running_min: %s " %(x, self.m_max, self.m_min))

			time.sleep_ms(50)

	def average_heading( self ):
		self._avg.set( 0,0,0 )
		for x in range(10):
			self._imu.read_mag()
			self._avg.x += self._imu.m.x
			self._avg.y += self._imu.m.y

		self._avg.x /= 10.0
		self._avg.y /= 10.0

		return self.heading() # angle in degree

	def relative_heading( self, heading_from, heading_to):
		# Relative Heading angle in degrées
		relative_heading=float(heading_to) - float(heading_from)
		if relative_heading > 180:
			relative_heading -=	360
		if  relative_heading < -180:
			relative_heading +=360

		return relative_heading

	def heading( self ):
		x_scaled = 2.0*(self._avg.x - self.m_min.x)/(self.m_max.x - self.m_min.x) - 1.0
		y_scaled = 2.0*(self._avg.y - self.m_min.y)/(self.m_max.y - self.m_min.y) - 1.0

		angle = math.atan2(y_scaled, x_scaled)*180/ math.pi # Radian
		if angle < 0 :
			angle+= 360
		return angle
