"""
Taking and editing pictures.
"""


#Anna 1/25/26
import cv2 #import cv2 library
import numpy as np #import numpy library
import time #import time library
from picamera2 import Picamera2 
from libcamera import controls

def init_camera(width = 1280, height = 720):
    picam2 = Picamera2()
    config = picam.create_still_configuration(
        #resolution of image, stores each color in a byte per R, B, G
        main = {"size": (width, height), "format": "RGB888"}
    )
    picam.configure(config)
    picam2.start()
    #gives it a sec to warm-up
    time.sleep(2) 
    return picam2

def take_picture(picam2, filename, exposure):
    picam2.set_controls({"AeEnable": False, "ExposureTime": exposure})
    image = picam2.capture_array()
    cv2.imwrite(filename, image) #saves image as a PNG

def take_video(picam2, filename):
    #takes 5 sec video
    picam2.start_recording(filename)
    picam2.wait_recording(5)
    picam2.stop_recording()

def focus_camera(picam2, lens_position):
    #manually focuses camera with a given value
    picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": lens_position})
    time.sleep(0.5) #gives lens time to move

def change_brightness(image, brightness_value):
    bright_image = image.astype(np.int16)
    #changes image storage so we can adjust brightness

    # Add brightness offset to every pixel
    bright_image += brightness_value

    #keeps values within range
    bright_image = np.clip(bright_image, 0, 255)

    # converts back to unit 8
    return bright_image.astype(np.uint8)
