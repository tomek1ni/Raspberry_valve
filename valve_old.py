#valve_old.py
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

sleepTime = .1
buttonPin = 18
lightPin = 22
relay1 = 23
relay2 =24
buttonState = 0

GPIO.setup(lightPin, GPIO.OUT)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True: # Run forever
    if GPIO.input(buttonPin) == 0:
        buttonState = 0
        GPIO.output(lightPin, 1)
        GPIO.output(relay1, 0)
        GPIO.output(relay2, 0)
    else:
        buttonState = 1
        GPIO.output(lightPin, 0)
        GPIO.output(relay1, 1)
        GPIO.output(relay2, 1)

    print("buttonState ", buttonState)
    print("buttonPin ", GPIO.input(buttonPin))
    sleep(.3)