# -*- coding: utf-8 -*-
"""
NCBI Metadata Database Utility Functions

@author: Katherine Eaton
"""

import os
from sys import platform as _platform
import sqlite3
import xml.etree.ElementTree as ET


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
    print(input_dict)
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
                    # simple name, gran associated attribute value
                    if type(attr_name) == str:
                        if(attr_name == item[0]):
                            attr_dict[attr_name] = str(item[1])
                    # complex node-attribute, grab nove value associated with attribute
                    elif type(attr_name) == list and value:
                        if item[0] == attr_name[1] and item[1] == attr_name[0]:
                             attr_dict[attr_name[0]] = str(value)

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
                else:
                    # ignore text nodes, this is only for SRA library layout
                    if child_node.nodeName != "#text":
                        node_dict[node_name] = str(child_node.nodeName)


def xml_find_attr_bak(xml_root, node_name, attr_name, attr_dict):
    if not xml_root.childNodes:
        # Pesky empty spaces in unicode strings
        if xml_root.nodeValue and xml_root.nodeValue.replace(" ",""):
            return(xml_root.nodeValue)
    else:
        for child_node in xml_root.childNodes:
            value = xml_find_attr(child_node,node_name,attr_name,attr_dict)
            if value:
                for item in xml_root.attributes.items():
                    if attr_name in item:
                        attr_dict[str(attr_name)] = str(value)
                        return(value)
            elif child_node.attributes:
                for item in child_node.attributes.items():
                    print(item)
                    if(attr_name == item[0]):
                        attr_dict[str(attr_name)] = str(item[1])


def xml_find_attr_bak2(xml_root, node_name, attr_name, attr_dict):
    if not xml_root.childNodes:
        # Pesky empty spaces in unicode strings
        if xml_root.nodeValue and xml_root.nodeValue.replace(" ",""):
            return(xml_root.nodeValue)
    else:
        for child_node in xml_root.childNodes:
            value = xml_find_attr(child_node,node_name,attr_name,attr_dict)
            #print(xml_root.nodeName, child_node.nodeName, value)
            if xml_root.nodeName == node_name and xml_root.attributes:
                for item in xml_root.attributes.items():
                    if type(attr_name) == str:
                        if(attr_name == item[0]):
                            attr_dict[str(attr_name)] = str(item[1])

                    elif type(attr_name) == list:
                        if item[0] == attr_name[1] and item[1] == attr_name[0]:
                             attr_dict[attr_name[0]] = value
            elif child_node.nodeName == node_name and child_node.attributes:
                for item in child_node.attributes.items():
                    if(attr_name == item[0]):
                        attr_dict[str(attr_name)] = str(item[1])

def xml_find_node_bak(xml_root, node_name, node_dict):
    if not xml_root.childNodes:
        # Pesky empty spaces in unicode strings
        if xml_root.nodeValue and xml_root.nodeValue.replace(" ",""):
            return(xml_root.nodeValue)
    else:
        for child_node in xml_root.childNodes:
            value = xml_find_node(child_node,node_name,node_dict)
            print(child_node, value)
            if value:
                if node_name == xml_root.nodeName:
                    node_dict[str(node_name)] = str(value)
                    return(value)



class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Original Author: Duncan McGregor
    Orignal URL: https://code.activestate.com/recipes/410469-xml-as-dictionary/
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
