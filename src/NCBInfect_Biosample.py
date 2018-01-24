# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 17:55:59 2016

NCBI BioSample Table Generator

@author: Katherine Eaton
"""

import sqlite3                                                                 # SQL database functionality
import datetime                                                                # Date and time for log files
import os


from Bio import Entrez                                                         # Entrez NCBI API from biopython
from NCBInfect_Utilities import sampledata_retrieve,os_check

def BioSampleTable(dbName, ORGANISM, EMAIL, output_dir):
    ''' '''
    print("\nCreating/Updating the BioSample table using the following parameters: ")
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
    
    str_biosample_log_file = log_path + OS_SEP + ORGANISM.replace(" ", "_") + "_db_biosample.log"

    if os.path.exists(str_biosample_log_file):
        biosample_log_file = open(str_biosample_log_file, "a")                # Open logfile for appending
    else:
        biosample_log_file = open(str_biosample_log_file, "w")                 # Open logfile for writing


    #-----------------------------------------------------------------------#
    #                                SQL Setup                              #
    #-----------------------------------------------------------------------#

    conn = sqlite3.connect(dbName)                                             # Connect to the DB
    cur = conn.cursor()                                                        # Create cursor for commands


    #cur.execute('''DROP TABLE IF EXISTS BioSample''')

    #---------------------------BioSample Table----------------------------#
    cur.execute('''
    Create TABLE IF NOT EXISTS BioSample (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                         biosample_accession TEXT,
                         bioproject_accession TEXT,
                         assembly_accession TEXT,
                         sra_run_accession TEXT,
                         organism TEXT,
                         strain TEXT,
                         sample_title TEXT,
                         organization TEXT,
                         collection_date TEXT,
                         geographic_location TEXT,
                         collected_by TEXT,
                         isolate_source TEXT,
                         habitat TEXT,
                         latitude TEXT,
                         longitude TEXT,
                         latitude_and_longitude TEXT,
                         host TEXT,
                         host_disease TEXT,
                         host_status TEXT,
                         biovar TEXT,
                         biotype TEXT,
                         biogroup TEXT,
                         description TEXT,
                         publication_date TEXT,
                         modification_date TEXT)''')


    #-----------------------------------------------------------------------#
    #                         Create BioSample List                         #
    #-----------------------------------------------------------------------#


    # Grab all assemblies to get their corresponding biosamples
    cur.execute('''SELECT biosample,
                          genbank_bioproject
                            FROM Assembly''')

    # Store assembly-associated samples as list
    assembly_sample_list = cur.fetchall()


    # Grab all SRA records to get their correspond biosamples
    cur.execute('''SELECT biosample_accession,
                          bioproject_accession
                            FROM SRA''')

    # Store SRA-associated samples as list
    sra_sample_list = cur.fetchall()


    # Concatenate lists
    master_sample_list = list(assembly_sample_list + sra_sample_list)

    # Number of biosamples to process
    num_asm_samples = len(assembly_sample_list)
    num_sra_samples = len(sra_sample_list)
    num_tot_samples = len(master_sample_list)

    # Counter for progress log
    num_asm_samples_processed = 0
    num_sra_samples_processed = 0
    num_tot_samples_processed = 0


    # START WITH ASSEMBLY BIOSAMPLES

    for tuple_pair in master_sample_list:
        biosample_accession = tuple_pair[0]
        bioproject_accession = tuple_pair[1]
       
        #-------------------Progress Log and Entry Counter-------------------#
        num_tot_samples_processed += 1                                            # Increment assembly entry counter

        print("Processing BioSample Accession: " +
                    str(num_tot_samples_processed) +
                    "/" +
                    str(num_tot_samples))                                         # Print record progress to screen






        # ---------------------Check if record exists-----------------------#
        cur.execute('''
        SELECT EXISTS(SELECT biosample_accession
                            FROM BioSample
                            WHERE biosample_accession=?)''',
                            (biosample_accession,))                                  # Check if biosample record is already in BioSample Table

        record_exists = cur.fetchone()[0]                                      # 0 if not found, 1 if found


        if record_exists:
            continue
        '''
        IMPORTANT:
        The biosample accession should not exists in the BioProject table
        UNLESS the BioProject record was fully parsed.
        ie. The database does not get updated until the end of each record.
        '''

        #-------------------------------------------------------------------#
        #                            ERROR CATCHING ACCESSION               #
        #-------------------------------------------------------------------#


        #---------------------Get Assembly Link------------------#
        cur.execute('''
                    SELECT accession
                                   FROM Assembly
                                   WHERE biosample=?''',
                                   (biosample_accession,))

        asm_sample_record = cur.fetchone()
        if asm_sample_record: assembly_accession = asm_sample_record[0]
        else: assembly_accession = None

        #--------------------Get SRA Link------------------------#

        cur.execute('''
                    SELECT run_accession
                                   FROM SRA
                                   WHERE biosample_accession=?''',
                                   (biosample_accession,))

        sra_sample_record = cur.fetchone()
        if sra_sample_record: sra_run_accession = sra_sample_record[0]
        else: sra_run_accession = None

        '''
        Check for the issue of different biosample accession between SRA and Assembly.
        Option 1) Biosample has both SRA and Assembly record = TOTALLY FINE
        Option 2) Biosample has only Assembly record = FINE,
               assembly biosample metadata is as good as it gets.
        Option 3) Biosample has only SRA Record = POTENTIAL PROBLEM
               3a) Legitimate separate record (No issue)
               3b) Submitter 'error', SRA points to wrong BioSample.
        '''

        # Option 3 Problem
        # If it's a legitimate separate record, the SRA-linked
        # BioProject WILL NOT be in the Assembly Table

        if sra_run_accession and not assembly_accession:
            # Check if Bioproject is in Assembly Table
            cur.execute('''
                       SELECT EXISTS(SELECT genbank_bioproject 
                                      FROM Assembly
                                      WHERE genbank_bioproject=?)''',
                                      (bioproject_accession,))

            asm_bioproject_record_exists = cur.fetchone()[0]
            
            # If it DOES Exists, the SRA likeliy points to the wrong
            # BioSample record
            if asm_bioproject_record_exists:
                print(biosample_accession, bioproject_accession)
                continue





        # ---------------------Get Biosample ID-----------------------#
        search_term = biosample_accession + "[Biosample]"
        handle = Entrez.esearch(db="biosample",
                    term=search_term,
                    retmax = 1)
        record = Entrez.read(handle)
        ID = record['IdList'][0]

        #-------------------------Bioproject Record--------------------#
        ID_handle = Entrez.esummary(db="biosample",id=ID)                                 # Search for biosample entry using ID
        ID_record = Entrez.read(ID_handle, validate = False)                                 # Read in the search results
        record_dict = ID_record['DocumentSummarySet']['DocumentSummary'][0]                                        # Store metadata as dictionary

        # -----------------------BioSample attributes-----------------------#
        organism = record_dict['Organism']

        sampledata = record_dict['SampleData']


        # Try and get strain from the SampleData
        strain = sampledata_retrieve(sampledata, "strain")
        # If not possible, try and get from the identifiers
        if not strain:
           identifiers = record_dict['Identifiers'].split("; ")
           for element in identifiers:
              if element.startswith("Sample name"):
                 split_element = element.split()
                 strain = split_element[len(split_element) - 1]

        sample_title = record_dict['Title'].replace(";","")
        org = record_dict['Organization']
        col_date = sampledata_retrieve(sampledata, "collection_date")
        geo = sampledata_retrieve(sampledata, "geo")
        collected_by = sampledata_retrieve(sampledata, "collected_by")
        isolate = sampledata_retrieve(sampledata, "isolate_source")
        habitat = sampledata_retrieve(sampledata, "habitat")
        latitude = sampledata_retrieve(sampledata, "latitude")
        longitude = sampledata_retrieve(sampledata, "longitude")
        lat_long = sampledata_retrieve(sampledata, "lat_long")
        host = sampledata_retrieve(sampledata, "host")
        host_disease = sampledata_retrieve(sampledata, "host_disease")
        host_status = sampledata_retrieve(sampledata, "host_status")
        biovar = sampledata_retrieve(sampledata, "biovar")
        biotype = sampledata_retrieve(sampledata, "biotype")
        biogroup = sampledata_retrieve(sampledata, "group")
        description = sampledata_retrieve(sampledata, "description")
        mod_date = record_dict['ModificationDate']
        pub_date = record_dict['PublicationDate']

        # --------------------------Update Database--------------------------#
        cur.execute("SELECT EXISTS(SELECT biosample_accession FROM BioSample WHERE biosample_accession=?)", (biosample_accession,))
        record_exists = cur.fetchone()[0]

        if not record_exists:
          # Write to database
          print ("Writing: " + biosample_accession + " to the database.\n")
          cur.execute('''
          INSERT INTO BioSample (biosample_accession,
                             bioproject_accession,
                             assembly_accession,
                             sra_run_accession,
                             organism,
                             strain,
                             sample_title,
                             organization,
                             collection_date,
                             geographic_location,
                             collected_by,
                             isolate_source,
                             habitat,
                             latitude,
                             longitude,
                             latitude_and_longitude,
                             host,
                             host_disease,
                             host_status,
                             biovar,
                             biotype,
                             biogroup,
                             description,
                             publication_date,
                             modification_date)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                  ?, ?, ?, ?, ?)''',
                             (biosample_accession,
                             bioproject_accession,
                             assembly_accession,
                             sra_run_accession,
                             organism,
                             strain,
                             sample_title,
                             org,
                             col_date,
                             geo,
                             collected_by,
                             isolate,
                             habitat,
                             latitude,
                             longitude,
                             lat_long,
                             host,
                             host_disease,
                             host_status,
                             biovar,
                             biotype,
                             biogroup,
                             description,
                             pub_date,
                             mod_date))

          # Write to logfile
          now = datetime.datetime.now()
          biosample_log_file.write("[" + str(now) + "]" +
                         "\t" + "New accession number added:" +
                         "\t" + biosample_accession + "." + "\n")

          conn.commit()



    #----------------------------------------------------------------------#
    #                                    Cleanup                           #
    #----------------------------------------------------------------------#
    conn.commit()                                                              # Make sure all changes are committed to database
    cur.close()                                                                # Close the database
    biosample_log_file.close()                                                 # Close the logfile

BioSampleTable("database/Yersinia_pestis_sqlite.sqlite", "Yersinia pestis", "ktmeaton@gmail.com", ".")
