"""
NCBImeta Test - Join

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

def test_join_run():
    '''Test the NCBImetaJoin application for run completion'''
    # Use the test database
    test_db = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test.sqlite")
    # If the test_db doesn't alread exist, run the test cmd from test_ncbimeta
    if not os.path.exists(test_db): test_ncbimeta.test_ncbimeta_run()
    test_anchor_table = 'BioSample'
    test_final_table = 'Master'
    test_accessory_table = "\'BioProject Assembly SRA Nucleotide\'"
    test_unique_field = "\'BioSampleAccession BioSampleAccessionSecondary BioSampleBioProjectAccession\'"
    test_cmd = ("ncbimeta/NCBImetaJoin.py --database " + test_db +
                " --final " + test_final_table  +
                " --anchor " + test_anchor_table +
                " --accessory " + test_accessory_table +
                " --unique " + test_unique_field)

    # test NCBImetaJoin through a subprocess
    returned_value = subprocess.call(test_cmd, shell=True)
    # If it returns a non-zero value, it failed
    assert returned_value == 0

#def test_join_ErrorDBNotExists():
    #To Be Done

#def test_join_ErrorTableNotInDB():
    #To Be Done

#def test_join_ErrorEntryNotInDB():
    #To Be Done

#def test_join_ErrorColumnsNotUnique():
    #To Be Done

#def test_join_unicode():
    #To Be Done
