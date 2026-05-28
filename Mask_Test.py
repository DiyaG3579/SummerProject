import cv2
import numpy as np
import math
from picamera2 import Picamera2

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
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
h, w = img.shape[:2]
cx = w / 2
cy = h / 2