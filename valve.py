#valve.py
import RPi.GPIO as GPIO
import numpy as np
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep

GPIO.setwarnings(False)         # Ignore warning for now
GPIO.setmode(GPIO.BCM)

sleepTime = .1
buttonPin = 18
lightPin = 22
relay1 = 23
relay2 = 24
buttonState = False
buttonPrev = False
valveState = False


i2c = busio.I2C(board.SCL, board.SDA)       # Create the I2C bus
ads = ADS.ADS1015(i2c)                      # Create the ADC object using the I2C bus
chan = AnalogIn(ads, ADS.P1)                # Create single-ended input on channel 3

GPIO.setup(lightPin, GPIO.OUT)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True: # Run forever
    while GPIO.input(buttonPin) == False:   #While the button is pressed
        buttonState = not buttonPrev
    if buttonState != buttonPrev or chan.value < 20000:
        if valveState == True or chan.value < 20000:              # 
            GPIO.output(relay1, 1)          # Close the valve
            GPIO.output(lightPin, 0)        # Turn the LED off
            valveState = False              # Assign opened state to the valve state value
        else:
            GPIO.output(relay1, 0)          # Open the valve
            GPIO.output(lightPin, 1)        # Turn the LED on
            valveState = True               # Assign opened state to the valve state value
        buttonPrev = buttonState

    print("buttonState", buttonState)
    print("buttonPrev", buttonPrev)
    print("moisture level: ", chan.value, chan.voltage)
    sleep(.2)