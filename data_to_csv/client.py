#!/usr/bin/env python

""" client.py - Echo client for sending/receiving C-like structs via socket

References:
- Ctypes fundamental data types: https://docs.python.org/2/library/ctypes.html#ctypes-fundamental-data-types-2
- Ctypes structures: https://docs.python.org/2/library/ctypes.html#structures-and-unions
- Sockets: https://docs.python.org/2/howto/sockets.html
"""


import sys
import json
import socket
import random
import datetime
#import Adafruit_DHT
import RPi.GPIO as GPIO
import numpy as np
from mq import *
from ctypes import *
""" This class defines a C-like struct """
class Payload(Structure):
    _fields_ = [("lpg", c_float),
                ("co", c_float),
                ("smoke", c_float)]

def make_anmaly_data(n, t, h, gas):
    
    if n == 1:
        t = t + np.random.randint(30)
    elif n == 2:
        h = h + np.random.randint(30)
    elif n ==3:
        gas = gas + np.random.randint(30)
    elif n ==4:
        t = t + np.random.randint(30)
        h = h + np.random.randint(30)
    elif n ==5:
        h = h + np.random.randint(30)
        gas = gas + np.random.randint(30)
    elif n==6:
        t = t + np.random.randint(30)
        h = h + np.random.randint(30)
        gas = gas + np.random.randint(30)
    
    return t, h, gas

def main():
    server_addr = ("192.168.0.55",8080)
    # server_addr = ('185.244.128.27', 2300)
    
    #sensor = Adafruit_DHT.DHT11
    pin = 4
    button = 5
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s < 0:
        print("Error creating socket")

    try:
        s.connect(server_addr)
        print ("Connected to %s" % repr(server_addr))
    except:
        print ("ERROR: Connection to %s refused" % repr(server_addr))
        sys.exit(1)

    try:
        mq = MQ();
        # for i in range(10):
        #file_path = "./data.json"
        while(1):
            inputIO = GPIO.input(button)
            now = datetime.datetime.now()
            dateTime = now.strftime('%Y-%m-%d %H:%M:%S')
            #dateTime = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
            #h, t = Adafruit_DHT.read_retry(sensor, pin)
            h=np.random.randint(0, 100)
            t=np.random.randint(0, 100)
            print("Temperature = {0:0.1f}*C Humidity = {1:0.1f}%".format(t, h))
            temp_hum_data = [dateTime, t, h]
            perc = mq.MQPercentage()
            print("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm\n" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
            time.sleep(1)
            payload_out = Payload(perc["GAS_LPG"], perc["CO"], perc["SMOKE"])
            gas_data = [dateTime, payload_out.lpg, payload_out.co, payload_out.smoke]
            print ("Sending LPG=%f ppm, CO=%f, SMOKE=%f" % (payload_out.lpg, payload_out.co, payload_out.smoke))
            
            data ={
                    "Time": dateTime,
                    "temparature": t,
                    "humidity": h,
                    "LPG": payload_out.lpg
                    }
            datajson=json.dumps(data)
            
            '''
            nsent = s.send(payload_out)
            # Alternative: s.sendall(...): coontinues to send data until either
            # all data has been sent or an error occurs. No return value.

            print "Sent %d bytes" % nsent

            buff = s.recv(sizeof(Payload))
            payload_in = Payload.from_buffer_copy(buff)
            print "Received LPG=%f ppm, CO=%f, SMOKE=%f" % (payload_in.lpg, payload_in.co, payload_in.smoke)
            '''
            #if inputIO == false:
            s.sendall(datajson.encode())
            #else:
            #  n = np.random.randint(6)
             #   t, h, gas = make_anomaly_data(n, t, h, payload_out.lpg)
              #  data ={
                  #  "Time": dateTime,
                   # "temparature": t,
                    #"humidity": h,
                    #"LPG": gas
                    #}
                #datajson=json.dumps(data)
                #s.sendall(datajson.encode())
    finally:
        print ("Closing socket")
        s.close()

if __name__ == "__main__":
    main()
