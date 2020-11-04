#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:52:45 2020

@author: Nic
"""

from datetime import datetime
import os

import sqlalchemy as sa
from flask import Flask, request, Response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import psycopg2

from config import Config

# from sqlalchemy import create_engine, func
# from sqlalchemy import create_engine, inspect

# from sqlalchemy.ext.declarative import declarative_base

# from record import Record

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///habitica_db"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['DATABASE_URL'] = "postgresql://localhost/books_store"
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
        return {"data": self.data, "timestamp": self.timestamp}

db.create_all()
db.session.commit()

db.init_app(app)

@app.route("/")
def test():
    # return "gucci gang"
    con = psycopg2.connect(database="Angels_Attic", user="postgres", password="", host="127.0.0.1", port="5432")
    cursor = con.cursor()
    cursor.execute("select * from record")
    result = cursor.fetchall()
    return render_template('home.html', data=result)


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