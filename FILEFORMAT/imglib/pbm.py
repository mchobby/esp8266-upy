Not developped yet!!!!

REVIEW THIS CODE TO CREATE THE READER

pbm file format store images with 1 bit per pixel (so black / white)

while True:
    # Code inspired from twobitarcade.net
    #   https://www.twobitarcade.net/article/displaying-images-oled-displays/
    with open('ncd-mch.pbm', 'rb' ) as f:
        f.readline() # Magic number    P4 for pbm (Portable Bitmap)
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())

    fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
    lcd.invert(1)
    lcd.blit(fbuf, 0, 0)
    lcd.show()

    time.sleep(3)

    with open('upy-logo.pbm', 'rb' ) as f:
        f.readline() # Magic number    P4 for pbm (Portable Bitmap)
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())

    fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
    lcd.invert(1)
    lcd.blit(fbuf, 0, 0)
    lcd.show()

    time.sleep(3)
