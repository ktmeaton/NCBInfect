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


