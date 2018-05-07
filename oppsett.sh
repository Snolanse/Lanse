#!/bin/bash
cd ..
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python3 -y
sudo apt-get install --no-install-recommends xserver-xorg -y
sudo apt-get install --no-install-recommends xinit -y
sudo apt-get install raspberrypi-ui-mods -y
sudo apt-get install lightdm -y
sudo apt-get install python3-tk -y
sudo apt-get install python3-requests -y
sudo apt-get install python3-numpy -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-rpi.gpio
sudo apt-get install build-essential python-dev python-smbus python-pip -y
sudo pip3 install adafruit-mcp3008 
rm pigpio.zip
sudo rm -rf PIGPIO
wget abyz.me.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make
sudo make install
cd ..
cd Lanse
echo "Lanseoppsett er ferdig!"