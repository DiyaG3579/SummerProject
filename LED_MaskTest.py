import cv2
import numpy as np
import math
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time

blue = False

GPIO.setmode(GPIO.BOARD)
r = 11
g = 12
b = 13
GPIO.setup(r, GPIO.OUT)
GPIO.setup(g, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)
GPIO.output(r, GPIO.LOW)
GPIO.output(g, GPIO.LOW)
GPIO.output(b, GPIO.LOW)


camera = Picamera2()
camera.start()
camera.capture_file('mask_test.jpg')

img = cv2.imread("mask_test.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(hsv, (95, 150, 150), (140, 255,255))
cv2.imwrite('mask.jpg', mask)
mask_blur = cv2.blur(mask,(5,5))
cv2.imwrite('mask_blur.jpg',mask_blur)
thresh = cv2.threshold(mask_blur, 200, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('blue_tape_thresh.jpg', thresh)

M = cv2.moments(thresh)

if (M["m00"] != 0.0):
    blue = True

if blue:
    GPIO.output(b, GPIO.HIGH)
    time.sleep(2)

GPIO.cleanup()