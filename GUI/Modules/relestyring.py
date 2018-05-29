import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import time
    
Luft = 7
Steg2 = 11
Steg1 = 13
Vann1 = 15
Vann2 = 29

DO0 = 37        # Digital Utgang 0, GPIO 26
DO1 = 33        # Digital Utgang 1, GPIO 13
DO2 = 31        # Digital Utgang 2, GPIO 06
DO3 = 29        # Digital Utgang 3, GPIO 05
DO4 = 15        # Digital Utgang 4, GPIO 22
DO5 = 13        # Digital Utgang 5, GPIO 27
DO6 = 11        # Digital Utgang 6, GPIO 17
DO7 = 7         # Digital Utgang 7, GPIO 04


GPIO.setmode(GPIO.BOARD)  # Adresser pinner etter nummer
GPIO.setup(Luft, GPIO.OUT)  # Set pinmode as output
GPIO.setup(Vann1, GPIO.OUT)  # Set pinmode as output    #Denne er lengst nede i brønnen
GPIO.setup(Vann2, GPIO.OUT)                             #Denne er nærmest lansen
GPIO.setup(Steg1, GPIO.OUT)
GPIO.setup(Steg2, GPIO.OUT)

GPIO.setmode(GPIO.BOARD)    # Adresser pinner etter nummer
GPIO.setup(DO0, GPIO.OUT)   # Definerer de aktuelle pinnene som utganger
GPIO.setup(DO1, GPIO.OUT)
GPIO.setup(DO2, GPIO.OUT)
GPIO.setup(DO3, GPIO.OUT)
GPIO.setup(DO4, GPIO.OUT)
GPIO.setup(DO5, GPIO.OUT)
GPIO.setup(DO6, GPIO.OUT)
GPIO.setup(DO7, GPIO.OUT)

def on_off(i, type):
    
    if i == 1:                          # If input is 1 turn on LED
        GPIO.output(type, GPIO.HIGH)
        print(type, 'is on')
    else:                               # else turn LED off
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
