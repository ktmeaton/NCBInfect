# -*- coding: utf-8 -*-
"""
NCBImeta Error Classes

@author: Katherine Eaton
"""


class ErrorAnnotFileNotExists(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorAnnotFileNotExists class.

        Parameters:
        value(str): Path to the annotation file.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the annotation file path."""
        return (
            "\n\nFile does not exist."
            + "\n"
            + "User entered: --annotfile "
            + self.value
        )


class ErrorTableNotInDB(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorTableNotInDB class.

        Parameters:
        value(str): Name of the requested table in a sqlite database.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the name of the table."""
        return (
            "\n\nThe table does not exist in the database."
            + "\n"
            + "Unknown table found: "
            + self.value
        )


class ErrorEntryNotInDB(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorEntryNotInDB class.

        Parameters:
        value(str): Name of the entry in a sqlite database.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the name of the entry."""
        return (
            "\n\nThe entry does not exist in the database."
            + "\n"
            + "Unknown entry found: "
            + self.value
        )


class ErrorEntryMultipleMatches(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorEntryMultipleMatches class.

        Parameters:
        value(str): Name of the entry in a sqlite database.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the name of the entry."""
        return (
            "\n\nThe entry has multiple matches in the database."
            + "\n"
            + "Multiple matches for entry: "
            + self.value
        )


class ErrorConfigFileNotExists(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorConfigFileNotExists class.

        Parameters:
        value(str): Path to the configuration file.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the path to the configuration file."""
        return (
            "\n\nConfig file does not exist in the specified location."
            + "\n"
            + "Location specified: "
            + self.value
        )


class ErrorColumnsNotUnique(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorColumnsNotUnique class.

        Parameters:
        value(str): Name of the column in a sqlite database.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the name of the column."""
        return (
            "\n\nThe following columns are not unique in the database:"
            + "\n"
            + str(self.value)
        )


class ErrorDBNotExists(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorDBNotExists class.

        Parameters:
        value(str): Path to the database file.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the path to the configuration file."""
        return "\n\nDatabase does not exist." + "\n" + self.value


class ErrorMaxFetchAttemptsExceeded(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorMaxFetchAttemptsExceeded class.

        Parameters:
        value(int): The number of fetch attempts.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the number of fetch attempts."""
        return (
            "\n\nThe Maximum number of fetch attempts was exceeded for ID:"
            + "\n"
            + self.value
        )


class ErrorMaxReadAttemptsExceeded(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorMaxReadAttemptsExceeded class.

        Parameters:
        value(int): The number of read attempts.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the number of read attempts."""
        return (
            "\n\nThe Maximum number of read attempts was exceeded for table:"
            + "\n"
            + self.value
        )


class ErrorConfigParameter(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorConfigParameter class.

        Parameters:
        value(int): The name of the config parameter.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the name of the config parameter."""
        return (
            "\n\nA parameter name and/or value in the "
            + "configuration file is set incorrectly:"
            + "\n"
            + self.value
        )


class ErrorConfigYAMLFormat(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorConfigYAMLFormat class.

        Parameters:
        value (str): The name of the config file.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the name of the config file."""
        return (
            "\n\nThe configuration file could not be loaded, "
            + "please confirm that this is a proper YAML file: "
            + "\n"
            + self.value
        )


class ErrorSQLNameSanitize(Exception):
    def __init__(self, value, sanitize_value):
        """
        The constructor for ErrorSQLNameSanitize class.

        Parameters:
        value (str): The name of the SQL Table or Column.
        """
        self.value = value
        self.sanitize_value = sanitize_value

    def __str__(self):
        """When the error is raised, prints the name and sanitized version."""
        return (
            "\n\nThe name: "
            + self.value
            + " contains problematic characters. Please rename it to: "
            + self.sanitize_value
        )


class ErrorXPathQueryMultiElement(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorXPathQueryMultiElement class.

        Parameters:
        value (str): The Xpath query.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the problematic Xpath query."""
        return (
            "\n\nMore than one element returned for XPath "
            + str(self.value)
            + ". Are you using the correct XPath query?"
        )


class ErrorXPathElementUnknown(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorXPathElementUnknown class.

        Parameters:
        value (str): The returned search result from an Xpath query.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the problematic search result."""
        return "\n\nUnknown XPath return element: {}".format(type(self.value))


class ErrorXPathQueryMissing(Exception):
    def __init__(self, value):
        """
        The constructor for ErrorXPathQueryMissing class.

        Parameters:
        value (str): The column name with an empty XPath query.
        """
        self.value = value

    def __str__(self):
        """When the error is raised, print the problematic column name."""
        return (
            "\n\nThe following column name uses XPath "
            + "but no query was supplied: "
            + str(self.value)
        )
