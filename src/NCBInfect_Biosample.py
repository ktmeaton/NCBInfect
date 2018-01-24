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
from NCBInfect_Utilities import os_check
from xml.dom import minidom

def BioSampleTable(db_name, SEARCH_TERM, EMAIL, output_dir):
    ''' '''
    print("\nCreating/Updating the BioSample table using the following parameters: ")
    print("Database: " + "\t" + db_name)
    print("SEARCH_TERM: " + "\t" + SEARCH_TERM)
    print("Email: " + "\t" + EMAIL)
    print("Output Directory: " + "\t" + output_dir + "\n\n")

    Entrez.email = EMAIL

    # Make sure directory separator is compatible with operating system
    OS_SEP = os_check()

    #-----------------------------------------------------------------------#
    #                                File Setup                             #
    #-----------------------------------------------------------------------#

    # Path to Database
    db_path = output_dir + OS_SEP + "database" + OS_SEP + db_name

    # Path and name of Biosample Log File
    log_path = output_dir + OS_SEP + "log"
    str_biosample_log_file = output_dir + OS_SEP + "log" + OS_SEP + db_name + "_biosample.log"


    # If log file exists, just append to it. Otherwise create it for writing.
    if os.path.exists(str_biosample_log_file):
        biosample_log_file = open(str_biosample_log_file, "a")
    else:
        biosample_log_file = open(str_biosample_log_file, "w")


    #-----------------------------------------------------------------------#
    #                                SQL Setup                              #
    #-----------------------------------------------------------------------#

    # Connect to database and establish cursor for commands.
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()


    #cur.execute('''DROP TABLE IF EXISTS BioSample''')

    #---------------------------BioSample Table----------------------------#
    cur.execute('''
    Create TABLE IF NOT EXISTS BioSample (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                         biosample_id TEXT,
                         biosample_accession TEXT,
                         biosample_secondary_accession TEXT,
                         bioproject_accession TEXT,
                         assembly_accession TEXT,
                         sra_run_accession TEXT,
                         organism TEXT,
                         strain TEXT,
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

    # Grab all assemblies to get their corresponding Biosamples
    cur.execute('''SELECT biosample,
                          genbank_bioproject
                          FROM Assembly''')

    # Store assembly-associated Biosamples as list
    assembly_sample_list = cur.fetchall()

    # Grab all SRA records to get their corresponding Biosamples
    cur.execute('''SELECT biosample_accession,
                          bioproject_accession
                          FROM SRA''')

    # Store SRA-associated Biosamples as list
    sra_sample_list = cur.fetchall()

    # Concatenate lists
    # NOTE: Assembly biosamples are always processed first
    master_sample_list = list(assembly_sample_list + sra_sample_list)

    # Number of biosamples to process
    num_biosamples = len(master_sample_list)

    # Counter for progress log
    num_biosamples_processed = 0



    #-----------------------------------------------------------------------#
    #                      Iterate Through BioSamples                       #
    #-----------------------------------------------------------------------#

    for tuple_pair in master_sample_list:
        # First element is the BioSample accession number
        biosample_accession = tuple_pair[0]
        # Second element is the BioProject accession number
        bioproject_accession = tuple_pair[1]

        #biosample_accession = "SAMN00704274"

        #-------------------Progress Log and Entry Counter-------------------#
        num_biosamples_processed += 1

        print("Processing BioSample Accession: " +
                    str(num_biosamples_processed) +
                    "/" +
                    str(num_biosamples))


        # ---------------------Check if record exists-----------------------#
        cur.execute('''
        SELECT EXISTS(SELECT biosample_accession
                            FROM BioSample
                            WHERE biosample_accession=?)''',
                            (biosample_accession,))

        # 0 if not found, 1 if found
        record_exists = cur.fetchone()[0]

        if record_exists:
            continue
        '''
        IMPORTANT:
        The Biosample accession should not exists in the BioSample table
        UNLESS the BioSample record was fully parsed.
        ie. The database does not get updated until the end of each record.
        '''

        #-------------------------------------------------------------------#
        #                        ERROR CATCHING ACCESSION                   #
        #-------------------------------------------------------------------#

        '''
        This section attempts to deals with the spurious issue in which an
        organism/isolate/strain has duplicate BioSample records. Typically one
        of the duplicate records is more 'metadata-rich' than the other
        (generally the one associated with the 'Assembly' is better, and the
        duplicate one associated with the 'SRA' is poor).
        '''

        biosample_secondary_accession = ""

        #---------------------Get Assembly Link------------------#
        # Check if Biosample has an Assembly record
        cur.execute('''
                    SELECT accession
                           FROM Assembly
                           WHERE biosample=?''',
                          (biosample_accession,))

        # 0 if not found, 1 if found
        asm_sample_record = cur.fetchone()

        if asm_sample_record: assembly_accession = asm_sample_record[0]
        else: assembly_accession = ""

        #--------------------Get SRA Link------------------------#
        # Check if Biosample has an SRA record
        cur.execute('''
                    SELECT run_accession, bioproject_accession, organism_taxid, strain, sample_alias
                           FROM SRA
                           WHERE biosample_accession=?''',
                           (biosample_accession,))

        # 0 if not found, 1 if found
        sra_sample_record = cur.fetchone()

        if sra_sample_record: sra_run_accession = sra_sample_record[0]
        else: sra_run_accession = ""

        '''
        Check for the issue of different biosample accession between SRA and Assembly.
        Option 1) Biosample has both SRA and Assembly record = TOTALLY FINE
        Option 2) Biosample has only Assembly record = FINE,
               assembly biosample metadata is as good as it gets.
        Option 3) Biosample has only SRA Record = POTENTIAL PROBLEM
               3a) Legitimate separate record (No issue)
               3b) Submitter 'error', SRA points to duplicate BioSample (poor metadata).
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

            print(biosample_accession)
            asm_bioproject_record_exists = cur.fetchone()[0]
            # If it DOES NOT exist, no problem, this is an SRA exclusive!

            # If it DOES Exists, there are two options:
            # 1) Not all strains in the BioProject were assembled = FINE
            # 2) SRA points to duplicate/poor-metadata BioSample
            if asm_bioproject_record_exists:

                sra_bioproject = sra_sample_record[1]
                sra_taxid = sra_sample_record[2]
                sra_strain = sra_sample_record[3]
                sra_sample_alias = sra_sample_record[4]

                cur.execute('''SELECT infraspecies, biosample, taxid, accession
                                 FROM Assembly
                                 WHERE genbank_bioproject=?''',
                                 (bioproject_accession,))

                assembly_match = cur.fetchall()

                for record_match in assembly_match:
                    asm_infraspecies = record_match[0]
                    asm_biosample = record_match[1]
                    asm_taxid = record_match[2]
                    asm_accession = record_match[3]



                    if sra_strain and (sra_strain.lower() == asm_infraspecies.lower())  :
                        biosample_secondary_accession = asm_biosample
                        assembly_accession = asm_accession
                        break

                    elif sra_sample_alias and (sra_sample_alias.lower() == asm_infraspecies.lower()):
                        biosample_secondary_accession = asm_biosample
                        assembly_accession = asm_accession
                        break

                if not biosample_secondary_accession:
                    print("WARNING: NO MATCH FOUND")
                    return(0)



        #return(0)


        # ---------------------Get Biosample ID-----------------------#
        search_term = biosample_accession + "[Biosample]"
        handle = Entrez.esearch(db="biosample",
                    term=search_term,
                    retmax = 1)
        record = Entrez.read(handle)
        ID = record['IdList'][0]

        biosample_ID = ID

        #-------------------------Bioproject Record--------------------#
        # Search for biosample entry using ID
        ID_handle = Entrez.esummary(db="biosample",id=ID)
        # Read in the search results
        ID_record = Entrez.read(ID_handle, validate = False)
        # Store metadata as dictionary
        record_dict = ID_record['DocumentSummarySet']['DocumentSummary'][0]

        # --------------------Attributes in Record Dict------------------------#
        organism = record_dict['Organism']
        org = record_dict['Organization']
        mod_date = record_dict['ModificationDate']
        pub_date = record_dict['PublicationDate']
        sampledata = record_dict['SampleData']

        # ------------------Attributes Requiring XML Parsing-------------------#
        # Just in case, wrap sampledata in a root node for XML formatting
        sample_xml = "<Root>" + sampledata + "</Root>"

        # minidom doc object for xml manipulation and parsing
        doc = minidom.parseString(sample_xml)

        # description is a straightforward singular tag to pull from 'Title'
        title_tag = doc.getElementsByTagName("Title")[0]
        description = title_tag.firstChild.data

        # A variety of fields found under generic tag "attribute_name"
        attribute_name_list = ['strain','collection_date','geo_loc_name','collected_by',
                          'isolation_source','habitat','latitude','longitude',
                          'lat_lon','host','host_disease','host_status',
                          'biovar','biotype','biogroup']

        # A dictionary to store names and values
        attribute_dict = {}

        # Grab all the attribute tags from the metadata XML
        attribute_tag_list = doc.getElementsByTagName("Attribute")

        # Iterate over each XML tag element
        for element in attribute_tag_list:
            # Grab the attribute name of that element
            try:
                attribute_name = element.attributes['harmonized_name'].value
            except KeyError:
                attribute_name = element.attributes['attribute_name'].value
            # If it's one of our desired fields, store it in the dictionary
            if attribute_name in attribute_name_list:
                attribute_dict[attribute_name] = element.firstChild.data

        # Now add in all the attribute names that were missing from the xml
        for attribute_name in attribute_name_list:
            if attribute_name not in attribute_dict:
                attribute_dict[attribute_name] = ""


        '''
        # If not possible, try and get from the identifiers
        if not strain:
           identifiers = record_dict['Identifiers'].split("; ")
           for element in identifiers:
              if element.startswith("Sample name"):
                 split_element = element.split()
                 strain = split_element[len(split_element) - 1]
        '''

        # --------------------------Update Database--------------------------#
        print ("Writing: " + biosample_accession + " to the database.\n")
        cur.execute('''
                     INSERT INTO BioSample (biosample_id,
                             biosample_accession,
                             biosample_secondary_accession,
                             bioproject_accession,
                             assembly_accession,
                             sra_run_accession,
                             organism,
                             strain,
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
                                  ?, ?, ?, ?, ?, ?)''',
                             (biosample_ID,
                             biosample_accession,
                             biosample_secondary_accession,
                             bioproject_accession,
                             assembly_accession,
                             sra_run_accession,
                             organism,
                             attribute_dict['strain'],
                             org,
                             attribute_dict['collection_date'],
                             attribute_dict['geo_loc_name'],
                             attribute_dict['collected_by'],
                             attribute_dict['isolation_source'],
                             attribute_dict['habitat'],
                             attribute_dict['latitude'],
                             attribute_dict['longitude'],
                             attribute_dict['lat_lon'],
                             attribute_dict['host'],
                             attribute_dict['host_disease'],
                             attribute_dict['host_status'],
                             attribute_dict['biovar'],
                             attribute_dict['biotype'],
                             attribute_dict['biogroup'],
                             description,
                             pub_date,
                             mod_date))

        # Write to logfile
        now = datetime.datetime.now()
        biosample_log_file.write("[" + str(now) + "]" +
                         "\t" + "New accession number added:" +
                         "\t" + biosample_accession + "." + "\n")

        # Commit individual record to database
        conn.commit()



    #----------------------------------------------------------------------#
    #                              Cleanup                                 #
    #----------------------------------------------------------------------#
    # Make sure all changes are committed to database
    conn.commit()
    # Close the database
    cur.close()
    # Close the logfile
    biosample_log_file.close()

BioSampleTable("Yersinia_pestis_db.sqlite", "Yersinia pestis[Orgn]", "ktmeaton@gmail.com", ".")
