#valve_reverse.py
# U.S. Solid Motorized Ball Valve- 1/2” 15mm, 2 Wire Reverse Polarity USS-MSV00012 SKU:JFMSV00012
# Valve connected to two channel relay in reverse polarity setup powered by 12V DC.
# Two buttons on the breadboard (green and yellow). The green (GPIO18) opens the valve, yellow (GPIO16) closes.
# While button held down valve continuously opens/closes until released. One short tap on a button powers the 
# valve for 4 seconds making it fully open/close. One more press on either button interrupts 'exit.wait (4)' 
# statement and stops valve from actuating. Within one second after last interrupt event and if the variable
# 'susp_auto' is set to '1' the 'exit.wait (4)' isn't available. It suppose to prevent situation when after one
# interrupt event valve goes directly into an other full close/open cycle.

import RPi.GPIO as GPIO
import board
from threading import Event
from time import time

buttonPin1 = 18 # Green button - open
buttonPin2 = 16 # Yellow button - close
relay1 = 23
relay2 = 19
exit = Event ()
susp_auto = 0
susp_start = time ()

GPIO.setup (relay1, GPIO.OUT)
GPIO.setup (relay2, GPIO.OUT)
GPIO.setup (buttonPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup (buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def quick_press ():                         # Function is executed after short tap on one of the buttons
    global susp_auto
    susp_stop = time ()
    if ((susp_stop - susp_start) > 1) & (susp_auto == 0): 
        GPIO.add_event_detect (buttonPin1, GPIO.FALLING, callback=button_callback, bouncetime=50)
        GPIO.add_event_detect (buttonPin2, GPIO.FALLING, callback=button_callback, bouncetime=50)
        exit.wait (4)
        GPIO.remove_event_detect (buttonPin1)
        GPIO.remove_event_detect (buttonPin2)
    elif ((susp_stop - susp_start) > 1) & (susp_auto == 1):
        susp_auto = 0
    exit.clear ()

def button_callback (channel):              # Function executed after button interrupt event in quick_press()
    global susp_auto
    exit.set()
    susp_auto = 1
    global susp_start
    susp_start = time ()

def reset_relays ():                        # Function deenergizing the valve
    GPIO.output (relay1, 1)
    GPIO.output (relay2, 0)
    
reset_relays()

while True: # Run forever
    if (GPIO.input (buttonPin1) == False) or (GPIO.input (buttonPin2) == False):
        start_press = time ()
        while GPIO.input (buttonPin1) == False:
            GPIO.output (relay1, 0)
            GPIO.output (relay2, 0)
        while GPIO.input (buttonPin2) == False:
            GPIO.output (relay1, 1)
            GPIO.output (relay2, 1)
        end_press = time ()
        if end_press - start_press < 0.15:
            quick_press ()
        reset_relays ()