import pigpio  # Importerer pigpio biblioteket

def hpwm(freq,dcycle):                  # Funksjon tar inn frekvens og dutycycle
    pi = pigpio.pi()
    pi.hardware_PWM(18, freq, dcycle)   # Starter hardware PWM på GPIO 18
