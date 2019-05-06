#/usr/bin/python3
#
# Python script to access wind service from IAR
#
# Programmed by F. Garcia for PuMA Collaboration
# based on IAR weather service from Federico Bareilles
#
# lynx is needed to read web service
# spd-say is needed to enable audible alarm
#

import os, subprocess, time, signal

CRED = '\033[91m'
CEND = '\033[0m'

sound=True
refresh_every_sec=10

if(os.system('which lynx > /dev/null')!=0):
        print('You must first install lynx with apt-get.')
        exit(0)

if(os.system('which spd-say > /dev/null')!=0):
	print('Audible alarm cannot be set. Please install spd-say with apt-get.')
	sound=False

def sigint_handler(signum, frame):
    print('\n\nStopped by user with CTRL+C')
    exit(0)

signal.signal(signal.SIGINT, sigint_handler)


def get_weather():
	lines=subprocess.check_output('lynx -dump http://tux.iar.unlp.edu.ar/~fede/tiempo.shtml',shell=True).decode("utf-8")
	return lines

print('Welcome to IAR wind service (press Ctrl+C to exit)')

while(True):
	lines=get_weather()
	wind  = lines.split('\n')[8]
	value = int(wind.split()[2])

	if value>25:
		print(CRED+'\r{0}   -   ATTENTION HIGH WIND!!!            '.format(wind)+CEND,end='')
		if(sound): os.system('spd-say "ATTENTION PLEASE: WIND IS ABOVE 25 KILOMETERS PER HOUR"')
	else:
		print('\r{0}   -   WIND IS FINE                      '.format(wind),end='')

	time.sleep(refresh_every_sec)
