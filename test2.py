import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)

is_running = True

GPIO.setup(23, GPIO.IN)  # 센서 입력

GPIO.setup(25, GPIO.OUT)  # LED

try:

    while is_running:

        if GPIO.input(23) == 1:

            GPIO.output(25, GPIO.HIGH)  # LED ON

            print("on")

        else:

            GPIO.output(25, GPIO.LOW)  # LED OFF

            print("off")

except KeyboardInterrupt:

    GPIO.cleanup()
    00

    is_running = False