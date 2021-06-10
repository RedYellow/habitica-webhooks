#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:52:45 2020

@author: Nic
"""

from datetime import datetime
import os
import pytz

# import sqlalchemy as sa
from flask import Flask, request, Response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.postgresql import JSON
from threading import Thread
# import psycopg2


# import json

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

# class Record(db.Model):
#     __tablename__ = 'record'
#     data = db.Column(name = "data", type_ = JSON)
#     timestamp = db.Column(name = "timestamp", type_ = sa.Float(), primary_key = True, unique = True)

#     def __init__(self, data):
#         self.data = json.loads(data) if isinstance(data, str) else data
#         self.timestamp = datetime.now().timestamp()

#     def __repr__(self):
#         return str(self.timestamp)

#     def serialize(self):
#         return {"data": json.dumps(self.data), "timestamp": self.timestamp}

#     def serialize_json(self):
#         return {"data": self.data, "timestamp": self.timestamp}

db.create_all()
db.session.commit()
db.init_app(app)

@app.route("/")
def home():
    records=Record.query.order_by(Record.timestamp.desc()).all()
    js = [e.serialize_json() for e in records]
    data = [js_extract(entry) for entry in js ]

    return render_template("home.html", data=data)

# def create_dataframe(db):
#     records=Record.query.all()
#     js = [e.serialize_json() for e in records]
#     df = pd.DataFrame([js_extract(entry) for entry in js ])
#     return df

# def init_dashboard(server):
#     """Create a Plotly Dash dashboard."""
#     dash_app = dash.Dash(
#         server=server,
#         routes_pathname_prefix="/dashapp/",
#         external_stylesheets=[
#             "/static/dist/css/styles.css",
#             "https://fonts.googleapis.com/css?family=Lato",
#         ],
#     )

#     # Load DataFrame
#     df = create_dataframe(server.db)

#     # Custom HTML layout
#     dash_app.index_string = html_layout

#     # Create Layout
#     dash_app.layout = html.Div(
#         children=[
#             dcc.Graph(
#                 id="histogram-graph",
#                 figure={
#                     "data": [
#                         {
#                             "x": df["complaint_type"],
#                             "text": df["complaint_type"],
#                             "customdata": df["key"],
#                             "name": "311 Calls by region.",
#                             "type": "histogram",
#                         }
#                     ],
#                     "layout": {
#                         "title": "NYC 311 Calls category.",
#                         "height": 500,
#                         "padding": 150,
#                     },
#                 },
#             ),
#             create_data_table(df),
#         ],
#         id="dash-container",
#     )
#     return dash_app.server

# def create_data_table(df):
#     """Create Dash datatable from Pandas DataFrame."""
#     table = dash_table.DataTable(
#         id="database-table",
#         columns=[{"name": i, "id": i} for i in df.columns],
#         data=df.to_dict("records"),
#         sort_action="native",
#         sort_mode="native",
#         page_size=300,
#     )
#     return table


def add_data(data):
    db.session.add(data)
    db.session.commit()

@app.route('/webhook', methods=['POST'])
def respond():
    rec = Record(data = request.json)

    t = Thread(target=add_data, args=(rec, ))
    t.start()
    # print(request.json)
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
