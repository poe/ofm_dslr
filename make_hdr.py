import cv2 as cv
import numpy as np
import os

print(os.listdir("*.JPG"))
img_fn = [r"P1756330.JPG", r"P1756331.JPG", r"P1756332.JPG", r"P1756333.JPG", r"P1756334.JPG", r"P1756335.JPG", r"P1756336.JPG"]
img_list = [cv.imread(fn) for fn in img_fn]
exposure_times = np.array([800, 400, 1600, 200, 3200, 200, 3200], dtype=np.float32)
merge_robertson = cv.createMergeRobertson()
hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy())
tonemap1 = cv.createTonemap(gamma=2.2)
merge_mertens = cv.createMergeMertens()
res_mertens = merge_mertens.process(img_list)
res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')
cv.imwrite(r"./fusion_mertens.jpg", res_mertens_8bit)

