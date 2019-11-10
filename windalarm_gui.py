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

from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import ttk
import os, subprocess, time, signal

CRED = '\033[91m'
CEND = '\033[0m'

sound=True
refresh_every_sec=20
alarm_trigger=25

if(os.system('which lynx > /dev/null')!=0):
		print('You must first install lynx with apt-get.')
		exit(0)

if(os.system('which spd-say > /dev/null')!=0):
	print('Audible alarm cannot be set. Please install spd-say with apt-get.')
	sound=False


def close_window():
  global running
  running = False
  print("\n\n WINDOW CLOSED BY USER")
  exit(0)

def sigint_handler(signum, frame):
	print('\n\n Stopped by user with CTRL+C')
	exit(0)
signal.signal(signal.SIGINT, sigint_handler)


def get_weather():
	lines=subprocess.check_output('lynx -dump http://tux.iar.unlp.edu.ar/~fede/tiempo.shtml',shell=True).decode("utf-8")
	return lines

print('Welcome to IAR wind service (press Ctrl+C to exit)')

window = Tk()
window.title("IAR wind PuMA")
window.configure(bg="black")
#window.geometry('250x40')
window.protocol("WM_DELETE_WINDOW", close_window)


lines=get_weather()
wind  = lines.split('\n')[8]
value = int(wind.split()[2])

if value>alarm_trigger:
	print(CRED+'\r{0}   -   ATTENTION HIGH WIND!!!            '.format(wind)+CEND,end='')
	lbl = Label(window, text="{0}   -   HIGH WIND!!!".format(wind), bg = "red", fg="white")
	if(sound): os.system('spd-say "ATTENTION PLEASE: WIND IS ABOVE 25 KILOMETERS PER HOUR"')
else:
	print('\r{0}   -   WIND IS FINE                      '.format(wind),end='')
	lbl = Label(window, text="{0}   -   WIND IS FINE   ".format(wind), fg="white", bg="black")

lbl.grid(column=0, row=0)

style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='black')
bar = Progressbar(window, length=200, style='black.Horizontal.TProgressbar')
bar['value'] = 0
bar.grid(column=0, row=1)

timezero=time.time()

running=True

while running:
	interval=time.time()-timezero

	if(interval > refresh_every_sec):
		timezero+=interval
		lines=get_weather()
		wind  = lines.split('\n')[8]
		value = int(wind.split()[2])

		if value>alarm_trigger:
			print(CRED+'\r{0}   -   ATTENTION HIGH WIND!!!            '.format(wind)+CEND,end='')
			lbl['text']="{0}   -   HIGH WIND!!!".format(wind)
			lbl['fg']="white"
			lbl['bg']="red"
			if(sound): os.system('spd-say "ATTENTION PLEASE: WIND IS ABOVE 25 KILOMETERS PER HOUR"')
		else:
			print('\r{0}   -   WIND IS FINE                      '.format(wind),end='')
			lbl['text']="{0}   -   WIND IS FINE   ".format(wind)
			lbl['fg']="white"
			lbl['bg']="black"

	bar['value'] = float(interval*100.)/refresh_every_sec
	time.sleep(1.0)
	window.update()
