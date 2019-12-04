"""
NCBImeta Test - Main CLI (NCBImeta)

@author: Katherine Eaton
"""

#-----------------------------------------------------------------------#
#                         Modules and Packages                          #
#-----------------------------------------------------------------------#

import pytest                           # Testing suite
from ncbimeta import *                  # Main Program Import
from ncbimeta import NCBImetaErrors     # Error classes
import yaml                             # YAML config file parsing
import os                               # Filepath operations
import subprocess                       # Execute CLI/Shell

#-----------------------------------------------------------------------#
#                           Test Function                               #
#-----------------------------------------------------------------------#

def test_ncbimeta_run():
    '''Test the NCBImeta application for run completion'''
    # User the stripped down testing config file
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test1.yaml")
    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file
    # test the main NCBImeta.py through a subprocess
    returned_value = subprocess.call(test_cmd, shell=True)
    # If it returns a non-zero value, it failed
    assert returned_value == 0


def test_ncbimeta_ConfigFileNotExists(tmpdir):
    '''Test for error catching when a config file does not exist'''
    # This file is not created, just a tmp path
    config_file = os.path.join(tmpdir.strpath, "tmpfile")
    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file
    # Use a try-catch with the sub-process of module
    try:
        subprocess.check_output(test_cmd,
                                shell=True,
                                stderr=subprocess.STDOUT)
        # If an exception isn't raise then the assertion fails (0)
        assert 0
    except subprocess.CalledProcessError as e:
        # If the right error is raise, it's Error Class is in the output
        assert "ErrorConfigFileNotExists" in str(e.output)

def test_ncbimeta_ErrorConfigParameter():
    '''Test for error catching when a config file has improper parameters'''
    # User the stripped down testing config file
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test2.yaml")
    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file
    # test the main NCBImeta.py through a subprocess
    returned_value = subprocess.call(test_cmd, shell=True)
    # If it returns a non-zero value, it failed
    assert returned_value == 0
