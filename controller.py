# File that controls the pump and does the computing for the server
import os
import subprocess
import time
from board import SCL, SDA
import busio
from adafruit_seesaw.seesaw import Seesaw
import sqlite3, datetime
 
i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)
database = 'plant_data'

def water(status):
    if status == "on":
        os.system("uhubctl -l 1-1 -p 4 -a on")
    if status == "off":
        os.system("uhubctl -l 1-1 -p 4 -a off")


def auto_water():
    # TODO
    return False


def add_sensor_data():
    data = plant_data()
    insert = (str(datetime.datetime.now().date()), str(datetime.datetime.now().time()), data[0], data[1])
    query = """insert into sensor_data (date, time, temp, moisture) values (?,?,?,?)"""
    access_db(query, insert)
    return "Inserted data"


def plant_data():
    temp = ss.get_temp()
    moisture = ss.moisture_read()
    data = []
    data.append(str(temp))
    data.append(str(moisture))
    return data

def access_db(query: str, insert: str):
    return_data = None
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        first = query.split()[0]
        if first == "select":
            cursor.execute(query)
            return_data = cursor.fetchall()
        elif insert is not None:
            cursor.execute(query,insert)
        else:
            cursor.execute(query)
        db.commit()
    return return_data
