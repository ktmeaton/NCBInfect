# -*- coding: utf-8 -*-
"""
NCBI Metadata Database Errors

@author: Katherine Eaton
"""

class ErrorOutputDirNotExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nOutput directory does not exist.")
        print("User entered: " + repr(self.value))


class ErrorAnnotFileNotExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nFile does not exist.")
        print("User entered: --annotfile" + repr(self.value))


class ErrorTableNotInDB(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nThe table does not exist in the database.")
        print("Unknown table found: " + repr(self.value))

class ErrorEntryNotInDB(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nThe entry does not exist in the database.")
        print("Unknown entry found: " + repr(self.value))

class ErrorEntryMultipleMatches(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nThe entry has multiple matches in the database.")
        print("Multiple matches for entry: " + repr(self.value))

class ErrorConfigFileNotExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nConfig.py does not exist in the specified location.")
        print("Location specified: " + repr(self.value))
