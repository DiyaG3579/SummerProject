import RPi.GPIO as GPIO
import time
import pygame

pygame.mixer.init()
pygame.mixer.music.load("Hot_Coffee.mp3")
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

LED = False

time.sleep(4)

LED = True

while LED:
    pygame.mixer.music.play(-1)
    GPIO.output(r, GPIO.HIGH)
    GPIO.output(g, GPIO.HIGH)
    GPIO.output(r2, GPIO.HIGH)
    GPIO.output(g2, GPIO.HIGH)
    time.sleep(20)
    LED = False

pygame.mixer.music.stop()
GPIO.output(r, GPIO.LOW)
GPIO.output(g, GPIO.LOW)
GPIO.output(r2, GPIO.LOW)
GPIO.output(g2, GPIO.LOW)


GPIO.cleanup()