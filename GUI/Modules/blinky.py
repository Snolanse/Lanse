import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import time
    
Luft = 7
Steg2 = 11
Steg1 = 13
Vann1 = 15
Vann2 = 33

GPIO.setmode(GPIO.BOARD)  # Adresser pinner etter nummer
GPIO.setup(Luft, GPIO.OUT)  # Set pinmode as output
GPIO.setup(Vann1, GPIO.OUT)  # Set pinmode as output    #Denne er lengst nede i brønnen
GPIO.setup(Vann2, GPIO.OUT)                             #Denne er nærmest lansen
GPIO.setup(Steg1, GPIO.OUT)
GPIO.setup(Steg2, GPIO.OUT)

def on_off(i, type):
    
    if i == 1:  # If input is 1 turn on LED
        GPIO.output(type, GPIO.HIGH)
        print(type, 'is on')
    else:  # else turn LED off
        GPIO.output(type, GPIO.LOW)
        print(type, 'is off')

def avslutt():
    GPIO.cleanup()

def stengVann():
    GPIO.output(Vann2,GPIO.LOW)
    GPIO.output(Luft,GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(Vann1,GPIO.LOW)

def startVann():
    GPIO.output(Luft,GPIO.HIGH)
    GPIO.output(Vann2,GPIO.HIGH)
    GPIO.output(Vann1,GPIO.HIGH)
