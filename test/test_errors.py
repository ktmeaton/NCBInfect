"""
NCBImeta Test - Error Classes

@author: Katherine Eaton
"""

#-----------------------------------------------------------------------#
#                         Modules and Packages                          #
#-----------------------------------------------------------------------#

import pytest                               # Testing suite
from ncbimeta import NCBImetaErrors         # Utility Functions
import os                                   # Filepath operations
#-----------------------------------------------------------------------#
#                           Test Function                                #
#-----------------------------------------------------------------------#

def test_ErrorOutputDirNotExists(tmpdir):
    '''Test the class ErrorOutputDirNotExists (error when a directory doesn't exist)'''
    tmpdir = tmpdir.strpath
    # Test instantiation
    test_error = NCBImetaErrors.ErrorOutputDirNotExists(tmpdir)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nOutput directory does not exist." + "\n" + "User entered: " + tmpdir)
    assert error_output == error_expect

def test_ErrorAnnotFileNotExists(tmpdir):
    '''Test the class test_ErrorAnnotFileNotExists (error when an annotation file doesn't exist)'''
    # This file is not created, just a tmp path
    tmpfile = tmpdir.strpath.join("tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorAnnotFileNotExists(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nFile does not exist." + "\n" + "User entered: --annotfile " + tmpfile)
    assert error_output == error_expect

def test_ErrorTableNotInDB(tmpdir):
    '''Test the class test_ErrorTableNotInDB (error when a table doesn't exist in a database)'''
    # This file is not created, just a tmp path
    tmpfile = tmpdir.strpath.join("tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorTableNotInDB(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nThe table does not exist in the database." + "\n" + "Unknown table found: " + tmpfile)
    assert error_output == error_expect

def test_ErrorEntryNotInDB():
    '''Test the class test_ErrorEntryNotInDB (error when an entry doesn't exist in a database)'''
    # This file is not created, just a tmp path
    test_entry = "TestEntry"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorEntryNotInDB(test_entry)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nThe entry does not exist in the database." + "\n" + "Unknown entry found: " + test_entry)
    assert error_output == error_expect

def test_ErrorEntryMultipleMatches():
    '''Test the class test_ErrorEntryMultipleMatches (error when their are multiple matching entries in a database)'''
    # This file is not created, just a tmp path
    test_entry = "TestEntry"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorEntryMultipleMatches(test_entry)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nThe entry has multiple matches in the database." + "\n" + "Multiple matches for entry: " + test_entry)
    assert error_output == error_expect

def test_ErrorConfigFileNotExists(tmpdir):
    '''Test the class test_ErrorAnnotFileNotExists (error when a configuration file doesn't exist)'''
    # This file is not created, just a tmp path
    tmpfile = tmpdir.strpath.join("tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorConfigFileNotExists(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nConfig file does not exist in the specified location." + "\n" + "Location specified: " + tmpfile)
    assert error_output == error_expect

def test_ErrorColumnsNotUnique():
    '''Test the class test_ErrorColumnsNotUnique (error when their are non unique columns in a database)'''
    # This file is not created, just a tmp path
    test_column = "TestColumn"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorColumnsNotUnique(test_column)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nThe following columns are not unique in the database:" + "\n" + test_column)
    assert error_output == error_expect

#def test_ErrorDBNotExists():

#def test_ErrorMaxFetchAttemptsExceeded():

#def test_ErrorMaxReadAttemptsExceeded():

#def test_ErrorConfigParameter():
