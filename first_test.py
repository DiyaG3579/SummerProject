import RPi.GPIO as GPIO
import time
import argparse
from picamera2 import Picamera2
import cv2
import numpy as np
import math

GPIO.setmode(GPIO.BOARD)
r = 11
g = 12
b = 13
r2 = 15
g2 = 16
b2 = 18
GPIO.setup(r, GPIO.OUT)
GPIO.setup(g, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)
GPIO.setup(r2, GPIO.OUT)
GPIO.setup(g2, GPIO.OUT)
GPIO.setup(b2, GPIO.OUT)
GPIO.output(r, GPIO.LOW)
GPIO.output(g, GPIO.LOW)
GPIO.output(b, GPIO.LOW)
GPIO.output(r2, GPIO.LOW)
GPIO.output(g2, GPIO.LOW)
GPIO.output(b2, GPIO.LOW)
#parser = argparse.ArgumentParser()
#parser.add_argument("--tim", type = float, default = 8.5, help = "Time to Run")
#parser.add_argument("--low", type=float, default=4, help="Lower Bound Duty Cycle")
#parser.add_argument("--upp", type=float, default=10, help="Upper Bound Duty Cycle")
#parser.add_argument("--debug", default = False, help="Enable debug mode")
#args = parser.parse_args()

#start_time = time.time()

# Define pin, frequency and duty cycle
blue = False
PWM_pin   = 36 
freq      = 45

GPIO.setup(PWM_pin, GPIO.OUT)
#elapsed = time.time() - start_time

# Create PWM instance for pin w freqency
pwm = GPIO.PWM(PWM_pin, freq) 
pwm.start(7.0)
time.sleep(10.0)

pwm.ChangeDutyCycle(7.0)
time.sleep(1.0)
pwm.ChangeDutyCycle(11.5)
time.sleep(2.0)
camera = Picamera2()
camera.start()
camera.capture_file('first_test.jpg')
pwm.ChangeDutyCycle(7.0)
time.sleep(1.0)


img = cv2.imread("mask_test.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (95, 150, 150), (140, 255,255))
cv2.imwrite('mask_.jpg', mask)
mask_blur = cv2.blur(mask,(5,5))
cv2.imwrite('mask_blur.jpg',mask_blur)
thresh = cv2.threshold(mask_blur, 200, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('blue_tape_thresh.jpg', thresh)

M = cv2.moments(thresh)

if (M["m00"] != 0.0):
    blue = True

if blue:
    GPIO.output(r, GPIO.HIGH)
    GPIO.output(r2, GPIO.HIGH)
    time.sleep(2.0)
    GPIO.output(r, GPIO.LOW)
    GPIO.output(r2, GPIO.LOW)

pwm.stop()
GPIO.cleanup()
