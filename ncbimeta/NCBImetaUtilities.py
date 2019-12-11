# -*- coding: utf-8 -*-
"""
NCBImeta Utility Functions

@author: Katherine Eaton
"""

#-----------------------------------------------------------------------#
#                         Modules and Packages                          #
#-----------------------------------------------------------------------#

import os                               # Filepath operations
from sys import platform as _platform   # Get Platform for OS separator
import sqlite3                          # Database storage and queries
import xml.etree.ElementTree as ET      # XML Processing
from ncbimeta import NCBImetaErrors     # NCBImeta Error classes
import urllib.error                     # HTTP Error Catching
import time                             # Allow sleeping of processes
from lxml import etree                  # XML Parsing

#-----------------------------------------------------------------------#
#                         Utility Functions                             #
#-----------------------------------------------------------------------#

def check_accessory_dir(output_dir):
    '''
    Check if the accessory directories already exist.

    Parameters:
    output_dir(str): Path to the output directory.
    '''
    if not os.path.exists(os.path.join(output_dir,"log")):
        os.makedirs(os.path.join(output_dir,"log"))
    if not os.path.exists(os.path.join(output_dir,"database")):
        os.makedirs(os.path.join(output_dir,"database"))

def table_exists(db_cur, table_name):
    '''
    Return the result of fetching a table name from a sqlite database to check if it exists.

    Parameters:
    db_cur(Cursor): A sqlite cursor connection.
    table_name(str): Name of a table in the sqite database.
    '''
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(table_name)
    return db_cur.execute(query).fetchone() is not None

def xml_search(xml_root, search_list, current_tag, column_name, xml_dict):
    '''
    Search xml_root for nodes, attributes in search_list and update node_dict.

    Parameters:
    xml_root (ElementTree): xml document as etree object
    search_list (list): list of nodes and attributes in descending hierarchy
    current_tag (str): current tag (or attribute/value) to be searching
    xml_dict (dict): A dictionary to modify and store found values.

    Returns:
    Void. Instead the function mutates the dictionary xml_dict.
    '''
    # Search query (as tag or attribute)
    tag_xpath = ".//"  + current_tag
    print("CURRENT TAG:", current_tag)
    # Modify dict (stop recursion), if we're at the end of the list
    if search_list.index(current_tag) == len(search_list) - 1:
        # First tag as attribute
        try:
            fetch_attrib = xml_root.get(current_tag)
            print("FETCH ATTRIB1:", fetch_attrib)
            if fetch_attrib:
                # Add or append attribute to xml dictionary
                xml_dict[column_name].append(fetch_attrib)
        except AttributeError:
            pass
        # Then try tag as node
        # Attempt to check search results, exception if there are none
        try:
            search_results = xml_root.findall(tag_xpath)
            for result in search_results:
                print("SEARCH RESULT NODE:", result)
                if result.text:
                    # Remove empty string elements
                    result_text = result.text.strip()
                    print("SEARCH RESULT1 TEXT:", result_text)
                    # Str conversion here is mainly for None results
                    xml_dict[column_name].append(str(result_text))
                # Or if has no text but does have child nodes
                elif len(result) > 0:
                    # Experiment with first child node as value
                    print("SEARCH RESULT1 CHILD NODE:", result[0].tag)
                    xml_dict[column_name].append(result[0].tag)
        except IndexError:
            pass
    else:
        # First try tag as node, allowing multiple results
        next_tag = search_list[search_list.index(current_tag) + 1]
        print("NEXT TAG:", next_tag)
        #print("Current Root Before:", etree.tostring(xml_root))
        search_results = xml_root.findall(tag_xpath)
        # If there are no results, this is an attribute matching situation
        if not search_results:
            #print("NO RESULTS")
            # Retry the search with unescaped characters
            xml_root_string = etree.tostring(xml_root)
            open_char = "&lt;"
            close_char = "&gt;"
            xml_root_string = str(xml_root_string).replace(open_char,"<").replace(close_char,">").strip()
            xml_root_string = str(xml_root_string).replace("\\n","").replace("\t","")
            #print("Current Root After:", xml_root_string)
            # Strip off the first 2 char (b') and the final char '
            #print("Current Root Mod:", xml_root_string[2:-1])
            xml_root = etree.fromstring(xml_root_string[2:-1])

            search_results = xml_root.findall(tag_xpath)
            # If attributes of interest are present and matching
            try:
                if xml_root.get(current_tag) == next_tag:
                    xml_dict[column_name].append(xml_root.text)
            except AttributeError:
                # Fails if no attributes, just a non-existent node
                pass
        # If there were multiple results, need to keep searching recursively
        for result in search_results:
            #print("Search Result Ongoing:", result)
            # If there was a result, but not a text node, try attribute
            fetch_attrib = ""
            if not result.text:
                fetch_attrib = result.get(next_tag)
                print("FETCH ATTRIB2:", fetch_attrib)
                #print("ATTEMPTING GET2:", fetch_attrib)
                if fetch_attrib:
                    xml_dict[column_name].append(fetch_attrib)
            else:
                # Check if the xml_result contains CDATA
                result_text = result.text.strip()
                print("SEARCH RESULT2 TEXT:", result_text)
                if result_text:
                    # Check if result contains CDATA
                    first_char = result_text[0]
                    last_char = result_text[-1]
                    if first_char == "<" and last_char == ">":
                        # Reformat CDATA as complete XML
                        result_text = ("<" + current_tag + ">" + result_text + "</" + current_tag + ">")
                        #print("Working Text Edit:", result_text)
                        result = etree.fromstring(result_text)
                        #print(etree.tostring(result))

            # If an attribute wasn't succesfully fetched, need recursion
            if not fetch_attrib:
                xml_search(result, search_list, next_tag, column_name, xml_dict)


def HTTPErrorCatch(http_method, max_fetch_attempts, sleep_time, **kwargs):
    '''
    Return result of http_method and check if an HTTP Error is generated

    Parameters:
    http_method (function): An http record-fetching or searching method.
    max_fetch_attempts (int): Maximum number of tries for fetching a record_dict.
    sleep_time (float): Number of seconds to wait in between fetch read_attempts.
    kwargs(dict): keyword arguments for the http_method function.
    '''
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
                print("Fetch Attempt: " + str(fetch_attempts) + "/" + str(max_fetch_attempts))
                print("Sleeping for " + str(sleep_time) + " seconds before retrying.")
                time.sleep(sleep_time)
            # General HTTP Error Code, non specific
            else:
                fetch_attempts += 1
                print("HTTP Error " + str(error.code) + ": " + str(error.reason))
                print("Fetch Attempt: " + str(fetch_attempts) + "/" + str(max_fetch_attempts))
                print("Retrying record fetching.")
        # URL Errors
        except urllib.error.URLError as error:
            fetch_attempts += 1
            print("URL Error: " + str(error.reason))
            print("Fetch Attempt: " + str(fetch_attempts) + "/" + str(max_fetch_attempts))
            print("Retrying record fetching.")


        # If the maximum number of fetch attempts has been exceeded
        if fetch_attempts == max_fetch_attempts and not ID_handle_retrieved:
            raise NCBImetaErrors.ErrorMaxFetchAttemptsExceeded(ID)

    return ID_handle
