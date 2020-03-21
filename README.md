[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ktmeaton/NCBImeta/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/ktmeaton/NCBImeta.svg?branch=master)](https://travis-ci.org/ktmeaton/NCBImeta)
[![codecov](https://codecov.io/gh/ktmeaton/ncbimeta/branch/dev/graph/badge.svg)](https://codecov.io/gh/ktmeaton/NCBImeta/branch/master)
[![status](https://joss.theoj.org/papers/72376aa12ddf832465c92490b2074e7b/status.svg)](https://joss.theoj.org/papers/72376aa12ddf832465c92490b2074e7b)
[![GitHub issues](https://img.shields.io/github/issues/ktmeaton/NCBImeta.svg)](https://github.com/ktmeaton/NCBImeta/issues)
[![PyPI version](https://badge.fury.io/py/NCBImeta.svg)](https://badge.fury.io/py/NCBImeta)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/ncbimeta/badges/version.svg)](https://anaconda.org/bioconda/ncbimeta)

# NCBImeta
Efficient and comprehensive metadata acquisition from NCBI databases (includes SRA).  

## SARS-CoV2
This is the SARS-CoV2 database branch. If you are interested in installing the program NCBImeta, please visit the [master branch](https://github.com/ktmeaton/NCBImeta).  

### Create/Update the SQLite Database
```
NCBImeta.py --config config/sarscov2.yaml
```

### Export the SQLite Database to Text Files
```
NCBImetaExport.py --database database/sarscov2.sqlite --outputdir database/
```

### Visualize
<img src="https://github.com/ktmeaton/NCBImeta/blob/SARSCOV2/images/sarscov2_sra.png" alt="SARSCOV2_SRA" width="700px"/>

### Database Links
1. [All DB - SQLite](https://github.com/ktmeaton/NCBImeta/raw/SARSCOV2/database/sarscov2.sqlite). View with [DB Browser for SQLite](https://sqlitebrowser.org/).
2. ['Assembly' Text DB](https://raw.githubusercontent.com/ktmeaton/NCBImeta/SARSCOV2/database/sarscov2_Assembly.txt)
3. ['BioProject' Text DB](https://raw.githubusercontent.com/ktmeaton/NCBImeta/SARSCOV2/database/sarscov2_BioProject.txt)
4. ['BioSample' Text DB](https://raw.githubusercontent.com/ktmeaton/NCBImeta/SARSCOV2/database/sarscov2_BioSample.txt)
5. ['Nucleotide' Text DB](https://raw.githubusercontent.com/ktmeaton/NCBImeta/SARSCOV2/database/sarscov2_Nucleotide.txt)
6. ['Pubmed' Text DB](https://raw.githubusercontent.com/ktmeaton/NCBImeta/SARSCOV2/database/sarscov2_PubMed.txt)
7. ['SRA' Text DB](https://raw.githubusercontent.com/ktmeaton/NCBImeta/SARSCOV2/database/sarscov2_SRA.txt)
