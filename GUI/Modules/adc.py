import Adafruit_GPIO.SPI as SPI
from Modules.MCP3008 import MCP3008

# Software SPI
# CLK  = 18
# MISO = 23
# MOSI = 24
# CS   = 25
# mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def lesADC(channel):
    verdi = mcp.read_adc(channel)
    return verdi
