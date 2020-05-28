# NCBImeta

**Efficient and comprehensive metadata acquisition from NCBI databases (includes SRA).**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ktmeaton/NCBImeta/blob/master/LICENSE)
[![Build Status](https://github.com/ktmeaton/NCBImeta/workflows/Building/badge.svg?branch=master)](https://github.com/ktmeaton/NCBImeta/actions?query=workflow%3ABuilding+branch%3Amaster)
[![codecov](https://codecov.io/gh/ktmeaton/ncbimeta/branch/master/graph/badge.svg)](https://codecov.io/gh/ktmeaton/NCBImeta/branch/master)
[![status](https://joss.theoj.org/papers/72376aa12ddf832465c92490b2074e7b/status.svg)](https://joss.theoj.org/papers/72376aa12ddf832465c92490b2074e7b)
[![GitHub issues](https://img.shields.io/github/issues/ktmeaton/NCBImeta.svg)](https://github.com/ktmeaton/NCBImeta/issues)
[![PyPI version](https://badge.fury.io/py/NCBImeta.svg)](https://badge.fury.io/py/NCBImeta)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/ncbimeta/badges/version.svg)](https://anaconda.org/bioconda/ncbimeta)

## Why NCBImeta?

NCBImeta is a command-line application that retrieves and organizes metadata from the National Centre for Biotechnology Information (NCBI). While the NCBI web browser experience allows filtered searches, the output does not facilitate inter-record comparison or bulk record retrieval. NCBImeta tackles this issue by creating a local database of NCBI metadata constructed by user-defined search criteria and customizable metadata columns. The output of NCBImeta, optionally a SQLite database or text files, can then be used by computational biologists for applications such as record filtering, project discovery, sample interpretation, or meta-analyses of published work.

## Requirements

* NCBImeta is written in Python 3 and supported on Linux and macOS.
* Dependencies that will be installed are listed in [requirements.txt](https://github.com/ktmeaton/NCBImeta/blob/master/requirements.txt).
* [Check all Python versions and OS with verified build status](https://github.com/ktmeaton/NCBImeta/actions?query=workflow%3ABuilding+branch%3Amaster)

Conda is the recommended installation method. To install with pip or setuptools, ```gcc``` is required.

## Installation

There are three installation options for NCBImeta:

### 1. Bioconda

```bash
conda install -c bioconda ncbimeta
```

### 2. PyPI

```bash
pip install ncbimeta
```

### 3. Github

```bash
git clone https://github.com/ktmeaton/NCBImeta.git
cd NCBImeta
pip install .
```

Test that the installation was successful:

```bash
NCBImeta.py --version
```

## Quick Start Example

### Access the quick start config file

Download the NCBImeta github repository to get access to the example configuration files:

```bash
git clone https://github.com/ktmeaton/NCBImeta.git
cd NCBImeta
```

### Run the program

Download a selection of genomic metadata pertaining to the plague pathogen *Yersinia pestis*.

```bash
NCBImeta.py --flat --config example/config.yaml
```

(Note: The 'quick' start config file forces slow downloads to accommodate users with slow internet. For faster record retrieval, please see the [Config File README](https://github.com/ktmeaton/NCBImeta/blob/master/config/README_config.md) to start editing config files.)

Example output of the command-line interface (v0.6.1):
[![asciicast](https://asciinema.org/a/289560.svg)](https://asciinema.org/a/289560)

### Annotate the database with the user's custom metadata

```bash
NCBImetaAnnotateReplace.py --database example/yersinia_pestis_db.sqlite --annotfile example/annot.txt --table BioSample
```

Note that the first column of your annotation file MUST be a column that is unique to each record. An Accession number or ID is highly recommended. The column headers in your annotation file must also exactly match the names of your columns in the database.

```NCBImetaAnnotateReplace.py```, as the name implies, replaces the existing annotation with the data in your custom metadata file. Alternatively, the script ```NCBImetaAnnotateConcatenate.py``` will concatenate your custom metadata with the pre-existing value in the database cell (separated by a semi-colon).

```bash
NCBImetaAnnotateConcatenate.py --database example/yersinia_pestis_db.sqlite --annotfile example/annot.txt --table BioSample
```

### Join NCBI tables into a unified master table

```bash
NCBImetaJoin.py --database example/yersinia_pestis_db.sqlite --final Master --anchor BioSample --accessory "BioProject Assembly SRA Nucleotide" --unique "BioSampleAccession BioSampleAccessionSecondary BioSampleBioProjectAccession"
```

The rows of the output "Master" table will be from the anchor table "BioSample", with additional columns added in from the accessory tables "BioProject", "Assembly", "SRA", and "Nucleotide". Unique accession numbers for BioSample (both primary and secondary) and BioProject allow this join to be unambiguous.

### Export the database to tab-separated text files by table.

```bash
NCBImetaExport.py --database example/yersinia_pestis_db.sqlite --outputdir example/
```

Each table within the database will be exported to its own tab-separated .txt file in the specified output directory.

### Explore!

1. Explore your database text files using a spreadsheet viewer (Microsoft Excel, Google Sheets, etc.)
2. Browse your SQLite database using DB Browser for SQLite (<https://sqlitebrowser.org/>)
3. Use the columns with FTP links to download your data files of interest.

Example database output (a subset of the BioSample table)

<img src="https://raw.githubusercontent.com/ktmeaton/NCBImeta/master/images/NCBImetaDB.gif" alt="NCBImetaDB" width="700px"/>

## Currently Supported NCBI Tables

* Assembly
* BioProject
* BioSample
* Nucleotide
* SRA
* Pubmed

## Upcoming Features

* [Project v0.6.6 - "PyPI Fix and Contributor's Guide"](https://github.com/ktmeaton/NCBImeta/projects/8): Deployment and Linting - DEVELOPMENT
* [Project v0.6.7 - "Read The Docs"](https://github.com/ktmeaton/NCBImeta/projects/7): Documentation Overhaul - DEVELOPMENT

## Documentation

To get started with customizing the search terms, database, and metadata fields, please read:

1. [Config File README](https://github.com/ktmeaton/NCBImeta/blob/master/config/README_config.md)
2. [Schema File README](https://github.com/ktmeaton/NCBImeta/blob/master/schema/README_schema.md)

## Issues, Questions, and Suggestions

Please submit your questions, suggestions, and bug reports to the
[Issue Tracker](https://github.com/ktmeaton/NCBImeta/issues).

Please do not hesitate to post any manner of curiosity in the "Issues" tracker :) User-feedback and ideas are the most valuable resource for emerging software.

## Contributing

Want to add features and fix bugs? Check out the [Contributor's Guide](https://github.com/ktmeaton/NCBImeta/blob/master/.github/CONTRIBUTING.md) for suggestions on getting started.

## Community

GitHub not your style? Join the [NCBImeta Slack Group](https://join.slack.com/t/ncbimeta/shared_invite/zt-crbtn51t-bdQKeBqz6Nkmj~hgU8ZZFA) to see release alerts, chat with other users, and get insider perspective on development.

## Citation

Eaton, K. (2020). NCBImeta: efficient and comprehensive metadata retrieval from NCBI databases. Journal of Open Source Software, 5(46), 1990, <https://doi.org/10.21105/joss.01990>

## Credits

Author: [Katherine Eaton](https://github.com/ktmeaton) (ktmeaton@gmail.com)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
