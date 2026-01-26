"""
Determining orientation to send to data handling and to enhance ML accuracy.
Uses Madgwick AHRS (gyro + accel + mag -> quaternion).
"""
# importing libraries

import time
import board
import numpy as np
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from ahrs.filters import Madgwick, EKF

# initialize pins and sensors as objects

i2c = board.I2C()
accel_gyro = LSM6DS(i2c) 
mag = LIS3MDL(i2c)

filt = Madgwick(beta=0.1) 
# beta is how much accelerometer and magnetometer correct the gyroscope, might change later
# madgwick makes the quaternion orientation based on the imu data
# filt stores the quaternion algorithm
q = np.array([1.0, 0.0, 0.0, 0.0])   # quaternion initialization (w, x, y, z)
dt = 0.01 # seconds between madgwick filter updates, change later because it'll depend on what all is running
H = np.eye(4) # stores a 4x4 matrix of 0s but a diagonal of 1s from left to right
# exists so kalman filter can compare its guess to the measurement
# is matrixed the way it is to tell the program to iterate through the code 4 times, one to pay attention to a certain value in a certain position
HT = H.T
R = np.eye(4) * 0.01 # noise assumption, goes through same way H does, 0.01 is noise baseline estimate

def measure(): # function for imu measurements
    ax, ay, az = accel_gyro.acceleration     # m/s^2 acceleration
    gx, gy, gz = accel_gyro.gyro             # deg/s angular velocity
    mx, my, mz = mag.magnetic                 # uT strength of magnetic field
    return ax, ay, az, gx, gy, gz, mx, my, mz

def pre_filter(): # noise reduction based on specific issues
    pass

def madgwick_update(ax, ay, az, gx, gy, gz, mx, my, mz): # makes quaternion estimation through madgwick filter

    acc = np.array([ax, ay, az]) # stores accelerometer values 
    gyr = np.array([gx, gy, gz]) * np.pi / 180.0   # deg/s → rad/s # stores gyroscope values
    magv = np.array([mx, my, mz]) # stores magnetometer values 

    q = filt.updateMARG(q, gyr=gyr, acc=acc, mag=magv, dt=dt) # computes quaternion based on the values
    return q

def predict(): # kalman prediction of orientation
    P = None # kalman uncertainty 
    return P

def innovate(z, P): # compute error between measurement and prediction 
    y = z - H @ q # computes innovation
    S = H @ P @ HT + R # computes innovation uncertainity
    return y

def kalman_gain(P, H, S): # how much you care about that error 
    K = P @ HT @ np.linalg.inv(S) # computes how much you should trust measurement vs kalman guess based on kalman uncertainity, H is used for making comparisons, and R which is noise assumption
    return HT, kalman_gain

def update(q, z, P, y, K): # computes new quaternion based on measurements, prediction, innovation, and kalman gain
    I = np.eye(len(q)) # makes 4x4 matrix of 0s with a diagonal of 1s from left to right, is a baseline matrix for kalman uncertainty comparisons
    q = q + K @ y # updates quaternion based on based on previous quaternion, kalman gain, and innovation
    P = (I - K @ H) @ P # updates filter uncertainty based on K, and previous P, with instructions and I and H
    return I, y, K, q, P

def post_filter(): # more error reduction based on particular measurement errors
    pass

def main(): # putting everything together to make orientation computations
    while True:
        ax, ay, az, gx, gy, gz, mx, my, mz = measure()
        pre_filter()
        z = madgwick_update(ax, ay, az, gx, gy, gz, mx, my, mz)
        predict()
        innovate()
        HT, K = kalman_gain()
        I, y, S, K, x, P = update(q , z, P)
        post_filter() 

if __name__ == "__main__": # run safely
    main()