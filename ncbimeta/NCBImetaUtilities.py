# -*- coding: utf-8 -*-
"""
NCBImeta Utility Functions

@author: Katherine Eaton
"""

# -----------------------------------------------------------------------------#
#                         Modules and Packages                                 #
# -----------------------------------------------------------------------------#

import os  # Filepath operations
from ncbimeta import NCBImetaErrors  # NCBImeta Error classes
import urllib.error  # HTTP Error Catching
import time  # Allow sleeping of processes
from lxml import etree  # XML Parsing

# -----------------------------------------------------------------------------#
#                         Utility Functions                                    #
# -----------------------------------------------------------------------------#


def check_accessory_dir(output_dir):
    """
    Check if the accessory directories already exist.

    Parameters:
    output_dir(str): Path to the output directory.
    """
    if not os.path.exists(os.path.join(output_dir, "log")):
        os.makedirs(os.path.join(output_dir, "log"))
    if not os.path.exists(os.path.join(output_dir, "database")):
        os.makedirs(os.path.join(output_dir, "database"))


def table_exists(db_cur, table_name):
    """
    Return a table name from a sqlite database to check if it exists.

    Parameters:
    db_cur(Cursor): A sqlite cursor connection.
    table_name(str): Name of a table in the sqite database.
    """
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(
        table_name
    )
    return db_cur.execute(query).fetchone() is not None


def adv_xml_search(xml_root, targ_xpath, column_name, xml_dict):
    """
    Search xml_root using targ_xpath query, assign to column name in xml_dict.
    Contributor: @ktmeaton, @hellothisisMatt

    Parameters:
    xml_root (ElementTree): xml document as etree object
    targ_xpath (str): XPATH query (lxml python module, XPATH 1.0)
    column_name (str): column_name in xml_dict to assign node value to.
    xml_dict (dict): A dictionary to modify and store found values.

    Returns:
    Void. Instead the function mutates the dictionary xml_dict.
    """
    results = xml_root.xpath(targ_xpath)

    for result in results:
        # Lets figure out the returned element from our XPath query.
        # First check if we returned an XML node.
        if isinstance(result, etree._Element):
            # If it's an XML node, lets make sure it returned a unique value.
            # getchildren function returns a list, test no children with len
            if len(result.getchildren()) == 0:
                # Now lets check if it has a text value that it can return.
                if result.text is not None:
                    result_text = result.text.strip()
                # Now check if we can use the tag as a value to return.
                elif result.tag is not None:
                    result_text = result.tag.strip()
                # Can't return anything, set to None to avoid an error.
                # Hmm do we want this to be None or an empty string...
                else:
                    result_text = None
            else:
                # Didn't get a unique value from the XPath query. Help!
                raise NCBImetaErrors.ErrorXPathQueryMultiElement(targ_xpath)
        elif isinstance(result, str):
            # Didn't get an element, then returned an attribute (a string)!
            result_text = result.strip()
        else:
            # Rreceived a value from XPath that we don't know how to deal with.
            raise NCBImetaErrors.ErrorXPathElementUnknown(result)

        # Add the found node value to the dictionary
        xml_dict[column_name].append(str(result_text))


def xml_search(xml_root, search_list, current_tag, column_name, xml_dict):
    """
    Search xml_root using XPATH for nodes, attributes in search_list.
    Assign to column_name in xml_dict. In addition to searching, this function
    also handles escaped XML as text &lt; and &gt; characters, as well as
    CDATA sections.

    Parameters:
    xml_root (ElementTree): xml document as etree object
    search_list (list): list of nodes and attributes in descending hierarchy
    current_tag (str): current tag (or attribute/value) to be searching
    column_name (str): column_name in xml_dict to assign node value to.
    xml_dict (dict): A dictionary to modify and store found values.

    Returns:
    Void. Instead the function mutates the dictionary xml_dict.
    """
    # Xpath query (could be tag or attribute)
    tag_xpath = ".//" + current_tag
    # -------------------------------------------------------------------------#
    #                   Recursion Bottom (End of Search List)                  #
    # -------------------------------------------------------------------------#
    if search_list.index(current_tag) == len(search_list) - 1:
        # --- First try the current_tag as attribute ---#
        try:
            fetch_attrib = xml_root.get(current_tag)
            # If successful, add to dictionary
            if fetch_attrib:
                xml_dict[column_name].append(fetch_attrib)
        except AttributeError:
            pass
        # --- Next, try the current_tag as a node ---#
        try:
            search_results = xml_root.findall(tag_xpath)
            # Iterate over all possible nodes
            for result in search_results:
                # If the result was a text node
                if result.text:
                    # Remove empty string elements/empty whitespace
                    result_text = result.text.strip()
                    xml_dict[column_name].append(str(result_text))
                # If the result wasn't a text node, but does have child nodes
                elif len(result) > 0:
                    xml_dict[column_name].append(result[0].tag)
        except IndexError:
            pass
    # -------------------------------------------------------------------------#
    #                                 Ongoing Recursion                        #
    # -------------------------------------------------------------------------#
    else:
        # First try current_tag as node, allowing multiple results
        search_results = xml_root.findall(tag_xpath)
        # We need to know the next tag
        next_tag = search_list[search_list.index(current_tag) + 1]

        # --- No results, first possibility is xml tags have been recoded ---#
        if not search_results:
            # Retry the search with unescaped characters
            xml_root_string_orig = etree.tostring(xml_root)
            open_char = "&lt;"
            close_char = "&gt;"
            xml_root_string = (
                str(xml_root_string_orig)
                .replace(open_char, "<")
                .replace(close_char, ">")
                .strip()
            )
            xml_root_string = str(xml_root_string).replace("\\n", "")
            xml_root_string = xml_root_string.replace("\\t", "")
            # Strip off the first 2 char (b') and the final char '
            # print(xml_root_string)
            try:
                xml_root = etree.fromstring(xml_root_string[2:-1])
            # Too aggressive, greater than/less than signs got replaced
            except etree.XMLSyntaxError:
                xml_root_string = (
                    str(xml_root_string_orig).replace("\\n", "").replace("\\t", "")
                )
                xml_root = etree.fromstring(xml_root_string[2:-1])
            # Now retry the search with the tags fixed up
            search_results = xml_root.findall(tag_xpath)
            # If attributes of interest are present and matching

        # --- See if the info we want exists here as attribute values---#
        try:
            if xml_root.get(current_tag) == next_tag:
                xml_dict[column_name].append(xml_root.text)
        except AttributeError:
            pass

        # --- With multiple results, need to keep searching recursively ---#
        for result in search_results:
            # If there was a result, but not a text node, try attribute
            fetch_attrib = ""
            if not result.text:
                fetch_attrib = result.get(next_tag)
                if fetch_attrib:
                    xml_dict[column_name].append(result.get(next_tag))
            # If there was a text node found
            elif result.text:
                result_text = result.text.strip()
                if result_text:
                    # Check if result contains CDATA
                    first_char = result_text[0]
                    last_char = result_text[-1]
                    if first_char == "<" and last_char == ">":
                        # Reformat CDATA as complete XML
                        result_text = (
                            "<"
                            + current_tag
                            + ">"
                            + result_text
                            + "</"
                            + current_tag
                            + ">"
                        )
                        result = etree.fromstring(result_text)

            if not fetch_attrib:
                # If an attribute wasn't succesfully fetched, need recursion
                xml_search(result, search_list, next_tag, column_name, xml_dict)


def HTTPErrorCatch(http_method, max_fetch_attempts, sleep_time, **kwargs):
    """
    Return result of http_method and check if an HTTP Error is generated

    Parameters:
    http_method (function): An http record-fetching or searching method.
    max_fetch_attempts (int): Maximum number of tries to fetch a record_dict.
    sleep_time (float): Number of seconds to wait during fetch read_attempts.
    kwargs(dict): keyword arguments for the http_method function.
    """
    # Attemp the http_method function, wrapped in HTTP error checking
    ID_handle_retrieved = False
    fetch_attempts = 0
    while not ID_handle_retrieved and fetch_attempts < max_fetch_attempts:
        try:
            ID_handle = http_method(**kwargs)
            ID_handle_retrieved = True
        # HTTP Errors
        except urllib.error.HTTPError as error:
            # Error code 429: Too Many Requests
            if error.code == 429:
                fetch_attempts += 1
                print("HTTP Error " + str(error.code) + ": " + str(error.reason))
                print(
                    "Fetch Attempt: "
                    + str(fetch_attempts)
                    + "/"
                    + str(max_fetch_attempts)
                )
                print("Sleeping for " + str(sleep_time) + " seconds before retrying.")
                time.sleep(sleep_time)
            # General HTTP Error Code, non specific
            else:
                fetch_attempts += 1
                print("HTTP Error " + str(error.code) + ": " + str(error.reason))
                print(
                    "Fetch Attempt: "
                    + str(fetch_attempts)
                    + "/"
                    + str(max_fetch_attempts)
                )
                print("Retrying record fetching.")
        # URL Errors
        except urllib.error.URLError as error:
            fetch_attempts += 1
            print("URL Error: " + str(error.reason))
            print(
                "Fetch Attempt: " + str(fetch_attempts) + "/" + str(max_fetch_attempts)
            )
            print("Retrying record fetching.")

        # If the maximum number of fetch attempts has been exceeded
        if fetch_attempts == max_fetch_attempts and not ID_handle_retrieved:
            raise NCBImetaErrors.ErrorMaxFetchAttemptsExceeded(str(kwargs))

    return ID_handle


def sql_sanitize(sql_name):
    """
    Return a SQL name (table or column) cleaned of problematic characters.
    ex. punctuation )(][; whitespace
    Don't use with values, which can be properly escaped with parameterization.
    Ideally retaining only alphanumeric char.
    Credits: Donald Miner, Source: StackOverflow, DateAccessed: 2020-02-20
    """
    sanitize_name = "".join(char for char in sql_name if char.isalnum())
    return sanitize_name
