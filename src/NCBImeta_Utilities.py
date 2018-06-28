# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:10:08 2016

@author: Katherine Eaton
"""

import os
from sys import platform as _platform
import sqlite3
import xml.etree.ElementTree as ET


def os_check():
    ''' Return OS Separator'''
    if 'linux' in _platform:
        return "/"
    elif 'cygwin' in _platform:
        return "/"
    elif "win" in _platform:
        return "\\"
    else:
        return "/"

def check_accessory_dir(output_dir):
    OS_SEP = os_check()
    output_dir = output_dir + OS_SEP
    if not os.path.exists(output_dir + OS_SEP + "log"):
        os.makedirs(output_dir + OS_SEP + "log")
    if not os.path.exists(output_dir + OS_SEP + "database"):
        os.makedirs(output_dir + OS_SEP + "database")
    #if not os.path.exists(output_dir + OS_SEP + "annotate"):
    #    os.makedirs(output_dir + OS_SEP + "annotate")
    #return 0

def table_exists(db_cur, table_name):
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(table_name)
    return db_cur.execute(query).fetchone() is not None

def flatten_dict(input_dict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(input_dict, dict):
        for key, value in input_dict.items():
            if isinstance(value, dict):
                for d in flatten_dict(value, [key] + pre):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in flatten_dict(v, [key] + pre):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield input_dict


def xml_find_rec(xml_root, node_name, attr_dict):
    if not xml_root.childNodes:
        # Pesky empty spaces in unicode strings
        if xml_root.nodeValue and xml_root.nodeValue.replace(" ",""):
            return(xml_root.nodeValue)
    else:
        for child_node in xml_root.childNodes:
            value = xml_find_rec(child_node,node_name,attr_dict)
            if value:
                for item in xml_root.attributes.items():
                    if node_name in item:
                        attr_dict[str(node_name)] = str(value)
                        return(value)


def xml_find_rec_bak2(xml_root, node_name, attr_dict):
    if xml_root.childNodes:
        for child_node in xml_root.childNodes:
            print("Descend: " + xml_find_rec(child_node,node_name))
        for key in xml_root.attributes.keys():
            if xml_root.attributes[key].value == node_name:
                print(xml_find_rec(xml_root.firstChild,node_name))
                return(xml_find_rec(xml_root.firstChild,node_name))
        #for child_node in xml_root.childNodes:
        #    xml_find_rec(child_node,node_name)
    else:
        print("Bottom: " + xml_root.wholeText)
        return(xml_root.wholeText)


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
