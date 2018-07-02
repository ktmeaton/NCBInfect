# Configuration File Instructions

The configuration files contain all the options required to run the NCBImeta program.
They consist of 6 variables:

OUTPUT_DIR    
EMAIL    
DATABASE    
TABLES    
SEARCH_TERMS    
TABLE_COLUMNS    

The names of these variables should not be altered in any way. Just their assigned value.    

The configuration file can be named anything, as long as it ends in ".py" and doesn't have any other periods in the name.

## 1) OUTPUT_DIR
Type "str", example:    
    
      OUTPUT_DIR = "../NCBImeta_ouput/"  
    
Can be a relative or absolute path. Note that when using a relative path, it will be relative from wherever you are EXECUTING the program (not necessarily from where the config file is located).    

This directory must exist, otherwise the program will exit with an error status.    

## 2) EMAIL
Type "str", example:    

      EMAIL = "myemailname@domain.com"    

This must be a valid email address for using biopython/NCBI's API.    

## 3) DATABASE
Type "str", example:    

        DATABASE = "my_organism_db.sqlite"    

This will be the name of your created database and should not be a path. By default, a "database" directory will be created in your output directory to store this file. If you choose the --flat option at runtime, the database directory will not be created, and it will simply be stored in your selected output directory.    

It does not need to end in "".sqlite", but you may find that helpful as your computer will associate that with an appropriate viewer application.    

## 4) TABLES
Type "list" containing comma separated "str" elements:   

        TABLES = ["Assembly","BioSample"]

This list contains the names of all tables you want to search in. Note that these must match exactly to SEARCH TERMS and TABLE COLUMNS. 

## 5) SEARCH_TERMS
Type "dict" containing comma separated key value pairs of type "str", example:    

        SEARCH_TERMS = {"Assembly": "Yersinia pestis[Orgn]",    
                        "BioSample": "Yersinia pestis[Orgn]"}    

This list contains the names of all tables and corresponding ENTREZ search queries.    
Building an appropriate search query is sometimes the most difficult part.    
Test your queries in the web browser first before committing.    

Note that these must match exactly to TABLES and TABLE COLUMNS.    

*** Note that record retrieval is currently limited to 9999999 records per table. This can be changed locally in your program by searching for the first instance of "retmax" in the NCBImeta.py source file (src/NCBImeta.py). ***    

## 5) TABLE_COLUMNS
Type "dict" containing comma separated key value pairs. The key is always of type "str", the value always of type "list" of "str", example:    

    TABLE_COLUMNS = {
       "Assembly" : [
                {"AssemblyAccession" : "AssemblyAccession"},
                {"BioSampleAccession" : 'BioSampleAccn'},
                {"Organism" : 'Organism'}
                ],
      "BioSample" : [
                {"Accession": "Accession"},
                {"BioProject": ["Link","label"]},
                {"SRAAccession": ["Id","SRA","db"]},
                {"BioSampleTitle": "Title"}
                ]
                }
                
This dictionary contains metadata elements selected from the schema files (schema/). They should be copy-pasted, with a comma-separating each. Line breaks are added after each element just for readability.    

Note that these must match exactly to SEARCH TERMS and TABLES.    

** Tips, don't put a comma after the final element in each list (ie. in each square-bracket separated list).
