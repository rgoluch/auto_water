from flask import Flask, jsonify
from flask_pymongo import pymongo
from controller import *
from apscheduler.schedulers.background import BackgroundScheduler
# import pymongo


app = Flask(__name__)
connection_string = "mongodb+srv://opus:autowater@cluster0-hhj2f.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client.get_database('plant_data')

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
    data = []
    cursor = db.data.find({})
    for c in cursor:
        c['temp'] = str(c['temp'])
        c['moisture'] = str(c['moisture'])
        data.append(c)
    return jsonify(data)

@app.route("/add", methods=['GET'])
def add_sensor_data():
    data = plant_data()
    temp = data[0]
    m = data[1]

    reading = {
        "temp": temp,
        "moisture": m
    }
    db.data.insert_one(reading)
    return "Inserted data"

# sched = BackgroundScheduler(daemon=True)
# sched.add_job(add_sensor_data, 'interval', seconds=30)
# sched.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
