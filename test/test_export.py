"""
NCBImeta Test - Export

@author: Katherine Eaton
"""

#-----------------------------------------------------------------------#
#                         Modules and Packages                          #
#-----------------------------------------------------------------------#

import pytest                             # Testing suite
from ncbimeta import *                    # Main Program
import os                                 # Filepath operations
import test.test_ncbimeta                 # Run the program to create test db
import subprocess                         # Execute CLI/Shell

#-----------------------------------------------------------------------#
#                           Test Function                               #
#-----------------------------------------------------------------------#

def test_export_run():
    '''Test the NCBImetaExport application for run completion'''
    # Use the test database
    test_db = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test.sqlite")
    test_output_dir = os.path.dirname(os.path.abspath(__file__))
    # If the test_db doesn't alread exist, run the test cmd from test_ncbimeta
    if not os.path.exists(test_db): test_ncbimeta.test_ncbimeta_run()
    test_cmd = ("ncbimeta/NCBImetaExport.py --database " + test_db +
                " --outputdir " + test_output_dir)

    # test NCBImetaExport through a subprocess
    returned_value = subprocess.call(test_cmd, shell=True)
    # If it returns a non-zero value, it failed
    assert returned_value == 0

def test_export_assemblyvalues(assembly_table_data):
    '''
    Test the integrity of the Assembly table values based on expected values.

    Parameters:
    assembly_table_data (fixture): Dict fixture of Assembly table data from conftest.py
    '''
    # Setup the assembly table file
    test_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_Assembly.txt")
    test_file = open(test_filename,'r')
    # Retrieve the headers and fields
    test_column_list = test_file.readline().strip('\n').split("\t")
    # Add empty tab on the end for empty comment field
    test_metadata_list = (test_file.readline().strip('\n') + "\t" + "").split("\t")
    # Populate the dict with data
    test_dict = {}

    for i in range(0,len(test_column_list)):
        key = test_column_list[i]
        value = test_metadata_list[i]
        test_dict[key] = value
    # Test whether the values are as expected
    assert test_dict == assembly_table_data
    #Cleanup
    test_file.close()

def test_export_bioprojectvalues(bioproject_table_data):
    '''
    Test the integrity of the BioProject table values based on expected values.

    Parameters:
    bioproject_table_data (fixture): Dict fixture of BioProject table data from conftest.py
    '''
    # Setup the assembly table file
    test_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_BioProject.txt")
    test_file = open(test_filename,'r')
    # Retrieve the headers and fields
    test_column_list = test_file.readline().strip('\n').split("\t")
    test_metadata_list = (test_file.readline().strip('\n') + "\t" + "").split("\t")
    # Populate the dict with data
    test_dict = {}
    for i in range(0,len(test_column_list)):
        key = test_column_list[i]
        value = test_metadata_list[i]
        test_dict[key] = value
    # Test whether the values are as expected
    assert test_dict == bioproject_table_data
    #Cleanup
    test_file.close()

def test_export_biosamplevalues(biosample_table_data):
    '''
    Test the integrity of the BioSample table values based on expected values.

    Parameters:
    biosample_table_data (fixture): Dict fixture of BioSample table data from conftest.py
    '''
    # Setup the assembly table file
    test_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_BioSample.txt")
    test_file = open(test_filename,'r')
    # Retrieve the headers and fields
    test_column_list = test_file.readline().strip('\n').split("\t")
    test_metadata_list = (test_file.readline().strip('\n') + "\t" + "").split("\t")
    # Populate the dict with data
    test_dict = {}
    for i in range(0,len(test_column_list)):
        key = test_column_list[i]
        value = test_metadata_list[i]
        test_dict[key] = value
    # Test whether the values are as expected
    assert test_dict == biosample_table_data
    #Cleanup
    test_file.close()

def test_export_nucleotidevalues(nucleotide_table_data):
    '''
    Test the integrity of the Nucleotide table values based on expected values.

    Parameters:
    nucleotide_table_data (fixture): Dict fixture of Nucleotide table data from conftest.py
    '''
    # Setup the assembly table file
    test_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_Nucleotide.txt")
    test_file = open(test_filename,'r')
    # Retrieve the headers and fields
    test_column_list = test_file.readline().strip('\n').split("\t")

    # Populate the dict with data
    test_dict = {}
    read_line = test_file.readline().strip('\n')
    while read_line:
        test_metadata_list = (read_line + "\t" + "").split("\t")
        for i in range(0,len(test_column_list)):
            key = test_column_list[i]
            value = test_metadata_list[i]
            # Check if key is in dict, if not create as list
            if key not in test_dict:
                test_dict[key] = [value]
            # Otherwise, append to it
            else:
                test_dict[key].append(value)

        read_line = test_file.readline().strip('\n')

    # Test whether the values are as expected
    assert test_dict == nucleotide_table_data
    #Cleanup
    test_file.close()

def test_export_pubmedvalues(pubmed_table_data):
    '''
    Test the integrity of the Pubmed table values based on expected values.

    Parameters:
    pubmed_table_data (fixture): Dict fixture of Pubmed table data from conftest.py
    '''
    # Setup the assembly table file
    test_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_Pubmed.txt")
    test_file = open(test_filename,'r')
    # Retrieve the headers and fields
    test_column_list = test_file.readline().strip('\n').split("\t")
    # Add an extra empty string for the empty comment
    test_metadata_list = (test_file.readline().strip('\n')  + "\t" + "").split("\t")
    # Populate the dict with data
    test_dict = {}
    for i in range(0,len(test_column_list)):
        key = test_column_list[i]
        value = test_metadata_list[i]
        test_dict[key] = value

    # Test whether the values are as expected
    assert test_dict == pubmed_table_data
    #Cleanup
    test_file.close()

def test_export_sravalues(sra_table_data):
    '''
    Test the integrity of the SRA table values based on expected values.

    Parameters:
    sra_table_data (fixture): Dict fixture of SRA table data from conftest.py
    '''
    # Setup the assembly table file
    test_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_SRA.txt")
    test_file = open(test_filename,'r')
    # Retrieve the headers and fields
    test_column_list = test_file.readline().strip('\n').split("\t")

    # Populate the dict with data
    test_dict = {}
    read_line = test_file.readline().strip('\n')
    while read_line:
        test_metadata_list = (read_line + "\t" + "").split("\t")
        for i in range(0,len(test_column_list)):
            key = test_column_list[i]
            value = test_metadata_list[i]
            # Check if key is in dict, if not create as list
            if key not in test_dict:
                test_dict[key] = [value]
            # Otherwise, append to it
            else:
                test_dict[key].append(value)

        read_line = test_file.readline().strip('\n')

    # Test whether the values are as expected
    assert test_dict == sra_table_data
    #Cleanup
    test_file.close()

# def test_export_mastervalues(assembly_table_data,
#                                 bioproject_table_data,
#                                 biosample_table_data,
#                                 nucleotide_table_data,
#                                 pubmed_table_data,
#                                 sra_table_data):
#     '''
#     Test the integrity of the Master table values based on expected values.
#
#     Parameters:
#     biosample_table_data (fixture): Dict fixture of BioSample table data from conftest.py
#     '''
#     # Setup the assembly table file
#     test_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_Master.txt")
#     test_file = open(test_filename,'r')
#     # Retrieve the headers and fields
#     test_column_list = test_file.readline().strip('\n').split("\t")
#     test_metadata_list = test_file.readline().strip('\n').split("\t")
#     # Populate the dict with data
#     test_dict = {}
#     for i in range(0,len(test_column_list)):
#         key = test_column_list[i]
#         value = test_metadata_list[i]
#         test_dict[key] = value
#
#
#     # Construct the master_table_data
#     master_table_data = {'id':'1'}
#     # Nucleotide and sra are multi-row tables
#     for record in nucleotide_table_data:
#         # Concatenate the values
#         unique_value_list = list(set(nucleotide_table_data[record]))
#         nucleotide_table_data[record] = ";".join(unique_value_list)
#
#     for record in sra_table_data:
#         # Concatenate the values
#         unique_value_list = list(set(sra_table_data[record]))
#         sra_table_data[record] = ";".join(unique_value_list)
#
#     for table in assembly_table_data, bioproject_table_data, biosample_table_data, nucleotide_table_data, pubmed_table_data, sra_table_data:
#         table.pop('id', None)
#         master_table_data.update(table)
#
#     # Test whether the values are as expected
#     assert test_dict == master_table_data
#     #Cleanup
#     test_file.close()
