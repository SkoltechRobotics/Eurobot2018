import picamera
import time

camera = picamera.PiCamera()
time.sleep(1)
camera.capture('imgs/img1.png')
