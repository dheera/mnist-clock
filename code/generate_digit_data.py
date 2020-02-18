#!/usr/bin/env python3

# generates the files digit_N.data.
# this script is intended to be run on a desktop to generate the .data files only
# and does not need to be copied to the microcontroller.

# if you downloaded the .data files from the repo you don't need to run this script.

import mnist
import numpy as np

# use images from the test set. you can also use images from the training set if you want.
test_images = mnist.test_images()
test_labels = mnist.test_labels()

# maximum total images to read. i couldn't figure out how to use all 4MB on my TinyPICO;
# formatting it for littlefs gave me 2MB. 8000 images fits in under 2MB at 2bpp.
max_images = 8000

# all 2bpp image data for 10 digits, indexed by digit (0-9)
# each bytearray should always have exactly a multiple of 196 bytes in it; each image is 196 bytes
# 196 = (28*28*2/8)
digit_data = [b''] * 10

for i in range(min(test_images.shape[0], 8000)):
    print(i)
    test_image = test_images[i].flatten()

    # reduce to 2bpp
    image_lsb = ((test_image >> 6) & 0b1).astype(np.bool)
    image_msb = ((test_image >> 7) & 0b1).astype(np.bool)
    image = np.hstack(zip(image_lsb, image_msb))
    data = np.packbits(image, bitorder='little').tobytes('C')

    # append to digit_data
    digit_data[int(test_labels[i])] += data

for digit in range(10):
    f = open('digit_' + str(digit) + '.data', 'wb')
    f.write(digit_data[digit])
    f.close()
