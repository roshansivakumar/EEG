import serial
import numpy as np
import time
import sys

if sys.platform.startswith('win'): # Get port number automatically
        ports = ['COM%s' % (i + 1) for i in range(256)]
        print("ports: ", ports)
result = []
for port in ports:
    try:
        ser = serial.Serial(port)
        print("Serial Port: ", ser)
    except (OSError, serial.SerialException):
        pass

connect = serial.Serial(
    port='COM5',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("serial connection made, I think: ", connect)
print("connected to: " + ser.portstr)

lol = ser.readline()

print(lol)
