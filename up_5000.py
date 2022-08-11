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
 
def handler(signum, frame):
    msg = "Ctrl-c was pressed. Do you really want to exit? y/n "
    print(msg, end="", flush=True)
    res = readchar.readchar()
    if res == 'y':
        print("")
        exit(1)
    else:
        print("", end="\r", flush=True)
        print(" " * len(msg), end="", flush=True) # clear the printed line
        print("    ", end="\r", flush=True)
 
 
signal.signal(signal.SIGINT, handler)
 
def printbuffer(serialPort):
    if serialPort.in_waiting > 0:
        buffer = serialPort.readline()
        print('buffer = ', buffer)

def main():
  serialPort = serial.Serial(port="/dev/ttyACM0", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
  print("connected to: " + serialPort.portstr)
  printbuffer(serialPort)
  time.sleep(2)
  printbuffer(serialPort)
  serialPort.write(b"mr -5000 -5000 -5000")
  printbuffer(serialPort)
  serialPort.close()
  return 0

if __name__ == "__main__":
    sys.exit(main())
