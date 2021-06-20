#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 15:46:03 2021

@author: Nic
"""

# import pandas as pd
from .app import db
from .models import Record
import json

def add_data(data):
    db.session.add(data)
    db.session.commit()

def save_backup():
    db.engine.execute("SELECT * FROM records")

def load_backup(file):
    #automatically save a backup before?
    # with open(file, "r") as f:
    #     dic = json.load(f)
    data = file.read().decode("utf-8")
    js = json.loads(data)
    for i in js:
        # print(i)
        add_data(Record(i["data"]))