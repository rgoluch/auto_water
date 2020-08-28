from flask import Flask, jsonify
from controller import *
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import schedule

app = Flask(__name__)

@app.route("/")
def temp():
    return "hello world"


@app.route("/water/<status>", methods=["POST"])
def water_plant(status: str):
    
    if status == "on":
        insert = (str(datetime.datetime.now().date().strftime('%m.%d.%Y')), str(datetime.datetime.now().time()))
        query = "insert into water_log (date, time) values (?,?)"
        access_db(query, insert)
    water(status)
    return "command sent!"


@app.route("/last_water", methods=["GET"])
def get_last_water():
    log = access_db('select * from water_log order by rowid desc limit 1', None)
    date = log[0][0]
    # date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m.%d.%y')
    time = log[0][1]
    time = datetime.datetime.strptime(time, '%H:%M:%S.%f').strftime('%H:%M')
    temp = {
            "date" : date,
            "time" : time
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

sched = BackgroundScheduler(daemon=True)
sched.add_job(add_sensor_data, 'interval', hours=6)
sched.start()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
