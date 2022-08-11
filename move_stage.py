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

x = 0
y = 0
z = 0

if __name__ == "__main__":
  print(f"Arguments count: {len(sys.argv)}")
  try:
    x = sys.argv[1]
    y = sys.argv[2]
    z = sys.argv[3]
  except IndexError:
    raise SystemExit(f"Usage: move_stage.py x y z")

def move_stage(serialPort,x,y,z):
  focus_move = str.encode("mr " + str(x) + " " + str(y) + " " + str(z))
  serialPort.write(focus_move)
  serialPort.read(1)

def printbuffer(serialPort):
    if serialPort.in_waiting > 0:
        buffer = serialPort.readline()
        print('buffer = ', buffer)

def main():
  serialPort = serial.Serial(port="/dev/ttyACM0", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
  print("connected to: " + serialPort.portstr)
  printbuffer(serialPort)
  time.sleep(2)
  for i in range(photos_per_frame):
    print("frame " + str(i))
    printbuffer(serialPort)
    move_stage(serialPort,x,y,z)
    os.system("gphoto2 --capture-preview --force-overwrite --filename=test_" + str(i) + ".jpg")
  printbuffer(serialPort)
  serialPort.close()
  return 0

if __name__ == "__main__":
    sys.exit(main())