#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 15:12:21 2021

@author: Nic
"""

"""Prepare data for Plotly Dash."""
import pandas as pd
import pytz
import os
from models import Record

from datetime import datetime

try:
    str_tz = os.environ["TZ"] #TODO: make this into an app.config['str_tz'] = ...
except:
     str_tz = 'America/Los_Angeles'

TZ = pytz.timezone(str_tz)

def tstamp_to_str(timestamp):
        dt_stamp = datetime.fromtimestamp(timestamp)
        return dt_stamp.astimezone(TZ).strftime('%Y-%m-%d %I:%M:%S %p')

def tstamp_to_day_str(timestamp):
        dt_stamp = datetime.fromtimestamp(timestamp)
        return dt_stamp.astimezone(TZ).strftime('%Y-%m-%d')

def tstamp_to_time_str(timestamp):
    dt_stamp = datetime.fromtimestamp(timestamp)
    return dt_stamp.astimezone(TZ).time().strftime("%H:%M")

def js_extract(js_entry):
        try:
            if "timestamp" in js_entry["data"].keys():
                js_entry = js_entry["data"]

            if js_entry["data"]["type"] in ["created", "updated", "deleted", "scored", "checklistScored"]:
                return [js_entry["timestamp"],
                        tstamp_to_day_str(js_entry["timestamp"]),
                        js_entry["data"]["type"],
                        js_entry["data"]["task"]["text"],
                        tstamp_to_time_str(js_entry["timestamp"])]
            elif js_entry["data"]["type"] == "leveledUp":
                return [js_entry["timestamp"],
                        tstamp_to_day_str(js_entry["timestamp"]),
                        js_entry["data"]["type"],
                        js_entry["data"]["finalLvl"],
                        tstamp_to_time_str(js_entry["timestamp"])]
            elif js_entry["data"]["type"] in ["petHatched", "mountRaised"]:
                return [js_entry["timestamp"],
                        tstamp_to_day_str(js_entry["timestamp"]),
                        js_entry["data"]["type"],
                        js_entry["data"]["message"],
                        tstamp_to_time_str(js_entry["timestamp"])]
        except Exception as e:
            print(e)
            return [js_entry["timestamp"],
                        tstamp_to_day_str(js_entry["timestamp"]),
                        js_entry["data"],
                        js_entry["data"],
                        tstamp_to_time_str(js_entry["timestamp"])]

def create_dataframe(db):
    records=Record.query.all()
    js = [e.serialize_json() for e in records]
    df = pd.DataFrame([js_extract(entry) for entry in js ], columns = ["timestamp", "date", "type", "data", "time"  ])
    return df