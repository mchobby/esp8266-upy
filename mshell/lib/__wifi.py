""" MiniShell wifi command for station mode. """

import time, binascii

def wifi( shell, args ):
	# All input should be made via the shell
	try:
		import network
	except:
		shell.println( 'No network support!' )
		return -1

	sCmd = '' if len(args)==0 else args[0].upper()
	sta = network.WLAN( network.STA_IF )

	if sCmd=='UP':
		if not sta.active():
			shell.println('Going up')
			sta.active(True)
		else:
			shell.println('Already up!')
		return 0
	elif sCmd=='DOWN':
		if sta.active():
			shell.println('Going down')
			sta.active(False)
		else:
			shell.println('Already down!')
		return 0
	elif sCmd=='CONNECT':
		if len(args)<3:
			shell.println( 'requires SSID and PASSWORD arguments!' )
			return -1
		wifi_ssid = args[1].encode("utf-8")
		wifi_pswd = args[2].encode("utf-8")
		if not sta.active():
			shell.println('Going up')
			sta.active(True)
		if sta.isconnected():
			shell.println( 'Disconnecting...' )
			sta.disconnect()
		shell.println( 'Connecting to %s...' % args[1] )
		sta.connect( wifi_ssid, wifi_pswd )
		# Waiting for connexion.
		dt = time.time()
		while ((time.time()-dt)<40) and not sta.isconnected():
			time.sleep(0.5)
		if sta.isconnected():
			shell.println('connected!')
			return 0
		shell.println('still not connected' )
		return -1

	elif sCmd=='SCAN':
		_sec_text = { 0:'open', 1:'WEP', 2:'WPA-PSK', 3:'WPA2-PSK', 4:'WPA/WPA2-PSK',
					5:'WPA3'}
		def _hex( data ):
			val = binascii.hexlify( data )
			return '.'.join( [val[i:i+2].decode('utf-8').upper() for i in range(0, len(val), 2)] )
		def _SecAsText( i ):
			if i in _sec_text:
				return _sec_text[i]
			else:
				return '%s' % i

		if not sta.active():
			shell.println('Interface down')
			return -1
		_l = sta.scan()
		shell.println('%-25s : %-20s : %4s : %4s : %-15s : %s' % ( 'SSID','BSSID','Ch', 'RSSI', 'Security', 'Hidden') )
		shell.println( '' )
		for _i in _l:
			shell.println( '%-25s : %-20s : %4i : %4i : %-15s : %i' % (_i[0].decode('utf8'), _hex(_i[1]), _i[2], _i[3], _SecAsText(_i[4]), _i[5]) )

		return 0
	else:
		st = sta.status()
		shell.println( '%r' % sta )
		status_dic = {
				network.STAT_IDLE : "STAT_IDLE - no connection and no activity",
				network.STAT_CONNECTING : "STAT_CONNECTING - connecting in progress",
				network.STAT_WRONG_PASSWORD: "STAT_WRONG_PASSWORD - failed due to incorrect password",
				network.STAT_NO_AP_FOUND : "STAT_NO_AP_FOUND - failed because no access point replied",
				network.STAT_CONNECT_FAIL : "STAT_CONNECT_FAIL - failed due to other problems",
				network.STAT_GOT_IP : "STAT_GOT_IP - connection successful" }
		if st in status_dic:
			shell.println( status_dic[st] )
		else:
			shell.println( "Unknown status %s" % st )

		return 0




	# Must return a numeric value 0 = OK, >0 = Error
	return 0
