# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project "attempts" to adhere to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Development]

- TO DO: A true quick start example, just SRA data?
- Fetching nucleotide annotations could probably be improved with xpath xml.
- error check the "for \_index" in NCBImeta.py
- migrate documentation to Read The Docs

## [v0.6.6] - 2020-0527 - PyPI and Linting

### Added

- MANIFEST.in to make sure requirements.txt is packaged for PyPI (Issue #10)
- GitHub Actions Continuous Integration (Build, Test, Example, Linting)
- Linting: python (black and flake8), markdown, yaml
- pre-commit hooks, config in [setup.cfg](https://github.com/ktmeaton/NCBImeta/blob/master/setup.cfg) and [markdown_lint.yaml](https://github.com/ktmeaton/NCBImeta/blob/master/.github/markdown_lint.yaml).
- [Contributor's Guide](https://github.com/ktmeaton/NCBImeta/blob/master/.github/CONTRIBUTING.md)
- [Pull Request Template](https://github.com/ktmeaton/NCBImeta/blob/master/.github/PULL_REQUEST_TEMPLATE/pull_request_template.md)

### Changed

- Convert BioProjectTitle to XPath query
- The Annotate scripts (Replace and Concatenate) now properly handle inserting/updating values.

### Removed

- Travis Continuous Integration
- Keep an eye on BioProjectPublished values.

## [v0.6.5] - 2020-0318 - XPath Advanced

### Added

- NCBImetaUtilties.py function: adv_xml_search to allow pre-formatted XPath query (PR #9)
- Three new error classes ErrorXPathQueryMultiElement, ErrorXPathElementUnknown, ErrorXPathQueryMissing

### Changed

- Bug: Improved specificity of SRABioSampleAccession and SRABioProjectAccession
- NucleotideBioSampleAccession now a preformatted XPath query (previously empty value)
- BioSampleBioProjectAccession now a preformatted XPath query (previously non-specific)

### Removed

- Non-specific node NucleotideAssemblyAccession

## [v0.6.4] - 2020-0220 - Bobby Tables

### Added

- Extra param checking for yaml config files (Issue #7)

### Changed

- Bugfix for table joining multiple records (Isssue #8))
- SQL query execution is now done by parameterizing Value
- SQL query tables and columns are checked manually
- NCBImetaJoin.py will use an empty string (blank cell) instead of NULL
- Now free of unnecessary/poorly thought out use of encode and decode

## [v0.6.3] - 2020-0124 - Automating the Chain

### Added

- Will rely on bioconda's autobump to maintain bioconda releases.
- Just in case, packaging scripts are located in the new branch bioconda as a backup
- .conda_update.sh to automate conda recipe updating after Travis-CI tag run
- .bioconda_autobump.sh (draft) to automate bioconda-utils autobump PR pipeline
- ver_update.sh to automate version number updating of executables and build scripts
- git update-index --add --chmod=+x conda_update.sh
- git update-index --add --chmod=+x ver_update.sh

### Changed

- 2020-01-23: the master branch switched to the bioconda-recipes repo. I'm uncertain about why this happened but I
copied the master branch to a new branch called 'bc-tbd' (bioconda to-be-determined). To recover, I'm copying v0.6.2 to
a new master branch.
- 2020-01-24: Solved. This happened during Travis-CI testing. While working in the bioconda-recipes repo, my remote.origin.url was pointed towards the NCBImeta repo because of incorrected usage of the TRAVIS_REPO_SLUG env var. And I force pushed the bioconda commits onto the NCBImeta master branch. This can be undone with git reset --hard \<commit\> and then git push --force. Deleted branch 'bc-tbd'.

## [v0.6.2] - 2020-0123 - JOSS Review and Bioconda

### Added

- Bioconda packaging and installation now available (PR: \#5 , credits and thanks to @druvus)
- Discovered biocontainers automatically created through bioconda
- PyPI Deployment through Travis-CI on tagged commits
- Discovered piwheels automatically created through PyPI

### Changed

- If the output directory does not exist, it is now created rather than raising an error (Issue: \#4).

## [v0.6.1] - 2019-1220 - JOSS Submission and Zenodo

### Added

- paper directory
- JOSS Paper: paper.md and paper.bib
- JOSS Figures: NCBImeta_Workflow.jpg, NCBImeta_aeruginosa_db_subset.jpg, NCBImeta_aeruginosa_geogene.jpg
- JOSS Data: pseudomonas aeruginosa database files
- Zenodo Integration

### Changed

- Switched CLI gif to an asciinema recording (web host)
- Switched DB gif to ShareX recording (github host)
- Fixed changelog compare links
- Fixed version numbering in python executables

## [v0.6.0] - 2019-1218 - XML Overhaul XPath

Jumps directly from v0.5.0 to v0.6.0 because changes are significant enough to be not backwards compatible.

### Added

- XML overhaul (lxml module added, minidom removed)
- Multimatch nodes are concatenated by semi-colon
- All tables except assembly now use efetch rather than esummary
- BioProject Fields: BioProjectSpeciesTaxID, BioProjectModificationDate, BioProjectReleaseDate, BioProjectPublished, BioProjectDatePublished, BioProjectPublicationID, BioProjectPublicationDB
- BioSample Fields: BioSampleSerovar, BioSampleHostHealthState
- Nucleotide Fields: NucleotideAssemblyAccession, NucleotideCDSProtein, NucleotideCDSTotal, NucleotideGenesTotal, NucleotidePseudoGenesTotal, NucleotideCDSWithoutProtein
- Pubmed Fields: AbstractText
- Download equivalent files from the NCBI Web Browser:
  - Assembly: XML
  - BioSample: Full XML (text)
  - BioProject: XML
  - Nucleotide: INSDSeq XML (replace "INSD" with "GB")
  - SRA: Full XML
  - Pubmed: XML

### Removed

- BioProject Fields: BioProjectType, BioProjectSequencingStatus
- SRA Fields: SRAExperimentStatus, SRAExperimentVersion, SRAStudyName, SRATotalRuns, SRAUpdateDate
- Nucleotide Fields: NucleotideFirstAccession, NucleotideLastAccession

### Changed

- BioProject Fields: BioProjectRegistrationDate -> BioProjectSubmissionDate
- BioSample Fields: BioSampleDate -> BioSampleSubmissionDate
- SRA Fields: SRAContactName -> SRAContactEmail, SRACreateDate -> SRARunPublishDate
- Nucleotide Fields: NucleotideJournal -> NucleotideReferenceJournal
- Experimented with changing Assembly to efetch, does not support this, only docsum

## [v0.5.0] - 2019-1204 - PyTest and Codecov

### Removed

- Python 3.4 Support (End of Life) and pytest 5.x.y conflicts.
- NCBImeta now requires Python3.5+

### Added

- pytest integration (all NCBImeta functions and classes, verify database contents)
- codecov integration
- conftest file to control fixtures for pytest
- pytest, codecov, pytest-cov are requirements for travis build only
- bugfix in ncbimeta record parsing: column_index position

### Changed

- Code documentation, Major cleanup of unneeded
- Major bugfix of flatten_dict method
- Move method HTTPErrorCatch to NCBImetaUtilties
- Change unicode to str for Python3
- Reuploaded truncated gif files
- Typo Nucleotidet fixed in example config.yaml
- Re-update execute permissions (git update-index --add --chmod=+x ncbimeta/\*.py)
- bash uploader for codecov

## [v0.4.2] - 2019-1127 - Pip Installation

### Added

- setup.py for installation from PyPI and source

### Changed

- Rename all files containing "NCBImeta_" to "NCBImeta", correct all references
- Change src/ directory to ncbimeta/ directory
- requirements.txt loads into setup.py
- Update docs to reflect path changes

## [v0.4.1] - 2019-1127 - Travis CI Integration

### Changed

- Execute permissions (git update-index --add --chmod=+x src/\*.py)
- Bugfix for esearch, more HTTP Error catching
- Travis CI Integration (Linux, MacOSX)

## [v0.4.0] - 2019-1031 - YAML Configuration Files

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

## [v0.3.4] - 2019-1028 - HTTP Error Catching

### Added

- HTTP Error catching
- Bug fixes for HTTP Error 429

## [v0.3.3] - 2019-0912 - Pubmed Table Support

### Added

- Pubmed Table support

## [v0.3.2] - 2019-0905 - Genome Annotation Capture

### Added

- Command example in README.md for creating a master join table of BioSample, BioProject, Assemble, SRA, and Nucleotide tables.
- Three new annotation files for the example.

### Changed

- Python2 no longer supported, Python3 is now mandatory.
- Improved Nucleotide Table annotation parsing
- Fixed missing BioSampleAccession from the Nucleotide Table
- Fixed incorrect directory paths in README.md example commands.

## [v0.3.1] - 2018-0702 - Alpha Release for User Testing

### Added

- README files for config and schema
- Usage in main README

### Changed

- Alphabetized schema entries

## [v0.3.0] - 2018-0629

### Added

- Automation mode
- Supported Tables: Assembly, BioProject, BioSample, Nucleotide, SRA

### Changed

- Repository Rename: NCBInfect -> NCBImeta

## [v0.2.1] - 2018-0308

### Changed

- Fully Functional

## [v0.2.0] - 2018-0122

### Changed

- Repository Rename: GenomeCollector -> NCBInfect

## [v0.1.2] - 2017-0920

### Added

- Bugfixes

## [v0.1.1] - 2017-0919

### Added

- SRA Table

### Changed

- Bug-fix, multiple accession versions
- Started better version control

## [v0.1.0] - 2016-0622

- Repository migrated from GenomeCollector

[Development]: https://github.com/ktmeaton/NCBImeta/compare/HEAD...dev
[v0.6.5]: https://github.com/ktmeaton/NCBImeta/compare/v0.6.5...HEAD
[v0.6.4]: https://github.com/ktmeaton/NCBImeta/compare/v0.6.4...v0.6.5
[v0.6.3]: https://github.com/ktmeaton/NCBImeta/compare/v0.6.3...v0.6.4
[v0.6.2]: https://github.com/ktmeaton/NCBImeta/compare/v0.6.2...v0.6.3
[v0.6.1]: https://github.com/ktmeaton/NCBImeta/compare/v0.6.1...v0.6.2
[v0.6.0]: https://github.com/ktmeaton/NCBImeta/compare/v0.6.0...v0.6.1
[v0.5.0]: https://github.com/ktmeaton/NCBImeta/compare/v0.5.0...v0.6.0
[v0.4.2]: https://github.com/ktmeaton/NCBImeta/compare/v0.4.2...v0.5.0
[v0.4.1]: https://github.com/ktmeaton/NCBImeta/compare/v0.4.1...v0.4.2
[v0.4.0]: https://github.com/ktmeaton/NCBImeta/compare/v0.4.0...v0.4.1
[v0.3.4]: https://github.com/ktmeaton/NCBImeta/compare/v0.3.4...v0.4.0
[v0.3.3]: https://github.com/ktmeaton/NCBImeta/compare/v0.3.3...v0.3.4
[v0.3.2]: https://github.com/ktmeaton/NCBImeta/compare/v0.3.2...v0.3.3
[v0.3.1]: https://github.com/ktmeaton/NCBImeta/compare/v0.3.1...v0.3.2
[v0.3.0]: https://github.com/ktmeaton/NCBImeta/compare/1c97b6b42b0c774b96c8d404d61f4768d3aeea5c...v0.3.1
[v0.2.1]: https://github.com/ktmeaton/NCBImeta/compare/7e77ac2009192eb1905de9d2b687cbac080ebf8a...1c97b6b42b0c774b96c8d404d61f4768d3aeea5c
[v0.2.0]: https://github.com/ktmeaton/NCBImeta/compare/9dfe4d7ef53e17e482e28b37e809203648ac972e...7e77ac2009192eb1905de9d2b687cbac080ebf8a
[v0.1.2]: https://github.com/ktmeaton/NCBImeta/compare/0e3e2f33a8d12b49e203e2a1d8205be7e9fa6f39...9dfe4d7ef53e17e482e28b37e809203648ac972e
[v0.1.1]: https://github.com/ktmeaton/NCBImeta/compare/43c68690ccca7a56031c1914f8a45865302a3696...0e3e2f33a8d12b49e203e2a1d8205be7e9fa6f39
[v0.1.0]: https://github.com/ktmeaton/NCBImeta/compare/126e2f15b43ab3f12942e845bbef4121cc9baf40...43c68690ccca7a56031c1914f8a45865302a3696
