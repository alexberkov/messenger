import datetime
import json
import time

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "<h2> Hello, Skillbox </h2> <br> <a href='/status'> Status </a> <br> <a href='/about_us'> About Us </a>"


@app.route("/status")
def status():
    t = time.time()
    dt = datetime.datetime.fromtimestamp(t)
    response = {'status': 'true',
                'name': 'Swisher',
                'time': f'{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute}:{dt.second}'}
    return json.dumps(response)


@app.route("/about_us")
def about_us():
    description: str = "<h2> Welcome! </h2> <p> We are a new Flask-based messenger called Swisher! </p>"
    return description


app.run()
