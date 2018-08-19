#!/usr/bin/env python3

# <debug>
import cv2
# </debug>

import json
import os
import random
import sys
import time
import numpy as np

from PIL import Image

def update_display(pos, img):
    print("updating position %d" % pos)

def update_clock():
    t = time.localtime()
    time_string = "%02d%02d" % (t.tm_hour, t.tm_min)
    if time_string == update_clock.last_time_string:
        return

    for pos, digit in enumerate(time_string):
        img_pil = Image.open(os.path.join(
            "digits", digit, random.choice(digit_filenames[digit])
        ))
        img = np.reshape(img_pil.getdata(), img_pil.size).astype(np.uint8)
        update_display(pos, img)

    update_clock.last_time_string = time_string
update_clock.last_time_string = "----"

# <debug>
#    imgs = np.concatenate(imgs, axis=1).astype(np.uint8)
#    imgs = cv2.resize(imgs, (imgs.shape[1]*10, imgs.shape[0]*10))
#    cv2.imshow('clock', imgs)
#    cv2.waitKey(1)
# </debug>

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
