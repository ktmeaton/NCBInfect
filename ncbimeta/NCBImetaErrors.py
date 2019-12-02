# -*- coding: utf-8 -*-
"""
NCBImeta Error Classes

@author: Katherine Eaton
"""

class ErrorOutputDirNotExists(Exception):
    '''Error class for when an output directory does not exist'''
    def __init__(self, value):
        '''
        The constructor for ErrorOutputDirNotExists class.

        Parameters:
        value(str): Path to the output directory.
        '''
        self.value = value
    def __str__(self):
        '''When the error is raised, print the output directory path.'''
        print("\n\nOutput directory does not exist.")
        print("User entered: " + self.value)


class ErrorAnnotFileNotExists(Exception):
    def __init__(self, value):
        '''
        The constructor for ErrorAnnotFileNotExists class.

        Parameters:
        value(str): Path to the annotation file.
        '''
        self.value = value
    def __str__(self):
        '''When the error is raised, print the annotation file path.'''
        print("\n\nFile does not exist.")
        print("User entered: --annotfile" + self.value)


class ErrorTableNotInDB(Exception):
    def __init__(self, value):
        '''
        The constructor for ErrorTableNotInDB class.

        Parameters:
        value(str): Name of the requested table in a sqlite database.
        '''
        self.value = value
    def __str__(self):
        '''When the error is raised, print the name of the table.'''
        print("\n\nThe table does not exist in the database.")
        print("Unknown table found: " + self.value)

class ErrorEntryNotInDB(Exception):
    def __init__(self, value):
        '''
        The constructor for ErrorEntryNotInDB class.

        Parameters:
        value(str): Name of the entry in a sqlite database.
        '''
        self.value = value
    def __str__(self):
        '''When the error is raised, print the name of the entry.'''
        print("\n\nThe entry does not exist in the database.")
        print("Unknown entry found: " + self.value)

class ErrorEntryMultipleMatches(Exception):
    def __init__(self, value):
        '''
        The constructor for ErrorEntryMultipleMatches class.

        Parameters:
        value(str): Name of the entry in a sqlite database.
        '''
        self.value = value
    def __str__(self):
        '''When the error is raised, print the name of the entry.'''
        print("\n\nThe entry has multiple matches in the database.")
        print("Multiple matches for entry: " + self.value)

class ErrorConfigFileNotExists(Exception):
    def __init__(self, value):
        '''
        The constructor for ErrorConfigFileNotExists class.

        Parameters:
        value(str): Path to the configuration file.
        '''
        self.value = value
    def __str__(self):
        '''When the error is raised, print the path to the configuration file.'''
        print("\n\nConfig file does not exist in the specified location.")
        print("Location specified: " + self.value)

class ErrorColumnsNotUnique(Exception):
    def __init__(self, value):
        '''
        The constructor for ErrorColumnsNotUnique class.

        Parameters:
        value(str): Name of the column in a sqlite database.
        '''
        self.value = value
    def __str__(self):
        '''When the error is raised, print the name of the column.'''
        print("\n\nThe following columns are not unique in the database:")
        print(self.value)

class ErrorDBNotExists(Exception):
    def __init__(self, value):
        '''
        The constructor for ErrorDBNotExists class.

        Parameters:
        value(str): Path to the database file.
        '''
        self.value = value
    def __str__(self):
        '''When the error is raised, print the path to the configuration file.'''
        print("\n\nDatabase does not exist.")
        print(self.value)

class ErrorMaxFetchAttemptsExceeded(Exception):
    def __init__(self, value):
        '''
        The constructor for ErrorMaxFetchAttemptsExceeded class.

        Parameters:
        value(int): The number of fetch attempts.
        '''
        self.value = value
    def __str__(self):
        '''When the error is raised, print the number of fetch attempts.'''
        print("\n\nThe Maximum number of fetch attempts was exceeded for ID:")
        print(self.value)

class ErrorMaxReadAttemptsExceeded(Exception):
    def __init__(self, value):
        '''
        The constructor for ErrorMaxReadAttemptsExceeded class.

        Parameters:
        value(int): The number of read attempts.
        '''
        self.value = value
    def __str__(self):
        '''When the error is raised, print the number of read attempts.'''
        print("\n\nThe Maximum number of read attempts was exceeded for table:")
        print(self.value)

class ErrorConfigParameter(Exception):
    def __init__(self, value):
        '''
        The constructor for ErrorConfigParameter class.

        Parameters:
        value(int): The name of the config parameter.
        '''
        self.value = value
    def __str__(self):
        '''When the error is raised, print the name of the config parameter.'''
        print("\n\nA parameter name and/or value in the configuration file is set incorrectly:")
        print(self.value)
