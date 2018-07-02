[![GitHub (pre-)release](https://img.shields.io/badge/Release-v0.3.1-red.svg)](https://github.com/ktmeaton/NCBImeta/releases/tag/v0.3.1)
[![GitHub license](https://img.shields.io/github/license/ktmeaton/NCBImeta.svg?style=flat)](https://github.com/ktmeaton/NCBImeta/blob/master/LICENSE)




# NCBImeta
Creates a SQLite database of metadata from the NCBI database.  


## Version

Development - Version 0.3.2 (v0.3.2)  
Stable - Version v0.3.1 (master)

## Python Requirements
Module SQLite3 (sqlite3 in Python3+, pysqlite in Python2.7+)     
BioPython 1.70 (biopython)  
Python2.7+ (Minimum requirement unverified)    


pip install --user biopython

## Installation
Stable:  
```
git clone https://github.com/ktmeaton/NCBImeta.git   
cd NCBImeta  
```
Development: 
```
git clone -b v0.3.1 https://github.com/ktmeaton/NCBImeta.git   
cd NCBImeta  
```
## Usage

### Run the program, creating accessory directories 'log' and 'database'
python src/NCBImeta.py --config example/config.py --flat

### Annotate the database with a curated tab-separated text file of metadata
python src/NCBImeta_Annotate.py --database example/my_organism_db.sqlite --annotfile example/my_organism_annot.txt --table BioSample

Note that the first column of your annotation file MUST be a column that is unique to
each record. An Accession number or ID is highly recommended.

### Export the database to tab-separated text files by table.
python src/NCBImeta_Export.py --database example/my_organism_db.sqlite --outputdir example/


## Supported NCBI Tables  
Assembly  
BioProject  
BioSample  
Nucleotide  
SRA  

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

## Credits

author: Katherine Eaton (ktmeaton@gmail.com)

## License

TODO: Write license

## Helpful commands  
Merging a development branch into master:  
        (on branch development)$ git merge master  
        (resolve any merge conflicts if there are any)  
        git checkout master  
        git merge --no-ff development (there won't be any conflicts now)  

## About

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
