import cv2 as cv
import numpy as np
import os
import re

file_list = []
file_number = 0
if os.path.exists("./"):
  file_list = os.listdir("./")
  r = re.compile(".*JPG")
  file_list = list(filter(r.match, file_list))
  file_list.sort()
if len(file_list) > 7:
  split_lists = [file_list[x:x+7] for x in range(0, len(file_list), 7)]
  print(split_lists)
  print(len(split_lists))
else:
  print("not enough files found")

exposure_times = np.array([800, 400, 1600, 200, 3200, 200, 3200], dtype=np.float32)
for img_fn in split_lists:
  print(img_fn)
  img_list = [cv.imread(fn) for fn in img_fn]
#  merge_robertson = cv.createMergeRobertson()
#  hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy())
  tonemap1 = cv.createTonemap(gamma=2.2)
  merge_mertens = cv.createMergeMertens()
  res_mertens = merge_mertens.process(img_list)
  res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')
  filename = r"./HDR_" + str(file_number) + ".jpg"
  print(filename)
  file_number = file_number + 1
  cv.imwrite(filename, res_mertens_8bit)
