"""
Determining orientation to send to data handling and to enhance ML accuracy.
Uses Madgwick AHRS (gyro + accel + mag -> quaternion).
"""

# =========================
# IMPORTS
# =========================
import time
import board
import numpy as np
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from ahrs.filters import Madgwick

# =========================
# IMU INITIALIZATION
# =========================
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

# =========================
# MADGWICK FILTER STATE
# =========================
filt = Madgwick(beta=0.1)
q = np.array([1.0, 0.0, 0.0, 0.0])   # quaternion (w, x, y, z)
dt = 0.01                            # seconds

def predict():
    pass

# =========================
# MEASUREMENT
# =========================
def measure():
    ax, ay, az = accel_gyro.acceleration     # m/s^2
    gx, gy, gz = accel_gyro.gyro             # deg/s
    mx, my, mz = mag.magnetic                 # uT
    return ax, ay, az, gx, gy, gz, mx, my, mz

# =========================
# MADGWICK UPDATE
# =========================
def madgwick_update(ax, ay, az, gx, gy, gz, mx, my, mz):
    global q

    acc = np.array([ax, ay, az])
    gyr = np.array([gx, gy, gz]) * np.pi / 180.0   # deg/s → rad/s
    magv = np.array([mx, my, mz])

    q = filt.updateMARG(q, gyr=gyr, acc=acc, mag=magv, dt=dt)
    return q

def innovate():
    pass

def kalman_gain():
    pass

def update():
    pass

# =========================
# MAIN LOOP
# =========================
def main():
    while True:
        predict()
        ax, ay, az, gx, gy, gz, mx, my, mz = measure()
        q_est = madgwick_update(ax, ay, az, gx, gy, gz, mx, my, mz)
        # q_est = (w, x, y, z)
        # send to data handling / ML / logging here
        print(q_est)
        time.sleep(dt)
        innovate()
        kalman_gain()
        update()

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
