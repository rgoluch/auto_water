# File that controls the pump and does the computing for the server
from server import *
import os
import time
from board import SCL, SDA
import busio
from adafruit_seesaw.seesaw import Seesaw
 
i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)

def water(status):
    if status == "on":
        os.system("uhubctl -l 1-1 -p 4 -a on")
    if status == "off":
        os.system("uhubctl -l 1-1 -p 4 -a off")

def auto_water():
    # TODO
    return False

def plant_data():
    temp = ss.get_temp()
    moisture = ss.moisture_read()
    data = []
    data.append(str(temp))
    data.append(str(moisture))
    return data