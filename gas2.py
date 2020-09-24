import sys
import spidev
import wiringpi as w

CS_MCP3208 = 8
SPI_CHANNEL = 0
SPI_SPEED = 1000000
ADC_CHANNEL = 0

FAN_MT_P_PIN = 4
FAN_MT_N_PIN = 17
WARNING_LEVEL = 700


class gasLeakage:

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1000000
        self.setupWiringPiGpio()
        self.initMQ5()
        self.initFan()

    def setupWiringPiGpio(self):
        if w.wiringPiSetupGpio() == -1:
            print("[ERROR] Error in wiringSetupGpio")
            sys.exit(1)

    def getSensorData(self):
        SensingVal = self.readMQ5(ADC_CHANNEL)

        return SensingVal

    def controlFan(self, sensorValue):
        if sensorValue >= WARNING_LEVEL:
            self.FanOn()
        else:
            self.FanOff()

    def initFan(self):
        print("[DEBUG] Fan Initialize")
        w.pinMode(FAN_MT_P_PIN, 1)
        w.pinMode(FAN_MT_N_PIN, 1)
        self.FanOff()

    def FanOn(self):
        w.digitalWrite(FAN_MT_P_PIN, 1)
        w.digitalWrite(FAN_MT_N_PIN, 0)

    def FanOff(self):
        w.digitalWrite(FAN_MT_P_PIN, 0)
        w.digitalWrite(FAN_MT_N_PIN, 0)

    def readMQ5(self, nAdcChannel):
        nAdcValue = self.ReadMcp3208ADC(nAdcChannel)

        return nAdcValue

    def ReadMcp3208ADC(self, adcChannel):

        w.digitalWrite(CS_MCP3208, 0)
        nAdcValue = self.spi.xfer2([1, (8 + adcChannel) << 4, 0])
        nAdcValue = ((nAdcValue[1] & 3) << 8) + nAdcValue[2]

        w.digitalWrite(CS_MCP3208, 1)

        return nAdcValue

    def initMQ5(self):
        if w.wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED) == -1:
            print("[ERROR] Error in wiringPiSPISetup")
            sys.exit(1)

        print("[DEBUG] MQ-5 Initialization")
        w.pinMode(CS_MCP3208, 1)