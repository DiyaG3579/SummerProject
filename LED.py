import RPi.GPIO as GPIO
import time

#Intial setup and defining all the pins
GPIO.setmode(GPIO.BOARD)
r = 11
g = 12
b = 13
r2 = 15
g2 = 16
b2 = 18

#Actual setup for the PI and starting them all as off
GPIO.setup(r, GPIO.OUT)
GPIO.setup(g, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)
GPIO.output(r, GPIO.LOW)
GPIO.output(g, GPIO.LOW)
GPIO.output(b, GPIO.LOW)

#Now it gets fun - lighting them up

GPIO.output(r, GPIO.HIGH)
time.sleep(1)
GPIO.output(g, GPIO.HIGH)
time.sleep(1)
GPIO.output(r, GPIO.LOW)
time.sleep(1)
GPIO.output(b, GPIO.HIGH)
time.sleep(1)
GPIO.output(g, GPIO.LOW)
time.sleep(1)
GPIO.output(r, GPIO.HIGH)
time.sleep(1)
GPIO.output(g, GPIO.HIGH)
time.sleep(1)


GPIO.cleanup()