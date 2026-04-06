[Ce fichier existe également en FRANCAIS](btntls_readme.md)

# btntls library

The [btntls.py](lib/btntls.py) library offers functions and classes about button implementations.

# BtnClicks click
The `BtnClicks` class is used to count the number of consecutive button press.

`BtnClicks` setup software debouncing (25ms) and forseen a minimum time laps (250ms, configurable) 
to detect subsequent button press. Finally, the button counter is available after a trigger time 
(1000ms, configurable), time starting after the last button press.

`BtnClicks` expose the count of button press on the the `count` property, only after a trigger time
 (trigger_timeout). Otherwise, `count`will return `None`.

Once the counter available, reading the `count` property is a one-time operation. Immediately after, the 
returned value will be again `None`.

__Important Note:__
* The classe activates the pull-up resistor on the Pin. Pressing the button will connect the Pin to the ground.
* The classe use the interrupt mechanism (aka IRQ) to capture button press.

``` python
import micropython
import time
from btntls import BtnClicks

# because ClickBtn use IRQ
micropython.alloc_emergency_exception_buf(100)

btn_mode = BtnClicks( 17 ) # Button wired on GPIO 17
btn_both = BtnClicks( 18 ) # Button wired on GPIO 18

while True:
	_m = btn_mode.count
	_b = btn_both.count
	if (_m==None) and (_b==None):
		time.sleep_ms( 10 )
		continue
	if _m:
		print( "Mode button was pressed %i times" % _m)
	if _b:
		print( "Both button was pressed %i times" % _b )
```

Which would display the following result on the REPL session.

```
Both button was pressed 2 times
Mode button was pressed 1 times
Mode button was pressed 3 times
Both button was pressed 1 times
Both button was pressed 5 times
Mode button was pressed 1 times
Mode button was pressed 1 times
Both button was pressed 4 times
```

