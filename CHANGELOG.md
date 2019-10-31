# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project "attempts" to adhere to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2019-1031
### Added
- requirements.txt for pip install dependencies
- PyYAML is now a required module for yaml config file loading
- HTTP 429 Error catching for efetch
- Database Read Runtime Error catching for Entrez.read(handle) for Issue: #2
- yaml schema metadata files for all 6 tables

### Changed
- Configuration files now implemented in YAML format
- Source file (NCBImeta.py) and documentation changes to reflect
- Minimal Working Example (MWE) back to plague for quicker execution
- Schema documentation to explain yaml format changes
- README section reorganize
- renamed the annot file and restricted records to 2019-2020.

### Removed
- Configuration Files: Comprehensive_config.py,  pseudomonas_aeruginosa.py, config.py
- All 6 schema txt files: (ex. schema/Assembly.txt)
- scripts folder with very deprecated R code for plotting
- excessive annotation files 2 and 3.

## [0.3.4] - 2019-1028
### Added
- HTTP Error catching
- Bug fixes for HTTP Error 429

## [0.3.3] - 2019-0912
### Added
- Pubmed Table support


## [0.3.2] = 2019-0905
### Added
- Command example in README.md for creating a master join table of BioSample, BioProject, Assemble, SRA, and Nucleotide tables.
- Three new annotation files for the example.

### Changed
- Python2 no longer supported, Python3 is now mandatory.
- Improved Nucleotide Table annotation parsing
- Fixed missing BioSampleAccession from the Nucleotide Table
- Fixed incorrect directory paths in README.md example commands.

## [0.3.1] - 2018-0702
### Added  
- README files for config and schema
- Usage in main README

### Changed
- Alphabetized schema entries

## [0.3.0] - 2018-0629
### Added
- Automation mode
- Supported Tables: Assembly, BioProject, BioSample, Nucleotide, SRA

### Changed
- Repository Rename: NCBInfect -> NCBImeta

## [0.2.1] - 2018-0308

### Changed
- Fully Functional

## [0.2.0] - 2018-0122
### Changed
- Repository Rename: GenomeCollector -> NCBInfect

## [0.1.2] - 2017-0920
### Added
- Bugfixes

## [0.1.1] - 2017-0919
### Added
- SRA Table

### Changed
- Bug-fix, multiple accession versions
- Started better version control

https://github.com/ktmeaton/NCBImeta

[Unreleased]: https://github.com/ktmeaton/NCBImeta/compare/dev...HEAD
