# MNIST clock

A clock that displays using randomly selected MNIST digits.

Hardware/software implementation by Dheera Venkatraman ([www](http://dheera.net/), [twitter](https://twitter.com/dheeranet))

Original idea/concept by Evan Pu ([www](https://evanthebouncy.github.io), [twitter](https://twitter.com/evanthebouncy))

![image](/images/final.jpg "image")
Finished MNIST clock.

![image](/images/assembly1.jpg "image")
ESP32 and 4 Waveshare e-Ink displays.

![image](/images/design.jpg "image")
Hand-drawn design by Evan Pu that was posted as a social media status in 2018.

### Original design

### Hardware

It uses an TinyPICO which is an awesome, compact ESP32 board with plenty of GPIO pins, 4MB flash, Wi-Fi, and lots of other features not needed for this project.

4 e-Ink displays are used for the digits. I chose e-Ink since it matches with the idea of handwritten digits, works well in all lighting conditions, and doesn't light up your bedroom when you're trying to sleep. The Waveshare e-Ink displays are mostly SPI, although they have some annoying extra pins. One would wish they were just SPI + one CS pin for each board, but a few more connections are necessary. Here is a diagram of the connections to the ESP32. Crimp the wires according to this.

![image](/images/schematic.jpg "schematic")

I use 2 10-pin JST-EH connectors on the TinyPICO. JST-EH connectors are awesome, lower profile than JST-XH, more satisfying to plug in than JST-XH, and shorter and more secure than standard pin headers. I use them to connectorize almost all 0.1"/2.5mm pitch breakout boards.

### Software

I usually write in C++ or C but I was curious about this new MicroPython stuff, so I tried it for this project.

I use 2 bits per pixel of greyscale depth on each MNIST digit (i.e. 4 greyscale levels). At that bit depth, each 28x28 pixel MNIST digit occupies 196 bytes, so 4MB of flash should be able to fit the entire MNIST validation set. If you want to fit more digits you could (a) use a microcontroller board with a lot more flash (b) use 1-bit depth (c) use compression or some combination of the above.

Put all the files in /code in the root directory of your TinyPICO. Also create a file called .wifi with your SSID in the first line and password in the second line.

### Assembly

#### 3D printed parts

* Bottom and top cover: see .stl files in design/

#### COTS parts

* 4 x [Waveshare 1.54 inch e-Ink display](https://www.amazon.com/Waveshare-Module-Resolution-Electronic-Interface/dp/B0728BJTZC/) -- CAUTION: There are V1, V2, and V2.1 versions of the board that use different communication protocols. Some sellers have mixed-up stockpiles of both versions. You may do best to order 8 or more, pick out 4 identical ones and return the rest. The current state of this repo supports V1 and V2 only. If you get a board that says "Rev 2.1" on it, it will not work.

* 1 x [TinyPICO](https://www.adafruit.com/product/4335)

* 2 x [JST-EH 10-pin right angle header](https://www.digikey.com/products/en/connectors-interconnects/rectangular-connectors-headers-male-pins/314?k=S+B-EH%28LF%29%28SN%29&k=&pkeyword=S+B-EH%28LF%29%28SN%29&sv=0&pv88=63986&sf=0&quantity=&ColumnSort=0&page=1&pageSize=25)

* 2 x [JST-EH 10-pin housing](https://www.digikey.com/products/en/connectors-interconnects/rectangular-connectors-housings/319?k=EHR-&k=&pkeyword=EHR-&sv=0&pv88=63986&sf=0&FV=-8%7C319&quantity=&ColumnSort=0&page=1&pageSize=25)

* 20 x [JST-EH crimps](https://www.digikey.com/product-detail/en/jst-sales-america-inc/SEH-001T-P0.6/455-1042-1-ND/527266)

* 1 x [Anker 6ft white USB-A to USB-Micro-B cable](https://www.amazon.com/Anker-Powerline-Micro-USB-Smartphones/dp/B012VZT5IO/)

* E6000 or similar adhesive to attach the TinyPICO to the case

#### Tools

* [PA-09 crimp tool](https://www.amazon.com/Engineers-Precision-Crimping-Pliers-Pa-09/dp/B002AVVO7K/ref=sr_1_1?keywords=pa-09+engineer&qid=1581612815&sr=8-1) works for JST-EH
