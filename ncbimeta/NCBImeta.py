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
import yaml                             # YAML config file parsing
from lxml import etree                  # XML Parsing
import tempfile                         # Temporary file for XML parsing

from ncbimeta import NCBImetaUtilities  # NCBImeta helper functions
from ncbimeta import NCBImetaErrors     # NCBImeta Error classes



#-----------------------------------------------------------------------#
#                            Argument Parsing                           #
#-----------------------------------------------------------------------#

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
                    version='%(prog)s v0.6.2')

# Retrieve user parameters
args = vars(parser.parse_args())

config_path = args['configPath']
flat_mode = args['flatMode']

#------------------------------------------------------------------------------#
#                            Error Catching                                    #
#------------------------------------------------------------------------------#

# Check if configuration file exists
if not os.path.exists(config_path):
    raise NCBImetaErrors.ErrorConfigFileNotExists(config_path)

# Load the YAML configuration file
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

#--- Print the retrieved config file parameters ---#
print(
"\n" + "NCBImeta was run with the following options: " + "\n" +
"\t" + "Config File: " + str(config_path) + "\n" +
"\t" + "Output Directory: " + str(CONFIG_OUTPUT_DIR) + "\n" +
"\t" + "Email: " + str(CONFIG_EMAIL) + "\n" +
    "\t" + "API Key: " + "\t\t" + str(CONFIG_API_KEY) + "\n" +
"\t" + "User Database: " + str(CONFIG_DATABASE) + "\n" +
"\t" + "Tables: " + str(CONFIG_TABLES) + "\n" +
"\t" + "Search Terms: ", flush = True)
for table_search_term in CONFIG_SEARCH_TERMS:
    print("\t\t" + str(table_search_term), flush = True)
print("\n", flush = True)

# Check if output dir exists
if not os.path.exists(CONFIG_OUTPUT_DIR):
    os.makedirs(CONFIG_OUTPUT_DIR)

# Flat mode checking
if flat_mode:
    print("Flat mode was requested, organizational directories will not be used.", flush = True)
    DB_DIR = os.path.join(CONFIG_OUTPUT_DIR, "")
    LOG_PATH = CONFIG_OUTPUT_DIR

# Or Create accessory directory (ex. log, data, database, etc.)
elif not flat_mode:
    print("Flat mode was not requested, organization directories will be used.", flush = True)
    NCBImetaUtilities.check_accessory_dir(CONFIG_OUTPUT_DIR)
    DB_DIR = os.path.join(CONFIG_OUTPUT_DIR, "", "database", "")
    LOG_PATH = os.path.join(CONFIG_OUTPUT_DIR, "", "log")

# Database path (depending on flat mode or not)
DB_PATH = os.path.join(DB_DIR, "", CONFIG_DATABASE)

#------------------------------------------------------------------------------#
#                       Database connection                                    #
#------------------------------------------------------------------------------#
if not os.path.exists(DB_PATH):
    print("\n" + "Creating database: " + DB_PATH, flush = True)
    conn = sqlite3.connect(DB_PATH)
    conn.commit()
    print("\n" + "Connected to database: " + DB_PATH, flush = True)

elif os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    conn.commit()
    print("\n" + "Connected to database: " + DB_PATH, flush = True)

#-----------------------------------------------------------------------#
#                      CONSTANTS and Config                             #
#-----------------------------------------------------------------------#

XPATH_SPECIAL_CHAR =['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                     '+', '{', '}', '|', ':', '"', '<', '>', '?', '`', '=',
                     '[', ']', '\\', ';', '‘', ',', '.', '/']

DB_VALUE_SEP = ";"

# lxml parser
LXML_CDATA_PARSER = etree.XMLParser(strip_cdata=False)

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
    "\t" + "API Key: " + "\t\t" + api_key + "\n" +
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

    # Database reading and entrez searching occur in a while loop to catch errors
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
        # The Assembly table cannot be retrieved using efetch, only docsum esummary
        if table.lower() == "assembly":
            # Use the http function to return a record summary, but wrapped in HTTP error checking
            kwargs = {"db":table.lower(), "id":ID, "retmode": "xml"}
            entrez_method = Entrez.esummary
        else:
            # We're working with any other table instead, use efetch and get xml
            kwargs = {"db": table.lower(), "id": ID, "retmode": "xml"}
            if table.lower() == "nucleotide":
                kwargs["rettype"] = "gb"
            entrez_method = Entrez.efetch

        # ID_handle is an _io.TextIOWrapped object, which originally had utf-8 encoding
        ID_handle = NCBImetaUtilities.HTTPErrorCatch(entrez_method, Entrez.max_tries, Entrez.sleep_between_tries, **kwargs)

        # Ideal world: Pass an undecoded string to the xml parser
        # Could be accomplished by opening in binary ('rb')
        # tempfiles by default are opened as mode='w+b'
        with tempfile.NamedTemporaryFile(delete=False) as temp_b:
            # Write the data from ID_handle to a temporary file (binary)
            for line in ID_handle: temp_b.write(str.encode(line))
            temp_b.close()
            # Read the data as binary, into the XML parser. Avoids encoding issues
            with open(temp_b.name, 'rb') as xml_source:
                ID_root = etree.parse(xml_source, parser=LXML_CDATA_PARSER)

        #----------------------------------------------------------------------#
        #                         NCBI Record Parsing                          #
        #----------------------------------------------------------------------#

        #print(etree.tostring(ID_root).decode())

        column_dict = {}
        # Add ID to the dictionary
        column_dict[table + "_id"] = [ID]
        # A special dictionary for gbseq annotations
        gbseq_dict = {}
        # Iterate through each column to search for metadata
        for column in table_columns:
            column_name = list(column.keys())[0]
            column_value = []
            column_payload = list(column.values())[0]
            column_payload = column_payload.split(", ")
            # Initialize with empty values
            column_dict[column_name] = column_value

            #-------------------------------------------------------#
            #   XML Parse for node or attribute
            #-------------------------------------------------------#
            working_root =ID_root
            # If there are special character, this query should not be used for xpath!!
            bool_special_char = False
            for char in XPATH_SPECIAL_CHAR:
                for xquery in column_payload:
                    if char in xquery:
                        bool_special_char = True
            # If no special characters, run xpath search Functions
            if not bool_special_char:
                NCBImetaUtilities.xml_search(working_root, column_payload, column_payload[0], column_name, column_dict)

            # Special parsing for GBSeq_comment
            # If we're on the GBSeq_comment element and the comment was added to the dictionary
            if "GBSeq_comment" in column_payload and len(column_dict[column_name]) > 0:
                comment = column_dict[column_name][0]
                # Fix the CDS vs CDSs ambiguity
                comment = comment.replace("CDSs", "CDS")
                # comment is initialize subdivided by semi-colons
                split_comment = comment.split(";")
                for item in split_comment:
                    # Further subdivided by double colons
                    split_item = item.split("::")
                    # The elements we're interested have the :: otherwise skip
                    if len(split_item) < 2: continue
                    # Left side is the column name, right side is the metadata
                    split_key = split_item[0].lstrip(" ").rstrip(" ")
                    split_value = split_item[1].lstrip(" ").rstrip(" ")
                    gbseq_dict[split_key] = split_value

            # If the value was still empty, check for gbseq comment
            if column_payload[0] in gbseq_dict:
                column_dict[column_name].append(gbseq_dict[column_payload[0]])

        # Add quotations around each value for sql insertion
        for key in column_dict:
            # Remove empty string elements
            while "" in column_dict[key]: column_dict[key].remove("")
            # Remove quotations from each list element
            for i in range(0,len(column_dict[key])):
                column_dict[key][i] = column_dict[key][i].replace("\"","")
            # The following is to help with single quotes inside
            column_dict[key] = "\"" + DB_VALUE_SEP.join(column_dict[key]) + "\""

        # Write the column values to the db with dynamic variables
        sql_dynamic_table = "INSERT INTO " + table + " ("
        sql_dynamic_vars = ",".join([column for column in column_dict.keys()]) + ") "
        sql_dynamic_qmarks = "VALUES (" + ",".join(["?" for column in column_dict.keys()]) + ") "
        sql_dynamic_values = " VALUES (" + ",".join([column_dict[column] for column in column_dict.keys()]) + ")"
        sql_query = sql_dynamic_table + sql_dynamic_vars + sql_dynamic_values
        sql_query_q = sql_dynamic_table + sql_dynamic_vars + sql_dynamic_qmarks
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
