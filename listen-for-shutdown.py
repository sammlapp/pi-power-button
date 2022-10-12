#!/usr/bin/env python3
"""this script listenes for a shutdown command (3 second hold of power button)

it shuts down the pi if and only if there are no external drives mounted at /media/pi
when the shutdown button command is recieved.

The error LED blinks 10 times rapidly if shutdown was aborted due to mounted drives.
"""

import RPi.GPIO as GPIO
import subprocess
from datetime import datetime
from pathlib import Path
from gpiozero import Button, LED
from time import sleep
import os

sleep_time = 0.1 #run loop 10x/sec
button_hold_time = 3 #require 3 second hold to shut down pi
power_button = Button(3, hold_time=3)
status_led = LED(18)
progress_led = LED(27)
error_led = LED(22)

def blink_error():
    """send 10 rapid blinks in succession"""
    for i in range(10):
        error_led.on()
        sleep(0.1)
        error_led.off()
        sleep(0.1)

def blink_shutting_down():
    """blink all 3 LEDs 5x indicating the devices is shutting down"""
    for i in range(5):
        error_led.on()
        status_led.on()
        progress_led.on()
        sleep(0.3)
        error_led.off()
        status_led.off()
        progress_led.off()
        sleep(0.3)

def shutdown():
    """attempts shutdown
    - if any external drives mounted, does not shutdown
    - returns True if shutdown happens, false otherwise """
    # if any external drives are mounted, do not shut down
    num_external_drives = len(os.listdir('/media/pi'))
    if num_external_drives>0:
        # do not shut down. 
        # add event to the log.
        with open('/home/pi/shutdown_log.txt','a+') as f:
            f.write(f'{datetime.now()}: Shutdown blocked due to mounted drives.\n')
        
        # flash error light 10x fast as a warning
        blink_error()

        return False

    else: #shutdown
        #blink all 3 LEDs 
        blink_shutting_down()

        # write to log file
        with open('/home/pi/shutdown_log.txt','a+') as f:
            f.write(f'{datetime.now()}: Shutting down.\n')
        
        # force shutdown
        subprocess.call(['sudo','shutdown', '-h', 'now'], shell=False)

        return True

shutting_down = False
while not shutting_down:
    sleep(sleep_time)
    if power_button.is_held:
        shutting_down =  shutdown()