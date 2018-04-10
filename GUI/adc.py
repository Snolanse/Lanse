import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time

class adc():
    def __init__(self):
        self.mcp = Adafruit_MCP3008.MCP3008(clk=18, cs=25, miso=23, mosi=24)

    def lesADC(self,channel):
        #doshit
        verdi = self.mcp.read_adc(channel)
        return verdi
