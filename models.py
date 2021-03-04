#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 19:19:34 2021

@author: Nic
"""

from .app import db

from sqlalchemy.dialects.postgresql import JSON
import sqlalchemy as sa

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
