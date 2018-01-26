# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 17:55:59 2016

NCBI BioSample Table Generator

@author: Katherine Eaton
"""

# Default python libraries to import
import sqlite3                                                                 # SQL database functionality
import datetime                                                                # Date and time for log files
import os
from xml.dom import minidom

# Extra modules (pip installed) and custom files
from Bio import Entrez                                                         # Entrez NCBI API from biopython
from NCBInfect_Utilities import os_check

#-----------------------------------------------------------------------#
#                       Manipulating The BioSample Table                #
#-----------------------------------------------------------------------#

def BioSampleTable(db_name, SEARCH_TERM, EMAIL, output_dir):
    # User input variables to output
    print("\nCreating/Updating the BioSample table using the following parameters: ")
    print("Database: " + "\t" + db_name)
    print("SEARCH_TERM: " + "\t" + SEARCH_TERM)
    print("Email: " + "\t" + EMAIL)
    print("Output Directory: " + "\t" + output_dir + "\n\n")

    # Valid email to monitor entrez queries
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
                         warning TEXT,
                         biosample_id TEXT,
                         biosample_accession TEXT,
                         biosample_secondary_accession TEXT,
                         bioproject_accession TEXT,
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
    assembly_sample_set = set(cur.fetchall())
    assembly_sample_list = list(assembly_sample_set)

    # Grab all SRA records to get their corresponding Biosamples
    cur.execute('''SELECT biosample_accession,
                          bioproject_accession
                          FROM SRA''')

    # Store SRA-associated Biosamples as list
    sra_sample_set = set(cur.fetchall())
    sra_sample_list = list(sra_sample_set)

    # Concatenate lists (first convert to a set to get only unique biosamples)
    master_sample_list = assembly_sample_list + sra_sample_list
    master_sample_list.sort()

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

        # Secondary biosample accession when SRA points to 'wrong' biosample record
        biosample_secondary_accession = ""

        #biosample_accession = "SAMN00115134"
        #biosample_accession = "SAMN02141470"
        #bioproject_accession = "PRJNA47685"


        #-------------------Progress Log and Entry Counter-------------------#
        num_biosamples_processed += 1

        print("Processing BioSample Accession: " +
                    str(num_biosamples_processed) +
                    "/" +
                    str(num_biosamples))

        # ---------------------Check if record exists-----------------------#

        # Check if record exists as primary biosample accession
        cur.execute('''
        SELECT EXISTS(SELECT biosample_accession
                            FROM BioSample
                            WHERE biosample_accession=?)''',
                            (biosample_accession,))

        # 0 if not found, 1 if found
        record_exists_primary = cur.fetchone()[0]

        # Check if record exists as secondary biosample accession
        cur.execute('''
        SELECT EXISTS(SELECT biosample_secondary_accession
                            FROM BioSample
                            WHERE biosample_secondary_accession=?)''',
                            (biosample_accession,))

        # 0 if not found, 1 if found
        record_exists_secondary = cur.fetchone()[0]
        if record_exists_primary or record_exists_secondary:
            continue
        '''
        IMPORTANT:
        The Biosample accession should not exists in the BioSample table
        UNLESS the BioSample record was fully parsed.
        ie. The database does not get updated until the end of each record.
        '''

        #-------------------------------------------------------------------#
        #                        ERROR CATCHING BIOSAMPLES                  #
        #-------------------------------------------------------------------#

        # This table contains a heuristic to connecting records in the Assembly
        # and SRA tables. As a result, a perfect merge is not always possible. when
        # a perfect solution cannot be reached, warnings will be recorded.
        warning = ""
        '''
        This section attempts to deals with the spurious issue in which an
        organism/isolate/strain has duplicate BioSample records. Typically one
        of the duplicate records is more 'metadata-rich' than the other
        (generally the one associated with the 'Assembly' is better, and the
        duplicate one associated with the 'SRA' is poor).
        '''

        #-------------------------------------------------------------------#
        #            Check if Biosample is in Assembly and/or SRA           #
        #-------------------------------------------------------------------#

        #---------------------Get Assembly Record------------------#
        # Check if Biosample has an Assembly record
        cur.execute('''SELECT infraspecies, accession FROM Assembly WHERE biosample=?''',
                          (biosample_accession,))

        # Grab only the first record
        asm_sample_record = cur.fetchone()

        # If assembly record exists, save the infraspecies field
        if asm_sample_record:
            asm_sample_record_infraspecies = asm_sample_record[0]

        #--------------------Get SRA Record------------------------#
        # Check if Biosample has an SRA record
        cur.execute('''SELECT strain, sample_alias  FROM SRA WHERE biosample_accession=?''',
                           (biosample_accession,))

        # Grab just the first record
        sra_sample_record = cur.fetchone()

        # If SRA record exists, save the strain and alias fields
        if sra_sample_record:
            sra_sample_record_strain = sra_sample_record[0]
            sra_sample_record_alias = sra_sample_record[1]


        #-------------------------------------------------------------------#
        #               HEURISTIC DETECTION OF SECONDARY ACCESSION          #
        #-------------------------------------------------------------------#
        '''
        Check for the issue of different biosample accession between SRA and Assembly.
        Option 1) Biosample has both SRA and Assembly record = TOTALLY FINE
        Option 2) Biosample has only Assembly record = SEARCH FOR POSSIBLE SRA secondary accession
        Option 3) Biosample has only SRA Record = SEARCH FOR POSSIBLE Assembly secondary accession
        '''
        #---------------------------------------------------#
        # Option 1) No issue, no checking needed.           #
        #---------------------------------------------------#

        #---------------------------------------------------#
        # Option 2) Biosample has only Assembly record      #
        #           Search for secondary accession in SRA   #
        #---------------------------------------------------#
        if asm_sample_record and not sra_sample_record:
            # Check if Bioproject is in SRA Table
            cur.execute('''SELECT EXISTS(SELECT bioproject_accession FROM SRA
                                      WHERE bioproject_accession=?)''',
                                      (bioproject_accession,))

            sra_bioproject_exists = cur.fetchone()[0]

            # If it DOES NOT exist, no problem, this is an Assembly exclusive!
            if sra_bioproject_exists:

                # If it DOES Exists, there are two options:
                # 1) Not all strains in the BioProject were assembled = FINE
                # 2) SRA points to duplicate/poor-metadata BioSample = BAD

                # If Assembly:infraspecies field is missing, there's no hope of detecting
                if not asm_sample_record_infraspecies:
                    warning = "POSSIBLE SECONDARY ACCESSION IN SRA"

                # If Assembly:infraspecies field is present, good to compare
                else:
                    #-----------------Find Bioproject in SRA----------------------#
                    # Grab all SRA strains and sample_aliases associated with Bioproject
                    cur.execute('''SELECT biosample_accession, strain, sample_alias
                                     FROM SRA
                                     WHERE bioproject_accession=?''',
                                     (bioproject_accession,))

                    sra_bioproject_match = cur.fetchall()

                    # Go through each record, checking to see if there's a match in Assembly
                    # match_found: Boolean if found
                    # match_biosample_list: biosample accessions as list
                    match_found = False
                    match_biosample_set = set()

                    for record_match in sra_bioproject_match:
                        # Store needed sra variables for comparison
                        sra_match_biosample = record_match[0]
                        sra_match_strain = record_match[1]
                        sra_match_sample_alias = record_match[2]


                        # Search for match in infraspecies, strain, and sample_alias
                        if (asm_sample_record_infraspecies.lower() == sra_match_strain.lower() or
                          asm_sample_record_infraspecies.lower() == sra_match_sample_alias.lower()):

                            # If a match has been found for the first time, set flag to True
                            if not match_found:
                                match_found = True
                                match_biosample_set.add(sra_match_biosample)

                            # If a match has already been found, add to set
                            else:
                                match_biosample_set.add(sra_match_biosample)

                    # If no secondary accession was found, warning
                    if not match_found:
                        warning = "POSSIBLE SECONDARY ACCESSION IN SRA"
                    # If multiple accession were found, warning
                    elif len(match_biosample_set) > 1:
                        warning = "MULTIPLE SECONDARY ACCESSIONS FOUND IN SRA"
                        biosample_secondary_accession = str(match_biosample_set)
                    else:
                        biosample_secondary_accession = match_biosample_set.pop()


        #---------------------------------------------------#
        # Option 3) Biosample has only SRA record           #
        #        Search for secondary accession in Assembly #
        #---------------------------------------------------#
        elif sra_sample_record and not asm_sample_record:
            # Check if Bioproject is in Assembly Table
            cur.execute('''SELECT EXISTS(SELECT genbank_bioproject,infraspecies FROM Assembly
                                      WHERE genbank_bioproject=?)''',
                                      (bioproject_accession,))

            asm_bioproject_exists = cur.fetchone()[0]

            # If it DOES NOT exist, no problem, this is an SRA exclusive!
            if asm_bioproject_exists:
                # If it DOES Exists, there are two options:
                # 1) Not all strains in the BioProject were assembled = FINE
                # 2) SRA points to duplicate/poor-metadata BioSample = BAD

                # If SRA:strain or SRA_sample_alias field is missing, there's no hope of detecting
                if not sra_sample_record_strain and not sra_sample_record_alias:
                    warning = "POSSIBLE SECONDARY ACCESSION IN ASSEMBLY"

                # If SRA:strain or SRA_sample_alias field is present, good to compare
                else:
                    #-----------------Find Bioproject in Assembly----------------------#
                    # Grab all Assembly infraspecies associated with Bioproject
                    cur.execute('''SELECT biosample, infraspecies
                                     FROM Assembly
                                     WHERE genbank_bioproject=?''',
                                     (bioproject_accession,))

                    asm_bioproject_match = cur.fetchall()

                    # Go through each record, checking to see if there's a match in SRA
                    # match_found: Boolean if found
                    # match_biosample_list: biosample accessions as list
                    match_found = False
                    match_biosample_set = set()

                    for record_match in asm_bioproject_match:
                        # Store needed sra variables for comparison
                        asm_match_biosample = record_match[0]
                        asm_match_infraspecies = record_match[1]

                        # Search for match in infraspecies, strain, and sample_alias
                        if (sra_sample_record_strain.lower() == asm_match_infraspecies.lower() or
                          sra_sample_record_alias.lower() == asm_match_infraspecies.lower()):

                            # If a match has been found for the first time, set flag to True
                            if not match_found:
                                match_found = True
                                match_biosample_set.add(asm_match_biosample)

                            # If a match has already been found, check if it's simply duplicate biosamples
                            else:
                                match_biosample_set.add(asm_match_biosample)

                    # If no secondary accession was found, warning
                    if not match_found:
                        warning = "POSSIBLE SECONDARY ACCESSION IN ASSEMBLY"
                    # If multiple accession were found, warning
                    elif len(match_biosample_set) > 1:
                        warning = "MULTIPLE SECONDARY ACCESSIONS FOUND IN ASSEMBLY"
                        biosample_secondary_accession = str(match_biosample_list)
                    else:
                        biosample_secondary_accession = match_biosample_set.pop()


        #-------------------------------------------------------------------#
        #                         Metadata Retrieval                        #
        #-------------------------------------------------------------------#

        #------------------------Multiple biosample records-----------------#
        if biosample_secondary_accession:
            search_term = (biosample_accession + "[Biosample] OR " +
                 biosample_secondary_accession + "[Biosample]")
            handle = Entrez.esearch(db="biosample",
                    term=search_term,
                    retmax = 2)
            record = Entrez.read(handle)
            ID_list = record['IdList']

            largest_sampledata = ""
            ID_largest_sampledata = ""
            for ID in ID_list:
                #-------------------------Biosample Record--------------------#
                # Search for biosample entry using ID
                ID_handle = Entrez.esummary(db="biosample",id=ID)
                # Read in the search results
                ID_record = Entrez.read(ID_handle, validate = False)
                # Store metadata as string
                sampledata = ID_record['DocumentSummarySet']['DocumentSummary'][0]['SampleData']
                # Pick best metdata by record with longest string (ie. most char)
                if len(sampledata) > len(largest_sampledata):
                    largest_sampledata = sampledata
                    ID_largest_sampledata = ID

            ID = ID_largest_sampledata

        else:
            #------------------------Single biosample record-----------------#
            search_term = biosample_accession + "[Biosample]"
            handle = Entrez.esearch(db="biosample",
                        term=search_term,
                        retmax = 1)
            record = Entrez.read(handle)
            ID = record['IdList'][0]


        #-------------------------Biosample Record--------------------#
        # Search for biosample entry using ID
        biosample_ID = ID
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


        # --------------------------Update Database--------------------------#
        print ("Writing: " + biosample_accession + " to the database.\n")
        cur.execute('''
                     INSERT INTO BioSample (warning,
                             biosample_id,
                             biosample_accession,
                             biosample_secondary_accession,
                             bioproject_accession,
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
                                  ?, ?, ?, ?, ?)''',
                             (warning,
                             biosample_ID,
                             biosample_accession,
                             biosample_secondary_accession,
                             bioproject_accession,
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

#BioSampleTable("Yersinia_pestis_db.sqlite", "Yersinia pestis[Orgn]", "ktmeaton@gmail.com", ".")
