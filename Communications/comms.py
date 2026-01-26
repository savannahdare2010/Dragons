'''
Communications Python Code
01/24/2026
'''
import socket # importing libraries needed
import struct
import time
import logging
import json
import zlib
import threading
import argparse
import random
import bluetooth

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect(("AA:BB:CC:DD:EE:FF", 1))  # target MAC

SEND_INTERVAL = 0.2  # 5 times per second

while True:
    msg = "sensor_data\n" #just default message
    sock.send(msg) #send data
    time.sleep(SEND_INTERVAL) #wait to send next data time specified earlier

