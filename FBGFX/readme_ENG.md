[Ce fichier existe aussi en FRANCAIS](readme.md)

# FrameBuffer GFX - FrameBuffer utility
This section contains class and exemple used to manipulates FrameBuffer.

* __[fbutil.py](lib/fbutil.py)__ :  circle, fill_circle, oval, fill_oval, rrect, fill_rrect, etc. Example: [here](https://github.com/mchobby/esp8266-upy/tree/master/ili934x/examples/fbutil)
* __[icon.py](lib/icon.py)__ :  5x5 icons definition from Micro:bit (coming from sense-hat sub-project). 

# Drawx an icon into the FrameBuffer

``` python
def icon( fb, icon, x=1, y=1, color=0x7BEF ):
  """ Display one of the icon in the fb FrameBuffer @ x,y position with the C color.
		    Icons are stored into the icons.py file. Only draws pixels (don't clear pixels) """
  size = icon[0]
  for row in range( size ):
    for col in range( size ):
      if (icon[row+1] & (1<<col)) > 0:
        fb.pixel(col+y,row+y,color)
```


