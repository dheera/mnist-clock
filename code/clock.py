import epaper1in54 as epaper
from machine import Pin, SPI

import os
import framebuf
import time
import random

pin_cs = Pin(5)
pin_dc = Pin(33)
pin_re = Pin(4)
pin_bu = Pin(22)

CONFIG_SPI = {
    "mosi": Pin(23),
    "miso": Pin(19),
    "sck": Pin(18),
}

CONFIG_DISPLAYS = [
    { "cs": Pin(26), "busy": Pin(25), "reset": Pin(4), "dc": Pin(33) },
    { "cs": Pin(15), "busy": Pin(27), "reset": Pin(4), "dc": Pin(33) },
    { "cs": Pin(5), "busy": Pin(22), "reset": Pin(4), "dc": Pin(33) },
    { "cs": Pin(21), "busy": Pin(32), "reset": Pin(4), "dc": Pin(33) },
]

spi = SPI(
    baudrate = 2000000,
    polarity = 0,
    phase = 0, 
    sck = CONFIG_SPI["sck"],
    miso = CONFIG_SPI["miso"],
    mosi = CONFIG_SPI["mosi"],
)

displays = [epaper.EPD(spi, config["cs"], config["dc"], config["reset"], config["busy"]) for config in CONFIG_DISPLAYS]

for display in displays:
    display.init()

w = 200
h = 200
x = 0
y = 0
white = 1
black = 0

buf = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
fb.fill(white)

pixel_grey_1_buf = bytearray(7 * 7 // 8 + 1)
pixel_grey_1 = framebuf.FrameBuffer(pixel_grey_1_buf, 7, 7, framebuf.MONO_HLSB)
pixel_grey_1.fill(white)
for i in range(7):
    for j in range(7):
        if random.randint(0, 3) >= 1:
            pixel_grey_1.pixel(i, j, black)

pixel_grey_2_buf = bytearray(7 * 7 // 8 + 1)
pixel_grey_2 = framebuf.FrameBuffer(pixel_grey_2_buf, 7, 7, framebuf.MONO_HLSB)
pixel_grey_2.fill(white)
for i in range(7):
    for j in range(7):
        if random.randint(0, 3) >= 2:
            pixel_grey_2.pixel(i, j, black)

def write_digit(display_num, digit):
    """
    @display: int display index
    @digit: int from 0 to 9 inclusive

    Given an integer digit, fetches a random MNIST image,
    upscales it and displays it on the eink display
    """
    global buf, fb, displays
    digit = digit % 10

    fb.fill(white)
    digit_data = read_digit_data(digit)

    for i in range(196):
        # 196 bytes for each digit (28 pixels)*(28 pixels)*(2 bits/pixel)/8
        for j in range(4):
        # 4 pixels of data stored in in each byte at 2 bits/pixel
            pixel_num = i * 4 + j
            pixel_i = pixel_num // 28   # pixel i in mnist data
            pixel_j = pixel_num % 28    # pixel j in mnist data
            
            pixel_value = (digit_data[i] >> (2*j)) & 0b11 # 2bpp grey value

            # upscale the entire image by factor of 7
            # (28*7 = 196) which almost fills the 200px screen
            # offset by 2 pixels to center it properly
            if pixel_value == 3:
                fb.fill_rect(2 + pixel_j * 7, 2 + pixel_i * 7, 7, 7, black)
            elif pixel_value == 1:
                fb.blit(pixel_grey_2, 2 + pixel_j * 7, 2 + pixel_i * 7)
            elif pixel_value == 2:
                fb.blit(pixel_grey_1, 2 + pixel_j * 7, 2 + pixel_i * 7)

    displays[display_num].set_frame_memory(buf, x, y, w, h)
    displays[display_num].display_frame()

def read_digit_data(digit):
    """
    @digit: int from 0 to 9 inclusive

    Given a digit, fetches a random MNIST digit and returns the raw
    binary data for its image at greyscale depth of 2 bits per pixel.
    Returns a bytearray of length (28*28)*2/8 = 196 in little endian
    """
    fn = 'digit_%d.data' % digit # filename where images for digit are stored
    fsize = os.stat(fn)[6]       # filesize
    N = fsize // 196             # number of images in file
    n = random.randint(0, N - 1) # pick a random index

    # fetch image
    f = open(fn, 'rb')
    f.seek(n*196)
    data = f.read(196)
    f.close()

    return data

def main():
    i = 0
    while True:
        time.sleep(2)
        write_digit(i)
        i += 1
