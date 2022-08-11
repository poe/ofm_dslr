import logging
import locale
import os
import subprocess
import sys
import serial
import time
import gphoto2 as gp
import signal
import readchar

photos_per_frame = 3
focal_depth = -1000
focus_move = str.encode("mr " + str(focal_depth) + " " + str(focal_depth) + " " + str(focal_depth))

def move_stage()
  serialPort.write(focus_move)

def printbuffer(serialPort):
    if serialPort.in_waiting > 0:
        buffer = serialPort.readline()
        print('buffer = ', buffer)

def main():
  serialPort = serial.Serial(port="/dev/ttyACM0", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
  print("connected to: " + serialPort.portstr)
  printbuffer(serialPort)
  time.sleep(2)
  for x in range(photos_per_frame):
    printbuffer(serialPort)
    os.system("gphoto2 --capture-image")
    move_stage()
  printbuffer(serialPort)
  serialPort.close()
  return 0

if __name__ == "__main__":
    sys.exit(main())
