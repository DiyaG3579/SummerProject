import RPi.GPIO as GPIO
import time
import argparse
GPIO.setmode(GPIO.BOARD)

#parser = argparse.ArgumentParser()
#parser.add_argument("--tim", type = float, default = 8.5, help = "Time to Run")
#parser.add_argument("--low", type=float, default=4, help="Lower Bound Duty Cycle")
#parser.add_argument("--upp", type=float, default=10, help="Upper Bound Duty Cycle")
#parser.add_argument("--debug", default = False, help="Enable debug mode")
#args = parser.parse_args()

#start_time = time.time()

# Define pin, frequency and duty cycle
PWM_pin   = 36 
freq      = 50

GPIO.setup(PWM_pin, GPIO.OUT)
#elapsed = time.time() - start_time

# Create PWM instance for pin w freqency
pwm = GPIO.PWM(PWM_pin, freq) 
pwm.start(7.5)
dc = 5.0

while (dc <= 11.5):
    pwm.ChangeDutyCycle(dc)
    print(dc)
    dc = dc + 0.5
    time.sleep(1.0)

# Stop the output for the PWM pin 
pwm.ChangeDutyCycle(7.0)
time.sleep(1.0)
pwm.ChangeDutyCycle(11.5)
time.sleep(2.0)
pwm.stop()
GPIO.cleanup()
