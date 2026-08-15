#I am going to include comments in here - because this will likely be my final draft
#Importing basically everything that I can think of
import RPi.GPIO as GPIO
import time
import argparse
from picamera2 import Picamera2
import cv2
import numpy as np
import math
import pygame
from mod4_funcs import ultrasonic_init, ultrasonic_read

#Setting up both of the LEDs in the Fireplace
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

#Setting up the Distance Sensor
TRIG_PIN = 37
ECHO_PIN = 38
ultrasonic_init(TRIG_PIN, ECHO_PIN)

#Setting up the Servo Motor
blue = False
PWM_pin = 36 
freq = 45
GPIO.setup(PWM_pin, GPIO.OUT)

#Starting at a Duty Cycle of 7.0
pwm = GPIO.PWM(PWM_pin, freq) 
pwm.start(6.0)
time.sleep(1.0)
pwm.ChangeDutyCycle(6.0)

#Setting up Sound
pygame.mixer.init()
pygame.mixer.music.load("Daytime_Forrest_Bonfire.mp3")
pygame.mixer.music.set_volume(1.0)

#Now setting up a time function for the program
start_time = time.time()
elapsed = time.time() - start_time

#Finally defining all the assumptions
Status = False
red = False
yellow = False
green = False
cyan = False
blue = False
purple = False
Exit = False

#Setting up a while loop for the program to run in
while elapsed < 300: #Using 5 minutes just incase the program keeps running
    elapsed = time.time() - start_time
    dist = ultrasonic_read(TRIG_PIN, ECHO_PIN)
    time.sleep(0.1)
    
    #Waiting for the Distance Sensor to Activate - When someone moves thier hand by it
    if dist < 5.0:
        #This then moves the servo which moves a painting - the PiCamera is in the painting
        pwm.ChangeDutyCycle(11.5)
        time.sleep(5.0)
        camera = Picamera2()
        camera.start()            
        camera.capture_file('Test_2.jpg')
        img = cv2.imread("Test_2.jpg")
        #A quick Camera flash - so that I know to move the Colored Chips out
        GPIO.output(r, GPIO.HIGH)
        GPIO.output(r2, GPIO.HIGH)
        GPIO.output(b, GPIO.HIGH)
        GPIO.output(b2, GPIO.HIGH)
        GPIO.output(g, GPIO.HIGH)
        GPIO.output(g2, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(r, GPIO.LOW)
        GPIO.output(r2, GPIO.LOW)
        GPIO.output(g, GPIO.LOW)
        GPIO.output(g2, GPIO.LOW)
        GPIO.output(b, GPIO.LOW)
        GPIO.output(b2, GPIO.LOW)
        time.sleep(1.0)
        pwm.ChangeDutyCycle(5.0) 
        time.sleep(1.0)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #All the masking components
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

        maskYellow = cv2.inRange(hsv, (10, 150, 120), (35, 255, 255))
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

        #In the tests, I originally looked for any of the colors at all - but that made masking really hard, so instead here I am looking
        #for the mask with the greatest number showing through for determination of the color
        redSize = cv2.countNonZero(threshR)
        yellowSize = cv2.countNonZero(threshY)
        greenSize = cv2.countNonZero(threshG)
        cyanSize = cv2.countNonZero(threshC)
        blueSize = cv2.countNonZero(threshB)
        purpleSize = cv2.countNonZero(threshP)

        if redSize == max(blueSize, cyanSize, greenSize, redSize, yellowSize, purpleSize):
            red = True
            Status = True

        elif yellowSize == max(blueSize, cyanSize, greenSize, redSize, yellowSize, purpleSize):
            yellow = True
            Status = True

        elif greenSize == max(blueSize, cyanSize, greenSize, redSize, yellowSize, purpleSize):
            green = True
            Status = True

        elif cyanSize == max(blueSize, cyanSize, greenSize, redSize, yellowSize, purpleSize):
            cyan = True
            Status = True

        elif blueSize == max(blueSize, cyanSize, greenSize, redSize, yellowSize, purpleSize):
            blue = True
            Status = True

        elif purpleSize == max(blueSize, cyanSize, greenSize, redSize, yellowSize, purpleSize):
            purple = True
            Status = True
        
        else:
            print("None")

    #This is where the fire place and fire sounds actually turn on
    if Status:
        print('Status')
        if blue:
            GPIO.output(b, GPIO.HIGH)
            GPIO.output(b2, GPIO.HIGH)
            pygame.mixer.music.play(-1)
            print('blue')

        if red:
            GPIO.output(r, GPIO.HIGH)
            GPIO.output(r2, GPIO.HIGH)
            pygame.mixer.music.play(-1)
            print('red')

        if cyan:
            GPIO.output(b, GPIO.HIGH)
            GPIO.output(b2, GPIO.HIGH)
            GPIO.output(g, GPIO.HIGH)
            GPIO.output(g2, GPIO.HIGH)
            pygame.mixer.music.play(-1)  
            print('cyan')

        if yellow:
            GPIO.output(r, GPIO.HIGH)
            GPIO.output(r2, GPIO.HIGH)
            GPIO.output(g, GPIO.HIGH)
            GPIO.output(g2, GPIO.HIGH)
            pygame.mixer.music.play(-1)
            print('yellow')

        if green:
            GPIO.output(g, GPIO.HIGH)
            GPIO.output(g2, GPIO.HIGH)
            pygame.mixer.music.play(-1)
            print('green')

        if purple:
            GPIO.output(r, GPIO.HIGH)
            GPIO.output(r2, GPIO.HIGH)
            GPIO.output(b, GPIO.HIGH)
            GPIO.output(b2, GPIO.HIGH)
            pygame.mixer.music.play(-1)
            print('purple')

        while Exit == False:
            time.sleep(10)
            if dist < 5.0:
                Exit = True

    if dist < 5.0:
        if Exit == True:
            elapsed = elapsed + 300

#And then everything comes to a stop
GPIO.output(r, GPIO.LOW)
GPIO.output(r2, GPIO.LOW)
GPIO.output(b, GPIO.LOW)
GPIO.output(b2, GPIO.LOW)
GPIO.output(g, GPIO.LOW)
GPIO.output(g2, GPIO.LOW)
pygame.mixer.music.stop()
pwm.stop()
GPIO.cleanup()
