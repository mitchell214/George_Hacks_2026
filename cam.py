from picamera2 import Picamera2
import cv2

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

# Capture a frame
frame = picam2.capture_array()
cv2.imwrite('frame.jpg', frame)

# Stop the camera
picam2.stop()