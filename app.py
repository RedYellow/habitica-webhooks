#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:52:45 2020

@author: Nic
"""

from datetime import datetime
import os
import pytz

from flask import Flask, request, Response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from threading import Thread

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True # for prettyprinting in /getall
from .plotlydash.dashboard import init_dashboard
app = init_dashboard(app, db)

from .models import Record

try:
    str_tz = os.environ["TZ"] #TODO: make this into an app.config['str_tz'] = ...
except:
     str_tz = 'America/Los_Angeles'

TZ = pytz.timezone(str_tz)

db.create_all()
db.session.commit()
db.init_app(app)

@app.route("/")
def home():
    records=Record.query.order_by(Record.timestamp.desc()).all()
    js = [e.serialize_json() for e in records]
    data = [js_extract(entry) for entry in js ]

    return render_template("home.html", data=data)

def add_data(data):
    db.session.add(data)
    db.session.commit()

@app.route('/webhook', methods=['POST'])
def respond():
    rec = Record(data = request.json)

    t = Thread(target=add_data, args=(rec, ))
    t.start()
    return Response(status=200)

@app.route("/getall")
def get_all():
    try:
        records=Record.query.all()
        return  jsonify([e.serialize_json() for e in records])
    except Exception as e:
	    return(str(e))

def tstamp_to_str(timestamp):
        dt_stamp = datetime.fromtimestamp(timestamp)
        return dt_stamp.astimezone(TZ).strftime('%Y-%m-%d %I:%M:%S %p')

def js_extract(js_entry):
        try:
            if "timestamp" in js_entry["data"].keys():
                js_entry = js_entry["data"]

            if js_entry["data"]["type"] in ["created", "updated", "deleted", "scored", "checklistScored"]:
                return [js_entry["timestamp"],
                        tstamp_to_str(js_entry["timestamp"]),
                        js_entry["data"]["type"],
                        js_entry["data"]["task"]["text"]]
            elif js_entry["data"]["type"] == "leveledUp":
                return [js_entry["timestamp"],
                        tstamp_to_str(js_entry["timestamp"]),
                        js_entry["data"]["type"],
                        js_entry["data"]["finalLvl"]]
            elif js_entry["data"]["type"] in ["petHatched", "mountRaised"]:
                return [js_entry["timestamp"],
                        tstamp_to_str(js_entry["timestamp"]),
                        js_entry["data"]["type"],
                        js_entry["data"]["message"]]
        except Exception as e:
            print(e)
            return [js_entry["timestamp"],
                        tstamp_to_str(js_entry["timestamp"]),
                        js_entry["data"],
                        js_entry["data"]]

if __name__ == "__main__":
    app.run(debug = True)
