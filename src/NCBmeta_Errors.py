# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 15:45:34 2016

@author: Katherine Eaton
"""

class ErrorInvalidMode(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nMode must be one of \'Create\', \'Update\', or \'Delete\'")
        print("User entered: --mode " + repr(self.value))

class ErrorDBExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nDatabase must not already exist.")
        print("User entered: --database" + repr(self.value))

class ErrorDBNotExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nDatabase does not exist.")
        print("User entered: --database" + repr(self.value))


class ErrorAnnotFileNotExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nFile does not exist.")
        print("User entered: --annotfile" + repr(self.value))

class ErrorAccessionNotInDB(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nFThe accession number does not exist in the database.")
        print("Unknown accession number found: " + repr(self.value))

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
