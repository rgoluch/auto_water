from flask import Flask, jsonify
from pymongo import MongoClient
from controller import *
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
client: MongoClient = MongoClient("localhost:270017")
db = client.data

@app.route("/")
def temp():
    return "hello world"

@app.route("/water/<status>", methods=["POST"])
def water_plant(status: str):
    print(status)
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

@app.route("/data", methods=["GET"])
def get_sensor_data():
    data = plant_data()

    return jsonify(data)

def add_sensor_data():
    data = plant_data()
    temp = data[0]
    m = data[1]

    reading = {
        "temp": temp,
        "moisture": m
    }
    db.data.insert_one(reading)

sched = BackgroundScheduler(daemon=True)
sched.add_job(add_sensor_data, 'interval', seconds='30')
sched.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
