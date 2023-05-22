''' rgbfx is RGB color effects for MOD-RGB board. 

  Based on former MC Hobby work (shop.mchobby.be)
  see: https://github.com/mchobby/esp8266-upy/blob/master/neopixel/fxdemo.py

rely on modrgb, the micropython module for the Olimex MOD-RGB board. 

The MIT License (MIT)
Copyright (c) 2018 Dominique Meurisse, support@mchobby.be, shop.mchobby.be

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import math
from time import sleep_ms # ESP8266

RGB_WAIT = 50 # Under 50 ms may cause I2C Bus ETimedOut 
              # on the MOD-RGB (original value was 10ms)

def fade_inout( modrgb, color, step=5 ):
    assert len(color)==3, "Invalid color tuple!"
    for b in range( 0, 256, step ):
        col = ( (color[0]*b)//255 , (color[1]*b)//255, (color[2]*b)//255 ) 
        modrgb.set_rgb( col )
        sleep_ms( RGB_WAIT )
    for b in range( 255, -1, -1*step ):
        col = ( (color[0]*b)//255 , (color[1]*b)//255, (color[2]*b)//255 ) 
        modrgb.set_rgb( col )
        sleep_ms( RGB_WAIT )

def cycle_wheel( modrgb ):
    for i in range( 0, 256 ):
        col = wheel( i )
        modrgb.set_rgb( col )
        sleep_ms( RGB_WAIT )

def candle( modrgb, iteration=25 ):
    while iteration>0 :
        iteration -= 1
        rnd0 = randrange( 255 ) # generate random byte (0-255)
        rnd1 = randrange( 255 ) # generate random byte (0-255)
        green = 50 + int(rnd0) 
        green = green if green <= 255 else 255
        red   = green + int(rnd1) 
        red   = red if red <= 255 else 255
        modrgb.set_rgb( (red, green, 0) )
        sleep_ms( RGB_WAIT )
    
# -- Tools ----------------------------------------------------------
def randrange( max ):
    assert max < 256
    import urandom
    r = urandom.getrandbits(8)
    while r > max:
        r = urandom.getrandbits(8)
    return r

def wheel( wheel_pos ):
    """ caculate color based on a color wheel. 
        Color are transistion r - g - b back r based on wheel_pos (0-255) """
    assert 0<= wheel_pos <= 255, "Invalid wheel_pos!"
    
    wheel_pos = 255 - wheel_pos
    if( wheel_pos < 85 ):
        return ( 255-(wheel_pos*3), 0, wheel_pos*3 )
    elif( wheel_pos < 170 ):
        wheel_pos -= 85
        return ( 0, wheel_pos*3, 255-(wheel_pos*3) )
    else:
        wheel_pos -= 170
    return ( wheel_pos*3, 255-(wheel_pos*3), 0 )

# hsv2rgb & rgb2hsv are sourced 
# from http://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/
def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b
    
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v