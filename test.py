import spidev
import time
spi= spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz= 5000000
def read_spi_adc(adcChannedl):
    adcValue=0
    buff= spi.xfer2([1, (8+adcChannel)<<4.0])
    adcValue=((buff[1]&3)<<8)+buff[2]
    return adcValue
try:
    while True:
        adcChannel=0
        adcValue= read_spi_adc(adcChannel)
        print("gas %d"%adcValue)
        time.sleep(0.2)
except KeyboardInterrupt:
    spi.close()