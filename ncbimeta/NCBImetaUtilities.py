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

def flatten_dict(input_dict, pre=[]):
    '''
    Yield a flattened generator list from a nested dictionary.

    Parameters:
    input_dict (dict): The nested dictionary to flatten.
    pre (list): The prefix path of keys to follow.

    Returns:
    Generator object list of flattened path elements of the dictionary key values.
    '''
    # If we are working with a dictionary for the value/payload, use recursion
    if isinstance(input_dict, dict):
        for key,value in input_dict.items():
            if isinstance(value, dict):
                for flat_path in flatten_dict(value, pre + [key]):
                    yield flat_path
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for flat_path in flatten_dict(v, pre + [key]):
                        yield flat_path
            else:
                yield pre + [key, value]
    # If the value/payload is a simple value, yield, including prefix
    else:
        yield pre + [input_dict]

def xml_find_attr(xml_root, node_name, attr_name, attr_dict):
    '''
    Recursive search of xml to find a desired node-attribute combination.

    Parameters:
        xml_root (minidom doc): xml object as a minidom documentElement
        node_name (str): node name to search for
        attr_name (str or list): attribute name to search for
        attr_dict (dict): dictionary object to store retrieved values

    Returns:
        Void. Internal recursion calls will return a node value,
        which is either str or None. The external call does not return anything,
        instead it mutates a dictionary.
    '''
    # The lowest depth/recursion end, when there are no more child nodes.
    if not xml_root.childNodes:
        # Pesky empty spaces in unicode strings
        if xml_root.nodeValue and xml_root.nodeValue.replace(" ",""):
            return(xml_root.nodeValue)
    # All other recursion possibilties, when there are still child nodes
    else:
        for child_node in xml_root.childNodes:
            # Recursive call, this value will be the node value at the lowest depth
            value = xml_find_attr(child_node,node_name,attr_name,attr_dict)

            # The node we're going to operate on, could be current root or child
            target_node = None

            # Most NCBI tables: using an attribute to get a specific node value
            if xml_root.nodeName == node_name and xml_root.attributes:
                target_node = xml_root

            # The special SRA table: using an attribute to get an attribute value
            elif child_node.nodeName == node_name and child_node.attributes:
                target_node = child_node

            # This fails if the node name doesn't match, or has no attributes
            if target_node:
                for item in target_node.attributes.items():
                    # complex node-attribute, grab node value associated with attribute
                    if type(attr_name) == list and value:
                        if item[0] == attr_name[1] and item[1] == attr_name[0]:
                             attr_dict[attr_name[0]] = str(value)
                    # The following code is suspected to be unnecssary
                    # simple name, grab associated attribute value
                    elif type(attr_name) == str:
                        if(attr_name == item[0]):
                            attr_dict[attr_name] = str(item[1])

def xml_find_node(xml_root, node_name, node_dict):
    '''
    Recursive search of xml to find a desired node value.

    Parameters:
        xml_root (minidom doc): xml object as a minidom documentElement
        node_name (str): node name to search for
        attr_dict (dict): dictionary object to store retrieved values

    Returns:
        Void. Internal recursion calls will return a node value,
        which is either str or None. The external call does not return anything,
        instead it mutates a dictionary.
    '''
    # The lowest depth/recursion end, when there are no more child nodes.
    if not xml_root.childNodes:
        # Pesky empty spaces in unicode strings
        if xml_root.nodeValue and xml_root.nodeValue.replace(" ",""):
            return(xml_root.nodeValue)
    else:
        for child_node in xml_root.childNodes:
            value = xml_find_node(child_node,node_name,node_dict)
            if node_name == xml_root.nodeName:
                if value:
                    node_dict[node_name] = str(value)
                    return(value)
                # ignore text nodes, this is only for SRA library layout
                else:
                    if child_node.nodeName != "#text":
                        node_dict[node_name] = str(child_node.nodeName)


def xml_search(xml_root, search_list, current_tag, column_name, xml_dict):
    '''Search xml_root for nodes, attributes in search_list, update node_dict'''
    # Search query (as tag or attribute)
    tag_xpath = ".//" + current_tag
    alt_attrib = current_tag
    print("Tag xpath:", tag_xpath)
    print("Alt Attribute:", alt_attrib)
    #print(etree.tostring(xml_root, pretty_print = True))

    # Modify dict (stop recursion), if we're at the end of the list
    if search_list.index(current_tag) == len(search_list) - 1:
        # First try tag as node
        # Attempt to check search results, exception if there are none
        try:
            search_result = xml_root.findall(tag_xpath)[0]
            print("Search Result End:", search_result)
            search_result_text = search_result.text
            # Str conversion here is mainly for None results
            xml_dict[column_name] = str(search_result_text)
        except IndexError:
            xml_dict[column_name] = ""
        # Then try tag as attribute
        # Something
    else:
        # First try tag as node, allowing multiple results
        next_tag = search_list[search_list.index(current_tag) + 1]
        print("Next Tag:", next_tag)
        print("Current Root Before:", etree.tostring(xml_root))
        search_results = xml_root.findall(tag_xpath)
        # If there are no results, this is an attribute matching situation
        if not search_results:
            print("NO RESULTS")
            # Retry the search with unescaped characters
            xml_root_string = etree.tostring(xml_root)
            open_char = "&lt;"
            close_char = "&gt;"
            xml_root_string = str(xml_root_string).replace(open_char,"<").replace(close_char,">").strip()
            xml_root_string = str(xml_root_string).replace("\\n","").replace("\\t","")
            print("Current Root After:", xml_root_string)
            # Strip off the first 2 char (b') and the final char '
            print("Current Root Mod:", xml_root_string[2:-1])
            xml_root = etree.fromstring(xml_root_string[2:-1])

            search_results = xml_root.findall(tag_xpath)
            # If attributes of interest are present and matching
            try:
                if xml_root.get(current_tag) == next_tag:
                    xml_dict[column_name] = xml_root.text
            except AttributeError:
                # Fails if no attributes, just a non-existent node
                xml_dict[column_name] = ""
        # If there were multiple results, need to keep searching recursively
        for result in search_results:
            print("Search Result Ongoing:", result)
            # Check if the xml_result contains cda  ta
            result_text = result.text.strip()
            if result_text:
                # Check if result contains CDATA
                first_char = result_text[0]
                last_char = result_text[-1]
                if first_char == "<" and last_char == ">":
                    # Reformat CDATA as complete XML
                    result_text = ("<" + current_tag + ">" + result_text + "</" + current_tag + ">")
                    print("Working Text Edit:", result_text)
                    result = etree.fromstring(result_text)
                    print(etree.tostring(result))
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
