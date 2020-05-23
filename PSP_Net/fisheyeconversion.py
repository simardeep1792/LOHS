import cv2
import numpy as np
import math
import os
import sys

if len(sys.argv) == 2:
    filepath = sys.argv[1]
    files = os.listdir(filepath)

    outputpath = filepath + '_FISHEYE'
    isExists = os.path.exists(outputpath)

    if not isExists:
        os.mkdir(outputpath)

    cx = 1024 / (2 * math.pi)
    cy = 1024 / (2 * math.pi)
    r0 = 1024 / (2 * math.pi)

    def create_fisheye_image(img_name):
        img = cv2.imread(filepath+'/'+ img_name)
        fisheyeimg = np.zeros([250, 250, 3], np.uint8)
        for xf in range(250):
            for yf in range(250):
                r = math.sqrt((xf - cx) ** 2 + (yf - cy) ** 2)
                if yf < cx:
                    theta = 3 * math.pi / 2 - math.atan((xf - cy) / (yf - cx))
                else:
                    theta = math.pi / 2 - math.atan((xf - cy) / (yf - cx))
                yc = int(theta * 1024 / (2 * math.pi))
                xc = int(r * 512 / r0)
                if (xc <= 256 and yc < 1024):
                    fisheyeimg[xf, yf] = img[xc, yc]

        cropped_fisheye = fisheyeimg[77:250, 77:250]
        fliped_img = cv2.flip(cropped_fisheye, 1, dst=None)  
        cv2.imwrite(outputpath+'/' + img_name, fliped_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    for img_name in files:
        if img_name=='.DS_Store':
            continue
        create_fisheye_image(img_name)


