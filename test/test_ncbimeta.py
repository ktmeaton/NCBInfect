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
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test.yaml")
    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file
    # test the main NCBImeta.py through a subprocess
    returned_value = subprocess.call(test_cmd, shell=True)
    # If it returns a non-zero value, it failed
    assert returned_value == 0

def test_ncbimeta_noflatmode(tmpdir):
    '''Test the NCBImeta application without flat mode'''
    # Use the stripped down testing config file, rewrite OUTPUT_DIR value
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test.yaml")
    test_cmd = "ncbimeta/NCBImeta.py --config " + config_file
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

def test_ncbimeta_ConfigFileNotYAML(tmpdir):
    '''Test for error catching when a config file has improper format'''
    # User the empty config file
    tmpdir = tmpdir.strpath
    config_file_name = os.path.join(tmpdir,'tmp_config.yaml')
    config_file = open(config_file_name, 'a').close()

    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file_name
    # Use a try-catch with the sub-process of module
    try:
        subprocess.check_output(test_cmd,
                                shell=True,
                                stderr=subprocess.STDOUT)
        # If an exception isn't raise then the assertion fails (0)
        assert 0
    except subprocess.CalledProcessError as e:
        # If the right error is raise, it's Error Class is in the output
        assert "ErrorConfigYAMLFormat" in str(e.output)
    os.remove(config_file_name)

def test_ncbimeta_ErrorConfigParameter_OUTPUT_DIR(tmpdir):
    '''Test for error catching when a config file has improper parameters'''
    # Prep the config file contents
    tmpdir = tmpdir.strpath
    config_file_name = os.path.join(tmpdir,'tmp_config.yaml')
    config_file = open(config_file_name, 'w')
    config_file.write('OUTPUT_DIRR: output')
    config_file.close()

    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file_name
    # Use a try-catch with the sub-process of module
    try:
        subprocess.check_output(test_cmd,
                                shell=True,
                                stderr=subprocess.STDOUT)
        # If an exception isn't raise then the assertion fails (0)
        assert 0
    except subprocess.CalledProcessError as e:
        # If the right error is raise, it's Error Class is in the output
        assert "ErrorConfigParameter" in str(e.output)
    # Cleanup
    os.remove(config_file_name)

def test_ncbimeta_ErrorConfigParameter_EMAIL(tmpdir):
    '''Test for error catching when a config file has improper parameters'''
    # Prep the config file contents
    tmpdir = tmpdir.strpath
    config_file_name = os.path.join(tmpdir,'tmp_config.yaml')
    config_file = open(config_file_name, 'w')
    config_file.write('OUTPUT_DIR: output' + '\n' +
                      'EMAILL: email')
    config_file.close()

    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file_name
    # Use a try-catch with the sub-process of module
    try:
        subprocess.check_output(test_cmd,
                                shell=True,
                                stderr=subprocess.STDOUT)
        # If an exception isn't raise then the assertion fails (0)
        assert 0
    except subprocess.CalledProcessError as e:
        # If the right error is raise, it's Error Class is in the output
        assert "ErrorConfigParameter" in str(e.output)
    # Cleanup
    os.remove(config_file_name)

def test_ncbimeta_ErrorConfigParameter_API_KEY(tmpdir):
    '''Test for error catching when a config file has improper parameters'''
    # Prep the config file contents
    tmpdir = tmpdir.strpath
    config_file_name = os.path.join(tmpdir,'tmp_config.yaml')
    config_file = open(config_file_name, 'w')
    config_file.write('OUTPUT_DIR: output' + '\n' +
                      'EMAIL: email' + '\n' +
                      'API_KEYY: api_key')
    config_file.close()

    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file_name
    # Use a try-catch with the sub-process of module
    try:
        subprocess.check_output(test_cmd,
                                shell=True,
                                stderr=subprocess.STDOUT)
        # If an exception isn't raise then the assertion fails (0)
        assert 0
    except subprocess.CalledProcessError as e:
        # If the right error is raise, it's Error Class is in the output
        assert "ErrorConfigParameter" in str(e.output)
    # Cleanup
    os.remove(config_file_name)

def test_ncbimeta_ErrorConfigParameter_FORCE_PAUSE_SECONDS(tmpdir):
    '''Test for error catching when a config file has improper parameters'''
    # Prep the config file contents
    tmpdir = tmpdir.strpath
    config_file_name = os.path.join(tmpdir,'tmp_config.yaml')
    config_file = open(config_file_name, 'w')
    config_file.write('OUTPUT_DIR: output' + '\n' +
                      'EMAIL: email' + '\n' +
                      'API_KEY: api_key' + '\n' +
                      'FORCE_PAUSE_SECONDSS: force_pause_seconds')
    config_file.close()

    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file_name
    # Use a try-catch with the sub-process of module
    try:
        subprocess.check_output(test_cmd,
                                shell=True,
                                stderr=subprocess.STDOUT)
        # If an exception isn't raise then the assertion fails (0)
        assert 0
    except subprocess.CalledProcessError as e:
        # If the right error is raise, it's Error Class is in the output
        assert "ErrorConfigParameter" in str(e.output)
    # Cleanup
    os.remove(config_file_name)

def test_ncbimeta_ErrorConfigParameter_DATABASE(tmpdir):
    '''Test for error catching when a config file has improper parameters'''
    # Prep the config file contents
    tmpdir = tmpdir.strpath
    config_file_name = os.path.join(tmpdir,'tmp_config.yaml')
    config_file = open(config_file_name, 'w')
    config_file.write('OUTPUT_DIR: output' + '\n' +
                      'EMAIL: email' + '\n' +
                      'API_KEY: api_key' + '\n' +
                      'FORCE_PAUSE_SECONDS: force_pause_seconds' + '\n' +
                      'DATABASEE: database')
    config_file.close()

    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file_name
    # Use a try-catch with the sub-process of module
    try:
        subprocess.check_output(test_cmd,
                                shell=True,
                                stderr=subprocess.STDOUT)
        # If an exception isn't raise then the assertion fails (0)
        assert 0
    except subprocess.CalledProcessError as e:
        # If the right error is raise, it's Error Class is in the output
        assert "ErrorConfigParameter" in str(e.output)
    # Cleanup
    os.remove(config_file_name)

def test_ncbimeta_ErrorConfigParameter_TABLES(tmpdir):
    '''Test for error catching when a config file has improper parameters'''
    # Prep the config file contents
    tmpdir = tmpdir.strpath
    config_file_name = os.path.join(tmpdir,'tmp_config.yaml')
    config_file = open(config_file_name, 'w')
    config_file.write('OUTPUT_DIR: output' + '\n' +
                      'EMAIL: email' + '\n' +
                      'API_KEY: api_key' + '\n' +
                      'FORCE_PAUSE_SECONDS: force_pause_seconds' + '\n' +
                      'DATABASE: database' + '\n' +
                      'TABLESS: tables')
    config_file.close()

    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file_name
    # Use a try-catch with the sub-process of module
    try:
        subprocess.check_output(test_cmd,
                                shell=True,
                                stderr=subprocess.STDOUT)
        # If an exception isn't raise then the assertion fails (0)
        assert 0
    except subprocess.CalledProcessError as e:
        # If the right error is raise, it's Error Class is in the output
        assert "ErrorConfigParameter" in str(e.output)
    # Cleanup
    os.remove(config_file_name)

def test_ncbimeta_ErrorConfigParameter_SEARCH_TERMS(tmpdir):
    '''Test for error catching when a config file has improper parameters'''
    # Prep the config file contents
    tmpdir = tmpdir.strpath
    config_file_name = os.path.join(tmpdir,'tmp_config.yaml')
    config_file = open(config_file_name, 'w')
    config_file.write('OUTPUT_DIR: output' + '\n' +
                      'EMAIL: email' + '\n' +
                      'API_KEY: api_key' + '\n' +
                      'FORCE_PAUSE_SECONDS: force_pause_seconds' + '\n' +
                      'DATABASE: database' + '\n' +
                      'TABLES: tables' + '\n' +
                      'SEARCH_TERMSS: search_terms')
    config_file.close()

    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file_name
    # Use a try-catch with the sub-process of module
    try:
        subprocess.check_output(test_cmd,
                                shell=True,
                                stderr=subprocess.STDOUT)
        # If an exception isn't raise then the assertion fails (0)
        assert 0
    except subprocess.CalledProcessError as e:
        # If the right error is raise, it's Error Class is in the output
        assert "ErrorConfigParameter" in str(e.output)
    # Cleanup
    os.remove(config_file_name)

def test_ncbimeta_ErrorConfigParameter_TABLE_COLUMNS(tmpdir):
    '''Test for error catching when a config file has improper parameters'''
    # Prep the config file contents
    tmpdir = tmpdir.strpath
    config_file_name = os.path.join(tmpdir,'tmp_config.yaml')
    config_file = open(config_file_name, 'w')
    config_file.write('OUTPUT_DIR: output' + '\n' +
                      'EMAIL: email' + '\n' +
                      'API_KEY: api_key' + '\n' +
                      'FORCE_PAUSE_SECONDS: force_pause_seconds' + '\n' +
                      'DATABASE: database' + '\n' +
                      'TABLES: tables' + '\n' +
                      'SEARCH_TERMS: search_terms' + '\n' +
                      'TABLE_COLUMNSS: table_columns')
    config_file.close()

    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file_name
    # Use a try-catch with the sub-process of module
    try:
        subprocess.check_output(test_cmd,
                                shell=True,
                                stderr=subprocess.STDOUT)
        # If an exception isn't raise then the assertion fails (0)
        assert 0
    except subprocess.CalledProcessError as e:
        # If the right error is raise, it's Error Class is in the output
        assert "ErrorConfigParameter" in str(e.output)
    # Cleanup
    os.remove(config_file_name)

def test_ncbimeta_OutputDirNotExists(tmpdir):
    '''Test for successfully running main program when outputdir doesn't exist'''
    tmpdir = tmpdir.strpath
    # Prep files and directories
    src_config = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test.yaml")
    dst_dir = os.path.join(tmpdir, "tmp-output-test")
    config_file = os.path.join(tmpdir,'tmp_config.yaml')

    # Read in the file
    with open(src_config, 'r') as file: filedata = file.read()
    # Replace the target data
    filedata = filedata.replace('OUTPUT_DIR : test', 'OUTPUT_DIR : ' + dst_dir )
    # Write to the destination file
    with open(config_file, 'a') as file: file.write(filedata)

    test_cmd = "ncbimeta/NCBImeta.py --flat --config " + config_file
    # Use a try-catch with the sub-process module
    try:
        subprocess.check_output(test_cmd,
                                shell=True,
                                stderr=subprocess.STDOUT)
        # If an exception isn't raise, then the program ran successfully
        assert 1
    except subprocess.CalledProcessError as e:
        # If an error is raised, it's Error Class is in the output
        #print(str(e.output))
        assert 0
    # Cleanup
    os.remove(config_file)
