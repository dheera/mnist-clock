#!/usr/bin/env python3

import cv2
import json
import os
import random
import sys
import time
import numpy as np

from PIL import Image

def update_clock():
    t = time.localtime()
    time_display = "%02d%02d" % (t.tm_hour, t.tm_min)
    imgs = []
    for digit in time_display:
        img = Image.open(os.path.join(
            "digits", digit, random.choice(digit_filenames[digit])
        ))
        imgs.append(np.reshape(img.getdata(), img.size))
    imgs = np.concatenate(imgs, axis=1).astype(np.uint8)
    imgs = cv2.resize(imgs, (imgs.shape[1]*10, imgs.shape[0]*10))
    cv2.imshow('clock', imgs)
    cv2.waitKey(1)

if __name__ == "__main__":

    digit_filenames = {}
    for digit in os.listdir("digits"):
        digit_filenames[digit] = list(filter(
            lambda x: x.endswith('.png'),
            os.listdir(os.path.join("digits", digit))
        ))

    while True:
        time.sleep(1)
        update_clock()
