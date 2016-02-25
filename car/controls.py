#!/usr/bin/python

import os

def init():
	os.system("echo 45 > /sys/class/gpio/export") 			#pin H-Bridge PB13
	os.system("echo out > /sys/class/gpio/pioB13/direction") 	#pin H-Bridge PB13
	os.system("echo 46 > /sys/class/gpio/export") 			#pin H-Bridge PB14
	os.system("echo out > /sys/class/gpio/pioB14/direction")	#pin H-Bridge PB14
	os.system("echo 95 > /sys/class/gpio/export") 			#pin Servo PC31
	os.system("echo out > /sys/class/gpio/pioC31/direction")	#pin Servo PC31
	os.system("echo 1 > /sys/class/gpio/pioC31/value")		#pin Servo PC31
	os.system("echo 0 > /sys/class/pwm/pwmchip0/export")		#pwm Servo
	os.system("echo 1000000 > /sys/class/pwm/pwmchip0/pwm0/period") #pwm Servo
	os.system("echo 1 > /sys/class/pwm/pwmchip0/export") 		#pwm Motor
	os.system("echo 1000000 > /sys/class/pwm/pwmchio0/pwm1/period") #pwm Motor

def motor(speed,deadzone):
	if speed > deadzone:
		os.system("echo 1 > /sys/class/gpio/pioB13/value")
		os.system("echo 0 > /sys/class/gpio/pioB14/value")
		os.system("echo "+str(int(speed/32768.0*1000000))+" > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
		os.system("echo 1 > /sys/class/pwm/pwmchip0/pwm1/enable")
	elif speed < deadzone*-1:
		os.system("echo 0 > /sys/class/gpio/pioB13/value")
		os.system("echo 1 > /sys/class/gpio/pioB14/value")
		os.system("echo "+str(int(speed/32768.0*1000000*-1))+" > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
		os.system("echo 1 > /sys/class/pwm/pwmchip0/pwm1/enable")
	else:
		os.system("echo 0 > /sys/class/gpio/pioB13/value")
		os.system("echo 0 > /sys/class/gpio/pioB14/value")

def steer(pos,deadzone):
	if (pos > deadzone) or (pos < deadzone*-1):
		os.system("echo "+str(int(pos/32768.0*1000000))+" > /sys/class/pwm/pwmchip0/pwm0/duty_cycle")
	else:
		os.system("echo 500000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle")

if __name__ == "__main__":
	import curses
	import time
	stdscr = curses.initscr()
	curses.cbreak()
	curses.noecho()
	curses.curs_set(0)
	stdscr.keypad(1)
	key=''
	while key != 27:
		key = stdscr.getch()
		if key == curses.KEY_UP:
			motor(32768,0)
			time.sleep(1000)
			motor(0,0)
		elif key == curses.KEY_DOWN:
			motor(-32768,0)
			time.sleep(1000)
			motor(0,0)
		elif key == curses.KEY_LEFT:
			steer(-32768,0)
			time.sleep(1000)
			steer(0,0)
		elif key == curses.KEY_RIGHT:
			steer(32768,0)
			time.sleep(1000)
			steer(0,0)
		elif key == curses.KEY_ENTER:
			spd = 0
			while spd <= 32768:
				spd +=1
				motor(spd,0)
			while spd >= -32768:
				spd -=1
				motor(spd,0)
			motor(0,0)
			spd = 0
			while spd <= 32760:
				spd += 10
				steer(spd,1000)
			while spd >= -32780:
				spd -=10
				steer(spd,1000)
			steer(0,0)
			spd = 0
	curses.endwin()
