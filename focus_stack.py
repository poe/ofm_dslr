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

photos_per_frame = 2
ppf = photos_per_frame

x = 0
y = 0
z = 0

total_photos = 0

if __name__ == "__main__":
  print(f"Arguments count: {len(sys.argv)}")
  try:
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    z = int(sys.argv[3])
  except IndexError:
    raise SystemExit(f"Usage: move_stage.py x y z")



def move_stage(serialPort,x,y,z):
  focus_move = str.encode("mr " + str(x) + " " + str(y) + " " + str(z))
  serialPort.write(focus_move)
  time.sleep(1)
  serialPort.read(1)
  serialPort.flush()

def printbuffer(serialPort):
    if serialPort.in_waiting > 0:
        buffer = serialPort.readline()
        print('buffer = ', buffer)

def stack_and_return(serialPort):
  total_photos = 0
  for i in range(photos_per_frame):
    total_photos = total_photos + 1
    print("frame " + str(total_photos))
    printbuffer(serialPort)
    move_stage(serialPort,x//ppf,y//ppf,z//ppf)
    os.system("gphoto2 --capture-image-and-download --force-overwrite --folder=/home/poe/new_pics")
  time.sleep(5)
  move_stage(serialPort,-1 * x,-1 * y,-1 * z)

def stack_x(serialPort,pan_distance):
  move_stage(serialPort,0,pan_distance,-1 * pan_distance)
  stack_and_return(serialPort)
  move_stage(serialPort,0,-1 * pan_distance,pan_distance)

  move_stage(serialPort,0,-1 * pan_distance,pan_distance)
  stack_and_return(serialPort)
  move_stage(serialPort,0,pan_distance,-1 * pan_distance)

def stack_y(serialPort,pan_distance):
  move_stage(serialPort,pan_distance,0,-1 * pan_distance)
  stack_and_return(serialPort)
  move_stage(serialPort,-1 * pan_distance,0,pan_distance)

  move_stage(serialPort,-1 * pan_distance,0,pan_distance)
  stack_and_return(serialPort)
  move_stage(serialPort,pan_distance,0,-1 * pan_distance)

def stack_z(serialPort,pan_distance):
  move_stage(serialPort,pan_distance,-1 * pan_distance,0)
  stack_and_return(serialPort)
  move_stage(serialPort,-1 * pan_distance,pan_distance,0)

  move_stage(serialPort,-1 * pan_distance,pan_distance,0)
  stack_and_return(serialPort)
  move_stage(serialPort,pan_distance,-1 * pan_distance,0)

def main():
  serialPort = serial.Serial(port="/dev/ttyACM0", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
  print("connected to: " + serialPort.portstr)
  printbuffer(serialPort)
  time.sleep(2)

  pan_distance = 10000

  stack_and_return(serialPort)
  stack_x(serialPort,16000)
  stack_y(serialPort,16000)
  stack_z(serialPort,16000)
  stack_x(serialPort,32000)
  stack_y(serialPort,32000)
  stack_z(serialPort,32000)

  printbuffer(serialPort)
  serialPort.close()
  return 0

if __name__ == "__main__":
    sys.exit(main())
