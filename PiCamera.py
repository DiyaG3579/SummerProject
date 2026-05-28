from picamera2 import Picamera2

camera = Picamera2()
camera.start()
camera.capture_file('Let_us_Begin.jpg')