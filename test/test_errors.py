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
#                           Test Function                               #
#-----------------------------------------------------------------------#

def test_ErrorAnnotFileNotExists(tmpdir):
    '''Test the class ErrorAnnotFileNotExists (error when an annotation file doesn't exist)'''
    # This file is not created, just a tmp path
    tmpfile = os.path.join(tmpdir.strpath, "tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorAnnotFileNotExists(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nFile does not exist." + "\n" + "User entered: --annotfile " + tmpfile)
    assert error_output == error_expect

def test_ErrorTableNotInDB(tmpdir):
    '''Test the class ErrorTableNotInDB (error when a table doesn't exist in a database)'''
    # This file is not created, just a tmp path
    tmpfile = os.path.join(tmpdir.strpath, "tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorTableNotInDB(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nThe table does not exist in the database." + "\n" + "Unknown table found: " + tmpfile)
    assert error_output == error_expect

def test_ErrorEntryNotInDB():
    '''Test the class ErrorEntryNotInDB (error when an entry doesn't exist in a database)'''
    # This file is not created, just a tmp path
    test_entry = "TestEntry"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorEntryNotInDB(test_entry)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nThe entry does not exist in the database." + "\n" + "Unknown entry found: " + test_entry)
    assert error_output == error_expect

def test_ErrorEntryMultipleMatches():
    '''Test the class ErrorEntryMultipleMatches (error when their are multiple matching entries in a database)'''
    # This file is not created, just a tmp path
    test_entry = "TestEntry"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorEntryMultipleMatches(test_entry)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nThe entry has multiple matches in the database." + "\n" + "Multiple matches for entry: " + test_entry)
    assert error_output == error_expect

def test_ErrorConfigFileNotExists(tmpdir):
    '''Test the class ErrorAnnotFileNotExists (error when a configuration file doesn't exist)'''
    # This file is not created, just a tmp path
    tmpfile = os.path.join(tmpdir.strpath, "tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorConfigFileNotExists(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nConfig file does not exist in the specified location." + "\n" + "Location specified: " + tmpfile)
    assert error_output == error_expect

def test_ErrorColumnsNotUnique():
    '''Test the class ErrorColumnsNotUnique (error when their are non unique columns in a database)'''
    # This file is not created, just a tmp path
    test_column = "TestColumn"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorColumnsNotUnique(test_column)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nThe following columns are not unique in the database:" + "\n" + test_column)
    assert error_output == error_expect

def test_ErrorDBNotExists(tmpdir):
    '''Test the class ErrorDBNotExists (error when a database doesn't exist)'''
    # This file is not created, just a tmp path
    tmpfile = os.path.join(tmpdir.strpath, "tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorDBNotExists(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nDatabase does not exist." + "\n" + tmpfile)
    assert error_output == error_expect

def test_ErrorMaxFetchAttemptsExceeded():
    '''Test the class ErrorMaxFetchAttemptsExceeded (error when maximum fetch attempts has been exceeded)'''
    # This file is not created, just a tmp path
    test_ID = '123456789'
    # Test instantiation
    test_error = NCBImetaErrors.ErrorMaxFetchAttemptsExceeded(test_ID)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nThe Maximum number of fetch attempts was exceeded for ID:" + "\n" + test_ID)
    assert error_output == error_expect

def test_ErrorMaxReadAttemptsExceeded():
    '''Test the class ErrorMaxReadAttemptsExceeded (error when maximum read attempts has been exceeded)'''
    # This file is not created, just a tmp path
    test_table = 'TestTable'
    # Test instantiation
    test_error = NCBImetaErrors.ErrorMaxReadAttemptsExceeded(test_table)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nThe Maximum number of read attempts was exceeded for table:" + "\n" + test_table)
    assert error_output == error_expect

def test_ErrorConfigParameter():
    '''Test the class ErrorConfigParameter (error when a configuration file parameter is incorrect)'''
    # This file is not created, just a tmp path
    test_parameter = "TestParameter"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorConfigParameter(test_parameter)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nA parameter name and/or value in the configuration file is set incorrectly:" + "\n" + test_parameter)
    assert error_output == error_expect

def test_ErrorConfigYAMLFormat(tmpdir):
    '''Test the class ErrorConfigYAMLFormat (error when a configuration file is improperly formatted)'''
    # This file is not created, just a tmp path
    tmpfile = os.path.join(tmpdir.strpath, "tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorConfigYAMLFormat(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = ("\n\nThe configuration file could not be loaded, please confirm that this is a proper YAML file: " + "\n" + tmpfile)
    print("TESTING")
    assert error_output == error_expect
