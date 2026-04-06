import micropython
import time
from btntls import BtnClicks

# because ClickBtn use IRQ
micropython.alloc_emergency_exception_buf(100)


btn_mode = BtnClicks( 17 )
btn_both = BtnClicks( 18 )

while True:
	_m = btn_mode.count
	_b = btn_both.count
	if (_m==None) and (_b==None):
		time.sleep_ms( 10 )
		continue
	if _m:
		print( "Mode was pressed %i times" % _m)
	if _b:
		print( "Both was pressed %i times" % _b )

