#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:52:45 2020

@author: Nic
"""

import time
from datetime import datetime
import os
import pytz

import sqlalchemy as sa
from flask import Flask, request, Response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
# import psycopg2

import json

from config import Config #TODO: do I need this?

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.config.from_object(Config()) #TODO: remove?

try:
    str_tz = os.environ["TZ"] #TODO: make this into an app.config['str_tz'] = ...
except:
     str_tz = 'America/Los_Angeles'

TZ = pytz.timezone(str_tz)

class Record(db.Model):
    __tablename__ = 'record'
    data = db.Column(name = "data", type_ = JSON)
    timestamp = db.Column(name = "timestamp", type_ = sa.Float(), primary_key = True, unique = True)
    
    def __init__(self, data):
        self.data = json.loads(data) if isinstance(data, str) else data
        self.timestamp = datetime.now().timestamp()
        
    def __repr__(self):
        return str(self.timestamp)
    
    def serialize(self):
        return {"data": json.dumps(self.data), "timestamp": self.timestamp}
    
    def serialize_json(self):
        return {"data": self.data, "timestamp": self.timestamp}

db.create_all()
db.session.commit()
db.init_app(app)

@app.route("/")
def home():    
    records=Record.query.all()
    js = [e.serialize_json() for e in records]
    data = []
    for i in js:
        # print(i)
        inf = js_extract(i)
        # print(inf)
        data.append(inf)
        # if "data" in i["data"].keys():
        #     # local mistakes
        #     data.append(js_extract(i["data"]))
        # else:
        #     # this is what it should be (in heroku)
        #     data.append(js_extract(i))
        
        # try:
        #     # this is for the local
        #     i = i["data"]
        #     data.append(js_extract(i))
        # except:
        #     print("zoop")
        #     # this is for heroku
        #     data.append(js_extract(i)) 
    print(data)
            
    return render_template("home.html", data=data)


@app.route('/webhook', methods=['POST'])
def respond():
    # print("zoop")
    # print(request)
    rec = Record(data = request.json)
    db.session.add(rec)
    db.session.commit()
    # print(request.json)
    return Response(status=200)

@app.route("/getall")
def get_all():
    #TODO: app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True # for prettyprinting
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
                print("data fix")
                js_entry = js_entry["data"]
                
            if js_entry["data"]["type"] == "scored":
                print("zop")
                return [js_entry["timestamp"], 
                        tstamp_to_str(js_entry["timestamp"]), 
                        js_entry["data"]["type"], 
                        js_entry["data"]["task"]["text"]]
            elif js_entry["data"]["type"] == "petHatched":
                print("hatched")
                return [js_entry["timestamp"], 
                        tstamp_to_str(js_entry["timestamp"]), 
                        js_entry["data"]["type"], 
                        js_entry["data"]["message"]]
        except Exception as e:
            print(js_entry)
            print(e)
            return [js_entry["timestamp"], 
                        tstamp_to_str(js_entry["timestamp"]), 
                        js_entry["data"],
                        js_entry["data"]]
    
if __name__ == "__main__":  
    app.run(debug = True)
