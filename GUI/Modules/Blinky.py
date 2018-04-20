import RPi.GPIO as GPIO

    
Luft = 29
Steg2 = 31
Steg1 = 33
Vann1 = 37
Vann2 = 35

GPIO.setmode(GPIO.BOARD)  # Adresser pinner etter nummer
GPIO.setup(Luft, GPIO.OUT)  # Set pinmode as output
GPIO.setup(Vann1, GPIO.OUT)  # Set pinmode as output
GPIO.setup(Vann2, GPIO.OUT)
GPIO.setup(Steg1, GPIO.OUT)
GPIO.setup(Steg2, GPIO.OUT)

def on_off(i, type):
    
    if i == 1:  # If input is 1 turn on LED
        GPIO.output(type, GPIO.HIGH)
        print(type, 'is on')
    else:  # else turn LED off
        GPIO.output(type, GPIO.LOW)
        print(type, 'is off')


