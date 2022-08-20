import gphoto2 as gp
import io
import locale
import logging
import os
import readchar
import serial
import signal
import subprocess
import sys
import time
import cv2
import numpy as np

from PIL import Image
from PIL import ImageFile

photos_per_frame = 10
ppf = photos_per_frame
focal_depth = -1000

x = 0
y = 0
z = 0

cpos = [0,0,0]

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
  cpos [0] = cpos[0] + x
  cpos [1] = cpos[1] + y
  cpos [2] = cpos[2] + z

def printbuffer(serialPort):
    if serialPort.in_waiting > 0:
        buffer = serialPort.readline()
        print('buffer = ', buffer)

def get_camera():
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    # required configuration will depend on camera type!
    print('Checking camera config')
    # get configuration tree
    config = gp.check_result(gp.gp_camera_get_config(camera))
    # find the image format config item
    # camera dependent - 'imageformat' is 'imagequality' on some
    OK, image_format = gp.gp_widget_get_child_by_name(config, 'imageformat')
    if OK >= gp.GP_OK:
        # get current setting
        value = gp.check_result(gp.gp_widget_get_value(image_format))
        # make sure it's not raw
        if 'raw' in value.lower():
            print('Cannot preview raw images')
            return 1
    # find the capture size class config item
    # need to set this on my Canon 350d to get preview to work at all
    OK, capture_size_class = gp.gp_widget_get_child_by_name( config, 'capturesizeclass')
    if OK >= gp.GP_OK:
        # set value
        value = gp.check_result(gp.gp_widget_get_choice(capture_size_class, 2))
        gp.check_result(gp.gp_widget_set_value(capture_size_class, value))
        # set config
        gp.check_result(gp.gp_camera_set_config(camera, config))
    return camera

def quick_capture(i,camera):
    # capture preview image (not saved to camera memory card)
    camera_file = gp.check_result(gp.gp_camera_capture_preview(camera))
    file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
    # display image
    data = memoryview(file_data)
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    image = Image.open(io.BytesIO(file_data))
    image.show()
    gp.check_result(gp.gp_camera_exit(camera))
    return image

def main():
  serialPort = serial.Serial(port="/dev/ttyACM0", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
  print("connected to: " + serialPort.portstr)
  time.sleep(2)
  printbuffer(serialPort)
  camera = get_camera()
  for i in range(photos_per_frame):
    print("frame " + str(i))
    printbuffer(serialPort)
    move_stage(serialPort,x//ppf,y//ppf,z//ppf)
    time.sleep(1)
    original_image = quick_capture(i,camera)
    original_image = np.asarray(original_image)

    ddepth = cv2.CV_16S
    kernel_size = 3
    image = cv2.GaussianBlur(original_image, (3, 3), 0)
    image = src_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dst = cv2.Laplacian(src_gray, ddepth, ksize=kernel_size)
    abs_dst = cv2.convertScaleAbs(dst)
    lap_var = cv2.Laplacian(image, cv2.CV_64F).var()
    print("at frame " + str(i) + " and height " + str(cpos) + " and lap_focus " + str(lap_var))
    if (lap_var > 10):
      cv2.imwrite("./test" + str(i) + ".jpg",original_image)
      cv2.imwrite("./lap" + str(i) + ".jpg",abs_dst)
  printbuffer(serialPort)
  serialPort.close()
  return 0

if __name__ == "__main__":
    sys.exit(main())
