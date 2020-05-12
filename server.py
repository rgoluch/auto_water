from flask import Flask
from controller import *


app = Flask(__name__)

@app.route("/")
def temp():
    return "hello world"

@app.route("/water/<status>")
def water_plant(status: str):
    water(status)
    # TODO add in a call to write last water time
    return "Watering Plant!"

@app.route("/last_water")
def get_last_water():
    # TODO
    return True

@app.route("/auto/<setting>", methods=["PUT"])
def set_auto_water(setting: str):
    if setting == "on":
        return "Auto water on!"
    return "Auto water off!"

@app.route("/data")
def get_sensor_data():
    data = plant_data()
    return data


if __name__ == '__main__':
    app.run(debug=True)