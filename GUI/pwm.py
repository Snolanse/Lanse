# import RPi.GPIO as GPIO
import pigpio

def hpwm(freq,dcycle):
    pi = pigpio.pi()
    pi.hardware_PWM(18, freq, dcycle)

# sudo pigpiod
#

'''
GPIO.setwarnings(False)

PWM0 = 16
PWM1 = 26

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PWM0, GPIO.OUT)
GPIO.setup(PWM1, GPIO.OUT)

p = GPIO.PWM(PWM0, 100)  # (channel, freq)
p.start(0)  # duty cycle [0 - 100]

while 1:                               #execute loop forever

    for x in range (50):                          #execute loop for 50 times, x being incremented from 0 to 49.
        p.ChangeDutyCycle(x)               #change duty cycle for varying the brightness of LED.
        time.sleep(0.1)                           #sleep for 100m second

    for x in range (50):                         #execute loop for 50 times, x being incremented from 0 to 49.
        p.ChangeDutyCycle(50-x)        #change duty cycle for changing the brightness of LED.
        time.sleep(0.1)                          #sleep for 100m second
'''


