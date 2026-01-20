"""
Determining orientation to send to data handling and to enhance ML accuracy. 
"""

# import libraries
import time                      # so everything doesn't happen too fast
import board                     # access physical pins by name
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo             # interact with GitHub
from picamera2 import Picamera2  # camera control
import os                        # interact with operating system

# =========================
# IMU & CAMERA INITIALIZATION
# =========================
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()

# =========================
# GIT PUSH FUNCTION
# =========================
def git_push():
    """
    Stages, commits, and pushes new images to the GitHub repository.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        origin.pull()
        repo.git.add(os.path.join(REPO_PATH, FOLDER_PATH))
        repo.index.commit('New Photo')
        origin.push()
        print("Image uploaded to GitHub.")
    except Exception as e:
        print("Git upload failed:", e)

def measuring():
    while True: 
        accelx, accely, accelz = accel_gyro.acceleration
        gyrox, gyroy, gyroz = accel_gyro.gyro
        magx, magy, magz = mag.magnetic



def main():
    measuring()

if __name__ == "__main__":
    main()