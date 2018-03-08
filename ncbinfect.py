#!/usr/bin env python
"""
Created on Thurs Mar 08 2018

@author: Katherine Eaton

"NCBInfect Main Program"
"""

# This program should only be called from the command-line
if __name__ != "__main__": quit()

import argparse                                                         # Command-line argument parsing
import sqlite3
import os
import sys
from Bio import Entrez

src_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '') + "src"
sys.path.append(src_dir)

import NCBInfect_Utilities
import NCBInfect_Errors


def UpdateDB(table):
	print("\nCreating/Updating the", table, "table using the following parameters: " + "\n" +
	"\t" + "Database: " + "\t\t" + DATABASE + "\n" +
	"\t" + "Search Term:" + "\t" + "\t" + SEARCH_TERM + "\n" +
	"\t" + "Email: " + "\t\t\t" + EMAIL + "\n" +
    "\t" + "Output Directory: "	 + "\t" + output_dir + "\n\n")


	Entrez.email = EMAIL

    #---------------------------------------------------------------------------#
    #                                File Setup                                 #
    #---------------------------------------------------------------------------#
    # Name of Log File
	log_file_path = os.path.join(LOG_PATH, "",
								os.path.splitext(DATABASE)[0] + "_" + table + ".log")

	# Check if the file already exists, either write or append to it.
	if os.path.exists(log_file_path):
		log_file = open(log_file_path, "a")
	else:
		log_file = open(log_file_path, "w")

    #--------------------------------------------------------------------------#
    #                                SQL Setup                                 #
    #--------------------------------------------------------------------------#

	# Connect to database and establish cursor for commands.
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()

    ## Create the database
    # Check if strain is in table
	sql_query = ("Create TABLE IF NOT EXISTS " + table +
	" (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " +
	"assembly_id TEXT")
	for column in TABLE_COLUMNS:
		# By default, every user-specified column is type TEXT
		sql_query += ", " + column + " TEXT"
	sql_query += ")"

	cur.execute(sql_query)

	#-----------------------------------------------------------------------#
	#                           Entrez Assemblies                           #
	#-----------------------------------------------------------------------#
	search_term = SEARCH_TERM
	handle = Entrez.esearch(db=table.lower(),
                            term=SEARCH_TERM,
                            retmax = 10)

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
		print("Processing record: " +
	   		str(num_processed) + \
	   		"/" + str(num_records))



	# CLEANUP
	conn.commit()
	cur.close()
	log_file.close()






#-----------------------------------------------------------------------#
#                            Argument Parsing                           #
#-----------------------------------------------------------------------#

# To Be Done: Full Description
parser = argparse.ArgumentParser(description='Description of NCBInfect.',
                                 add_help=True)


# Argument groups for the program
mandatory_parser = parser.add_argument_group('mandatory')
interactive_parser = parser.add_argument_group('interactive')

mandatory_parser.add_argument('--outputdir',
                    help = 'Output directory.',
                    action = 'store',
                    dest = 'outputDir',
					required = True)

parser.add_argument('--automate',
                    help = 'Non-interactive mode, automated with config file automate.py.',
                    action = 'store_true',
                    dest = 'automate')

parser.add_argument('--flat',
                    help = 'Do not create organization directories, output all files to output directory.',
                    action = 'store_true',
                    dest = 'flat')

interactive_parser.add_argument('--database',
                    help = 'User SQLite database.',
                    action = 'store',
                    dest = 'db')



# Retrieve user parameters
args = vars(parser.parse_args())

automate_mode = args['automate']
output_dir = args['outputDir']
flat_mode = args['flat']
db_name = args['db']



#------------------------------------#
#              Automated             #
#------------------------------------#

if automate_mode:
	if db_name:
		parser.error("Please remove --database argument when using --automate.")
	import automate as AUTOMATE
	# These are all global variables
	print(
	"\n" + "Automated mode selected with the following options: " + "\n" +
	"\t" + "Output Directory: " + AUTOMATE.OUTPUT_DIR + "\n" +
	"\t" + "Email: " + AUTOMATE.EMAIL + "\n" +
	"\t" + "User Database: " + str(AUTOMATE.DATABASE) + "\n" +
	"\t" + "Tables: " + str(AUTOMATE.TABLES) + "\n" +
	"\t" + "Search Terms: " + str(AUTOMATE.SEARCH_TERMS) + "\n\n")

	# Flat mode checking
	if flat_mode:
		print("Flat mode was requested, organizational directories will not be used.")
		DB_PATH = os.path.join(output_dir, "", AUTOMATE.DATABASE)
		LOG_PATH = output_dir


	elif not flat_mode:
		# Create accessory directory (ex. log, data, database, etc.)
		print("Flat mode was not requested, organization directories will be used.")
		NCBInfect_Utilities.check_accessory_dir(output_dir)
		DB_PATH = os.path.join(output_dir, "", "database", "", AUTOMATE.DATABASE)
		LOG_PATH = os.path.join(output_dir, "", "log")

	for table in AUTOMATE.TABLES:
		OUTPUT_DIR = AUTOMATE.OUTPUT_DIR
		DATABASE = AUTOMATE.DATABASE
		EMAIL = AUTOMATE.EMAIL
		SEARCH_TERM = AUTOMATE.SEARCH_TERMS[table]
		TABLE_COLUMNS = AUTOMATE.TABLE_COLUMNS[table]
		UpdateDB(table)

	quit()

#------------------------------------------------------------------------------#
#                           Argument Checking                                  #
#------------------------------------------------------------------------------#
if not automate_mode and not db_name:
	# Database arugment is conditionally dependent
		parser.error("--database argument is required when not using --automate.")

		# Database argument supplied, can use database name
		db_path = os.path.join(output_dir, "", db_name)



#------------------------- Database Connection---------------------------------#
if not os.path.exists(db_path):
	print('\nCreating database: ' + db_path)
	conn = sqlite3.connect(db_path)
	conn.commit()
	print('\nConnected to database: ' + db_path)

elif os.path.exists(db_path):
	conn = sqlite3.connect(db_path)
	conn.commit()
	print('\nConnected to database: ' + db_path)
