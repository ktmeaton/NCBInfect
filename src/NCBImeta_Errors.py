# -*- coding: utf-8 -*-
"""
NCBI Metadata Database Errors

@author: Katherine Eaton
"""

class ErrorOutputDirNotExists(Exception):
    def __init__(self, value):
        self.value = value
    #def __str__(self):
        print("\n\nOutput directory does not exist.")
        print("User entered: " + self.value)


class ErrorAnnotFileNotExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nFile does not exist.")
        print("User entered: --annotfile" + self.value)


class ErrorTableNotInDB(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nThe table does not exist in the database.")
        print("Unknown table found: " + self.value)

class ErrorEntryNotInDB(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nThe entry does not exist in the database.")
        print("Unknown entry found: " + self.value)

class ErrorEntryMultipleMatches(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nThe entry has multiple matches in the database.")
        print("Multiple matches for entry: " + self.value)

class ErrorConfigFileNotExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nConfig file does not exist in the specified location.")
        print("Location specified: " + self.value)

class ErrorColumnsNotUnique(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print("\n\nThe following columns are not unique in the database:")
        print(self.value)
