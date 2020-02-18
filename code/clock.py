import epaper1in54_1_0
import epaper1in54_2_0

import network
import ntptime

from machine import Pin, SPI

import os
import framebuf
import time
import random

CONFIG_SPI = {
    "mosi": Pin(23),
    "miso": Pin(19),
    "sck": Pin(18),
}

# list your pin connections here for the 4 displays here
# version should be (1,0) for Waveshare 1.54-inch V1 or (2,0) for Waveshare 1.54-inch V2.
# V2.1 is not supported yet.

CONFIG_DISPLAYS = [
    { "version": (2,0), "cs": Pin(26), "busy": Pin(25), "reset": Pin(4), "dc": Pin(33) },
    { "version": (2,0), "cs": Pin(15), "busy": Pin(27), "reset": Pin(4), "dc": Pin(33) },
    { "version": (1,0), "cs": Pin(5), "busy": Pin(22), "reset": Pin(4), "dc": Pin(33) },
    { "version": (1,0), "cs": Pin(21), "busy": Pin(32), "reset": Pin(4), "dc": Pin(33) },
]


##################################

# initialize Wi-Fi

with open(".wifi", "r") as f:
    CONFIG_WIFI_SSID = f.readline().strip()
    CONFIG_WIFI_PASSWORD = f.readline().strip()

routercon = network.WLAN(network.STA_IF)
routercon.active(True)
routercon.connect(CONFIG_WIFI_SSID, CONFIG_WIFI_PASSWORD)
print(routercon.ifconfig())

# initialize SPI

spi = SPI(
    baudrate = 2000000,
    polarity = 0,
    phase = 0, 
    sck = CONFIG_SPI["sck"],
    miso = CONFIG_SPI["miso"],
    mosi = CONFIG_SPI["mosi"],
)

# initialize displays

displays = []

for config in CONFIG_DISPLAYS:
    if config["version"] == (1,0):
        displays.append(epaper1in54_1_0.EPD(spi, config["cs"], config["dc"], config["reset"], config["busy"]))
    elif config["version"] == (2,0):
        displays.append(epaper1in54_2_0.EPD(spi, config["cs"], config["dc"], config["reset"], config["busy"]))

for display in displays:
    display.init()
    display.clear(0xFF)

w = 200
h = 200
white = 1
black = 0

# 200x200 framebuffer used to draw digits on Waveshare 1.54-inch display
buf = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
fb.fill(white)

# (constant) 7x7 framebuffer filled with dithered 66% gray used for gray value 1
# Q: why 7x7?
# A: MNIST is 28x28 and 28*7 x 28*7 = 196x196 which just almost fills the 200x200
pixel_grey_1_buf = bytearray(7 * 7 // 8 + 1)
pixel_grey_1 = framebuf.FrameBuffer(pixel_grey_1_buf, 7, 7, framebuf.MONO_HLSB)
pixel_grey_1.fill(white)
for i in range(7):
    for j in range(7):
        if random.randint(0, 3) >= 1:
            pixel_grey_1.pixel(i, j, black)

# (constant) 7x7 framebuffer filled with dithered 33% gray used for gray value 2
pixel_grey_2_buf = bytearray(7 * 7 // 8 + 1)
pixel_grey_2 = framebuf.FrameBuffer(pixel_grey_2_buf, 7, 7, framebuf.MONO_HLSB)
pixel_grey_2.fill(white)
for i in range(7):
    for j in range(7):
        if random.randint(0, 3) >= 2:
            pixel_grey_2.pixel(i, j, black)

def display_digit(display_num, digit):
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
            if pixel_value == 3: # gray value 3
                fb.fill_rect(193 - (2 + pixel_j * 7), 193 - (2 + pixel_i * 7), 7, 7, black)
            elif pixel_value == 2: # gray value 2
                fb.blit(pixel_grey_1, 193 - (2 + pixel_j * 7), 193 - (2 + pixel_i * 7))
            elif pixel_value == 1: # gray value 1
                fb.blit(pixel_grey_2, 193 - (2 + pixel_j * 7), 193 - (2 + pixel_i * 7))
            # do nothing for gray value 0; it is already white

    #displays[display_num].set_frame_memory(buf, x, y, w, h)
    displays[display_num].display(buf)

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
    last_digit_0 = -1
    last_digit_1 = -1
    last_digit_2 = -1
    last_digit_3 = -1

    while True:
        if i % 300 == 0:
            try:
                ntptime.settime()
            except:
                print("ntp error")
        # t = ntptime.time() + 946684800 # jan 1 2000 epoch

        the_time = time.localtime()
        digit_3 = the_time[4] % 10
        digit_2 = the_time[4] // 10
        digit_1 = the_time[3] % 10
        digit_0 = the_time[3] // 10

        print(digit_0, digit_1, digit_2, digit_3)

        if digit_0 != last_digit_0:
            display_digit(0, digit_0)
        if digit_1 != last_digit_1:
            display_digit(1, digit_1)
        if digit_2 != last_digit_2:
            display_digit(2, digit_2)
        if digit_3 != last_digit_3:
            display_digit(3, digit_3)

        last_digit_0 = digit_0
        last_digit_1 = digit_1
        last_digit_2 = digit_2
        last_digit_3 = digit_3

        i += 1

        time.sleep(1)
        
