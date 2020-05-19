from flask import Flask, jsonify
from controller import *
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

@app.route("/")
def temp():
    return "hello world"


@app.route("/water/<status>", methods=["POST"])
def water_plant(status: str):
    
    if status == "on":
        insert = (str(datetime.datetime.now().date()), str(datetime.datetime.now().time()))
        query = """insert into water_log (date, time) values (?,?)"""
        access_db(query, insert)
    water(status)
    return "command sent!"


@app.route("/last_water", methods=["GET"])
def get_last_water():
    log = access_db('select * from water_log order by date desc,time desc limit 1', None)
    temp = {
            "date" : log[0][0],
            "time" : log[0][1]
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
    rows = access_db("select * from sensor_data", None)
    for r in rows:
        temp = {
            "date" : r[0],
            "time" : r[1],
            "temp" : r[2],
            "m" : r[3]
        }
        data.append(temp)
    return jsonify(data)


def add_sensor_data():
    data = plant_data()
    insert = (str(datetime.datetime.now().date()), str(datetime.datetime.now().time()), data[0], data[1])
    query = """insert into sensor_data (date, time, temp, moisture) values (?,?,?,?)"""
    access_db(query, insert)
    return "Inserted data"


sched = BackgroundScheduler(daemon=True)
sched.add_job(add_sensor_data, 'interval', minutes=30)
sched.start()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
