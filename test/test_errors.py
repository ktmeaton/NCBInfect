"""
NCBImeta Test - Error Classes

@author: Katherine Eaton
"""

# -----------------------------------------------------------------------------#
#                         Modules and Packages                                 #
# -----------------------------------------------------------------------------#

from ncbimeta import NCBImetaErrors  # Utility Functions
import os  # Filepath operations

# -----------------------------------------------------------------------------#
#                           Test Function                                      #
# -----------------------------------------------------------------------------#


def test_ErrorAnnotFileNotExists(tmpdir):
    """Test error when an annotation file doesn't exist"""
    # This file is not created, just a tmp path
    tmpfile = os.path.join(tmpdir.strpath, "tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorAnnotFileNotExists(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = (
        "\n\nFile does not exist." + "\n" + "User entered: --annotfile " + tmpfile
    )
    assert error_output == error_expect


def test_ErrorTableNotInDB(tmpdir):
    """Test error when a table doesn't exist in a database"""
    # This file is not created, just a tmp path
    tmpfile = os.path.join(tmpdir.strpath, "tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorTableNotInDB(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = (
        "\n\nThe table does not exist in the database."
        + "\n"
        + "Unknown table found: "
        + tmpfile
    )
    assert error_output == error_expect


def test_ErrorEntryNotInDB():
    """Test error when an entry doesn't exist in a database"""
    # This file is not created, just a tmp path
    test_entry = "TestEntry"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorEntryNotInDB(test_entry)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = (
        "\n\nThe entry does not exist in the database."
        + "\n"
        + "Unknown entry found: "
        + test_entry
    )
    assert error_output == error_expect


def test_ErrorEntryMultipleMatches():
    """Test error when their are multiple matching entries in a database"""
    # This file is not created, just a tmp path
    test_entry = "TestEntry"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorEntryMultipleMatches(test_entry)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = (
        "\n\nThe entry has multiple matches in the database."
        + "\n"
        + "Multiple matches for entry: "
        + test_entry
    )
    assert error_output == error_expect


def test_ErrorConfigFileNotExists(tmpdir):
    """Test error when a configuration file doesn't exist"""
    # This file is not created, just a tmp path
    tmpfile = os.path.join(tmpdir.strpath, "tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorConfigFileNotExists(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = (
        "\n\nConfig file does not exist in the specified location."
        + "\n"
        + "Location specified: "
        + tmpfile
    )
    assert error_output == error_expect


def test_ErrorColumnsNotUnique():
    """Test error when their are non unique columns in a database"""
    # This file is not created, just a tmp path
    test_column = "TestColumn"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorColumnsNotUnique(test_column)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = (
        "\n\nThe following columns are not unique in the database:" + "\n" + test_column
    )
    assert error_output == error_expect


def test_ErrorDBNotExists(tmpdir):
    """Test error when a database doesn't exist"""
    # This file is not created, just a tmp path
    tmpfile = os.path.join(tmpdir.strpath, "tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorDBNotExists(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = "\n\nDatabase does not exist." + "\n" + tmpfile
    assert error_output == error_expect


def test_ErrorMaxFetchAttemptsExceeded():
    """Test error when maximum fetch attempts has been exceeded"""
    # This file is not created, just a tmp path
    test_ID = "123456789"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorMaxFetchAttemptsExceeded(test_ID)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = (
        "\n\nThe Maximum number of fetch attempts was exceeded for ID:" + "\n" + test_ID
    )
    assert error_output == error_expect


def test_ErrorMaxReadAttemptsExceeded():
    """Test error when maximum read attempts has been exceeded"""
    # This file is not created, just a tmp path
    test_table = "TestTable"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorMaxReadAttemptsExceeded(test_table)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = (
        "\n\nThe Maximum number of read attempts was exceeded for table:"
        + "\n"
        + test_table
    )
    assert error_output == error_expect


def test_ErrorConfigParameter():
    """Test error when a configuration file parameter is incorrect"""
    # This file is not created, just a tmp path
    test_parameter = "TestParameter"
    # Test instantiation
    test_error = NCBImetaErrors.ErrorConfigParameter(test_parameter)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = (
        "\n\nA parameter name and/or value in the "
        + "configuration file is set incorrectly:"
        + "\n"
        + test_parameter
    )
    assert error_output == error_expect


def test_ErrorConfigYAMLFormat(tmpdir):
    """Test error when a configuration file is improperly formatted"""
    # This file is not created, just a tmp path
    tmpfile = os.path.join(tmpdir.strpath, "tmpfile")
    # Test instantiation
    test_error = NCBImetaErrors.ErrorConfigYAMLFormat(tmpfile)
    # Test str representation (error message)
    error_output = str(test_error)
    error_expect = (
        "\n\nThe configuration file could not be loaded, "
        + "please confirm that this is a proper YAML file: "
        + "\n"
        + tmpfile
    )
    assert error_output == error_expect


def test_ErrorSQLNameSanitize():
    """Test error when a table name is improperly formatted"""
    # Use an improper table name
    test_name = "); drop tables --"
    test_sanitize_name = "droptables"
    # Raise the error
    test_error = NCBImetaErrors.ErrorSQLNameSanitize(test_name, test_sanitize_name)
    error_output = str(test_error)
    error_expect = (
        "\n\nThe name: "
        + test_name
        + " contains problematic characters. Please rename it to: "
        + test_sanitize_name
    )
    assert error_output == error_expect


def test_ErrorXPathQueryMultiElement():
    """Test when bad multiple matches have been found for an Xpath query"""
    # Use an improper table name
    test_xpath = "//RUN"
    # Raise the error
    test_error = NCBImetaErrors.ErrorXPathQueryMultiElement(test_xpath)
    error_output = str(test_error)
    error_expect = (
        "\n\nMore than one element returned for XPath "
        + str(test_xpath)
        + ". Are you using the correct XPath query?"
    )
    assert error_output == error_expect


def test_ErrorXPathElementUnknown():
    """Test unknown type of search result"""
    # Use an improper table name
    test_result = {"test": "dict"}
    # Raise the error
    test_error = NCBImetaErrors.ErrorXPathElementUnknown(test_result)
    error_output = str(test_error)
    error_expect = "\n\nUnknown XPath return element: {}".format(type(test_result))
    assert error_output == error_expect


def test_ErrorXPathQueryMissing():
    """Test when query was not specified"""
    # Use an improper table name
    test_col_name = {"AssemblyAccession"}
    # Raise the error
    test_error = NCBImetaErrors.ErrorXPathQueryMissing(test_col_name)
    error_output = str(test_error)
    error_expect = (
        "\n\nThe following column name uses XPath "
        + "but no query was supplied: "
        + str(test_col_name)
    )
    assert error_output == error_expect
