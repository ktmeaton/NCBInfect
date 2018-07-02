# NCBImeta
Creates an SQLite database of metadata from the NCBI database.

## Version

Development - Version 0.3.1 (v0.3.1)  
Stable - Version v0.3.0 (master)

## Requirements
Python3.4+ (??)   
BioPython 1.70 (biopython)

pip install --user biopython

## Installation

git clone https://github.com/ktmeaton/NCBImeta.git   
cd NCBImeta  

Development:  
git clone -b v0.3.1 https://github.com/ktmeaton/NCBImeta.git   
cd NCBImeta  

## Usage
### Run the program, creating accessory directories 'log' and 'database'
python src/NCBImeta.py --config config/NCBImeta_config.py

### Annotate the database with a curated tab-separated text file of metadata
python src/NCBImeta_Annotate.py --database my_organism_db.sqlite --annotfile my_organism_annot.txt --table Nucleotide

### Export the database to tab-separated text files by table.
python src/NCBImeta_Export.py --database my_organism_db.sqlite --outputdir NCBImeta_output


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
