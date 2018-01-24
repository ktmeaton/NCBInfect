# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 17:20:43 2016

NCBI BioProject Table Generator

@author: Katherine Eaton
"""

import sqlite3                                                                 # SQL database functionality
import datetime                                                                # Date and time for log files
import os


from Bio import Entrez                                                         # Entrez NCBI API from biopython
from NCBInfect_Utilities import metadata_count, os_check

def BioProjectTable(dbName, ORGANISM, EMAIL, output_dir):
    ''' '''
    print("\nCreating/Updating the BioProject table using the following parameters: ")
    print("Database: " + "\t" + dbName)
    print("Organism: " + "\t" + ORGANISM)
    print("Email: " + "\t" + EMAIL)
    print("Output Directory: " + "\t" + output_dir + "\n\n")

    Entrez.email = EMAIL

    OS_SEP = os_check()                                                        # Retrieve the directory separator by OS

    #-----------------------------------------------------------------------#
    #                                File Setup                             #
    #-----------------------------------------------------------------------#
    log_path = output_dir + OS_SEP + "log"

    str_bioproject_log_file = log_path + OS_SEP + ORGANISM.replace(" ", "_") + "_db_bioproject.log"

    if os.path.exists(str_bioproject_log_file):
        bioproject_log_file = open(str_bioproject_log_file, "a")               # Open logfile for appending
    else:
        bioproject_log_file = open(str_bioproject_log_file, "w")               # Open logfile for writing
        

    #-----------------------------------------------------------------------#
    #                                SQL Setup                              #
    #-----------------------------------------------------------------------#

    # Conncet to database and establish cursor for commands.
    conn = sqlite3.connect(dbName)                                             
    cur = conn.cursor()                                                       


    #---------------------------BioProjects Table----------------------------#
    cur.execute('''
    Create TABLE IF NOT EXISTS BioProject (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                           bioproject_id TEXT,
                                           accession TEXT,
                                           status TEXT,
                                           data_type TEXT,
                                           objectives TEXT,
                                           project_scope TEXT,
                                           description TEXT,
                                           organization TEXT,
                                           registration_date TEXT)''')




    #-----------------------------------------------------------------------#
    #                         Create Assembly/SRA List                          #
    #-----------------------------------------------------------------------#

    # Grab all assemblies to get their corresponding bioprojects
    cur.execute('''SELECT genbank_bioproject
                            FROM Assembly''')                  

    # Store assembly-associated projects as list
    assembly_bioproject_list = cur.fetchall()             


    # Grab all SRA records to get their correspond bioprojects
    cur.execute('''SELECT bioproject_accession
                            FROM SRA''')

    # Store SRA-associated proejcts as list
    sra_bioproject_list = cur.fetchall()

    # Combine the two lists into one master list
    # Using 'set' ensures no duplicate entries
    concat_bioproject_list = list(set(assembly_bioproject_list + sra_bioproject_list))
    master_bioproject_list = []
    
    for tuple_pair in concat_bioproject_list:
        master_bioproject_list.append(tuple_pair[0])

    master_bioproject_list.sort()

    
    # Number of bioprojects to process
    num_bioproject = len(master_bioproject_list)     
    # Counter for progress log
    num_bioproject_processed = 0                        




    for bioproject_accession in master_bioproject_list:
        
        #-------------------Progress Log and Entry Counter-------------------#
        num_bioproject_processed += 1                

        print("Processing Bioproject Accession: " +
                    str(num_bioproject_processed) +
                    "/" +
                    str(num_bioproject))             


        # ---------------------Check if record exists-----------------------#
 
        # Check if this bioproject already exists in the db
        cur.execute('''
        SELECT EXISTS(SELECT accession
                            FROM BioProject
                            WHERE accession=?)''',
                            (bioproject_accession,))                    

        # 0 if not found, 1 if found
        record_exists = cur.fetchone()[0]                  

        if record_exists:
            continue
            '''
            IMPORTANT:
            The bioproject accession should not exists in the BioProject table
            UNLESS the BioProject record was fully parsed.
            ie. The database does not get updated until the end of each record.
            '''

        # ---------------------Get Bioproject ID-----------------------#
        search_term = bioproject_accession + "[Bioproject]"
        handle = Entrez.esearch(db="bioproject",
                    term=search_term,
                    retmax = 1)
        record = Entrez.read(handle)
        ID = record["IdList"][0]

        #-------------------------Bioproject Record--------------------#
        ID_handle = Entrez.esummary(db="bioproject",id=ID)                 # Search for biorproject entry using ID
        ID_record = Entrez.read(ID_handle)                                 # Read in the search results
        record_dict = ID_record['DocumentSummarySet']['DocumentSummary'][0]                                        # Store metadata as dictionary


        # -----------------------Bioproject attributes-----------------#
        status = record_dict['Sequencing_Status']
        data_type = record_dict['Project_Data_Type']


        # Objective are a list containing multiple dictionary element
        obj_list = record_dict['Project_Objectives_List']

        # Going to construct a comma-separated strin gof objectives
        obj_str = ""
        obj_counter = 1

        # Iterate over each objective
        for item in obj_list:

           # This length is purely so a comma is only used to separate
           # the last two elements.
           if obj_counter < len(obj_list):
              obj_str += item['Project_ObjectivesType'] + ", "
           else:
              obj_str += item['Project_ObjectivesType']
           obj_counter += 1


        proj_scope = record_dict['Project_Target_Scope']
        description = record_dict['Project_Description']
        organization = record_dict['Submitter_Organization']
        reg_date = record_dict['Registration_Date']




        # --------------------------Update Database--------------------------#
        print ("Writing Bioproject: " + bioproject_accession + " to the database.\n")
        cur.execute('''
        INSERT INTO BioProject (bioproject_id,
                              accession,
                              status,
                              data_type,
                              objectives,
                              project_scope,
                              description,
                              organization,
                              registration_date)
                              VALUES
                              (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (ID,
                         bioproject_accession,
                          status,
                          data_type,
                          obj_str,
                          proj_scope,
                          description,
                          organization,
                          reg_date))

        # Write to logfile
        now = datetime.datetime.now()
        bioproject_log_file.write("[" + str(now) + "]" +
                     "\t" + "New accession number added:" +
                     "\t" + bioproject_accession + "." + "\n")
        conn.commit()



    #----------------------------------------------------------------------#
    #                                    Cleanup                           #
    #----------------------------------------------------------------------#
    conn.commit()                                                              # Make sure all changes are committed to database
    cur.close()                                                                # Close the database
    bioproject_log_file.close()                                                # Close the logfile

#BioProjectTable("database/Yersinia_pestis_sqlite.sqlite", "Yersinia pestis", "ktmeaton@gmail.com", ".")
