
---
title: 'NCBImeta: efficient and comprehensive metadata retrieval from NCBI databases'
tags:
  - Python
  - bioinformatics
  - genomics
  - metadata
  - NCBI
  - SRA
authors:
  - name: Katherine Eaton
    orcid: 0000-0001-6862-7756
    affiliation: "1, 2"
affiliations:
 - name: McMaster Ancient DNA Centre, McMaster University
   index: 1
 - name: Department of Anthropology, McMaster University
   index: 2

date: 29 November 2019
bibliography: paper.bib
---
# Summary

``NCBImeta`` is a Python application that downloads and organizes biological metadata from the National Centre for Biotechnology Information (NCBI). While the NCBI web portal provides an interface for searching and filtering molecular data, the output offers limited options for record retrieval and comparison on a much larger and broader scale. ``NCBImeta`` tackles this problem by creating a reformatted local database of NCBI metadata based on user search queries and customizable fields. The output of ``NCBImeta``, optionally a SQLite database or text file(s), can then be used by computational biologists for applications such as record filtering, project discovery, sample interpretation, and meta-analyses of published work.

# Background

Recent technological advances in DNA sequencing have propelled biological research into the realm of big data. Due to the tremendous output of Next Generation Sequencing (NGS) platforms, numerous fields have transformed to explore this novel high-throughput data. Projects that quickly adapted to incorporate these innovative techniques included monitoring the emergence of antibiotic resistance genes [@zankari_identification_2012], epidemic source tracking in human rights cases [@eppinger_genomic_2014], and global surveillance of uncharacterized organisms [@connor_species-wide_2015]. However, the startling rate at which sequence data are being deposited online have presented significant hurdles to the efficient reuse of published data. In response, there is growing recognition within the computational community that effective data mining techniques are a dire necessity [@nakazato_experimental_2013; @mackenzie_post-archival_2016].

An essential step in the data mining process is the efficient retrieval of comprehensive metadata. These metadata fields are diverse in nature, but often include the characteristics of the biological source material, the composition of the raw data, the objectives of the research initiative, and the structure of the post-processed data. Several software applications have been developed to facilitate bulk metadata retrieval from online repositories. Of the available tools, ``SRAdb`` [@zhu_sradb:_2013], the Pathogen Metadata Platform [@chang_pathogen_2016], ``MetaSRA`` [@bernstein_metasra:_2017], and ``pysradb`` [@choudhary_pysradb:_2019]  are among the most widely utilised and actively maintained. While these software extensions offer substantial improvements over the NCBI web browser experience, there remain several outstanding issues.

1. Existing tools assume external programming language proficiency (ex. R, Python, SQL), thus reducing tool accessibility.
2. Available software focuses on implementing access to singular NCBI databases in isolation, for example, the raw data repository the Sequence Read Archive (SRA). This does not empower researchers to incorporate evidence from multiple databases, as it fails to fully leverage the power of interconnected information within the relational database scheme of NCBI.
3. Existing software provides only intermittent database updates, where users are dependent on developers releasing new snapshots to gain access to the latest information. This gives researchers less autonomy over what data they may incorporate as newer records are inaccessible, and may even introduce sampling bias depending on when the snapshots are generated.  

In response, ``NCBImeta`` aims to provide a more user-inclusive experience to metadata retrieval, that emphasizes real-time access and provides generalized frameworks for a wide variety of NCBI’s databases.

# NCBImeta

``NBCImeta`` is a command-line application that executes user queries and metadata retrieval from the NCBI suite of databases. The software is written in Python 3, using the ``BioPython`` module [@cock_biopython:_2009] to connect to, search, and download XML records with NCBI’s E-Utilities [@kans_entrez_2019]. The ``lxml`` package is utilised to perform XPath queries to retrieve nodes containing biological metadata of interest. ``SQLite`` is employed as the database management system for storing fetched records, as implemented with the ``sqlite3`` python module. Accessory scripts are provided to supply external annotation files, to join tables within the local database so as to re-create the relational database structure, and finally to export the database as tabular text for downstream analyses. ``NCBImeta`` currently interfaces with the molecular and literature databases described in Table \ref{NCBI_databases} [@noauthor_entrez_2016; @noauthor_ncbi_nodate].

: NCBI Databases Supported in NCBImeta. \label{NCBI_databases}

+-----------------+-------------------------------------------------------------+
| **Database**    | **Description**                                             |
+=================+=============================================================+
| Assembly        | Descriptions of the names and structure of genomic assemblies, statistical reports, and sequence data links.  |
+-----------------+-------------------------------------------------------------+
| BioSample       | Characteristics of the biological source materials used in experiments. |
+-----------------+-------------------------------------------------------------+
| BioProject      | Goals and progress of the experimental initiatives, originating from an individual organization or a consortium. |
+-----------------+-------------------------------------------------------------+
| Nucleotide      | Sequences collected from a variety of sources, including GenBank, RefSeq, TPA and PDB. |
+-----------------+-------------------------------------------------------------+
| PubMed          | Bibliographic information and citations for biomedical literature from MEDLINE, life science journals, and other online publications. |
+-----------------+-------------------------------------------------------------+
| SRA             | Composition of raw sequencing data and post-processed alignments generated via high-throughput sequencing platforms. |
+-----------------+-------------------------------------------------------------+


The typical workflow of ``NCBImeta`` follows four major steps as outlined in Figure \ref{NCBImeta_Workflow}. Users first configure the program with their desired search terms. ``NCBImeta`` is then executed on the command-line to fetch relevant records and organize them into a local database. Next, the user optionally edits the database to, for example, add their own custom metadata. Finally, the resulting database, kept in SQLite format or exported to text, delivers 100+ biologically-relevant metadata fields to researcher’s fingertips. This process not only saves significant time compared to manual record retrieval through the NCBI web portal, but additionally unlocks attributes for comparison that were not easily accessible via the web-browser interface.


![NCBImeta User Workflow \label{NCBImeta_Workflow.}](figures/NCBImeta_Workflow.jpg)

``NCBImeta``’s implementation offers a novel approach to metadata management and presentation that improves upon the prevously described limitations of existing software in a number of ways. First, ``NCBImeta`` is run on the command-line, and the final database can be exported to a text file, thus no knowledge of an external programming language is required to generate or explore the output. Second, a general parsing framework for tables and metadata fields was developed which can be extended to work with diverse database types contained within NCBI’s infrastructure. Finally, a query system was implemented for record retrieval that allows users to access records in real-time, as opposed to working with intermittent or out-dated database snapshots.

# Use Case

The following section demonstrates how ``NCBImeta`` can be used to obtain current and comprehensive metadata for a pathogenic bacteria, *Pseudomonas aeruginosa*, from various sequencing projects across the globe. *P. aeruginosa* is an opportunistic pathogen associated with the disease cystic fibrosis (CF) and is highly adaptable to diverse ecological niches [@stewart_draft_2014]. As such, it is a target of great interest for comparative genomics and there are currently over 15,000 genomic sequence records available which are spread across two or more databases. In cases such as this, it is critical to leverage the tremendous power of these existing datasets while being conscious of the labor typically required to retrieve and contextualize this information. ``NCBImeta`` renders the problem of acquiring and sifting through this metadata trivial and facilitates the integration of information from multiple sources.

To identify publicly available *P. aeruginosa* genomes, ``NCBImeta`` is configured to search through the tables *Assembly* (assembled genomes) and *SRA* (raw data). For additional context, ``NCBImeta`` is used to retrieve metadata from the *Nucleotide* table for descriptive statistics of the genomic content, from the *BioProject* table to examine the research methodology of the initiative, from *Pubmed* to identify existing publications, and finally from the *Biosample* table to explore characteristics of the biological material. A small subset of the 100+ retrieved columns is shown in Figure \ref{NCBImeta_aeruginos_db_subset}, to provide a visual example of the output format and the metadata that is retrieved.

![ A subset of the 100+ metadata columns retrieved for *P. aeruginosa* sequencing projects. Viewed with DB Browser for SQLite (https://sqlitebrowser.org/) \label{NCBImeta_aeruginos_db_subset}](figures/NCBImeta_aeruginosa_db_subset.jpg)

Subsequently, the output of NCBImeta can be used for exploratory data visualization and analysis. The text file export function of NCBImeta ensures downstream compatibility with both  user-friendly online tools (ex. Google Sheets Charts)  as well as more advanced visualization packages [@wickham_ggplot2:_2016]. In Figure \ref{NCBImeta_aeruginosa_geogene}, the geospatial distribution of *P. aeruginosa* isolates are plotted alongside key aspects of genomic composition (ex. number of genes).

![Metadata visualization of *P. aeruginosa* sequencing projects. A) The geographic distribution of samples in this region highlights a large number originating in Japan. Visualized with Palladio (https://hdlab.stanford.edu/palladio/). B) The number of genes per organism reveals a multi-modal distribution within the species. \label{NCBImeta_aeruginosa_geogene}](figures/NCBImeta_aeruginosa_geogene.jpg)

Finally, NCBImeta can be used to streamline the process of primary data acquisition following careful filtration. FTP links are provided as metadata fields for databases attached to an FTP server (ex. Assembly, SRA) which can be used to download biological data for downstream analysis.

# Future Work

The development of ``NCBImeta`` has primarily focused on a target audience of researchers whose analytical focus is prokaryotic genomics and the samples of interest are the organisms themselves. Chief among those include individuals pursuing questions concerning epidemiology, phylogeography, and comparative genomics. Future releases of ``NCBImeta`` will seek to broaden database representation to include gene-centric and transcriptomics research (ex. NCBI’s Gene and GEO databases).

# Availability

NCBImeta is a Python 3 application that is supported on Linux and macOS systems. It is distributed for use under the OSD-compliant MIT license (https://opensource.org/licenses/MIT). Source code, documentation, and example files are available on the GitHub repository (https://github.com/ktmeaton/NCBImeta).

# Acknowledgements

I would like to thank Dr. Hendrik Poinar and Dr. Brian Golding for their guidance and support on this project, as well as for insightful conversations regarding biological metadata, the architecture of NCBI, and software deployment. Thank you to Dr. Andrea Zeffiro, Dr. John Fink, Dr. Matthew Davis, and Dr. Amanda Montague for valuable discussions regarding APIs, digital project management, and software publishing. Thank you to all past and present members of the McMaster Ancient DNA Centre and the Golding Lab.
This work was supported by the MacDATA Institute (McMaster University, Canada) and the Social Sciences and Humanities Research Council of Canada (\#20008499).

# References
