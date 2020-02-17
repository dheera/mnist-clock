#!/usr/bin/env python3

# generates the files digit_N.data.
# this script is intended to be run on a desktop to generate the .data files only
# and does not need to be copied to the microcontroller.

# if you downloaded the .data files from the repo you don't need to run this script.

import mnist
import numpy as np

test_images = mnist.test_images()
test_labels = mnist.test_labels()

digit_data = [b''] * 10

max_images = 8000

for i in range(min(test_images.shape[0], 8000)):
    print(i)
    test_image = test_images[i].flatten()
    image_lsb = ((test_image >> 6) & 0b1).astype(np.bool)
    image_msb = ((test_image >> 7) & 0b1).astype(np.bool)
    image = np.hstack(zip(image_lsb, image_msb))
    data = np.packbits(image, bitorder='little').tobytes('C')
    digit_data[int(test_labels[i])] += data

for digit in range(10):
    f = open('digit_' + str(digit) + '.data', 'wb')
    f.write(digit_data[digit])
    f.close()
