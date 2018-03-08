# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 14:09:59 2016
Edited: June 6, 2017 - post-GI number removal check
Major Update: January 22, 2018 - rename to NCBInfect, conceptual
change.

@author: Katherine Eaton

"NCBInfect Module"
"""

import argparse                                                         # Command-line argument parsing
import sqlite3
import os

from NCBInfect_Errors import *
import NCBInfect_SRA
import NCBInfect_Assembly
import NCBInfect_Utilities
import NCBInfect_Bioproject
import NCBInfect_Biosample


#-----------------------------------------------------------------------#
#                            Argument Parsing                           #
#-----------------------------------------------------------------------#


# Retrieve directory separator by Operating System
OS_SEP = NCBInfect_Utilities.os_check()

# To Be Done: Full Description
parser = argparse.ArgumentParser(description='Description of NCBInfect.',
                                 add_help=True)


# Mandatory arguments to the program
mandatory = parser.add_argument_group('mandatory')


mandatory.add_argument('--mode',
                    help = 'Create, Update, or Delete Genome Database',
                    action = 'store',
                    dest = 'mode',
                    required = True)


mandatory.add_argument('--database',
                    help='Genome Database Name',
                    type = str,
                    action = 'store',
                    dest = 'db_name',
                    required=True)

mandatory.add_argument('--outputdir',
                    help='Output Directory',
                    type = str,
                    action = 'store',
                    dest = 'output_dir',
                    required=True)


# Retrieve user parameters
args = vars(parser.parse_args())

mode = args['mode']
db_name = args['db_name'] + ".sqlite"
output_dir = args['output_dir']


#-------------------------------------------------------------------------------#
#                           Argument Checking                                   #
#-------------------------------------------------------------------------------#


# Create accessory directory (ex. log, data, database, etc.)
NCBInfect_Utilities.check_accessory_dir(output_dir)

db_path = output_dir + OS_SEP + "database" + OS_SEP + db_name

#-------------------------Delete Database-------------------------------------#

if mode.lower() == 'delete':
    if os.path.exists(db_path):
        os.remove(db_path)
        print('\nDeleting database: ' + db_path)
    else:
        raise ErrorDBNotExists(db_path)


#-------------------------Create Database-------------------------------------#
elif mode.lower() == 'create':
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.commit()
        print('\nCreating database: ' + db_path)
    else:
        raise ErrorDBExists(db_path)


#---------------------------------Update Database-----------------------------#
elif mode.lower() == 'update':
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        print('\nOpening database: ' + db_path)
    else:
        raise ErrorDBNotExists(db_path)

#----------------------------------Invalid Mode-------------------------------#
else:
    raise ErrorInvalidMode(mode)



#-----------------------------------------------------------------------------#
#                              Create/Update Tables                           #
#-----------------------------------------------------------------------------#


#-------------------------------Create Mode Processing------------------------#

if mode.lower() == 'create' or mode.lower() == 'update':

   #-----------------------------NCBI Info-----------------------------#
    EMAIL =  input('\n\
    Please enter a valid email address for NCBI queries: ')
    SEARCH_TERM = input('\n\
    Please enter an entrez search term: ')


    #------------------------Assembly User Input-----------------------#
    modify_assembly = input('\n\
    Do you want to create/update the Assembly table? (Y/N)')
    while modify_assembly.lower() != 'y' and modify_assembly.lower() != 'n':
        print ("\tInvalid input, must be either 'Y','y','N', or 'n'.")
        modify_assembly = input('\n\
        Do you want to create/update the Assembly table? (Y/N)')

    #---------------------------Assembly Table--------------------------#

    if modify_assembly.lower() == 'y':
        NCBInfect_Assembly.AssemblyTable(db_name, SEARCH_TERM, EMAIL, output_dir)





    #----------------------------SRA User Input-------------------------#
    modify_sra = input('\n\
    Do you want to create/update the SRA table? (Y/N)')
    while modify_sra.lower() != 'y' and modify_sra.lower() != 'n':
        print ("\tInvalid input, must be either 'Y','y','N', or 'n'.")
        modify_sra = input('\n\
        Do you want to create/update the SRA table? (Y/N)')


    #-----------------------------SRA Table-----------------------------#
    if modify_sra.lower() == 'y':
        NCBInfect_SRA.SRATable(db_name, SEARCH_TERM, EMAIL, output_dir)



    #------------------------Bioproject User Input----------------------#
    modify_bioproject = input('\n\
    Do you want to create/update the BioProject table? (Y/N)')
    while modify_bioproject.lower() != 'y' and modify_bioproject.lower() != 'n':
        print ("\tInvalid input, must be either 'Y','y','N', or 'n'.")
        modify_bioproject = input('\n\
        Do you want to create/update the Bioproject table? (Y/N)')


    #---------------------------Bioproject Table------------------------#
    if modify_bioproject.lower() == 'y':
        NCBInfect_Bioproject.BioProjectTable(db_name, SEARCH_TERM, EMAIL, output_dir)




    #------------------------Biosample User Input----------------------#
    modify_biosample = input('\n\
    Do you want to create/update the BioSample table? (Y/N)')
    while modify_biosample.lower() != 'y' and modify_biosample.lower() != 'n':
        print ("\tInvalid input, must be either 'Y','y','N', or 'n'.")
        modify_biosample = input('\n\
        Do you want to create/update the BioSample table? (Y/N)')


    #---------------------------Biosample Table------------------------#
    if modify_biosample.lower() == 'y':
        NCBInfect_Biosample.BioSampleTable(db_name, SEARCH_TERM, EMAIL, output_dir)



'''


    #-----------------------Nucleotide User Input----------------------#
    modify_nucleotide = input('\n\
    Do you want to create/update the Nucleotide table and download genomes? (Y/N)')
    while modify_nucleotide.lower() != 'y' and modify_nucleotide.lower() != 'n':
        print ("\tInvalid input, must be either 'Y','y','N', or 'n'.")
        modify_nucleotide = input('\n\
        Do you want to create/update the Nucleotide table and download genomes? (Y/N)')


    #--------------------------Nucleotide Table------------------------#
    if modify_nucleotide.lower() == 'y':
        genomenucleotide.NucleotideTable(db_path, SEARCH_TERM, EMAIL, output_dir)
'''

print("NCBInfect has finished.")
