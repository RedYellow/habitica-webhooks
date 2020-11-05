#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:52:45 2020

@author: Nic
"""

import time
from datetime import datetime
import os

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

app.config.from_object(Config())

class Record(db.Model):
    __tablename__ = 'record'
    data = db.Column(name = "data", type_ = JSON)
    timestamp = db.Column(name = "timestamp", type_ = sa.Float(), primary_key = True, unique = True)
    
    def __init__(self, data):
        self.data = data
        self.timestamp = datetime.now().timestamp()
        
    def __repr__(self):
        return str(self.timestamp)
    
    def serialize(self):
        # returns a dict of jsons
        return {"data": json.dumps(self.data), "timestamp": self.timestamp}
    
    def serialize_json(self):
        # returns a legit json string, to be loaded to dictionary with loads()
        return json.dumps({"data": self.data, "timestamp": self.timestamp})

db.create_all()
db.session.commit()

db.init_app(app)

@app.route("/")
def home():
    def tstamp_to_str(timestamp):
        return time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime(timestamp))
    records=Record.query.all()
    js = [json.loads(e.serialize_json()) for e in records]
    data = {}
    # data = {i["timestamp"] : i["data"]["data"]["type"] for i in js}
    for i in js:
        try:
            data[tstamp_to_str(i["timestamp"])] = i["data"]["data"]["type"]
        except:
            data[tstamp_to_str(i["timestamp"])] = i["data"]
    return render_template("home.html", data=data)
    # except Exception as e:
    #     print("big exe")
    #     return(str(e))


@app.route('/webhook', methods=['POST'])
def respond():
    print(request)
    rec = Record(data = request.json)
    db.session.add(rec)
    db.session.commit()
    print(request.json)
    return Response(status=200)

@app.route("/getall")
def get_all():
    try:
        records=Record.query.all()
        return  jsonify([e.serialize() for e in records])
    except Exception as e:
	    return(str(e))
    
if __name__ == "__main__":  
    app.run(debug = True)
