import RPi.GPIO as GPIO

GPIO.setwarnings(False)

PWM0 = 16
PWM1 = 26

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PWM0, GPIO.OUT)
GPIO.setup(PWM1, GPIO.OUT)

p = GPIO.PWM(PWM0, 100)  # (channel, freq)
p.start(0)  # duty cycle [0 - 100]

