WIFI_SSID = "MY_WIFI_SSID"
WIFI_PASSWORD = "MY_PASSWORD"

def sta_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        # connecting to network...
        wlan.connect( WIFI_SSID, WIFI_PASSWORD )
        
        import time
        ctime = time.time()
        while not wlan.isconnected():
            if time.time()-ctime > 40:
                print( 'WLAN timeout!')
                break
            time.sleep( 0.5 )

sta_connect()

import gc
#import webrepl
#webrepl.start()
gc.collect()
