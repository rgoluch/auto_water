from flask import Flask, jsonify
from flask_pymongo import pymongo
from controller import *
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3, datetime


app = Flask(__name__)
database = 'plant_data'

@app.route("/")
def temp():
    return "hello world"


@app.route("/water/<status>", methods=["POST"])
def water_plant(status: str):
    
    if status == "on":
        insert = (str(datetime.datetime.now().date()), str(datetime.datetime.now().time()))
        query = """insert into water_log (date, time) values (?,?)"""
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            cursor.execute(query,insert)
            db.commit()
            # db.close()
    water(status)
    return "command sent!"


@app.route("/last_water", methods=["GET"])
def get_last_water():
    db = sqlite3.connect(database)
    cursor = db.cursor()
    cursor.execute('select * from water_log order by time desc,date desc limit 1')
    log = cursor.fetchone()

    temp = {
            "date" : log[0],
            "time" : log[1]
        }
    return jsonify(temp)

# TODO
@app.route("/auto/<setting>", methods=["PUT"])
def set_auto_water(setting: str):
    if setting == "on":
        return "Auto water on!"
    return "Auto water off!"


@app.route("/data", methods=["GET"])
def get_sensor_data():
    data = []
    db = sqlite3.connect(database)
    cursor = db.cursor()
    cursor.execute('select * from sensor_data')
    rows = cursor.fetchall()
    for r in rows:
        temp = {
            "date" : r[0],
            "time" : r[1],
            "temp" : r[2],
            "m" : r[3]
        }
        data.append(temp)
    return jsonify(data)


# @app.route("/add", methods=['GET'])
def add_sensor_data():
    data = plant_data()
    insert = (str(datetime.datetime.now().date()), str(datetime.datetime.now().time()), data[0], data[1])
    query = """insert into sensor_data (date, time, temp, moisture) values (?,?,?,?)"""

    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        cursor.execute(query,insert)
        db.commit()
        # db.close()
        
    return "Inserted data"


sched = BackgroundScheduler(daemon=True)
sched.add_job(add_sensor_data, 'interval', minutes=30)
sched.start()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
