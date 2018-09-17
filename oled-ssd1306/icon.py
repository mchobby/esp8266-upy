from machine import Pin, I2C
import time
i2c = I2C( sda=Pin(4), scl=Pin(5) )
import ssd1306
lcd = ssd1306.SSD1306_I2C( 128, 32, i2c )
lcd.fill( 0 )
lcd.show()

HEART_ICON = [
  [0,0,0,0,0,0,0,0,0,0,0],
  [0,0,1,1,1,0,1,1,1,0,0],
  [0,1,1,0,1,1,1,1,1,1,0],
  [0,1,0,1,1,1,1,1,1,1,0],
  [0,1,1,1,1,1,1,1,1,1,0],
  [0,0,1,1,1,1,1,1,1,0,0],
  [0,0,0,1,1,1,1,1,0,0,0],
  [0,0,0,0,1,1,1,0,0,0,0],
  [0,0,0,0,0,1,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0] ]

# a: Alpha Channel (pas dessiné)
a = None
FB_ICON = [
  [a,a,a,a,a,a,a,a,a,a,0,0,a,a,a,a,a],
  [a,a,a,a,a,a,a,a,a,0,0,0,0,a,a,a,a],
  [a,a,a,a,a,a,a,a,0,0,1,1,0,0,a,a,a],
  [a,a,a,a,a,a,a,0,0,1,0,1,0,0,a,a,a],
  [a,a,a,a,a,a,a,0,0,1,0,1,0,0,a,a,a],
  [a,a,a,a,a,a,a,0,0,1,0,1,0,0,a,a,a],
  [a,a,a,a,a,a,0,0,1,0,0,1,0,0,0,0,a],
  [0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0],
  [0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
  [0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0],
  [0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0],
  [0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0],
  [0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0],
  [0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,0,0],
  [0,0,1,1,1,1,0,a,0,1,1,1,1,1,0,0,a],
  [a,0,0,0,0,0,0,a,0,0,0,0,0,0,0,a,a],
  [a,0,0,0,0,0,a,a,a,0,0,0,0,0,0,a,a] ]

def draw_icon( lcd, from_x, from_y, icon ):
    for y, row in enumerate( icon ):
        for x, color in enumerate( row ):
            if color==None:
                continue
            lcd.pixel( from_x+x, 
                       from_y+y,
                       color )

def randrange( max ):
    assert max < 256
    import urandom
    r = urandom.getrandbits(8)
    while r > max:
        r = urandom.getrandbits(8)
    return r

def random_icon( lcd, icon, count ):
    range_x = lcd.width - len(icon[0])
    range_y = lcd.height - len(icon)
    for i in range( count ):
        draw_icon( lcd, 
           randrange( range_x ),
           randrange( range_y ),
           icon
           )

# Affiche une Simple icone
lcd.fill( 0 )
draw_icon( lcd, 0, 0, HEART_ICON )
lcd.show() 
time.sleep( 2 ) # 2 secondes

# 4x affichage aléatoire de 25 icones
for i in range( 5 ):
    lcd.fill( 0 )
    random_icon( lcd, HEART_ICON, 25 )
    lcd.show()
    time.sleep( 2 ) 

# affichage de 30 icones (avec canal Alpha )
lcd.fill( 0 )
for i in range( 30 ):
    random_icon( lcd, FB_ICON, 1 )
    lcd.show()

time.sleep( 2 )
lcd.fill( 0 )

