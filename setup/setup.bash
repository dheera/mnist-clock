#!/bin/bash

echo "******** Installing system dependencies"
sudo apt-get update
sudo apt-get install -y python-dev python-smbus python-serial python-imaging python-numpy

echo "******** Installing wiringPi"
tar zxvf wiringPi.tar.gz
cd wiringPi
./build

echo "******** Installing bcm2835"
tar zxvf bcm2835-1.39.tar.gz
cd bcm2835-1.39
./configure
make
sudo make install

