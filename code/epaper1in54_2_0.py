"""
MicroPython Waveshare 1.54" Black/White GDEH0154D27 e-paper display driver V2

Based on code from
https://github.com/mcauser/micropython-waveshare-epaper
AND
https://github.com/waveshare/e-Paper

MIT License
Copyright (c) 2017 Waveshare
Copyright (c) 2018 Mike Causer
Copyright (c) 2020 Dheera Venkatraman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from micropython import const
from time import sleep_ms
import ustruct

# Display resolution
EPD_WIDTH  = const(200)
EPD_HEIGHT = const(200)

BUSY = const(1)  # 1=busy, 0=idle

class EPD:
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.is_power_on = True

    def _command(self, command):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([data]))
        self.cs(1)

    def wait_until_idle(self):
        print("wait_until_idle")
        while self.busy.value() == BUSY:
            sleep_ms(100)
        sleep_ms(10)

    def turn_on_display(self):
        self._command(0x22) # DISPLAY_UPDATE_CONTROL_2
        self._data(0xF7)
        #self._data(0xF4)
        self._command(0x20) # MASTER_ACTIVATION

        self.wait_until_idle()

    def turn_on_display_part(self):
        self._command(0x22) # DISPLAY_UPDATE_CONTROL_2
        self._data(0xFF)
        self._command(0x20) # MASTER_ACTIVATION

        self.wait_until_idle()


    def init(self):
        print("init")
        self.reset()

        self.wait_until_idle()
        self._command(0x12) # SWRESET
        self.wait_until_idle()

        self._command(0x01) # DRIVER_OUTPUT_CONTROL
        self._data(0xC7) # (EPD_HEIGHT-1) & 0xFF
        self._data(0x00) # ((EPD_HEIGHT-1) >> 8) & 0xFF
        #self._data(0x01) # GD=0 SM=0 TB=0
        self._data(0x00) # GD=0 SM=0 TB=0

        self._command(0x11) # data entry mode
        self._data(0x03)

        self._command(0x44) # set ram-x address start/end position
        self._data(0x00)
        self._data(0x18) # 0x0C --> (18+1)*8 = 200

        self._command(0x45) # set ram-y address start/end position
        self._data(0x00)
        self._data(0x00)
        self._data(0xC7) # 0xC7 --> (199+1) = 200
        self._data(0x00)

        self._command(0x3C) # borderwaveform
        self._data(0x01)

        self._command(0x18)
        self._data(0x80)

        self._command(0x22) # load temperature and waveform setting
        self._data(0xB1)
        self._command(0x20)

        self._command(0x4E) # set RAM x address count to 0
        self._data(0x00)
        self._command(0x4F) # set RAM y address count to 0x199
        self._data(0xC7)
        self._data(0x00)

        # from https://github.com/ZinggJM/GxEPD2/blob/master/src/epd/GxEPD2_154_D67.cpp
        #self._command(0x37)
        #self._data(0x00)
        #self._data(0x00)
        #self._data(0x00)
        #self._data(0x00)
        #self._data(0xff)
        #self._data(0x00)
        #self._data(0x00)
        #self._data(0x00)
        #self._data(0x00)
        #self._data(0x01)

        self.wait_until_idle()

        #self.power_off()

    def reset(self):
        print("reset")
        self.rst(1)
        sleep_ms(100)
        self.rst(0)
        sleep_ms(20)
        self.rst(1)
        sleep_ms(100)

    def clear(self, color):
        # self.power_on()

        self._command(0x24)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self._data(color)
        self.turn_on_display()

        # self.power_off()

    def getbuffer(self, image):
        buf = [0xFF] * (int(self.width/8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        if(imwidth == self.width and imheight == self.height):
            logging.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif(imwidth == self.height and imheight == self.width):
            logging.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy*self.width) / 8)] &= ~(0x80 >> (y % 8))
        return buf

    def power_off(self):
        # doesn't seem to work, causes updates to fail
        # https://github.com/ZinggJM/GxEPD2/blob/master/src/epd/GxEPD2_154_D67.cpp#L78
        if self.is_power_on:
            self._command(0x22)
            self._data(0x83)
            self._command(0x20)
            sleep_ms(20)
            self.is_power_on = False

    def power_on(self):
        # doesn't seem to work, causes updates to fail
        # https://github.com/ZinggJM/GxEPD2/blob/master/src/epd/GxEPD2_154_D67.cpp#L78
        if not self.is_power_on:
            self._command(0x22)
            self._data(0xF8)
            self._command(0x20)
            self.wait_until_idle()
            self.is_power_on = True

    def display(self, image):
        if (image == None):
            return
        
        #self.power_on()

        self._command(0x24)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self._data(image[i + j * int(self.width / 8)])   
        self.turn_on_display()

        #self.power_off()

    def display_part(self, image):
        if (image == None):
            return
            
        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self._data(image[i + j * int(self.width / 8)])
                
        self.turn_on_display_part()

    def sleep(self):
        self.send_command(0x10) # DEEP_SLEEP_MODE)
        self.send_data(0x01)

