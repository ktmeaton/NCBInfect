# -*- coding: utf-8 -*-
"""
NCBI Assembly Table Generator

"""

import sqlite3                                                                 # SQL database functionality
import datetime                                                                # Date and time for log files
import os
from xml.dom import minidom                                                    # XML Parsing


from Bio import Entrez                                                         # Entrez NCBI API from biopython
from NCBInfect_Utilities import metadata_count, os_check


def AssemblyTable(dbName, ORGANISM, EMAIL, output_dir):
    ''' '''
    print("\nCreating/Updating the Assembly table using the following parameters: ")
    print("Database: " + "\t" + dbName)
    print("Organism: " + "\t" + ORGANISM)
    print("Email: " + "\t" + EMAIL)
    print("Output Directory: " + "\t" + output_dir + "\n\n")

    Entrez.email = EMAIL

    OS_SEP = os_check()                                                         # Retrieve the directory separator by OS

    #---------------------------------------------------------------------------#
    #                                File Setup                                 #
    #---------------------------------------------------------------------------#

    # Path and name of Assembly Log File
    log_path = output_dir + OS_SEP + "log"    
    str_assembly_log_file = output_dir + OS_SEP + "log" + OS_SEP + ORGANISM.replace(" ", "_") + "_db_assembly.log"

    # Check if the file already exists, either write or append to it.
    if os.path.exists(str_assembly_log_file):
        assembly_log_file = open(str_assembly_log_file, "a")                   # Open logfile for appending
    else:
        assembly_log_file = open(str_assembly_log_file, "w")                   # Open logfile for writing

    #--------------------------------------------------------------------------#
    #                                SQL Setup                                 #
    #--------------------------------------------------------------------------#

    conn = sqlite3.connect(dbName)                                             # Connect to the DB
    cur = conn.cursor()                                                        # Create cursor for commands

    #--------------------------------------------------------------------------#
    #                             Assembly Table                               #
    #--------------------------------------------------------------------------#
    cur.execute('''
    Create TABLE IF NOT EXISTS Assembly (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                         assembly_id TEXT,
                                         accession TEXT UNIQUE,
                                         organism TEXT,
                                         infraspecies TEXT,
                                         assembly_status TEXT,
                                         organization TEXT,
                                         taxid TEXT,
                                         biosample TEXT,
                                         coverage FLOAT,
                                         replicon_count int,
                                         chromosome_count int,
                                         non_chromosome_replicon_count int,
                                         contig_count int,
                                         contig_l50_count int,
                                         contig_n50_count int,
                                         scaffold int,
                                         scaffold_l50_count int,
                                         scaffold_n50_count int,
                                         total_length int,
                                         ungapped_length int,
                                         genbank_bioproject TEXT,
                                         wgs_project TEXT,
                                         submission_date TEXT,
                                         sequence_release_date TEXT,
                                         assembly_release_date TEXT)''')



    #-----------------------------------------------------------------------#
    #                           Entrez Assemblies                           #
    #-----------------------------------------------------------------------#
    search_term = ORGANISM + "[Orgn]"
    handle = Entrez.esearch(db="assembly",
                            term=search_term,
                            retmax = 1000)

    record = Entrez.read(handle)                                                   # Read the record
    num_records = int(record['Count'])                                             # Count the total number of entries
    num_processed = 0                                                              # Counter for num entries processed


    #-----------------------------------------------------------------------#
    #                          Iterate Through ID List                      #
    #-----------------------------------------------------------------------#

    for ID in record['IdList']:
       #-------------------Progress Log and Entry Counter-------------------#
       num_processed += 1                                                          # Increment entry counter
       print("Processing record: " +
           str(num_processed) + \
           "/" + str(num_records))                                                 # Print record progress to screen


       #------------Check if Assembly Already Exists in Database------------#
       cur.execute('''
       SELECT EXISTS(SELECT assembly_id FROM Assembly WHERE assembly_id=?)''',\
       (ID,))                                                                      # Check if assembly exists in DB
       record_exists = cur.fetchone()[0]                                           # 0 if not found, 1 if found


       #---------------If Assembly Isn't in Database, Add it------------#
       if not record_exists:

           ID_handle = Entrez.esummary(db="assembly",id=ID)                        # Retrieve Assembly record using ID
           ID_record = Entrez.read(ID_handle, validate=False)                      # Read Assembly record
           record_dict = ID_record['DocumentSummarySet']['DocumentSummary'][0]     # Store Assembly information as dictionary


           entrez_string_element = type(record_dict['Taxid'])                      # Get type of Bio String object (used in type checking)


           # -----------------------Asssembly attributes-----------------------#
           accession = record_dict['AssemblyAccession']                            # Assembly accession number
           organism = record_dict['Organism']                                      # Organism name (sometimes includes straing)
           asm_status = record_dict['AssemblyStatus']                              # Status of assembly (complete, chromosome, scaffold, contig)
           organization = record_dict['SubmitterOrganization']                     # Organization that submitted the record
           taxid = record_dict['Taxid']                                            # NCBI Taxonomic ID number (specific to strain!)
           biosample = record_dict['BioSampleAccn']                                # Biosample accession number
           coverage = float(record_dict['Coverage'])                               # Average coverage of assembly
           sub_date = record_dict['SubmissionDate']                                # Submission date
           seq_rel_date = record_dict['SeqReleaseDate']                            # Sequence release date
           asm_rel_date= record_dict['SubmissionDate']                             # Assembly release date
           wgs_proj = record_dict['WGS']                                           # Whole genome sequence project accession
           meta_string = record_dict['Meta']                                       # Metadata as entered by submitter


           # The metadata is xml missing the root node. Wrap a root
           # node around it.
           meta_xml = "<Root>" + meta_string + "</Root>"
           doc = minidom.parseString(meta_xml)

           stat_tag_list = doc.getElementsByTagName("Stat")

           for element in stat_tag_list:

               category = element.attributes['category'].value

               if category == 'chromosome_count':
                   chromosome_count = element.firstChild.data

               elif category == 'replicon_count':
                   replicon_count = element.firstChild.data

               elif category == 'non_chromosome_replicon_count':
                   non_chr_replicon_count = element.firstChild.data

               elif category == 'contig_count':
                   contig_count = element.firstChild.data

               elif category == 'contig_l50':
                   contig_l50_count = element.firstChild.data

               elif category == 'contig_n50':
                   contig_n50_count = element.firstChild.data

               elif category == 'scaffold_count':
                   scaffold_count = element.firstChild.data

               elif category == 'scaffold_l50':
                   scaffold_l50_count = element.firstChild.data

               elif category == 'scaffold_n50':
                   scaffold_n50_count = element.firstChild.data

               elif category == 'total_length':
                   total_length = element.firstChild.data  

               elif category == 'ungapped_length':
                   ungapped_length = element.firstChild.data
                   

           # --------------------Inconsistent attributes---------------------#
           if record_dict['Biosource']['InfraspeciesList']:                        # Useful when 'Organism' does not include strain info
               infraspecies = record_dict['Biosource']['InfraspeciesList'][0]['Sub_value']
           else: infraspecies = ""                                                 # Sometimes the Infraspecies key is blank

           if record_dict['GB_BioProjects']:                                       # Genbank specific bioproject accession
               bioproj_gb_accession = record_dict['GB_BioProjects'][0]['BioprojectAccn']
           else: bioproj_gb_accession = ""                                         # Sometimes no Genabnk bioproject is associated

           #if record_dict['RS_BioProjects']:                                       # Refseq specific bioproject accession
           #    bioproj_rs_accession = record_dict['RS_BioProjects'][0]['BioprojectAccn']
           #else: bioproj_rs_accession = ""                                         # Sometimes no Refseq bioproject is associated





           # ------------------------Update Database-------------------------#
           print ("Writing: " + accession + " to the database.\n")                 # Print progress log to screen
           cur.execute('''
           INSERT INTO Assembly (assembly_id,
                                 accession,
                                organism,
                                infraspecies,
                                assembly_status,
                                organization,
                                taxid,
                                biosample,
                                coverage,
                                replicon_count,
                                chromosome_count,
                                non_chromosome_replicon_count,
                                contig_count,
                                contig_l50_count,
                                contig_n50_count,
                                scaffold,
                                scaffold_l50_count,
                                scaffold_n50_count,
                                total_length,
                                ungapped_length,
                                genbank_bioproject,
                                wgs_project,
                                submission_date,
                                sequence_release_date,
                                assembly_release_date)
                                VALUES (
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                ?, ?, ?, ?, ?)''',
                             (ID,
                             accession,
                             organism,
                             infraspecies,
                             asm_status,
                             organization,
                             taxid,
                             biosample,
                             coverage,
                             replicon_count,
                             chromosome_count,
                             non_chr_replicon_count,
                             contig_count,
                             contig_l50_count,
                             contig_n50_count,
                             scaffold_count,
                             scaffold_l50_count,
                             scaffold_n50_count,
                             total_length,
                             ungapped_length,
                             bioproj_gb_accession,
                             wgs_proj,
                             sub_date,
                             seq_rel_date,
                             asm_rel_date))



           # ------------------------WWrite to Logfile-------------------------#
           now = datetime.datetime.now()                                           # Get timestamp
           assembly_log_file.write("[" + str(now) + "]" +
                         "\t" + "New accession number added:" +
                         "\t" + accession + "." + "\n")                            # Write to logfile
           conn.commit()                                                           # Commit assembly record changes to database





    #-----------------------------------------------------------------------#
    #                                    Cleanup                            #
    #-----------------------------------------------------------------------#
    conn.commit()                                                                  # Make sure all changes are committed to database
    cur.close()                                                                    # Close the database
    assembly_log_file.close()                                                      # Close the logfile

#AssemblyTable("database/Yersinia_pestis_db.sqlite", "Yersinia pestis", "ktmeaton@gmail.com", ".")
