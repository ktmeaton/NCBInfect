"""
NCBImeta Test - Annotate Concatenate

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

def test_annotateconcatenate_run():
    '''Test the NCBImetaAnnotateConcatenate application for run completion'''
    # Use the test database
    test_db = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test.sqlite")
    test_annotfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_annot.txt')
    # If the test_db doesn't alread exist, run the test cmd from test_ncbimeta
    if not os.path.exists(test_db): test_ncbimeta.test_ncbimeta_run()
    test_table = 'BioSample'
    test_cmd = ("ncbimeta/NCBImetaAnnotateConcatenate.py --database " + test_db +
                " --table  " + test_table +
                " --annotfile " + test_annotfile)
    # test the main NCBImeta.py through a subprocess
    returned_value = subprocess.call(test_cmd, shell=True)
    # If it returns a non-zero value, it failed
    assert returned_value == 0

def test_annotateconcatenate_missingEntry(tmpdir):
    '''Test the NCBImetaAnnotateConcatenate application for a missing Entry'''
    # Prep the db and annot file
    test_db = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test.sqlite")
    src_annotfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_annot.txt')
    test_annotfile = os.path.join(tmpdir,'tmp_annot.txt')
    test_missing_entry = "MissingAccession123"

    # Read in the file
    with open(src_annotfile, 'r') as file: filedata = file.read()
    # Replace the target data
    filedata = filedata.replace('SAMN12991206', 'OUTPUT_DIR : ' + test_missing_entry )
    # Write to the destination file
    with open(test_annotfile, 'a') as file: file.write(filedata)

    # If the test_db doesn't alread exist, run the test cmd from test_ncbimeta
    if not os.path.exists(test_db): test_ncbimeta.test_ncbimeta_run()
    test_table = 'BioSample'
    test_cmd = ("ncbimeta/NCBImetaAnnotateConcatenate.py --database " + test_db +
            " --table  " + test_table +
            " --annotfile " + test_annotfile)

    # Cleanup
    os.remove(test_annotfile)

#def test_annotateconcatenate_multipleEntry(tmpdir):
    #To Be done

#def test_annotateconcatenate_ErrorDBNotExists(tmpdir):
    #To Be done

#def test_annotateconcatenate_ErrorAnnotFileNotExists(tmpdir):
    #To Be done

#def test_annotateconcatenate_ErrorTableNotInDB(tmpdir):
    #To Be done
