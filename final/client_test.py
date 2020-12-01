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
import Adafruit_DHT
import RPi.GPIO as GPIO
import numpy as np
from mq import *
from ctypes import *
import collections
import pickle
from gpiozero import LED
""" This class defines a C-like struct """
class Payload(Structure):
    _fields_ = [("lpg", c_float),
                ("co", c_float),
                ("smoke", c_float)]



def make_anmaly_data(n, t, h, gas):
    start_range= 5
    end_range= 10
    if n == 1:
        gas = gas + np.random.randint(start_range, end_range)
    elif n == 2:
        h = h + np.random.randint(start_range, end_range)
    elif n ==3:
        h = h + np.random.randint(start_range, end_range)
        gas = gas + np.random.randint(start_range, end_range)
    elif n ==4:
        t = t + np.random.randint(start_range, end_range)
        
    elif n ==5:
        t = t + np.random.randint(start_range, end_range)
        gas = gas + np.random.randint(start_range, end_range)
    elif n ==6:
        t = t + np.random.randint(start_range, end_range)
        h = h + np.random.randint(start_range, end_range)
    elif n==7:
        t = t + np.random.randint(start_range, end_range)
        h = h + np.random.randint(start_range, end_range)
        gas = gas + np.random.randint(start_range, end_range)
    
    return t, h, gas

def main():
    server_addr = ("192.168.0.55",8080)
    #server_addr = ('185.244.128.27', 2300)
    
    sensor = Adafruit_DHT.DHT11
    pin = 4
    button = 5
    period=1
    final=[]
    red_led= LED(20)
    green_led= LED(16)
    yellow_led= LED(12)
    red_led.off()
    green_led.off()
    yellow_led.off()
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
        
        while(1):
            inputIO = GPIO.input(button)
            now = datetime.datetime.now()
            dateTime = now.strftime('%Y-%m-%d %H:%M:%S')
            h, t = Adafruit_DHT.read_retry(sensor, pin)
            
            if inputIO == True:
                print("inputIO : %g" % inputIO)
                if h is not None and t is not None:
                    print("period: %g"% period)
                    temp_hum_data = [dateTime, t, h]
                    perc = mq.MQPercentage()
                    gas= perc["GAS_LPG"]
                    abnormal_state=0
                    if period % 10 == 0:
                        abnormal_state = np.random.randint(1,8)
                        t, h, gas = make_anmaly_data(abnormal_state, t, h, payload_out.lpg)
                    print("Temperature = {0:0.1f}*C Humidity = {1:0.1f}%".format(t, h))
                    temp_hum_data = [dateTime, t, h]
                    perc = mq.MQPercentage()
                    print("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm, Label: %g\n" % (gas, perc["CO"], perc["SMOKE"], abnormal_state))
                    time.sleep(1)
                    payload_out = Payload(gas, perc["CO"], perc["SMOKE"])
                    gas_data = [dateTime, payload_out.lpg, payload_out.co, payload_out.smoke]
                    # print ("Sending LPG=%f ppm, CO=%f, SMOKE=%f" % (payload_out.lpg, payload_out.co, payload_out.smoke))
                    obj=collections.OrderedDict()
                    obj['Time']=dateTime
                    obj['temparature']=t
                    obj['humidity']=h
                    obj['LPG']=gas
                    obj['label']=abnormal_state
                    period+=1
                    datajson=json.dumps(obj, sort_keys=True)
                    
                else:
                    print('read error')
                time.sleep(1)
            else:
                if h is not None and t is not None:
                    print("inputIO : %g" % inputIO)
                    
                    abnormal_state = np.random.randint(1,8)
                    t, h, gas = make_anmaly_data(abnormal_state, t, h, payload_out.lpg)
                    print("Temperature = {0:0.1f}*C Humidity = {1:0.1f}%".format(t, h))
                    temp_hum_data = [dateTime, t, h]
                    perc = mq.MQPercentage()
                    print("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm, Label: %g\n" % (gas, perc["CO"], perc["SMOKE"], abnormal_state))
                    time.sleep(1)
                    
                    payload_out = Payload(gas, perc["CO"], perc["SMOKE"])
                  
                    obj=collections.OrderedDict()
                    obj['Time']=dateTime
                    obj['temparature']=t
                    obj['humidity']=h
                    obj['LPG']=gas
                    obj['label']=abnormal_state
                    period+=1
                    datajson=json.dumps(obj, sort_keys=True)
                else:
                    print('read error')
                time.sleep(1)
            s.sendall(datajson.encode())
            final= s.recv(2048)
            data = final.decode()
            if data=='send':
                continue
            else:
                data_label = list(map(int, data.split(" ")))
                print(data_label)
                for i in data_label:
                    if i ==1:
                        yellow_led.on()
                        time.sleep(0.5)
                        yellow_led.off()
                    elif i==2:
                        green_led.on()
                        time.sleep(0.5)
                        green_led.off()
                    elif i==3:
                        yellow_led.on()
                        green_led.on()
                        time.sleep(0.5)
                        yellow_led.off()
                        green_led.off()
                    elif i==4:
                        red_led.on()
                        time.sleep(0.5)
                        red_led.off()
                    elif i==5:
                        red_led.on()
                        yellow_led.on()
                        time.sleep(0.5)
                        red_led.off()
                        yellow_led.off()
                    elif i==6:
                        red_led.on()
                        green_led.on()
                        time.sleep(0.5)
                        red_led.off()
                        green_led.off()
                    elif i==7:
                        red_led.on()
                        green_led.on()
                        yellow_led.on()
                        time.sleep(0.5)
                        red_led.off()
                        green_led.off()
                        yellow_led.off()
                    else: continue
                
            print(data)
    except KeyboardInterrupt:
        print('Terminated by Keyboard')
        s.close()
    finally:
        print ("Closing socket")
        s.close()

if __name__ == "__main__":
    main()

