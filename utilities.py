#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 15:46:03 2021

@author: Nic
"""

# import pandas as pd
from app import db
from models import Record
import json
from werkzeug.utils import secure_filename


def add_data(data):
    db.session.add(data)
    db.session.commit()

def save_backup():
    db.engine.execute("SELECT * FROM records")

def load_backup(file):
    """
    Load a json file from your computer to the database.
    Deletes everything before adding the new information, so be careful when using.

    Parameters
    ----------
    file : werkzeug.FileStorage
        The file that has already been read from the local storage.

    Returns
    -------
    str
        Describes if the file upload was successful, or if there was an error because the uploaded file was empty.

    """

    data = file.read().decode("utf-8")
    if len(data) > 0:
        #automatically save a backup before removing anything from the database
        file.save(secure_filename("last_backup.json"))

        Record.query.delete()
        js = json.loads(data)
        for i in js:
            add_data(Record(i["data"]))
        return 'file uploaded successfully'
    else:
        return "The file contained no data"

def revert():
    with open("last_backup.json", "r") as f:
        try:
            Record.query.delete()
            js = json.load(f)
            for i in js:
                add_data(Record(i["data"]))
            return 'database reverted'
        except:
            return "there was an error"

