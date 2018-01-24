# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:10:08 2016

@author: Katherine Eaton
"""

import os
from sys import platform as _platform

def metadata_count(meta_string, count_type):
    '''Return the number of structures in the metadata record.'''
    # Search for user specified attribute
    if count_type == "chromosome":
        tmp = meta_string[meta_string.find("\"chromosome_count"):]
    elif count_type == "replicon":
        tmp = meta_string[meta_string.find("\"replicon_count"):]
    elif count_type == "non_chr_rep":
        tmp = meta_string[meta_string.find("\"non_chromosome_replicon_count"):]
    elif count_type == "contig":
        tmp = meta_string[meta_string.find("\"contig_count"):]
    elif count_type == "contig_l50":
        tmp = meta_string[meta_string.find("contig_l50"):]
    elif count_type == "contig_n50":
        tmp = meta_string[meta_string.find("contig_n50"):]
    elif count_type == "scaffold":
        tmp = meta_string[meta_string.find("\"scaffold_count"):]
    elif count_type == "scaffold_l50":
        tmp = meta_string[meta_string.find("scaffold_l50"):]
    elif count_type == "scaffold_n50":
        tmp = meta_string[meta_string.find("scaffold_n50"):]
    elif count_type == "length":
        tmp = meta_string[meta_string.find("\"total_length"):]
    elif count_type == "ungap_len":
        tmp = meta_string[meta_string.find("\"ungapped_length"):]

    # Process
    start = tmp[tmp.find(">")+1:]
    count_string = start[:start.find("<")]
    return int(count_string)

def metadata_print(meta_string):
    ''' '''
    chrom = metadata_count(meta_string, "chromosome")
    rep = metadata_count(meta_string, "replicon")
    non_chr_rep = metadata_count(meta_string, "non_chr_rep")
    contig = metadata_count(meta_string, "contig")
    contig_l50 = metadata_count(meta_string, "contig_l50")
    contig_n50 = metadata_count(meta_string, "contig_n50")
    scaffold = metadata_count(meta_string, "scaffold")
    scaffold_l50 = metadata_count(meta_string, "scaffold_l50")
    scaffold_n50 = metadata_count(meta_string, "scaffold_n50")
    tot_len = metadata_count(meta_string, "length")
    ungap_len = metadata_count(meta_string, "ungap_len")

    print("Replicon Count: " + str(rep))
    print("Chromosome Count: " + str(chrom))
    print("Non-Chromosome Count: " + str(non_chr_rep))
    print("Contig Count: " + str(contig))
    print("Contig L50 Count: " + str(contig_l50))
    print("Contig N50 Count: " + str(contig_n50))
    print("Scaffold: " + str(scaffold))
    print("Scaffold L50 Count: " + str(scaffold_l50))
    print("Scaffold N50 Count: " + str(scaffold_n50))
    print("Total Length: " + str(tot_len))
    print("Ungapped Length: " + str(ungap_len))


def sampledata_retrieve(sampledata_string, retrieve_type):
    ''' '''

    # Make the sampledata all lowercase (for case insenstive searching)
    sampledata_string = sampledata_string.lower()

    if retrieve_type == "strain":
        tmp = sampledata_string[sampledata_string.find("\"strain"):]
    elif retrieve_type == "collection_date":
        tmp = sampledata_string[sampledata_string.find("\"collection_date"):]
    elif retrieve_type == "geo":
        tmp = sampledata_string[sampledata_string.find("\"geo_loc_name"):]
    elif retrieve_type == "isolate_source":
        tmp = sampledata_string[sampledata_string.find("\"isolation_source"):]
    elif retrieve_type == "title":
        tmp = sampledata_string[sampledata_string.find("<title"):]
    elif retrieve_type == "habitat":
        tmp = sampledata_string[sampledata_string.find("\"Habitat"):]
    elif retrieve_type == "latitude":
        tmp = sampledata_string[sampledata_string.find("\"latitude"):]
    elif retrieve_type == "longitude":
        tmp = sampledata_string[sampledata_string.find("\"longitude"):]
    elif retrieve_type == "host_status":
        if "\"Health status of host" in sampledata_string:
            tmp = sampledata_string[sampledata_string.find("\"Health status of host"):]
        else:
            tmp = sampledata_string[sampledata_string.find("\"host health state"):]
    elif retrieve_type == "biovar":
        tmp = sampledata_string[sampledata_string.find("\"biovar"):]
    elif retrieve_type == "collected_by":
        tmp = sampledata_string[sampledata_string.find("\"collected by"):]
    elif retrieve_type == "host":
        tmp = sampledata_string[sampledata_string.find("\"host"):]
    elif retrieve_type == "lat_long":
        tmp = sampledata_string[sampledata_string.find("\"latitude and longitude"):]
    elif retrieve_type == "biotype":
        tmp = sampledata_string[sampledata_string.find("\"biotype"):]
    elif retrieve_type == "host_disease":
        tmp = sampledata_string[sampledata_string.find("\"host disease"):]
    elif retrieve_type == "description":
        tmp = sampledata_string[sampledata_string.find("<paragraph"):]
    elif retrieve_type == "group":
        tmp = sampledata_string[sampledata_string.find("\"group"):]
    else:
        tmp = ""


    # Process
    start = tmp[tmp.find(">")+1:]
    retrieve_string = start[:start.find("<")]
    return retrieve_string



def sra_xml_parse(xml_string, keyword):
    ''' '''
    #print(xml_string)
    xml_string = xml_string.replace("Experiment acc", "Experiment_acc")
    xml_string = xml_string.replace("Organism taxid", "Organism_taxid")
    tmp = xml_string[xml_string.find(keyword)+len(keyword)+1:]  # Search for keyword, remove keyword header

    if(tmp[0] == "\""):
        tmp = tmp[tmp.find("\"")+1:]
        retrieve_string = tmp[:tmp.find("\"")]
    
    elif(tmp[0:2] == " <"):
        tmp = tmp[tmp.find("<")+1:]
        start = tmp[:tmp.find(">")]
        retrieve_string = start[:start.find("<")]        

    else:    
        start = tmp[:tmp.find(">")-2]
        retrieve_string = start[:start.find("<")]          
    return retrieve_string    

def sampledata_print(sampledata_string):
    ''' '''
    strain = sampledata_retrieve(sampledata_string, "strain")
    col_date = sampledata_retrieve(sampledata_string, "collection_date")
    geo = sampledata_retrieve(sampledata_string, "geo")
    isolate = sampledata_retrieve(sampledata_string, "isolate_source")
    title = sampledata_retrieve(sampledata_string, "title")
    habitat = sampledata_retrieve(sampledata_string, "habitat")
    latitude = sampledata_retrieve(sampledata_string, "latitude")
    longitude = sampledata_retrieve(sampledata_string, "longitude")
    host_status = sampledata_retrieve(sampledata_string, "host_status")
    biovar = sampledata_retrieve(sampledata_string, "biovar")
    collected_by = sampledata_retrieve(sampledata_string, "collected_by")
    host = sampledata_retrieve(sampledata_string, "host")
    lat_long = sampledata_retrieve(sampledata_string, "lat_long")
    biotype = sampledata_retrieve(sampledata_string, "biotype")
    host_disease = sampledata_retrieve(sampledata_string, "host_disease")
    description = sampledata_retrieve(sampledata_string, "description")
    group = sampledata_retrieve(sampledata_string, "group")
    print("Strain: " + strain)
    print("Collection Date:  " + col_date)
    print("Geographic Location: " + geo)
    print("Isolate Source: " + isolate)
    print("Title: " + title)
    print("Habitat: " + habitat)
    print("Latitude: " + latitude)
    print("Longitude: " + longitude)
    print("Latitude and Longitude: " + lat_long)
    print("Health Status of Host: " + host_status)
    print("Biovar: " + biovar)
    print("Collected By: " + collected_by)
    print("Host: " + host)
    print("Biotype: " + biotype)
    print("Host Disease: " + host_disease)
    print("Description: " + description)
    print("Group: " + group)

def print_record_keys(record_dict):
   ''' '''
   key_list = []
   for key in record_dict.keys():
       key_list.append(key)
   key_list.sort()
   for key in key_list:
       print(key)

def retrieve_bioproject_gb(gb_handle):
   ''' '''
   # Search for bioproject line
   gb_line = gb_handle.readline().strip()
   while "bioproject" not in gb_line.lower():
      gb_line = gb_handle.readline().strip()

   # Found bioproject line
   gb_split = gb_line.split()
   item_index = 0
   for item in gb_split:
       if "bioproject" in item.lower():
           return gb_split[item_index + 1]

       item_index += 1

   return ''

def parseSRARunInfo(run_info):
    ''' '''
    run_info_dict = {}
    list_run_info = run_info.replace("Run acc", "Run_acc").strip("<>/").split(" ")
    for element in list_run_info:
        key = element.split("=")[0]
        item = element.split("=")[1]
        run_info_dict[key] = item
    return(run_info_dict)

def os_check():
    ''' Return OS Separator'''
    if 'linux' in _platform:
        return "/"
    elif 'cygwin' in _platform:
        return "/"
    elif "win" in _platform:
        return "\\"
    else:
        return "/"

def check_accessory_dir(output_dir):
    OS_SEP = os_check()
    output_dir = output_dir + OS_SEP
    if not os.path.exists(output_dir + OS_SEP + "log"):                                              # Check if log directory exists
        os.makedirs(output_dir + OS_SEP + "log")
    if not os.path.exists(output_dir + OS_SEP + "docs"):                                              # Check if log directory exists
        os.makedirs(output_dir + OS_SEP + "docs")
    if not os.path.exists(output_dir + OS_SEP + "data"):                                              # Check if log directory exists
        os.makedirs(output_dir + OS_SEP + "data")
    if not os.path.exists(output_dir + OS_SEP + "database"):                                              # Check if log directory exists
        os.makedirs(output_dir + OS_SEP + "database")
    if not os.path.exists(output_dir + OS_SEP + "genomes"):                                              # Check if log directory exists
        os.makedirs(output_dir + OS_SEP + "genomes")
    if not os.path.exists(output_dir + OS_SEP + "annotate"):                                              # Check if log directory exists
        os.makedirs(output_dir + OS_SEP + "annotate")        
    if not os.path.exists(output_dir + OS_SEP + "genbank"):
        os.makedirs(output_dir + OS_SEP + "genbank")
    if not os.path.exists(output_dir + OS_SEP + "gff3"):
        os.makedirs(output_dir + OS_SEP + "gff3")
    return 0                                
