"""
Created on Thursday June 08 2017

NCBI Genome Database Annotator

@author: Katherine Eaton
"""

import argparse
import sqlite3
import datetime
import os

from NCBInfect_Errors import *
from NCBInfect_Utilities import os_check,table_exists

#-----------------------------------------------------------------------#
#                            Argument Parsing                           #
#-----------------------------------------------------------------------#

parser = argparse.ArgumentParser(description='Description of the NCBInfect Annotation Tool.',
                                 add_help=True)

mandatory = parser.add_argument_group('mandatory')
bonus = parser.add_argument_group('bonus')

mandatory.add_argument('--database',
                    help='Genome Database Name',
                    type = str,
                    action = 'store',
                    dest = 'dbName',
                    required=True)

mandatory.add_argument('--table',
                    help='Table in Database To Modify',
                    type = str,
                    action = 'store',
                    dest = 'dbTable',
                    required=True)

mandatory.add_argument('--annotfile',
                    help='Path to annotation file',
                    type = str,
                    action = 'store',
                    dest = 'annotFile',
                    required=True)

mandatory.add_argument('--outputdir',
                    help='Output Directory',
                    type = str,
                    action = 'store',
                    dest = 'outputDir',
                    required=True)

args = vars(parser.parse_args())


db_name = args['dbName'] + ".sqlite"
db_table = args['dbTable']
output_dir = args['outputDir']
annot_file_name = args['annotFile']


#-----------------------------------------------------------------------#
#                           Argument Checking                           #
#-----------------------------------------------------------------------#


OS_SEP = os_check()                                                     # Retrieve the directory separator by OS

# Create accessory directory (ex. log, data, database, etc.)
db_path = output_dir + OS_SEP + "database" + OS_SEP + db_name

#---------------------------Check Database------------------------------#

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    print('\nOpening database: ' + db_path)
else:
    raise ErrorDBNotExists(db_path)

if not os.path.exists(annot_file_name):
    raise ErrorAnnotFileNotExists(annot_file_name)

# no errors were raised, safe to connect to db
cur = conn.cursor()

#---------------------------Check Table---------------------------------#

if not table_exists(cur, db_table):
    raise ErrorTableNotInDB(db_table)




#-----------------------------------------------------------------------#
#                                File Setup                             #
#-----------------------------------------------------------------------#

# Path and name of Assembly Log File
log_path = output_dir + OS_SEP + "log"
str_annotate_log_file = output_dir + OS_SEP + "log" + OS_SEP + db_name + "_annotate.log"

# Check if the file already exists, either write or append to it.
if os.path.exists(str_annotate_log_file):
    annotate_log_file = open(str_annotate_log_file, "a")
else:
    annotate_log_file = open(str_annotate_log_file, "w")



# get list of column names in BioSample Table
cur.execute('''SELECT * FROM {}'''.format(db_table))
db_col_names = [description[0] for description in cur.description]

#-----------------------------------------------------------------------#
#                             Annotation Setup                          #
#-----------------------------------------------------------------------#
annot_file = open(annot_file_name, "r")
annot_dict = {}

# Read header columns into list
header_columns_list = annot_file.readline().split("\t")
header_dict = {}

for i,header in enumerate(header_columns_list):
    header_dict[i] = header

annot_line = annot_file.readline()

#-----------------------------------------------------------------------#
#                         Process Annotations                           #
#-----------------------------------------------------------------------#

while annot_line:
    # Create a dictionary for storing all attributes for this one line
    line_dict = {}
    # Split line since this is a tsv file
    split_line = annot_line.split("\t")
    # Walk through each column value
    for i,element in enumerate(split_line):
        # Save the name of the column/header being processed
        header = header_dict[i].strip()
        # Cleanup extra white space, remove extra quotation marks
        element = element.strip().replace('\"','')
        # Retrieve strain separately, it's the key to finding a matching record

        if header == 'strain':
            line_strain = element

        # IF annotation file header is a db column name, retain for annotation
        elif header in db_col_names:
            line_dict[header] = element

    # Check if strain is in table
    query = "SELECT * FROM {0} WHERE strain={1}".format(db_table,"'" + line_strain + "'")
    cur.execute(query)
    if not cur.fetchone():
        print("Entry not in DB: " + line_strain)
        #raise ErrorEntryNotInDB(line_strain)


    # This section allows for dynamic variable creation and column modification
    sql_dynamic_vars = ",".join([header + "=" + "'" + line_dict[header] + "'" for header in line_dict.keys()])
    query = ("UPDATE BioSample SET " + sql_dynamic_vars + " WHERE " + "strain=" + "'" + line_strain + "'")
    cur.execute(query)

    #------------------------WWrite to Logfile-------------------------#
    now = datetime.datetime.now()
    annotate_log_file.write("[" + str(now) + "]" +
                 "\t" + "Strain metadata modified:" +
                 "\t" + line_strain + "." + "\n")

    # Read in the next line
    annot_line = annot_file.readline()







#-----------------------------------------------------------------------#
#                                    Cleanup                            #
#-----------------------------------------------------------------------#
# Commit changes
conn.commit()
cur.close()
annotate_log_file.close()
annot_file.close()

print("File annotation is complete.")
