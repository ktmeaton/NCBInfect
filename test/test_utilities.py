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
from Bio import Entrez                      # Entrez queries (NCBI)
#-----------------------------------------------------------------------#
#                           Test Function                               #
#-----------------------------------------------------------------------#

def test_flatten_dict():
    '''Test the utility function flatten_dict (nested dict to list generator).'''
    test_dict = {'a' : 1,
                 'b' : {'c' : { 'd' : 1, 'e' : 2}},
                 'f' : [{'g' : 3, 'h' : 4}],
                 'i' : ['j', 'k', 'l', 5, 6, 7]}

    test_dict_flat_result = list(NCBImetaUtilities.flatten_dict(test_dict))
    test_dict_flat_expect = [['a', 1], ['b', 'c', 'd', 1], ['b', 'c', 'e', 2], ['f', 'g', 3],
        ['f', 'h', 4], ['i', 'j'], ['i', 'k'], ['i', 'l'], ['i', 5], ['i', 6], ['i', 7]]

    # Create a list that contains items that are different between the two
    # It was found that in diff versions of Py3, can't simply compare the lists
    # with the == operator because the order varies
    test_dict_diff = ([x for x in test_dict_flat_result if x not in test_dict_flat_expect] +
                      [x for x in test_dict_flat_expect if x not in test_dict_flat_result])

    # If the list is empty (length is 0) then the result is the same as expected
    assert len(test_dict_diff) == 0

def test_check_accessory_dir(tmpdir):
    '''Test the utility function check_accessory_dir (create log/ and database/).'''
    tmpdir = tmpdir.strpath
    NCBImetaUtilities.check_accessory_dir(tmpdir)
    assert os.path.exists(os.path.join(tmpdir,"log")) and os.path.exists(os.path.join(tmpdir,"database"))

def test_table_exists(tmpdir):
    '''Test the utility function table_exists (check if Table is present in sqlite db)'''
    # Connect to database and establish cursor for commands.
    tmpdir = tmpdir.strpath
    test_db = os.path.join(tmpdir, "test.sqlite")
    conn = sqlite3.connect(test_db)
    cur = conn.cursor()

    ## Create the database with a test Table
    table_name = "TestTable"
    sql_query = "Create TABLE IF NOT EXISTS " + table_name + " (id INTEGER)"
    cur.execute(sql_query)

    # Test Function Call
    assert NCBImetaUtilities.table_exists(cur, table_name)

def test_xml_find_attr_val():
    '''Test the utility function xml_find_attr (retrieve xml attribute payload)'''
    test_xml = "<Root><Stats><Stat category='chromosome_count' sequence_tag='all'>1</Stat></Stats></Root>"
    test_root = minidom.parseString(test_xml).documentElement
    test_node_name = "Stat"
    test_attr_name = ['chromosome_count', 'category']
    test_attr_dict = {}
    # Test Function Call
    NCBImetaUtilities.xml_find_attr(test_root,test_node_name,test_attr_name,test_attr_dict)
    assert test_attr_dict == {'chromosome_count': '1'}

def test_xml_find_attr_name():
    '''Test the utility function xml_find_attr (retrieve xml attribute name)'''
    test_xml = "<Root><Experiment acc='SRX6977650'/></Root>"
    test_root = minidom.parseString(test_xml).documentElement
    test_node_name = 'Experiment'
    test_attr_name = 'acc'
    test_attr_dict = {}
    # Test Function Call
    NCBImetaUtilities.xml_find_attr(test_root,test_node_name,test_attr_name,test_attr_dict)
    assert test_attr_dict == {'acc': 'SRX6977650'}

def test_xml_find_node():
    '''Test the utility function xml_find_attr (retrieve xml attribute payload)'''
    test_xml = "<Root><AssemblyAccession>GCA_003086155.1</AssemblyAccession></Root>"
    test_root = minidom.parseString(test_xml).documentElement
    test_node_name = "AssemblyAccession"
    test_node_dict = {}
    # Test Function Call
    NCBImetaUtilities.xml_find_node(test_root,test_node_name,test_node_dict)
    assert test_node_dict == {'AssemblyAccession':'GCA_003086155.1'}

def test_xml_find_node_child():
    '''Test the utility function xml_find_node (retrieve xml attribute child)'''
    test_xml = "<Root><LIBRARY_LAYOUT><PAIRED/></LIBRARY_LAYOUT></Root>"
    test_root = minidom.parseString(test_xml).documentElement
    test_node_name = 'LIBRARY_LAYOUT'
    test_node_dict = {}
    # Test Function Call
    NCBImetaUtilities.xml_find_node(test_root,test_node_name,test_node_dict)
    assert test_node_dict == {'LIBRARY_LAYOUT': 'PAIRED'}

def test_HTTPErrorCatch(tmpdir):
    '''Test the utility function HTTPErrorCatch (catch HTTP Errors)'''
    # Test query assembly
    test_ID = '5025191'
    test_email = 'ktmeaton@gmail.com'
    Entrez.email = test_email
    test_table = 'Assembly'
    test_max_tries = 10
    test_total_tries = 10
    test_sleep_between_tries = 0
    test_kwargs = {"db":test_table.lower(), "id":test_ID}
    test_entrez_method = Entrez.esummary

    for i in range(1, test_total_tries):
        ID_handle = NCBImetaUtilities.HTTPErrorCatch(test_entrez_method, test_max_tries, test_sleep_between_tries, **test_kwargs)
    try:
        ID_record = Entrez.read(ID_handle, validate=False)
        assert 1
    except RuntimeError:
        # The ID_handle was not succesfully retrieved or the data is not correct
        assert 0
