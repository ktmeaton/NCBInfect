#!/usr/bin env python3
"""
Created on Thurs Mar 08 2018

@author: Katherine Eaton

"NCBImeta Main Program"
"""

# This program should only be called from the command-line
if __name__ != "__main__": quit()

import argparse
import sqlite3
import os
import sys
import time
import importlib
import datetime
import Bio
from Bio import Entrez
from xml.dom import minidom
import urllib.error    # HTTP Error Catching

src_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '') + "src"
sys.path.append(src_dir)

# Deal with unicode function rename in version 3
if sys.version_info.major == 3:
    unicode = str

import NCBImeta_Utilities
import NCBImeta_Errors


def flushprint(message):
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------#
#                            Argument Parsing                           #
#-----------------------------------------------------------------------#

# To Be Done: Full Description
parser = argparse.ArgumentParser(description='Description of NCBImeta.',
                                 add_help=True)


# Argument groups for the program
mandatory_parser = parser.add_argument_group('mandatory')

parser.add_argument('--config',
                    help = 'Path to configuration file "NCBImeta_config.py".',
                    action = 'store',
                    dest = 'configPath',
                    required = True)

parser.add_argument('--flat',
                    help = 'Do not create organization directories, output all files to output directory.',
                    action = 'store_true',
                    dest = 'flatMode')



# Retrieve user parameters
args = vars(parser.parse_args())

config_path = args['configPath']
flat_mode = args['flatMode']




#------------------------------------------------------------------------------#
#                              Argument Parsing                                #
#------------------------------------------------------------------------------#


# Check if config.py file exists
if not os.path.exists(config_path):
    raise NCBImeta_Errors.ErrorConfigFileNotExists(config_path)

# Add the directory containing config.py to the system path for import
sys.path.append(os.path.dirname(config_path))

# Get the module name for import
config_module_name = os.path.basename(config_path).split(".")[0]

# Dynamic module loading
CONFIG = importlib.import_module(config_module_name)


flushprint(
"\n" + "NCBImeta run with the following options: " + "\n" +
"\t" + "Output Directory: " + CONFIG.OUTPUT_DIR + "\n" +
"\t" + "Email: " + CONFIG.EMAIL + "\n" +
"\t" + "User Database: " + str(CONFIG.DATABASE) + "\n" +
"\t" + "Tables: " + str(CONFIG.TABLES) + "\n" +
"\t" + "Search Terms: " + str(CONFIG.SEARCH_TERMS) + "\n\n")

# Check if output dir exists
if not os.path.exists(CONFIG.OUTPUT_DIR):
    raise NCBImeta_Errors.ErrorOutputDirNotExists(CONFIG.OUTPUT_DIR)

# Flat mode checking
if flat_mode:
    flushprint("Flat mode was requested, organizational directories will not be used.")
    DB_DIR = os.path.join(CONFIG.OUTPUT_DIR, "")
    LOG_PATH = CONFIG.OUTPUT_DIR


elif not flat_mode:
    # Create accessory directory (ex. log, data, database, etc.)
    flushprint("Flat mode was not requested, organization directories will be used.")
    NCBImeta_Utilities.check_accessory_dir(CONFIG.OUTPUT_DIR)
    DB_DIR = os.path.join(CONFIG.OUTPUT_DIR, "", "database", "")
    LOG_PATH = os.path.join(CONFIG.OUTPUT_DIR, "", "log")

DB_PATH = os.path.join(DB_DIR, "", CONFIG.DATABASE)

#------------------------- Database Connection---------------------------------#
if not os.path.exists(DB_PATH):
    flushprint("\n" + "Creating database: " + DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.commit()
    flushprint("\n" + "Connected to database: " + DB_PATH)

elif os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    conn.commit()
    flushprint("\n" + "Connected to database: " + DB_PATH)

#------------------------------------------------------------------------------#
#                       Database Processing Function                           #
#------------------------------------------------------------------------------#

def UpdateDB(table, output_dir, database, email, search_term, table_columns, log_path, db_dir, api_key, force_pause_seconds):
    flushprint("\nCreating/Updating the " + table + " table using the following parameters: " + "\n" +
    "\t" + "Database: " + "\t\t" + database + "\n" +
    "\t" + "Search Term:" + "\t" + "\t" + search_term + "\n" +
    "\t" + "Email: " + "\t\t\t" + email + "\n" +
    "\t" + "API Key: " + "\t\t\t" + api_key + "\n" + 
    "\t" + "Output Directory: "     + "\t" + output_dir + "\n\n")


    Entrez.email = email
    Entrez.api_key = api_key
    Entrez.sleep_between_tries = 1
    Entrez.max_tries = 3

    #---------------------------------------------------------------------------#
    #                                File Setup                                 #
    #---------------------------------------------------------------------------#
    # Name of Log File
    log_file_path = os.path.join(LOG_PATH, "",
                                os.path.splitext(database)[0] + "_" + table + ".log")

    # Check if the file already exists, either write or append to it.
    if os.path.exists(log_file_path):
        log_file = open(log_file_path, "a")
    else:
        log_file = open(log_file_path, "w")

    #--------------------------------------------------------------------------#
    #                                SQL Setup                                 #
    #--------------------------------------------------------------------------#

    # Connect to database and establish cursor for commands.
    conn = sqlite3.connect(os.path.join(db_dir, "", database))
    cur = conn.cursor()

    ## Create the database, with dynamic variables from config file
    sql_query = ("Create TABLE IF NOT EXISTS " + table +
    " (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " +
    table + "_id TEXT")

    for column_name_dict in table_columns:
        column_name = list(column_name_dict.keys())[0]
        # By default, every user-specified column is type TEXT
        sql_query += ", " + column_name + " TEXT"
    sql_query += ")"

    cur.execute(sql_query)

    #-----------------------------------------------------------------------#
    #                          Entrex Search                                #
    #-----------------------------------------------------------------------#
    
    handle = Entrez.esearch(db=table.lower(),
                            term=search_term,
                            retmax = 9999999)

    # Read the record, count total number entries, create counter
    record = Entrez.read(handle)
    num_records = int(record['Count'])
    num_processed = 0
   
    #-----------------------------------------------------------------------#
    #                          Iterate Through ID List                      #
    #-----------------------------------------------------------------------#

    for ID in record['IdList']:
        #-------------------Progress Log and Entry Counter-------------------#
        # Increment entry counter and record progress to screen
        num_processed += 1
        flushprint("ID: " + ID)
        flushprint("Processing record: " +
               str(num_processed) + \
               "/" + str(num_records))


        #------------Check if Record Already Exists in Database------------#

        sql_query = ("SELECT EXISTS(SELECT " + table + "_id FROM " +
                    table + " WHERE " + table + "_id=?)")
        cur.execute(sql_query, (ID,))

        # 0 if not found, 1 if found
        record_exists = cur.fetchone()[0]

        if record_exists:
            continue
        '''
        IMPORTANT:
        The ID should not exists in the table UNLESS the record was fully parsed.
        ie. The database does not get updated until the end of each record.
        '''
        # This is the sleep command before implementing the HTTPerror catching in next section
        time.sleep(force_pause_seconds)
        #---------------If Assembly Isn't in Database, Add it------------#
        # Retrieve Assembly record using ID, read, store as dictionary
        if table.lower() != "nucleotide":
            # Use the esummary function to return a record summary, but wrapped in HTTP error checking
            ID_handle_retrieved = False
            fetch_attempts = 0
            while not ID_handle_retrieved and fetch_attempts < Entrez.max_tries:
                try:
                    ID_handle = Entrez.esummary(db=table.lower(),id=ID)
                    ID_handle_retrieved = True
                except urllib.error.HTTPError as error:
                    # Error code 429: Too Many Requests
                    if error.code == 429:
                        fetch_attempts += 1
                        print("HTTP Error " + str(error.code) + ": " + str(error.reason))
                        print("Fetch Attempt: " + str(fetch_attempts) + "/" + str(Entrez.max_tries))
                        print("Sleeping for " + str(Entrez.sleep_between_tries) + " seconds before retrying.")
                        time.sleep(Entrez.sleep_between_tries)
                    # General Error Code, non specific
                    else:
                        fetch_attempts += 1
                        print("HTTP Error " + str(error.code) + ": " + str(error.reason))
                        print("Fetch Attempt: " + str(fetch_attempts) + "/" + str(Entrez.max_tries))
                        print("Retrying record fetching.")

            if fetch_attempts == Entrez.max_tries and not ID_handle_retrieved:
                raise ErrorMaxFetchAttemptsExceeded(ID)

            # If successfully fetched, move onto reading the record
            ID_record = Entrez.read(ID_handle, validate=False)
            try:
                record_dict = ID_record['DocumentSummarySet']['DocumentSummary'][0]
            except TypeError:
                record_dict = ID_record[0]
        else:
            ID_handle = Entrez.efetch(db=table.lower(),id=ID, retmode='xml')
            ID_record = Entrez.read(ID_handle, validate=False)
            try:
                record_dict = ID_record['DocumentSummarySet']['DocumentSummary'][0]
            except TypeError:
                record_dict = ID_record[0]

        #print(record_dict)
        flatten_record_dict = list(NCBImeta_Utilities.flatten_dict(record_dict))

        column_dict = {}

        # Add ID to the dictionary
        column_dict[table + "_id"] = ID



        # Iterate through each column to search for values
        for column in table_columns:
            column_name = list(column.keys())[0]
            column_payload = list(column.values())[0]
            column_value = ""
            column_index = 0

            # Special rules for hard-coded Nucleotide  Fields
            if "GBSeq_comment" in column.values():
                for row in flatten_record_dict:
                    if row[0] == "GBSeq_comment":
                        # Hard-coded field, also check for user custom column name
                        for i_column in table_columns:
                            if "GBSeq_comment" in i_column.values():
                                column_value = "'" + row[1].replace("'","") + "'"
                                column_dict[list(i_column.items())[0][0]] = column_value

                        split_comment = row[1].split(";")
                        for item in split_comment:
                            split_item = item.split("::")
                            if len(split_item) < 2: continue
                            split_key = split_item[0].lstrip(" ").rstrip(" ")
                            split_value = split_item[1].lstrip(" ").rstrip(" ")
                            # Accomodate all the inconsistently named fields
                            for i_column in table_columns:
                                cur_column = list(i_column.items())[0][1]			  
                                if (cur_column == split_key or 
                                  (cur_column == "CDS (total)" and split_key == "CDSs (total)") or
				  (cur_column == "CDS (total)" and split_key == "CDS") or
                                  (cur_column == "CDS (coding)" and split_key == "CDS (with protein)") or
				  (cur_column == "CDS (coding)" and split_key == "CDSs (with protein)") or
                                  (cur_column == "Genes (total)" and split_key == "Genes") or
                                  (cur_column == "Pseudo Genes (total)" and split_key == "Pseudo Genes")):				  
                                    column_value = "'" + split_value.replace("'","").replace(",","") + "'"
                                    column_dict[list(i_column.items())[0][0]] = column_value

            # Special hard-coded field for biosample
            elif "NucleotideBioSample" in column.values():
                for row in record_dict:
                    if row != "GBSeq_xrefs": continue
                    for subrow in record_dict[row]:
                        if subrow["GBXref_dbname"] != "BioSample": continue
                        for i_column in table_columns:
                            if list(i_column.items())[0][1] == "NucleotideBioSample":
                                column_value = "'" + subrow["GBXref_id"].replace("'","") + "'"
                                column_dict[list(i_column.items())[0][0]] = column_value


            #-------------------------------------------------------#
            # Attempt 1: Simple Dictionary Parse, taking first match

            for row in flatten_record_dict:
                #print(row)
                # For simple column types, as strings
                if type(column_payload) == str and column_payload in row:
                    column_value = row[-1]
                    break

                # For complex column types, as list
                elif type(column_payload) == list:
                    while column_payload[column_index] in row:
                        if column_index + 1 == len(column_payload):
                            column_value = row[-1]
                            break
                        column_index += 1

            # If the value was found, skip(?) the next section of XML parsing
            if column_value:
                column_value = "'" + column_value.replace("'","") + "'"
                column_dict[column_name] = column_value
		#continue?
	
	    # Briefly try to parse the original record dict
	    # This was for pubmed author lists originally
            elif type(column_payload) != list:
                try:
                    column_value = record_dict[column_payload]
                    # If list, convert to semicolon separated string		   
                    if isinstance(column_value,Bio.Entrez.Parser.ListElement):
                        column_value = '; '.join(str(e) for e in column_value)		    
                    column_value = "'" + column_value.replace("'","") + "'"
                    column_dict[column_name] = column_value
                except KeyError:
                    column_value = ""

            #-------------------------------------------------------#
            # Attempt 2: XML Parse for node or attribute
            for row in flatten_record_dict:
                if type(column_payload) == str:
                    # Pubmed records can have an int value (has abstract = 0 or 1)
                    result = [str(s) for s in row if column_payload in str(s)]

                elif type(column_payload) == list:
                    result = [s for s in row if column_payload[0] in s and column_payload[1] in s ]
                if not result: continue
                result = unicode(result[0].strip())
                if result[0] != "<" or result[-1] != ">": continue

                # Just in case, wrap sampledata in a root node for XML formatting
                xml = "<Root>" + result + "</Root>"
                # minidom doc object for xml manipulation and parsing
                try:
                    root = minidom.parseString(xml).documentElement
                except UnicodeEncodeError:
                    #xml = "<Root>" + unicode(result) + "</Root>"
                    xml = "<Root>" + result.encode('utf-8') + "</Root>"
                    root = minidom.parseString(xml).documentElement

                #print(root.toprettyxml())
                # Names of nodes and attributes we are searching for
                if type(column_payload) == str:
                    node_name = column_payload
                    attr_name = column_payload

                elif type(column_payload) == list:
                    node_name = column_payload[0]
                    if len(column_payload) > 2:
                        attr_name = column_payload[1:]
                    else:
                        attr_name = column_payload[1]
                # Dictionaries store recovered nodes and attributes
                node_dict = {}
                attr_dict = {}

                NCBImeta_Utilities.xml_find_node(root,node_name,node_dict)
                NCBImeta_Utilities.xml_find_attr(root,node_name,attr_name,attr_dict)
                #print(node_dict)
                #print(attr_dict)

                if type(column_payload) == list:
                    attr_name = column_payload[1]
                    try:
                        column_value = attr_dict[attr_name]
                        column_value = "'" + column_value.replace("'","") + "'"
                        column_dict[column_name] = column_value
                        break
                    except KeyError:
                        None
                else:
                    try:
                        column_value = node_dict[node_name]
                        column_value = "'" + column_value.replace("'","") + "'"
                        column_dict[column_name] = column_value
                    except KeyError:
                        None
                    break

        #print(column_dict)
        #quit()
        # Write the column values to the db with dynamic variables
        sql_dynamic_table = "INSERT INTO " + table + " ("
        sql_dynamic_vars = ",".join([column for column in column_dict.keys()]) + ") "
        #sql_dynamic_qmarks = "VALUES (" + ",".join(["?" for column in column_dict.keys()]) + ") "
        sql_dynamic_values = " VALUES (" + ",".join([column_dict[column] for column in column_dict.keys()]) + ")"
        sql_query = sql_dynamic_table + sql_dynamic_vars + sql_dynamic_values
        #print(sql_query)
        cur.execute(sql_query)

        # Write to logfile
        now = datetime.datetime.now()
        log_file.write("[" + str(now) + "]" +
                     "\t" + "New entry added with ID:" +
                     "\t" + ID + "." + "\n")
        conn.commit()


    # CLEANUP
    conn.commit()
    cur.close()
    log_file.close()


#------------------------Iterate Through Tables--------------------------------#

for table in CONFIG.TABLES:
    OUTPUT_DIR = CONFIG.OUTPUT_DIR
    DATABASE = CONFIG.DATABASE
    EMAIL = CONFIG.EMAIL
    SEARCH_TERM = CONFIG.SEARCH_TERMS[table]
    TABLE_COLUMNS = CONFIG.TABLE_COLUMNS[table]
    API_KEY = CONFIG.API_KEY
    FORCE_PAUSE_SECONDS = CONFIG.FORCE_PAUSE_SECONDS


    UpdateDB(table, OUTPUT_DIR, DATABASE, EMAIL, SEARCH_TERM, TABLE_COLUMNS, LOG_PATH, DB_DIR, API_KEY, FORCE_PAUSE_SECONDS)
