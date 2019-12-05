#!/usr/bin/env python3
"""
@author: Katherine Eaton

NCBImeta: Efficient and comprehensive metadata retrieval from the NCBI databases.
"""

# This program should only be called from the command-line
if __name__ != "__main__": quit()

#-----------------------------------------------------------------------#
#                         Modules and Packages                          #
#-----------------------------------------------------------------------#
import argparse                         # Command-line argument parsing
import sqlite3                          # Database storage and queries
import os                               # Filepath operations
import time                             # Allow sleeping of processes
import datetime                         # Get date and time for logfile
import Bio                              # Biopython NCBI API
from Bio import Entrez                  # Entrez queries (NCBI)
from xml.dom import minidom             # XML Processing
import yaml                             # YAML config file parsing

from ncbimeta import NCBImetaUtilities  # NCBImeta helper functions
from ncbimeta import NCBImetaErrors     # NCBImeta Error classes

#-----------------------------------------------------------------------#
#                            Argument Parsing                           #
#-----------------------------------------------------------------------#

# To Be Done: Full Description
parser = argparse.ArgumentParser(description='NCBImeta: Efficient and comprehensive metadata retrieval from the NCBI databases.',
                                 add_help=True)


# Argument groups for the program
mandatory_parser = parser.add_argument_group('mandatory')

parser.add_argument('--config',
                    help = 'Path to the yaml configuration file (ex. config.yaml).',
                    action = 'store',
                    dest = 'configPath',
                    required = True)

parser.add_argument('--flat',
                    help = 'Do not create organization directories, output all files to output directory.',
                    action = 'store_true',
                    dest = 'flatMode')

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s v0.4.2')



# Retrieve user parameters
args = vars(parser.parse_args())

config_path = args['configPath']
flat_mode = args['flatMode']


#------------------------------------------------------------------------------#
#                              Argument Parsing                                #
#------------------------------------------------------------------------------#

# Check if configuration file exists
if not os.path.exists(config_path):
    raise NCBImetaErrors.ErrorConfigFileNotExists(config_path)

# YAML switch in v0.3.5
with open(config_path) as config_file:
    config_data = yaml.load(config_file, Loader=yaml.FullLoader)
    if config_data is None:
        raise NCBImetaErrors.ErrorConfigYAMLFormat(config_file)

# Retrieve configuration file values and error catching
#--- Output Directory ---#
try:
    CONFIG_OUTPUT_DIR = config_data["OUTPUT_DIR"]
except KeyError:
    raise NCBImetaErrors.ErrorConfigParameter("OUTPUT_DIR")
#--- User Email ---#
try:
    CONFIG_EMAIL = config_data["EMAIL"]
except KeyError:
    raise NCBImetaErrors.ErrorConfigParameter("EMAIL")
#--- User API Key ---#
try:
    CONFIG_API_KEY = config_data["API_KEY"]
except KeyError:
    raise NCBImetaErrors.ErrorConfigParameter("API_KEY")
#--- Force pausing in between record fetching ---#
try:
    CONFIG_FORCE_PAUSE_SECONDS = config_data["FORCE_PAUSE_SECONDS"]
except KeyError:
    raise NCBImetaErrors.ErrorConfigParameter("FORCE_PAUSE_SECONDS")
#--- Database file name---#
try:
    CONFIG_DATABASE = config_data["DATABASE"]
except KeyError:
    raise NCBImetaErrors.ErrorConfigParameter("DATABASE")
#--- NCBI Tables to Search (list) ---#
try:
    CONFIG_TABLES = config_data["TABLES"]
except KeyError:
    raise NCBImetaErrors.ErrorConfigParameter("TABLES")
#--- Search terms for each table (dict) ---#
try:
    CONFIG_SEARCH_TERMS = config_data["SEARCH_TERMS"]
except KeyError:
    raise NCBImetaErrors.ErrorConfigParameter("SEARCH_TERMS")
#--- Table Columns/Metadata to retrieve (list of dict)---#
try:
    CONFIG_TABLE_COLUMNS = config_data["TABLE_COLUMNS"]
except KeyError:
    raise NCBImetaErrors.ErrorConfigParameter("TABLE_COLUMNS")

print(
"\n" + "NCBImeta was run with the following options: " + "\n" +
"\t" + "Config File: " + str(config_path) + "\n" +
"\t" + "Output Directory: " + str(CONFIG_OUTPUT_DIR) + "\n" +
"\t" + "Email: " + str(CONFIG_EMAIL) + "\n" +
"\t" + "User Database: " + str(CONFIG_DATABASE) + "\n" +
"\t" + "Tables: " + str(CONFIG_TABLES) + "\n" +
"\t" + "Search Terms: ", flush = True)
for table_search_term in CONFIG_SEARCH_TERMS:
    print("\t\t" + str(table_search_term), flush = True)
print("\n", flush = True)

# Check if output dir exists
if not os.path.exists(CONFIG_OUTPUT_DIR):
    raise NCBImetaErrors.ErrorOutputDirNotExists(CONFIG_OUTPUT_DIR)

# Flat mode checking
if flat_mode:
    print("Flat mode was requested, organizational directories will not be used.", flush = True)
    DB_DIR = os.path.join(CONFIG_OUTPUT_DIR, "")
    LOG_PATH = CONFIG_OUTPUT_DIR


elif not flat_mode:
    # Create accessory directory (ex. log, data, database, etc.)
    print("Flat mode was not requested, organization directories will be used.", flush = True)
    NCBImetaUtilities.check_accessory_dir(CONFIG_OUTPUT_DIR)
    DB_DIR = os.path.join(CONFIG_OUTPUT_DIR, "", "database", "")
    LOG_PATH = os.path.join(CONFIG_OUTPUT_DIR, "", "log")

DB_PATH = os.path.join(DB_DIR, "", CONFIG_DATABASE)

#------------------------- Database Connection---------------------------------#
if not os.path.exists(DB_PATH):
    print("\n" + "Creating database: " + DB_PATH, flush = True)
    conn = sqlite3.connect(DB_PATH)
    conn.commit()
    print("\n" + "Connected to database: " + DB_PATH, flush = True)

elif os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    conn.commit()
    print("\n" + "Connected to database: " + DB_PATH, flush = True)


#------------------------------------------------------------------------------#
#                       Database Processing Function                           #
#------------------------------------------------------------------------------#

def UpdateDB(table, output_dir, database, email, search_term, table_columns, log_path, db_dir, api_key, force_pause_seconds):
    '''
    Update the contents of a local sqlite database using records retrieved from NCBI as configured by the user.

    Parameters:
    table (str): Name of the NCBI database to search.
    output_dir (str): Path to the directory where output is written.
    database (str): Filename of the local sqlite database.
    email (str): User email.
    search_term (str): Entrez search query.
    table_columns(dict): Dictionary of column name and API name as value, ex. {AssemblyGenbankID : GbUid}.
    log_path(str): Path to the directory where the logfile is stored in.
    db_dir(str): Path to the directory where the database is stored in.
    api_key(str): NCBI user account API Key.
    force_pause_seconds(float): Number of seconds to wait in between fetch read_attempts.
    '''

    print("\nCreating/Updating the " + table + " table using the following parameters: " + "\n" +
    "\t" + "Database: " + "\t\t" + database + "\n" +
    "\t" + "Search Term:" + "\t" + "\t" + search_term + "\n" +
    "\t" + "Email: " + "\t\t\t" + email + "\n" +
    "\t" + "API Key: " + "\t\t\t" + api_key + "\n" +
    "\t" + "Output Directory: " + "\t" + output_dir + "\n\n", flush = True)


    Entrez.email = email
    Entrez.api_key = api_key
    # Allow a maximum of 3 tries for error catching before exiting program
    Entrez.max_tries = 3
    # Sleep for 1 second after an error has been generated before retrying
    Entrez.sleep_between_tries = 1

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
    #                          Entrez Search                                #
    #-----------------------------------------------------------------------#
    # Read the record, check for http, url, and runtime errors
    read_succeed = False
    read_attempts = 0

    while not read_succeed and read_attempts < Entrez.max_tries:
        kwargs = {"db": table.lower(), "term":search_term, "retmax":"9999999"}
        entrez_method = Entrez.esearch
        # Possible urllib error and RuntimeErrors occurring in the next line
        handle = NCBImetaUtilities.HTTPErrorCatch(entrez_method, Entrez.max_tries, Entrez.sleep_between_tries, **kwargs)
        try:
            record = Entrez.read(handle)
            read_succeed = True
        except RuntimeError:
            read_attempts += 1
            print("Runtime Error encountered. Sleeping for " + str(Entrez.sleep_between_tries) + " seconds before retrying.")
            time.sleep(Entrez.sleep_between_tries)

    if read_attempts == Entrez.max_tries and not read_succeed:
        raise ErrorMaxReadAttemptsExceeded(table)

    # Count total number of entries, create counter
    num_records = int(record['Count'])
    num_processed = 0

    #-----------------------------------------------------------------------#
    #                          Iterate Through ID List                      #
    #-----------------------------------------------------------------------#

    for ID in record['IdList']:
        #-------------------Progress Log and Entry Counter-------------------#
        # Increment entry counter and record progress to screen
        num_processed += 1
        print("ID: " + ID, flush = True)
        print("Processing record: " +
               str(num_processed) + \
               "/" + str(num_records), flush = True)

        #------------Check if Record Already Exists in Database------------#
        sql_query = ("SELECT EXISTS(SELECT " + table + "_id FROM " +
                    table + " WHERE " + table + "_id=?)")
        cur.execute(sql_query, (ID,))

        # 0 if not found, 1 if found
        record_exists = cur.fetchone()[0]

        # If the record_exists, skip the whole next part (ie. "continue" to next record)
        if record_exists:
            continue
        '''
        IMPORTANT:
        The ID should not exists in the table UNLESS the record was fully parsed.
        ie. The database does not get updated until the end of each record.
        '''
        # This is the sleep command before implementing the HTTPerror catching in next section
        # This is controlled by the user configuration file
        time.sleep(force_pause_seconds)

        #---------------If the table isn't in Database, Add it------------#
        # If we're not workinng with the Nucleotide table, we're using the "esummary function"
        # Retrieve table record using ID, read, store as dictionary
        if table.lower() != "nucleotide":
            # Use the http function to return a record summary, but wrapped in HTTP error checking
            kwargs = {"db":table.lower(), "id":ID}
            entrez_method = Entrez.esummary
        else:
            # We're working with the Nucleotide table instead, use efetch and get xml
            kwargs = {"db": table.lower(), "id":ID, "retmode":"xml"}
            entrez_method = Entrez.efetch

        # Possible urllib error occuring in the next line for unknown reasons
        ID_handle = NCBImetaUtilities.HTTPErrorCatch(entrez_method, Entrez.max_tries, Entrez.sleep_between_tries, **kwargs)

        # If successfully fetched, move onto reading the record
        ID_record = Entrez.read(ID_handle, validate=False)
        try:
            record_dict = ID_record['DocumentSummarySet']['DocumentSummary'][0]
        except TypeError:
            record_dict = ID_record[0]

        #DEBUG
        #print(record_dict)
        flatten_record_dict = list(NCBImetaUtilities.flatten_dict(record_dict))
        #for element in flatten_record_dict:
            #print(element)
        column_dict = {}

        # Add ID to the dictionary
        column_dict[table + "_id"] = ID

        #----------------------------------------------------------------------#
        #                         NCBI Record Parsing                          #
        #----------------------------------------------------------------------#

        # Iterate through each column to search for values
        for column in table_columns:
            column_name = list(column.keys())[0]
            column_payload = list(column.values())[0]
            column_value = ""

            # Check and see if column is special multi/hierarchical type
            # AssemblyGenbankBioprojectAccession : GB_BioProjects, BioprojectAccn
            split_column_payload = column_payload.split(", ")
            # if the split was successful, the payload should be a list
            if len(split_column_payload) > 1:
                column_payload = split_column_payload

            # Special rules for hard-coded Nucleotide Fields (ex. GBSeq_comment)
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
                                if (cur_column == split_key or (cur_column == "CDS (total)" and split_key == "CDSs (total)") or
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
                # For simple column types, as strings
                if type(column_payload) == str and column_payload in row:
                    column_value = row[-1]
                    break

                # For complex column types, as list
                elif type(column_payload) == list:
                    column_index = 0
                    while column_payload[column_index] in row:
                        if column_index + 1 == len(column_payload):
                            column_value = row[-1]
                            break
                        column_index += 1

            # If the value was found, skip(?) the next section of XML parsing
            if column_value:
                column_value = "'" + column_value.replace("'","") + "'"
                column_dict[column_name] = column_value

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
                result = str(result[0].strip())
                if result[0] != "<" or result[-1] != ">": continue

                # Just in case, wrap sampledata in a root node for XML formatting
                xml = "<Root>" + result + "</Root>"
                # minidom doc object for xml manipulation and parsing
                try:
                    root = minidom.parseString(xml).documentElement
                except UnicodeEncodeError:
                    #xml = "<Root>" + str(result) + "</Root>"
                    xml = "<Root>" + result.encode('utf-8') + "</Root>"
                    root = minidom.parseString(xml).documentElement

                #DEBUG
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

                #DEBUG
                #print('Node Name:', node_name)
                #print('Attr Name:', attr_name)
                #print('Column Name:', column_name)
                #print('Column Payload:', column_payload)
                NCBImetaUtilities.xml_find_node(root,node_name,node_dict)
                NCBImetaUtilities.xml_find_attr(root,node_name,attr_name,attr_dict)
                #print('Node Dict:', node_dict)
                #print('Attr Dict:', attr_dict)

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

#------------------------------------------------------------------------------#
#                     Iterate Through Tables in Config File                    #
#------------------------------------------------------------------------------#
for table in CONFIG_TABLES:
    OUTPUT_DIR = CONFIG_OUTPUT_DIR
    DATABASE = CONFIG_DATABASE
    EMAIL = CONFIG_EMAIL
    # Since API can be empty, force it to empty string for printing
    API_KEY = CONFIG_API_KEY
    if not API_KEY: API_KEY = ""
    FORCE_PAUSE_SECONDS = CONFIG_FORCE_PAUSE_SECONDS
    # Config search terms, match table to table name
    for index,search_term_table in enumerate(CONFIG_SEARCH_TERMS):
        table_name = list(search_term_table)[0]
        if table_name == table:
            break
    SEARCH_TERM = CONFIG_SEARCH_TERMS[index][table]
    # Table columns, match table to table name
    for index,table_column_dict in enumerate(CONFIG_TABLE_COLUMNS):
        table_name = list(table_column_dict)[0]
        if table_name == table:
            break
    TABLE_COLUMNS = CONFIG_TABLE_COLUMNS[index][table]

    # Check for duplicate column names
    # -- Note this is only PER TABLE (Checking for duplicate between table only happens
    # -- later in the database Join script)
    table_col_names = []
    for element in TABLE_COLUMNS: table_col_names += list(element.keys())
    dupl_table_col_names = set([col for col in table_col_names if table_col_names.count(col) > 1])
    if len(dupl_table_col_names) > 0:
        raise NCBImetaErrors.ErrorColumnsNotUnique(dupl_table_col_names)

    # Call the main database updating function
    UpdateDB(table, OUTPUT_DIR, DATABASE, EMAIL, SEARCH_TERM, TABLE_COLUMNS, LOG_PATH, DB_DIR, API_KEY, FORCE_PAUSE_SECONDS)
