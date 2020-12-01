# import Adafruit_DHT
import time
import sys
import datetime
# import RPi.GPIO as GPIO
# import spidev
from random import *
import socket

button = 18
HOST = "192.168.0.55"
PORT = 1626
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((HOST,PORT))

print('connection is success')
# sensor = Adafruit_DHT.DHT11

pin = 4

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
try:
    while True:
        dateTime = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        # h, t = Adafruit_DHT.read_retry(sensor, pin)
        h, t= 1, 1
        if h is not None and t is not None:
            print("start")
            t = randint(0, 100)
            h = randint(0, 100)
            print("Temperature = {0:0.1f}*C Humidity = {1:0.1f}%".format(t, h))
            time.sleep(0.1)
            data = [t, h, dateTime]
            msg = str(data)
            s.sendall(msg.encode()) # 소켓통신으로 data를 전송
            print('data successfully send')
        else:
            print("Read error")
            time.sleep(1)
except KeyboardInterrupt:
    print("Terminated by Keyboard")
    s.close()
    # GPIO.cleanup()

finally:
    print("End of Program")
    s.close()
    # GPIO.cleanup()
