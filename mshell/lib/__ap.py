""" MiniShell wifi command for access point mode. """

import time, binascii

def ap( shell, args ):
	# All input should be made via the shell
	try:
		import network
	except:
		shell.println( 'No network support!' )
		return -1

	sCmd = '' if len(args)==0 else args[0].upper()
	ap = network.WLAN( network.AP_IF )

	if sCmd=='UP':
		if not ap.active():
			shell.println('Going up')
			ap.active(True)
		else:
			shell.println('Already up!')
		return 0
	elif sCmd=='DOWN':
		if ap.active():
			shell.println('Going down')
			ap.active(False)
		else:
			shell.println('Already down!')
		return 0
	else:
		st = ap.status()
		shell.println( '%r' % ap )
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
