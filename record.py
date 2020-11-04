#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:56:34 2020

@author: Nic
"""

from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

# from datetime import datetime

# class Record(db.Model):
#     def __init__(self, JSON):
#         self.data = JSON
#         self.datetime = str(datetime.now())

# class Record(db.Model):
#     __tablename__ = 'restaurant'
#     data = db.Column(type_ = JSON)
#     timestamp = db.Column(type_ = db.Integer, primary_key = True, unique = True)
    
#     def __init__(self, data):
#         self.data = data
#         self.timestamp = int(datetime.now().timestamp())
        
#     def __repr__(self):
#         return str(self.timestamp)