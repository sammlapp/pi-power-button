#!/usr/bin/env python


import RPi.GPIO as GPIO
import subprocess


GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(3, GPIO.FALLING)

# remove any drives from /media/pi/
subprocess.call('sudo rm -rf /media/pi/*', shell=True)
# shut down the rpi
subprocess.call(['sudo','shutdown', '-h', 'now'], shell=False)
