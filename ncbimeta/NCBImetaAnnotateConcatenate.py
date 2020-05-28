#!/usr/bin/env python3
"""
NCBImeta Annotation Tool - Concatenate database fields with
                           values from an annotation file.

@author: Katherine Eaton
"""

# -----------------------------------------------------------------------------#
#                            Argument Parsing                                  #
# -----------------------------------------------------------------------------#

import argparse  # Command-line argument parsing
import sqlite3  # Database storage and queries
import os  # Filepath operations

from ncbimeta import NCBImetaErrors  # NCBImeta Error Classes
from ncbimeta import NCBImetaUtilities  # Need table_exists and sql_sanitize

# -----------------------------------------------------------------------------#
#                            Argument Parsing                                  #
# -----------------------------------------------------------------------------#

parser = argparse.ArgumentParser(
    description=(
        "NCBImeta Annotation Tool - Concatenate database fields with "
        + " values from an annotation file."
    ),
    add_help=True,
)

mandatory = parser.add_argument_group("mandatory")
bonus = parser.add_argument_group("bonus")

mandatory.add_argument(
    "--database",
    help="Path to the sqlite database generated by NCBImeta.",
    type=str,
    action="store",
    dest="dbName",
    required=True,
)

mandatory.add_argument(
    "--table",
    help="Table in NCBImeta database to modify",
    type=str,
    action="store",
    dest="dbTable",
    required=True,
)

mandatory.add_argument(
    "--annotfile",
    help=(
        "Path to annotation file. The first column must contain a "
        + "field that is unique to the record (ex. Accession)"
    ),
    type=str,
    action="store",
    dest="annotFile",
    required=True,
)

parser.add_argument("--version", action="version", version="%(prog)s v0.6.7a")


args = vars(parser.parse_args())

db_name = args["dbName"]
db_table = args["dbTable"]
annot_file_name = args["annotFile"]
db_value_sep = ";"


# -----------------------------------------------------------------------------#
#                           Argument Checking                                  #
# -----------------------------------------------------------------------------#


# ---------------------------Check Database------------------------------------#

if os.path.exists(db_name):
    conn = sqlite3.connect(db_name)
    print("\nOpening database: " + db_name, flush=True)
else:
    raise NCBImetaErrors.ErrorDBNotExists(db_name)

if not os.path.exists(annot_file_name):
    raise NCBImetaErrors.ErrorAnnotFileNotExists(annot_file_name)

# no errors were raised, safe to connect to db
cur = conn.cursor()

# ---------------------------Check Table---------------------------------------#

# Check table name
table_name = db_table
table_name_sanitize = NCBImetaUtilities.sql_sanitize(table_name)
if table_name != table_name_sanitize:
    raise NCBImetaErrors.ErrorSQLNameSanitize(table_name, table_name_sanitize)

# Check table exists
if not NCBImetaUtilities.table_exists(cur, db_table):
    raise NCBImetaErrors.ErrorTableNotInDB(db_table)


# -----------------------------------------------------------------------------#
#                                File Setup                                    #
# -----------------------------------------------------------------------------#

# get list of column names in Table
cur.execute("""SELECT * FROM {}""".format(db_table))
db_col_names = [description[0] for description in cur.description]

# -----------------------------------------------------------------------------#
#                             Annotation Setup                                 #
# -----------------------------------------------------------------------------#
annot_file = open(annot_file_name, "r")
annot_dict = {}

# Read header columns into list, remove whitespace char like newline
header_columns_list = annot_file.readline().strip().split("\t")

# Check column names
for col_name in header_columns_list:
    col_name_sanitize = NCBImetaUtilities.sql_sanitize(col_name)
    if col_name != col_name_sanitize:
        raise NCBImetaErrors.ErrorSQLNameSanitize(col_name, col_name_sanitize)

# Store in dictionary
header_dict = {}
header_db_dict = {}

for i, header in enumerate(header_columns_list):
    header_dict[i] = header

annot_line = annot_file.readline()


# -----------------------------------------------------------------------------#
#                         Process Annotations                                  #
# -----------------------------------------------------------------------------#

while annot_line:
    # Create a dictionary for storing all attributes for this one line
    line_dict = {}
    # Split line since this is a tsv file
    split_line = annot_line.split("\t")
    # Walk through each column value
    for i, element in enumerate(split_line):
        # Save the name of the column/header being processed
        header = header_dict[i].strip()
        # Cleanup extra white space?
        element = element.strip()

        # If it's the first col (index 0) this is the unique col for matching
        if i == 0:
            unique_header = header
            unique_element = element

        # IF annotation file header is a db column name, retain for annotation
        elif header in db_col_names:
            line_dict[header] = element

    # Check if unique_element is in table
    query = "SELECT * FROM {0} WHERE {1}=?".format(db_table, unique_header)

    cur.execute(query, (unique_element,))
    fetch_records = cur.fetchall()

    # Check if the record could be found in the database
    if not fetch_records:
        print(
            "Entry not in DB: " + unique_element + ". No annotation is added.",
            flush=True,
        )
        # raise NCBImetaErrors.ErrorEntryNotInDB(unique_element)
        annot_line = annot_file.readline()
        continue

    # Check if there were multiple hits in the database
    elif len(fetch_records) > 1:
        print(
            "Multiple Matches in DB: " + unique_element + ". No annotation is added.",
            flush=True,
        )
        # raise NCBImetaErrors.ErrorEntryMultipleMatches(line_strain)
        annot_line = annot_file.readline()
        continue

    # Retrieve the original database value for that cell
    for header in line_dict:
        header_query = "SELECT {0} FROM {1} WHERE {2}=?".format(
            header, db_table, unique_header
        )

        cur.execute(header_query, (unique_element,))
        db_value = cur.fetchall()[0]

        # Check if it's a tuple (mostly lat and lon)
        if type(db_value) == tuple:
            # If it's not just an empty tuple (None,)
            if db_value[0]:
                db_value = "".join(db_value)
            else:
                db_value = ""

        # If the database cell is non-empty concatenate custom Metadata
        # by db_value_sep (;)
        if db_value:
            line_dict[header] = db_value + db_value_sep + line_dict[header]

    # This section allows for dynamic variable creation and column modification
    sql_dynamic_colnames_list = [colname + "=?" for colname in line_dict.keys()]
    sql_dynamic_colnames = ",".join(sql_dynamic_colnames_list)
    sql_values_placeholder = [line_dict[header] for header in line_dict.keys()]
    sql_query = (
        "UPDATE "
        + db_table
        + " SET "
        + sql_dynamic_colnames
        + " WHERE "
        + unique_header
        + "="
        + "'"
        + unique_element
        + "'"
    )

    print(
        "Entry "
        + unique_element
        + " found in db. "
        + sql_query
        + str(sql_values_placeholder)
    )
    cur.execute(sql_query, sql_values_placeholder)

    # Read in the next line
    annot_line = annot_file.readline()

# -----------------------------------------------------------------------------#
#                                    Cleanup                                   #
# -----------------------------------------------------------------------------#
# Commit changes
conn.commit()
print("Closing database: " + db_name, flush=True)
cur.close()
annot_file.close()
