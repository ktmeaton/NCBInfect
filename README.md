[![GitHub (pre-)release](https://img.shields.io/badge/Release-v0.3.1-red.svg)](https://github.com/ktmeaton/NCBImeta/releases/tag/v0.3.1)
[![GitHub license](https://img.shields.io/dub/l/vibe-d.svg?style=flat)](https://github.com/ktmeaton/NCBImeta/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/ktmeaton/NCBImeta.svg)](https://github.com/ktmeaton/NCBImeta/issues)


# NCBImeta
Query and create a database of NCBI metadata (includes SRA). 
 
 
## Python Requirements
Python3.4+  
BioPython 1.70    

```
pip install --user biopython 
```

## Version

Release - Version v0.3.4 (master)  
Development - Version 0.3.5 (dev)  

## Installation

Release:  
```
git clone https://github.com/ktmeaton/NCBImeta.git   
cd NCBImeta  
```   
Development:  
```
git clone -b dev https://github.com/ktmeaton/NCBImeta.git   
cd NCBImeta  
```
## Quick Start Example

### Run the program
```
python3 src/NCBImeta.py --flat --config example/config.py
```
If HTTP 429 errors (Too Many Requests) are frequently raised, increase the parameter FORCE_PAUSE_SECONDS in example/config.py from 0 to 0.5 or 1. The rate at which you can fetch records from NCBI's servers will vary slightly by user (IP address).  

### Annotate the database with curated tab-separated text files of metadata
```
python3 src/NCBImeta_AnnotateReplace.py --database example/my_organism_db.sqlite --annotfile example/my_organism_annot_1.txt --table BioSample
python3 src/NCBImeta_AnnotateReplace.py --database example/my_organism_db.sqlite --annotfile example/my_organism_annot_2.txt --table BioSample
python3 src/NCBImeta_AnnotateReplace.py --database example/my_organism_db.sqlite --annotfile example/my_organism_annot_3.txt --table BioSample
```

Note that the first column of your annotation file MUST be a column that is unique to each record. An Accession number or ID is highly recommended. The column headers in your annotation file must also exactly match the names of your columns in the database.

### Join NCBI tables into a unified master table  
```
python3 src/NCBImeta_Join.py --database example/my_organism_db.sqlite --anchor BioSample --accessory "BioProject Assembly SRA Nucleotide" --final Master --unique "BioSampleAccession BioSampleAccessionSecondary BioSampleBioProjectAccession"
```  

### Export the database to tab-separated text files by table.
```
python3 src/NCBImeta_Export.py --database example/my_organism_db.sqlite --outputdir example/
```

### Explore!
Explore your database text files using a spreadsheet viewer (Microsoft Excel, Google Sheets, etc.)  
Browse your SQLite database using DB Browser for SQLite (see below for program links)   


## Example output of the command-line interface:  
<img src="https://github.com/ktmeaton/NCBImeta/blob/master/images/NCBImeta_CLI.gif" alt="NCBImeta_CLI" width="700px"/> 


## Currently Supported NCBI Tables  
Assembly  
BioProject  
BioSample  
Nucleotide  
SRA  
Pubmed

## Example database output (a subset of the Assembly table)      
<img src="https://github.com/ktmeaton/NCBImeta/blob/master/images/NCBImeta_DB_small.gif" alt="NCBImeta_DB" width="700px"/> 

## Usage
To customize the search terms and database to your needs, please read through config/README_config.md and schema/README_schema.md.
These two files provide instructions on writing configuration files and customizing metadata.


## Up-Coming Features
- Implement config file as yaml!
- Release packaging with conda.    
- Consider switching from minidom to lxml for XPath and XLST functionality.  
- Database join with EnteroBase metadata?  
- Any requested tables or metadata :)  

## Suggested Accessory Programs
### Database Browser
DB Browser for SQLite: https://sqlitebrowser.org/  

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

See CHANGELOG.md.

## License

This project is licensed under the MIT License - see the LICENSE file for details.    

## Credits

author: Katherine Eaton (ktmeaton@gmail.com)

## Helpful Development Commands  
Merging a development branch into master:  
        (on branch development) `git merge origin/master`
        (resolve any merge conflicts if there are any)  
        `git checkout master`  
        `git merge --no-ff development` (there won't be any conflicts now)  

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
