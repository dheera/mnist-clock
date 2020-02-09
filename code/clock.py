import epaper1in54 as epaper
from machine import Pin, SPI

import os
import framebuf
import time
import random

spi = SPI(baudrate=2000000,polarity=0,phase=0,sck=Pin(18),miso=Pin(19),mosi=Pin(23))
pin_cs = Pin(5)
pin_dc = Pin(22)
pin_re = Pin(21)
pin_bu = Pin(32)

e = epaper.EPD(spi, pin_cs, pin_dc, pin_re, pin_bu)
e.init()

w = 200
h = 200
x = 0
y = 0
white = 1
black = 0

buf = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
fb.fill(white)

def write_digit(digit):
    global buf, fb, e
    digit = digit % 10

    fb.fill(white)
    digit_data = read_digit(digit)
    for i in range(98):
        for j in range(8):
            pixel_num = i * 8 + j
            pixel_i = pixel_num // 28
            pixel_j = pixel_num % 28
            
            if ((1 << (7-j)) & digit_data[i]) > 0:
                fb.fill_rect(pixel_j * 7, pixel_i * 7, 7, 7, black)

    e.set_frame_memory(buf, x, y, w, h)
    e.display_frame()

def read_digit(digit):
    fn = 'digit_%d.data' % digit
    fsize = os.stat(fn)[6]
    N = fsize // 98
    n = random.randint(0, N - 1)

    f = open(fn, 'rb')
    f.seek(n*98)
    data = f.read(98)
    f.close()

    return data

def main():
    i = 0
    while True:
        time.sleep(2)
        write_digit(i)
        i += 1
