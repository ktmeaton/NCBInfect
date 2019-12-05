"""
NCBImeta Test - Annotate Replace

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

def test_annotatereplace_run():
    '''Test the NCBImetaAnnotateReplace application for run completion'''
    # Use the test database
    test_db = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test.sqlite")
    test_annotfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_annot.txt')
    # If the test_db doesn't alread exist, run the test cmd from test_ncbimeta
    if not os.path.exists(test_db): test_ncbimeta.test_ncbimeta_run()
    test_table = 'BioSample'
    test_cmd = ("ncbimeta/NCBImetaAnnotateReplace.py --database " + test_db +
                " --table  " + test_table +
                " --annotfile " + test_annotfile)
    # test NCBImetaAnnotateReplace through a subprocess
    returned_value = subprocess.call(test_cmd, shell=True)
    # If it returns a non-zero value, it failed
    assert returned_value == 0

#def test_annotateconcatenate_multipleEntry(tmpdir):
    #To Be done

#def test_annotatereplace_ErrorDBNotExists(tmpdir):
    #To Be done

#def test_annotatereplace_ErrorAnnotFileNotExists(tmpdir):
    #To Be done

#def test_annotatereplace_ErrorTableNotInDB(tmpdir):
    #To Be done
