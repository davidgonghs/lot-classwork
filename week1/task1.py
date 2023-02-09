import RPi.GPIO as GPIO
import time

#test 1
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
print("LED on")

GPIO.output(18,GPIO.HIGH)
time.sleep(2)
print("LED off")
GPIO.output(18,GPIO.LOW)

#test 2
# while (1):
#     x = raw_input()
#     if x == 'o':
#         print("LED ON")
#
#     elif x == 'f':
#         print("LED OFF")
#
#     else:
#         print("No Action")

#test 3
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
#
# GPIO.setup(10,GPIO.IN)
#
# while True:
#     if GPIO.input(10):
#         print("Button Pressed")
#     else:
#         print("Button Released")


#own task
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(10,GPIO.IN)
GPIO.setup(9,GPIO.OUT)

while True:
    if GPIO.input(10):
        print("Button Pressed")
        print("LED on")
        GPIO.output(9,GPIO.HIGH)
        time.sleep(5)
    else:
        print("Button Released")
        print("LED OFF")
        GPIO.output(9, GPIO.LOW)
        time.sleep(5)
