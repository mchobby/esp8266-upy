""" PID Controler

	Domeu - Aug 8, 2021 - sourced from https://forum.mchobby.be/viewtopic.php?f=23&t=728
	Domeu - Aug 8, 2021 - deinit doesn't release the Timer & Callback. Set the temperature to 0 to halt the PID regulation.
"""
from machine import Timer
import time

class PID:

	def __init__(self, Kp, Ki, Kd, dt, setpoint, measure_func, output_func, output_min, output_max):
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd
		self.dt = int(round(dt / 1000)) # Convert from ms
		self.setpoint = setpoint
		self.measure_func = measure_func
		self.output_func = output_func
		self.output_min = output_min
		self.output_max = output_max

		self.last_measure = measure_func() # Store last measure for external access
		self.error = setpoint - self.last_measure
		self.integral = 0

		self.timer = Timer(-1) # Virtual timer
		self.timer.init(mode=Timer.PERIODIC, period=dt, callback=self.control)

	def control(self, timer):
		self.last_measure = self.measure_func()
		error = self.setpoint - self.last_measure
		proportional = self.Kp * error
		self.integral = self.integral + error * self.dt

		# Prevent integral windup
		if (proportional > self.output_max) or (proportional < self.output_min):
			self.integral = 0

		self.derivative = (error - self.error) / self.dt
		output = proportional + self.Ki * self.integral + self.Kd * self.derivative
		self.error = error

		output = max(self.output_min, output)
		output = min(self.output_max, output)
		self.output_func(output)

	def set(self, value):
		self.setpoint = value

	def stop(self):
		# self.timer.deinit() THAT's DOESN'T WORK!!!
		# self.timer.callback( None )
		self.set(0)
