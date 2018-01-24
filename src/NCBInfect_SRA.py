
"""
Created on June 12, 2017
NCBI SRA Table Generator

@author: Katherine Eaton
"""

import sqlite3                                                              # SQL database functionality
import datetime                                                             # Date and time for log files
import os
from xml.dom import minidom

from Bio import Entrez                                                      # Entrez NCBI API from biopython
from NCBInfect_Utilities import os_check


def SRATable(db_name, SEARCH_TERM, EMAIL, output_dir):
    ''' '''
    print("\nCreating/Updating the SRA table using the following parameters: ")
    print("Database: " + "\t" + db_name)
    print("Search Term: " + "\t" + SEARCH_TERM)
    print("Email: " + "\t" + EMAIL)
    print("Output Directory: " + "\t" + output_dir + "\n\n")

    Entrez.email = EMAIL

    # Retrieve the directory separator by OS
    OS_SEP = os_check()


    #-----------------------------------------------------------------------#
    #                                File Setup                             #
    #-----------------------------------------------------------------------#

    # Path to Database
    db_path = output_dir + OS_SEP + "database" + OS_SEP + db_name

    # Path and name of SRA Log File
    log_path = output_dir + OS_SEP + "log"
    str_sra_log_file = output_dir + OS_SEP + "log" + OS_SEP + db_name + "_sra.log"


    # Check if this log file exists, if not create, if so append to it.
    if os.path.exists(str_sra_log_file):
        sra_log_file = open(str_sra_log_file, "a")                          # Open logfile for appending
    else:
        sra_log_file = open(str_sra_log_file, "w")                          # Open logfile for writing

    #-----------------------------------------------------------------------#
    #                                SQL Setup                              #
    #-----------------------------------------------------------------------#

    # Connect to database and establish cursor for commands.
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    #cur.execute('''Drop TABLE IF EXISTS SRA''')

    #---------------------------SRA Table-----------------------------------#
    cur.execute('''
    Create TABLE IF NOT EXISTS SRA (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                           sra_ID TEXT,
                                           bioproject_accession TEXT,
                                           run_accession TEXT,
                                           create_date TEXT,
                                           update_date TEXT,
                                           total_bases int,
                                           total_spots int,
                                           scientific_name TEXT,
                                           sample_alias TEXT,
                                           strain TEXT,
                                           library_layout TEXT,
                                           library_source TEXT,
                                           library_selection TEXT,
                                           title TEXT,
                                           biosample_accession TEXT,
                                           total_runs TEXT,
                                           experiment_accession TEXT,
                                           organism_taxid TEXT,
                                           instrument TEXT,
                                           model TEXT)''')


    num_sra_processed = 0                                                   # Counter for the number of SRA records processed

    #-----------------------------------------------------------------------#
    #                                Processing                             #
    #-----------------------------------------------------------------------#

    # ---------------------Get SRA ID-----------------------------------#

    # Entrez search
    search_term = SEARCH_TERM

    # Search the SRA database with constructed search term
    # retmax is set to 999999 as a limit that will not be exceeded.
    handle = Entrez.esearch(db="sra",
                term=search_term,
                retmax = 999999)

    # Parse/read the entrez search result
    record = Entrez.read(handle)

    # Construct a list containing record identifer numbers.
    ID_list = record['IdList']

    # The length of previous list is the total number of records found.
    num_ID = len(ID_list)

    # Keep a counter of how many records have been processed so far.
    num_ID_processed = 0

    #-------------------------SRA Record--------------------------------#
    for ID in ID_list:
        # Store unique ID
	# Note this is different than unique 'accession'
        # ID is primarily useful for API queries.
        sra_ID = ID

        # Increment SRA record counter.
        num_ID_processed += 1

        # Print a progress log of records processed.
        print("Processing SRA Record: " +
            str(num_ID_processed) +
            "/" +
            str(num_ID))

        #------------------Check if Record Exists in DB----------------#
        cur.execute('''
        SELECT EXISTS(SELECT sra_ID FROM SRA WHERE sra_ID=?)''',
        (sra_ID,))

        # Return 0 if not found, return 1 if found
        record_exists = cur.fetchone()[0]

        # If record exists in DB, go to next ID in list.
        if record_exists: continue

        # If record didn't exist, proceed with parsing.


        #-----------------Record Retrieval---------------------------#

        # Retrieve an individual SRA record.
        ID_handle = Entrez.esummary(db="sra",
                                    id=ID,
                                    retmode="xml")

        ID_XML_handle = Entrez.efetch(db="sra",
                                    id=ID,
                                    rettype="full",
                                    retmode="xml")

        ID_XML = ID_XML_handle.read()
        id_xml_doc = minidom.parseString(ID_XML)

        # It is very unfortunate that NCBI named tags "TAG"
        # Strain information is under one of these TAG tags
        sample_attr_tag_list = id_xml_doc.getElementsByTagName("SAMPLE_ATTRIBUTE")
        for node in sample_attr_tag_list:
            tag = node.childNodes[0].firstChild.data
            value = node.childNodes[1].firstChild.data
            if tag == 'strain': strain = value
            else: strain = ""

        # When strain information is missing Sample name/Sample alias
        # is a useful backup.
        sample_alias_tag = id_xml_doc.getElementsByTagName("SAMPLE")[0]
        sample_alias = sample_alias_tag.attributes['alias'].value

        # Biosample accession is contained within an EXTERNAL_ID tag
        # Originally, this script searched the esummary doc for the
        # Biosample accession. But author KE noticed at least two
        # records where it was filled out wrong (said "spleen" or
        # "lung" instead of an accession.
        external_ID_tag_list = id_xml_doc.getElementsByTagName("EXTERNAL_ID")
        for element in external_ID_tag_list:
            namespace_attr = element.attributes['namespace'].value
            if namespace_attr == 'BioSample':
                biosample_accession = element.firstChild.data
                break


        # Parse xml record in python object.
        '''
        This object is a list containing one element.
        That one element is a complex dictionary, in which keys are
            strings, and values are either strings, full xml, or
            partial xml.
        '''
        ID_record = Entrez.read(ID_handle)

        # Store first and only element of the record list.
        # Remember this single item is a dictionary.
        sra_metadata = ID_record[0]

        # Retrieve 'date' fields by key:value return.
        create_date = sra_metadata["CreateDate"]
        update_date = sra_metadata["UpdateDate"]


        '''
        Retrieve `Run Info` by key:value return
        This is of type string, but looks like a partial xml, missing
        a root node.
        '''
        # First add a root node
        run_info_xml = "<Root>" + sra_metadata["Runs"] + "</Root>"

        # Second parse it into a proper minidom object
        run_info_doc = minidom.parseString(run_info_xml)


        # Third, look for the 'Run' tag (it should be there)
        run_info_tag = run_info_doc.getElementsByTagName("Run")[0]

        # The retrieve tag is actually a dictionary
        run_accession = run_info_tag.attributes['acc'].value
        run_total_bases = run_info_tag.attributes['total_bases'].value
        run_total_spots = run_info_tag.attributes['total_spots'].value


        # The metadata dictionary contains a xml type under the
        # key 'ExpXml'. But it is missing a root node. Forcibly wrap
        # the xml string with a <Root></Root> node.
        exp_xml = "<Root>" + sra_metadata["ExpXml"] + "</Root>"
        #print(exp_xml)

        # Parse newly formatted xml string to an xml object for
        # manipulation by the minidom library.
        doc = minidom.parseString(exp_xml)


        layout_tag = doc.getElementsByTagName("LIBRARY_LAYOUT")[0]
        # Info about library layout is stored as an empty node.
        # Parsing it requires walking through the child nodes.
        for child in list(layout_tag.childNodes):
            if(child.localName):
                library_layout = child.localName

        # Library source is an 'element' object, containing one child
        # node containing the data.
        library_source_tag = doc.getElementsByTagName("LIBRARY_SOURCE")[0]
        library_source = library_source_tag.firstChild.data

        library_selection_tag = doc.getElementsByTagName("LIBRARY_SELECTION")[0]
        library_selection = library_selection_tag.firstChild.data

        sample_tag = doc.getElementsByTagName("Sample")[0]
        sample_name = sample_tag.attributes['name'].value

        title_tag = doc.getElementsByTagName("Title")[0]
        title = title_tag.firstChild.data

        bioproject_tag = doc.getElementsByTagName("Bioproject")[0]
        bioproject_accession = bioproject_tag.firstChild.data

        statistics_tag = doc.getElementsByTagName("Statistics")[0]
        total_runs = statistics_tag.attributes['total_runs'].value

        experiment_tag = doc.getElementsByTagName("Experiment")[0]
        experiment_accession = experiment_tag.attributes['acc'].value

        organism_tag = doc.getElementsByTagName("Organism")[0]
        organism_taxid = organism_tag.attributes['taxid'].value
        try:
           scientific_name = organism_tag.attributes['ScientificName'].value
        except KeyError:
           scientific_name = ""

        # Instrument is a tuple: key is insttrument, value is model
        instrument_tag = doc.getElementsByTagName("Instrument")[0]
        instrument = instrument_tag.attributes.items()[0][0]
        model = instrument_tag.attributes.items()[0][1]


        # --------------------------Update Database--------------------------#
        print ("Writing: " + run_accession + " to the database.\n")
        cur.execute('''
        INSERT INTO SRA (sra_ID,
                                       bioproject_accession,
                                       run_accession,
                                       create_date,
                                       update_date,
                                       total_bases,
                                       total_spots,
                                       scientific_name,
		                       sample_alias,
                                       strain,
                                       library_layout,
                                       library_source,
                                       library_selection,
                                       title,
                                       biosample_accession,
                                       total_runs,
                                       experiment_accession,
                                       organism_taxid,
                                       instrument,
                                       model)
                                  VALUES
                                  (?, ?, ?, ?, ?,
                                   ?, ?, ?, ?, ?,
                                   ?, ?, ?, ?, ?,
                                   ?, ?, ?, ?, ?)''',
                             (sra_ID,
                                       bioproject_accession,
                                       run_accession,
                                       create_date,
                                       update_date,
                                       run_total_bases,
                                       run_total_spots,
                                       scientific_name,
                                       sample_alias,
                                       strain,
                                       library_layout,
                                       library_source,
                                       library_selection,
                                       title,
                                       biosample_accession,
                                       total_runs,
                                       experiment_accession,
                                       organism_taxid,
                                       instrument,
                                       model))

        # Write to logfile
        now = datetime.datetime.now()
        sra_log_file.write("[" + str(now) + "]" +
                     "\t" + "New SRA accession files added:" +
                     "\t" + run_accession + "." + "\n")
        conn.commit()

    #----------------------------------------------------------------------#
    #                                    Cleanup                           #
    #----------------------------------------------------------------------#
    conn.commit()                                                      # Make sure all changes are committed to database
    cur.close()                                                        # Close the database
    sra_log_file.close()                                                   # Close the logfile

#SRATable("database/yersinia_pestis_sqlite.sqlite", "Yersinia pestis", "ktmeaton@gmail.com", ".")
