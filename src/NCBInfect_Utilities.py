# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:10:08 2016

@author: Katherine Eaton
"""

import os
from sys import platform as _platform
import sqlite3


def os_check():
    ''' Return OS Separator'''
    if 'linux' in _platform:
        return "/"
    elif 'cygwin' in _platform:
        return "/"
    elif "win" in _platform:
        return "\\"
    else:
        return "/"

def check_accessory_dir(output_dir):
    OS_SEP = os_check()
    output_dir = output_dir + OS_SEP
    if not os.path.exists(output_dir + OS_SEP + "log"):                                              # Check if log directory exists
        os.makedirs(output_dir + OS_SEP + "log")
    if not os.path.exists(output_dir + OS_SEP + "database"):                                              # Check if log directory exists
        os.makedirs(output_dir + OS_SEP + "database")
    if not os.path.exists(output_dir + OS_SEP + "annotate"):                                              # Check if log directory exists
        os.makedirs(output_dir + OS_SEP + "annotate")
    return 0

def table_exists(db_cur, table_name):
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(table_name)
    return db_cur.execute(query).fetchone() is not None
