# Hysteresis Thermostat tester for eather 
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/LIBRARIAN
#
from hyst import HeaterTh

# Create a temperature cycle
tcycle = [i for i in range(10,31)] + [i for i in range(31,9,-1)]

# Create a Thermostat set on 22°C with an Hysteresis of 2.5°C (-1.25°C to +1.25°C)
thermostat = HeaterTh( 22, 2.5 ) 

print( "--- SetPoint %f -------------------------------" % thermostat.setpoint )
for temp in tcycle:
	state = thermostat.update( temp )
	print( "[%s] at %i°C heater is %s" % (thermostat.setpoint, temp, "ON" if state else 'off') )


thermostat.setpoint = 25.6
print( "--- SetPoint %f -------------------------------" % thermostat.setpoint )
for temp in tcycle:
	state = thermostat.update( temp )
	print( "[%s] at %i°C heater is %s" % (thermostat.setpoint, temp, "ON" if state else 'off') )
