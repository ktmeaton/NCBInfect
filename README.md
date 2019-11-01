[![GitHub (pre-)release](https://img.shields.io/badge/Release-v0.4.0-red.svg)](https://github.com/ktmeaton/NCBImeta/releases/tag/v0.4.0)
[![GitHub license](https://img.shields.io/dub/l/vibe-d.svg?style=flat)](https://github.com/ktmeaton/NCBImeta/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/ktmeaton/NCBImeta.svg)](https://github.com/ktmeaton/NCBImeta/issues)
[![Build Status](https://travis-ci.org/ktmeaton/NCBImeta.svg?branch=dev)](https://travis-ci.org/ktmeaton/NCBImeta)


# NCBImeta
Query and create a database of NCBI metadata (includes SRA).


## Python Requirements
Python3, BioPython, PyYAML, NumPy

```
pip3 install --user -r requirements.txt
```

## Version

Release - [Version v0.4.0](https://github.com/ktmeaton/NCBImeta/releases/tag/v0.4.0) (master)  
Development - Version 0.4.1 (dev)  

## Installation

Release:  
```
git clone https://github.com/ktmeaton/NCBImeta.git   
cd NCBImeta  
```   

## Quick Start Example

### Run the program
```
src/NCBImeta.py --flat --config example/config.yaml
```

Example output of the command-line interface (v0.3.4):  
<img src="https://github.com/ktmeaton/NCBImeta/blob/master/images/NCBImeta_CLI.gif" alt="NCBImeta_CLI" width="700px"/>


### Annotate the database with curated tab-separated text files of metadata
```
src/NCBImeta_AnnotateReplace.py --database example/yersinia_pestis_db.sqlite --annotfile example/annot.txt --table BioSample
```

Note that the first column of your annotation file MUST be a column that is unique to each record. An Accession number or ID is highly recommended. The column headers in your annotation file must also exactly match the names of your columns in the database.  

NCBImeta_AnnotateReplace.py, as the name implies, replaces the existing annotation with the data in your custom metadata file. If you would like to retain the original metadata from NCBI, and simply concatenate (append) your custom metadata (separated by a semi-colon), instead use the NCBImeta_AnnotateConcatenate.py script.  
```
src/NCBImeta_AnnotateConcatenate.py --database example/yersinia_pestis_db.sqlite --annotfile example/annot.txt --table BioSample
```
### Join NCBI tables into a unified master table  
```
src/NCBImeta_Join.py --database example/yersinia_pestis_db.sqlite --anchor BioSample --accessory "BioProject Assembly SRA Nucleotide" --final Master --unique "BioSampleAccession BioSampleAccessionSecondary BioSampleBioProjectAccession"
```  
The rows of the output "Master" table will be from the anchor table "BioSample", with additional columns added in from the accessory tables "BioProject", "Assembly", "SRA", and "Nucleotide". Unique accession numbers for BioSample (both primary and secondary) and BioProject allow this join to be unambiguous.


### Export the database to tab-separated text files by table.
```
src/NCBImeta_Export.py --database example/yersinia_pestis_db.sqlite --outputdir example/
```
Each table within the database will be exported to its own tab-separated .txt file in the specified output directory.

### Explore!
1. Explore your database text files using a spreadsheet viewer (Microsoft Excel, Google Sheets, etc.)  
2. Browse your SQLite database using DB Browser for SQLite (see below for program links)  
3. Use the columns with FTP links to download your data of interest.

Example database output (a subset of the Assembly table)      
<img src="https://github.com/ktmeaton/NCBImeta/blob/master/images/NCBImeta_DB_small.gif" alt="NCBImeta_DB" width="700px"/>

## Currently Supported NCBI Tables  
Assembly  
BioProject  
BioSample  
Nucleotide  
SRA  
Pubmed


## Documentation
To get started with customizing the search terms, database, and metadata fields, please read:
1. [Config File README](config/README_config.md)
2. [Schema File README](schema/README_schema.md)


## Up-Coming Features  
- Identify a Pubmed field that will allow this table to be joined.
- Any requested tables or metadata :)  

## Suggested Accessory Programs
### Database Browser
DB Browser for SQLite: https://sqlitebrowser.org/  

## Credits

author: [Katherine Eaton](https://github.com/ktmeaton) (ktmeaton@gmail.com)  

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Helpful Development Commands  
Merging a development branch into master:  
        (on branch dev) `git merge origin/master`
        (resolve any merge conflicts if there are any)  
        `git checkout master`  
        `git merge --no-ff dev` (there won't be any conflicts now)  

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
