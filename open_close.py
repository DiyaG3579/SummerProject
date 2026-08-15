import RPi.GPIO as GPIO
import time
import argparse
GPIO.setmode(GPIO.BOARD)

# Define pin, frequency and duty cycle
PWM_pin   = 36 
freq      = 50

GPIO.setup(PWM_pin, GPIO.OUT)
#elapsed = time.time() - start_time

# Create PWM instance for pin w freqency
pwm = GPIO.PWM(PWM_pin, freq) 
pwm.start(6.0)
time.sleep(1.0)
pwm.ChangeDutyCycle(12.0)
time.sleep(2.0)
pwm.stop()
GPIO.cleanup()
