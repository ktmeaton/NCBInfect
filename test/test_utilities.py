"""
NCBImeta Test - Utility Functions

@author: Katherine Eaton
"""

#-----------------------------------------------------------------------#
#                         Modules and Packages                          #
#-----------------------------------------------------------------------#

import pytest                               # Testing suite
from ncbimeta import NCBImetaUtilities      # Utility Functions
import os                                   # Filepath and directory operations
import sqlite3                              # Database storage and queries
from xml.dom import minidom                 # XML Processing
#-----------------------------------------------------------------------#
#                           Test Function                               #
#-----------------------------------------------------------------------#

def test_flatten_dict():
    '''
    Test the utility function flatten_dict (nested dict to list generator).
    '''
    test_dict = {'a' : 1,
                 'b' : {'c' : { 'd' : 1, 'e' : 2}},
                 'f' : [{'g' : 3, 'h' : 4}],
                 'i' : ['j', 'k', 'l', 5, 6, 7]}

    test_dict_flat_result = list(NCBImetaUtilities.flatten_dict(test_dict))
    test_dict_flat_expect = [['a', 1], ['b', 'c', 'd', 1], ['b', 'c', 'e', 2], ['f', 'g', 3],
        ['f', 'h', 4], ['i', 'j'], ['i', 'k'], ['i', 'l'], ['i', 5], ['i', 6], ['i', 7]]
    assert test_dict_flat_result == test_dict_flat_expect

def test_check_accessory_dir():
    '''
    Test the utility function check_accessory_dir (create log/ and database/).
    '''
    current_dir = os.path.dirname(os.path.realpath(__file__))
    NCBImetaUtilities.check_accessory_dir(current_dir)
    assert os.path.exists(os.path.join(current_dir,"log") and os.path.exists(os.path.join(current_dir,"database")))
    # Cleanup testing accessory dir
    os.rmdir(os.path.join(current_dir,"log"))
    os.rmdir(os.path.join(current_dir,"database"))

def test_table_exists():
    '''
    Test the utility function table_exists (check if Table is present in sqlite db)
    '''
    # Connect to database and establish cursor for commands.
    current_dir = os.path.dirname(os.path.realpath(__file__))
    test_db = os.path.join(current_dir,"test.sqlite")
    conn = sqlite3.connect(test_db)
    cur = conn.cursor()

    ## Create the database with a test Table
    table = "TestTable"
    sql_query = ("Create TABLE IF NOT EXISTS " + table +
        " (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " +
        table + "_id TEXT)")
    cur.execute(sql_query)
    # Test Function Call
    assert NCBImetaUtilities.table_exists(cur, "TestTable")
    # Remove test database
    os.remove(test_db)

def test_xml_find_attr():
    '''
    Test the utility function xml_find_attr (retrieve xml attribute payload)
    '''
    test_xml = "<Root><Stats><Stat category='chromosome_count' sequence_tag='all'>1</Stat></Stats></Root>"
    test_root = minidom.parseString(test_xml).documentElement
    test_node_name = "Stat"
    test_attr_name = ['chromosome_count', 'category']
    test_attr_dict = {}
    # Test Function Call
    NCBImetaUtilities.xml_find_attr(test_root,test_node_name,test_attr_name,test_attr_dict)
    assert test_attr_dict == {'chromosome_count': '1'}

def test_xml_find_node():
    '''
    Test the utility function xml_find_attr (retrieve xml attribute payload)
    '''
    test_xml = "<Root><AssemblyAccession>GCA_003086155.1</AssemblyAccession></Root>"
    test_root = minidom.parseString(test_xml).documentElement
    test_node_name = "AssemblyAccession"
    test_node_dict = {}
    # Test Function Call
    NCBImetaUtilities.xml_find_node(test_root,test_node_name,test_node_dict)
    assert test_node_dict == {'AssemblyAccession':'GCA_003086155.1'}
