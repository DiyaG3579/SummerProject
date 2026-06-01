import cv2
import numpy as np
import math
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time

red= False
yellow = False
green = False
cyan = False
blue = False
purple = False

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


camera = Picamera2()
camera.start()
camera.capture_file('mask_test.jpg')

img = cv2.imread("mask_test.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_red1 = np.array([0, 180, 150])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 180, 150])
upper_red2 = np.array([180, 255, 255])
mask1r = cv2.inRange(hsv, lower_red1, upper_red1)
mask2r = cv2.inRange(hsv, lower_red2, upper_red2)
maskRed = mask1r + mask2r
mask_blurRed = cv2.blur(maskRed,(5,5))
threshR = cv2.threshold(mask_blurRed, 200, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('testingMaskRed.jpg', threshR)

maskYellow = cv2.inRange(hsv, (20, 180, 180), (35, 255,255))
mask_blurYellow = cv2.blur(maskYellow,(5,5))
threshY = cv2.threshold(mask_blurYellow, 200, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('testingMaskYellow.jpg',threshY)

maskGreen = cv2.inRange(hsv, (41, 150, 80), (75, 255, 210))
mask_blurGreen = cv2.blur(maskGreen,(5,5))
threshG = cv2.threshold(mask_blurGreen, 200, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('testingMaskGreen.jpg', threshG)

maskCyan = cv2.inRange(hsv, (85, 120, 150), (104, 255, 255))
mask_blurCyan = cv2.blur(maskCyan,(5,5))
threshC = cv2.threshold(mask_blurCyan, 200, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('testingMaskCyan.jpg', threshC)

maskBlue = cv2.inRange(hsv, (105, 150, 100), (125, 255, 220))
mask_blurBlue = cv2.blur(maskBlue,(5,5))
threshB= cv2.threshold(mask_blurBlue, 200, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('testingMaskBlue.jpg', threshB)

maskPurple = cv2.inRange(hsv, (125, 80, 80), (155, 220, 200))
mask_blurPurple = cv2.blur(maskPurple,(5,5))
threshP = cv2.threshold(mask_blurPurple, 200, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('testingMaskPurple.jpg', threshP)


M_R = cv2.moments(threshR)
M_Y = cv2.moments(threshY)
M_G = cv2.moments(threshG)
M_C = cv2.moments(threshC)
M_B = cv2.moments(threshB)
M_P = cv2.moments(threshP)

if (M_R["m00"] != 0.0):
    red = True

if (M_Y["m00"] != 0.0):
    yellow = True

if (M_G["m00"] != 0.0):
    green = True

if (M_C["m00"] != 0.0):
    cyan = True

if (M_B["m00"] != 0.0):
    blue = True

if (M_P["m00"] != 0.0):
    purple = True

if blue:
    GPIO.output(b, GPIO.HIGH)
    GPIO.output(b2, GPIO.HIGH)
    time.sleep(2)

if red:
    GPIO.output(r, GPIO.HIGH)
    GPIO.output(r2, GPIO.HIGH)
    time.sleep(2)

if yellow:
    GPIO.output(r, GPIO.HIGH)
    GPIO.output(r2, GPIO.HIGH)
    GPIO.output(g, GPIO.HIGH)
    GPIO.output(g2, GPIO.HIGH)
    time.sleep(2)

if green:
    GPIO.output(g, GPIO.HIGH)
    GPIO.output(g2, GPIO.HIGH)
    time.sleep(2)

if purple:
    GPIO.output(r, GPIO.HIGH)
    GPIO.output(r2, GPIO.HIGH)
    GPIO.output(b, GPIO.HIGH)
    GPIO.output(b2, GPIO.HIGH)
    time.sleep(2)

GPIO.cleanup()