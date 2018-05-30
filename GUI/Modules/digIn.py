import RPi.GPIO as GPIO     # Importering av pakker
GPIO.setwarnings(False)     # Fjern ubruklige advarsler

DI0 = 36                    # Digital Inngang 0
DI1 = 38                    # Digital Inngang 1
DI2 = 40                    # Digital Inngang 2

GPIO.setmode(GPIO.BOARD)    # Adresser pinner etter nummer
GPIO.setup(DI0, GPIO.IN)    # Set pinmode as input
GPIO.setup(DI1, GPIO.IN)
GPIO.setup(DI2, GPIO.IN)

