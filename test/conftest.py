"""
NCBImeta Conftest
This is the pytest fixture file.

@author: Katherine Eaton
"""

#-----------------------------------------------------------------------#
#                         Modules and Packages                          #
#-----------------------------------------------------------------------#
import pytest

#-----------------------------------------------------------------------#
#                             Fixtures                                  #
#-----------------------------------------------------------------------#

# Reminder, awk was used to help efficiently format the column and value lists
# To get the column names:
# head -n 1 test_Assembly.txt | awk 'BEGIN{FS="\t"; ORS=", "}{for (i=1;i<=NF;i++){print "\x27"$i"\x27"}}'
# To get the metadata field values:
# tail -n+2 test_Assembly.txt | awk 'BEGIN{FS="\t"; ORS=", "}{for (i=1;i<=NF;i++){print "\x27"$i"\x27"}}'


@pytest.fixture(scope="module")
def assembly_table_data():
    '''Return a dictionary containing the expected database values of the Assembly Table'''
    columns = ['id', 'Assembly_id', 'AssemblyAccession', 'AssemblyBioSampleAccession',
                'AssemblyBioSampleID', 'AssemblyGenbankBioprojectAccession', 'AssemblyGenbankID',
                'AssemblyRefseqBioprojectAccession', 'AssemblyRefSeqCategory', 'AssemblyRefSeqID',
                'AssemblyWGSAccession', 'AssemblyInfraspecies', 'AssemblyIsolate', 'AssemblyOrganism',
                'AssemblySpeciesTaxonomicID', 'AssemblySpeciesName', 'AssemblyTaxonomicID',
                'AssemblyName', 'AssemblyStatus', 'AssemblyType', 'AssemblyCoverage',
                'AssemblyChromosomes', 'AssemblyContigCount', 'AssemblyContigN50',
                'AssemblyContigL50', 'AssemblyNonChromosomalReplicons', 'AssemblyReplicons',
                'AssemblyScaffolds', 'AssemblyScaffoldN50', 'AssemblyScaffoldL50',
                'AssemblyTotalLength', 'AssemblyUngappedLength', 'AssemblySubmitterOrganization',
                'AssemblySubmissionDate', 'AssemblyReleaseDate', 'AssemblyFTPAssemblyReport',
                'AssemblyFTPGenbank', 'AssemblyFTPRefSeq', 'AssemblyFTPStatsReport', 'AssemblyComment']

    metadata = ['1', '5025191', 'GCF_009295945.1', 'SAMN12991206', '12991206', 'PRJNA269675',
                '14768768', 'PRJNA224116', 'na', '14769648', '', 'SCPM-O-DNA-18 (I-3113)', 'None',
                'Yersinia pestis (enterobacteria)', '632', 'Yersinia pestis', '632', 'ASM929594v1',
                'Complete Genome', 'haploid', '176.1', '1', '5', '4546217', '1', '4',
                '5', '0', '4546217', '1', '4759144', '4759144', 'SRCAMB', '2019/10/24 00:00', '2019/10/24 00:00',
                'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1/GCF_009295945.1_ASM929594v1_assembly_report.txt',
                'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/009/295/945/GCA_009295945.1_ASM929594v1',
                'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1',
                'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1/GCF_009295945.1_ASM929594v1_assembly_stats.txt',
                'None']

    table_dict = {}
    # Populate the dict with data
    for i in range(0,len(columns)):
        key = columns[i]
        value = metadata[i]
        table_dict[key] = value

    return table_dict

@pytest.fixture(scope="module")
def bioproject_table_data():
    '''Return a dictionary containing the expected database values of the BioProject Table'''
    columns = ['id', 'BioProject_id', 'BioProjectAccession', 'BioProjectDataType',
                'BioProjectDescription', 'BioProjectMethodType', 'BioProjectName',
                'BioProjectTargetCapture', 'BioProjectTargetMaterial', 'BioProjectTargetScope',
                'BioProjectTitle', 'BioProjectType', 'BioProjectOrganismLabel', 'BioProjectOrganismStrain',
                'BioProjectSupergroup', 'BioProjectTaxonomicID', 'BioProjectRegistrationDate',
                'BioProjectRelevanceMedical', 'BioProjectSequencingStatus',
                'BioProjectSubmitterOrganization', 'BioProjectComment']

    metadata = ['1', '269675', 'PRJNA269675',
                'Genome sequencing and assembly',
                'Genome sequencing of bacteria from State collection of pathogenic microorganisms Obolensk. Collection includes bacteria, fungi, and cell-lines.',
                'Sequencing', 'Bacteria', 'Whole', 'Genome', 'Multispecies',
                'Pathogenic microorganism Genome sequencing', 'Primary submission',
                '', '', 'Bacteria', '2', '2015/03/11 00:00', 'yes', 'Complete', 'SRCAMB', 'None']

    table_dict = {}
    # Populate the dict with data
    for i in range(0,len(columns)):
        key = columns[i]
        value = metadata[i]
        table_dict[key] = value

    return table_dict

@pytest.fixture(scope="module")
def biosample_table_data():
    '''Return a dictionary containing the expected database values of the BioSample Table'''
    columns = ['id', 'BioSample_id', 'BioSampleAccession', 'BioSampleAccessionSecondary',
    'BioSampleBioProjectAccession', 'BioSampleSRAAccession', 'BioSampleTitle', 'BioSampleName',
    'BioSampleType', 'BioSamplePackage', 'BioSampleInfraspecies', 'BioSampleOrganism',
    'BioSampleOrganismAlt', 'BioSampleSubSpecies', 'BioSampleStrain', 'BioSampleTaxonomyID',
    'BioSampleBiovar', 'BioSampleCollectionDate', 'BioSampleGeographicLocation', 'BioSampleHost',
    'BioSampleHostDisease', 'BioSampleIsolateNameAlias', 'BioSampleIsolationSource',
    'BioSampleLat', 'BioSampleLatLon', 'BioSampleLon', 'BioSampleDate',
    'BioSampleModificationDate', 'BioSamplePublicationDate', 'BioSampleOrganization',
    'BioSampleComment']

    metadata = ['1', '12991206', 'SAMN12991206', 'None', 'None', 'SRS5502739',
    'Microbe sample from Yersinia pestis', '2019 Sample 199', 'Cell culture',
    'Microbe.1.0', 'strain: SCPM-O-DNA-18 (I-3113)', 'Yersinia pestis', 'Yersinia pestis',
    'None', 'SCPM-O-DNA-18 (I-3113)', '632', 'None', '1984', 'Russia: Tuva',
    'Marmota sibirica', 'Plague', 'None', 'None', 'None', 'None', 'None',
    '2019/10/08', '2019/10/11', '2019/10/08', 'SRCAMB', 'None']

    table_dict = {}
    # Populate the dict with data
    for i in range(0,len(columns)):
        key = columns[i]
        value = metadata[i]
        table_dict[key] = value

    return table_dict

@pytest.fixture(scope="module")
def nucleotide_table_data():
    '''Return a dictionary containing the expected database values of the Nucleotide Table'''

    columns = ['id', 'Nucleotide_id', 'NucleotideAccession', 'NucleotideAccessionVersion',
    'NucleotideBioSampleAccession', 'NucleotideBioProjectAccession', 'NucleotideFirstAccession',
    'NucleotideLastAccession', 'NucleotideOrganism', 'NucleotideTaxonomy', 'NucleotideDefinition',
    'NucleotideDivision', 'NucleotideJournal', 'NucleotideLength', 'NucleotideMoleculeType',
    'NucleotideReferenceTitle', 'NucleotideSeqDataName', 'NucleotideSource', 'NucleotideStrandedness',
    'NucleotideTopology', 'NucleotideCreateDate', 'NucleotideUpdateDate', 'NucleotideGenBankComment',
    'NucleotideAnnotationDate', 'NucleotideAnnotationMethod', 'NucleotideAnnotationPipeline',
    'NucleotideAnnotationProvider', 'NucleotideAnnotationSoftwarerevision', 'NucleotideAssemblyDate',
    'NucleotideAssemblyMethod', 'NucleotideAssemblyName', 'NucleotideCDS', 'NucleotideCDSCoding',
    'NucleotideCRISPRArrays', 'NucleotideExpectedFinalVersion', 'NucleotideFeaturesAnnotated',
    'NucleotideGenes', 'NucleotideGenesCoding', 'NucleotideGenesRNA', 'NucleotideGenomeCoverage',
    'NucleotideGenomeRepresentation', 'NucleotidencRNAs', 'NucleotidePseudoGenes',
    'NucleotidePseudoGenesAmbResidues', 'NucleotidePseudoGenesFrameshifted', 'NucleotidePseudoGenesIncomplete',
    'NucleotidePseudoGenesInternalStop', 'NucleotidePseudoGenesMultipleProblems', 'NucleotiderRNAs',
    'NucleotiderRNAsComplete', 'NucleotiderRNAsPartial', 'NucleotideSequencingTechnology',
    'NucleotideRNAs', 'NucleotideComment',]

    metadata = ['1', '1769169004', 'NZ_CP045153', 'NZ_CP045153.1', 'SAMN12991206', 'PRJNA224116', 'None', 'None', 'Yersinia pestis', 'Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia', 'Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pPCP, complete sequence', 'CON', 'Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation', '9610', 'DNA', 'None', 'None', 'Yersinia pestis', 'double', 'circular', '25-OCT-2019', '25-OCT-2019', 'REFSEQ INFORMATION: The reference sequence was derived from CP045153.; Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI RefSeq ; Annotation Date :: 10/25/2019 01:44:09 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.10 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##; COMPLETENESS: full length.', '10/25/2019 01:44:09', 'Best-placed reference protein set', 'NCBI Prokaryotic Genome Annotation Pipeline (PGAP)', 'NCBI RefSeq', '4.10', 'None', 'Unicycler v. v0.4.7', 'None', '4427', '4239', '2', 'Yes', 'Gene', '4531', '4239', '104', '176.1x', 'Full', '11', '188', '0 of 188', '89 of 188', '108 of 188', '27 of 188', '32 of 188', '8 7 7 (5S 16S 23S)', '8 7 7 (5S 16S 23S)', 'None', 'Illumina MiSeq', '71', 'None', '2', '1769169003', 'NZ_CP045152', 'NZ_CP045152.1', 'SAMN12991206', 'PRJNA224116', 'None', 'None', 'Yersinia pestis', 'Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia', 'Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pTP33, complete sequence', 'CON', 'Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation', '33990', 'DNA', 'None', 'None', 'Yersinia pestis', 'double', 'circular', '25-OCT-2019', '25-OCT-2019', 'REFSEQ INFORMATION: The reference sequence was derived from CP045152.; Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI RefSeq ; Annotation Date :: 10/25/2019 01:44:09 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.10 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##; COMPLETENESS: full length.', '10/25/2019 01:44:09', 'Best-placed reference protein set', 'NCBI Prokaryotic Genome Annotation Pipeline (PGAP)', 'NCBI RefSeq', '4.10', 'None', 'Unicycler v. v0.4.7', 'None', '4427', '4239', '2', 'Yes', 'Gene', '4531', '4239', '104', '176.1x', 'Full', '11', '188', '0 of 188', '89 of 188', '108 of 188', '27 of 188', '32 of 188', '8 7 7 (5S 16S 23S)', '8 7 7 (5S 16S 23S)', 'None', 'Illumina MiSeq', '71', 'None', '3', '1769169002', 'NZ_CP045151', 'NZ_CP045151.1', 'SAMN12991206', 'PRJNA224116', 'None', 'None', 'Yersinia pestis', 'Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia', 'Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pCD, complete sequence', 'CON', 'Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation', '68343', 'DNA', 'None', 'None', 'Yersinia pestis', 'double', 'circular', '25-OCT-2019', '25-OCT-2019', 'REFSEQ INFORMATION: The reference sequence was derived from CP045151.; Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI RefSeq ; Annotation Date :: 10/25/2019 01:44:09 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.10 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##; COMPLETENESS: full length.', '10/25/2019 01:44:09', 'Best-placed reference protein set', 'NCBI Prokaryotic Genome Annotation Pipeline (PGAP)', 'NCBI RefSeq', '4.10', 'None', 'Unicycler v. v0.4.7', 'None', '4427', '4239', '2', 'Yes', 'Gene', '4531', '4239', '104', '176.1x', 'Full', '11', '188', '0 of 188', '89 of 188', '108 of 188', '27 of 188', '32 of 188', '8 7 7 (5S 16S 23S)', '8 7 7 (5S 16S 23S)', 'None', 'Illumina MiSeq', '71', 'None', '4', '1769169001', 'NZ_CP045150', 'NZ_CP045150.1', 'SAMN12991206', 'PRJNA224116', 'None', 'None', 'Yersinia pestis', 'Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia', 'Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pMT, complete sequence', 'CON', 'Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation', '100984', 'DNA', 'None', 'None', 'Yersinia pestis', 'double', 'circular', '25-OCT-2019', '25-OCT-2019', 'REFSEQ INFORMATION: The reference sequence was derived from CP045150.; Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI RefSeq ; Annotation Date :: 10/25/2019 01:44:09 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.10 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##; COMPLETENESS: full length.', '10/25/2019 01:44:09', 'Best-placed reference protein set', 'NCBI Prokaryotic Genome Annotation Pipeline (PGAP)', 'NCBI RefSeq', '4.10', 'None', 'Unicycler v. v0.4.7', 'None', '4427', '4239', '2', 'Yes', 'Gene', '4531', '4239', '104', '176.1x', 'Full', '11', '188', '0 of 188', '89 of 188', '108 of 188', '27 of 188', '32 of 188', '8 7 7 (5S 16S 23S)', '8 7 7 (5S 16S 23S)', 'None', 'Illumina MiSeq', '71', 'None', '5', '1769169000', 'NZ_CP045149', 'NZ_CP045149.1', 'SAMN12991206', 'PRJNA224116', 'None', 'None', 'Yersinia pestis', 'Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia', 'Yersinia pestis strain SCPM-O-DNA-18 (I-3113) chromosome, complete genome', 'CON', 'Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation', '4546217', 'DNA', 'None', 'None', 'Yersinia pestis', 'double', 'circular', '25-OCT-2019', '25-OCT-2019', 'REFSEQ INFORMATION: The reference sequence was derived from CP045149.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; Bacteria and source DNA available from SRC AMB.; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI RefSeq ; Annotation Date :: 10/25/2019 01:44:09 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.10 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##; COMPLETENESS: full length.', '10/25/2019 01:44:09', 'Best-placed reference protein set', 'NCBI Prokaryotic Genome Annotation Pipeline (PGAP)', 'NCBI RefSeq', '4.10', 'None', 'Unicycler v. v0.4.7', 'None', '4427', '4239', '2', 'Yes', 'Gene', '4531', '4239', '104', '176.1x', 'Full', '11', '188', '0 of 188', '89 of 188', '108 of 188', '27 of 188', '32 of 188', '8 7 7 (5S 16S 23S)', '8 7 7 (5S 16S 23S)', 'None', 'Illumina MiSeq', '71', 'None', '6', '1769094081', 'CP045153', 'CP045153.1', 'SAMN12991206', 'PRJNA269675', 'None', 'None', 'Yersinia pestis', 'Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia', 'Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pPCP, complete sequence', 'BCT', 'Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation', '9610', 'DNA', 'None', 'None', 'Yersinia pestis', 'double', 'circular', '24-OCT-2019', '24-OCT-2019', 'Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI ; Annotation Date :: 10/16/2019 14:40:45 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.9 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##', '10/16/2019 14:40:45', 'Best-placed reference protein set', 'NCBI Prokaryotic Genome Annotation Pipeline (PGAP)', 'NCBI', '4.9', 'None', 'Unicycler v. v0.4.7', 'None', '4427', '4239', '2', 'Yes', 'Gene', '4531', '4239', '104', '176.1x', 'Full', '11', '188', '0 of 188', '89 of 188', '108 of 188', '27 of 188', '32 of 188', '8 7 7 (5S 16S 23S)', '8 7 7 (5S 16S 23S)', 'None', 'Illumina MiSeq', '71', 'None', '7', '1769094034', 'CP045152', 'CP045152.1', 'SAMN12991206', 'PRJNA269675', 'None', 'None', 'Yersinia pestis', 'Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia', 'Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pTP33, complete sequence', 'BCT', 'Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation', '33990', 'DNA', 'None', 'None', 'Yersinia pestis', 'double', 'circular', '24-OCT-2019', '24-OCT-2019', 'Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI ; Annotation Date :: 10/16/2019 14:40:45 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.9 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##', '10/16/2019 14:40:45', 'Best-placed reference protein set', 'NCBI Prokaryotic Genome Annotation Pipeline (PGAP)', 'NCBI', '4.9', 'None', 'Unicycler v. v0.4.7', 'None', '4427', '4239', '2', 'Yes', 'Gene', '4531', '4239', '104', '176.1x', 'Full', '11', '188', '0 of 188', '89 of 188', '108 of 188', '27 of 188', '32 of 188', '8 7 7 (5S 16S 23S)', '8 7 7 (5S 16S 23S)', 'None', 'Illumina MiSeq', '71', 'None', '8', '1769093958', 'CP045151', 'CP045151.1', 'SAMN12991206', 'PRJNA269675', 'None', 'None', 'Yersinia pestis', 'Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia', 'Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pCD, complete sequence', 'BCT', 'Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation', '68343', 'DNA', 'None', 'None', 'Yersinia pestis', 'double', 'circular', '24-OCT-2019', '24-OCT-2019', 'Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI ; Annotation Date :: 10/16/2019 14:40:45 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.9 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##', '10/16/2019 14:40:45', 'Best-placed reference protein set', 'NCBI Prokaryotic Genome Annotation Pipeline (PGAP)', 'NCBI', '4.9', 'None', 'Unicycler v. v0.4.7', 'None', '4427', '4239', '2', 'Yes', 'Gene', '4531', '4239', '104', '176.1x', 'Full', '11', '188', '0 of 188', '89 of 188', '108 of 188', '27 of 188', '32 of 188', '8 7 7 (5S 16S 23S)', '8 7 7 (5S 16S 23S)', 'None', 'Illumina MiSeq', '71', 'None', '9', '1769093841', 'CP045150', 'CP045150.1', 'SAMN12991206', 'PRJNA269675', 'None', 'None', 'Yersinia pestis', 'Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia', 'Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pMT, complete sequence', 'BCT', 'Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation', '100984', 'DNA', 'None', 'None', 'Yersinia pestis', 'double', 'circular', '24-OCT-2019', '24-OCT-2019', 'Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI ; Annotation Date :: 10/16/2019 14:40:45 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.9 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##', '10/16/2019 14:40:45', 'Best-placed reference protein set', 'NCBI Prokaryotic Genome Annotation Pipeline (PGAP)', 'NCBI', '4.9', 'None', 'Unicycler v. v0.4.7', 'None', '4427', '4239', '2', 'Yes', 'Gene', '4531', '4239', '104', '176.1x', 'Full', '11', '188', '0 of 188', '89 of 188', '108 of 188', '27 of 188', '32 of 188', '8 7 7 (5S 16S 23S)', '8 7 7 (5S 16S 23S)', 'None', 'Illumina MiSeq', '71', 'None', '10', '1769089848', 'CP045149', 'CP045149.1', 'SAMN12991206', 'PRJNA269675', 'None', 'None', 'Yersinia pestis', 'Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia', 'Yersinia pestis strain SCPM-O-DNA-18 (I-3113) chromosome, complete genome', 'BCT', 'Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation', '4546217', 'DNA', 'None', 'None', 'Yersinia pestis', 'double', 'circular', '24-OCT-2019', '24-OCT-2019', 'Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI ; Annotation Date :: 10/16/2019 14:40:45 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.9 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##', '10/16/2019 14:40:45', 'Best-placed reference protein set', 'NCBI Prokaryotic Genome Annotation Pipeline (PGAP)', 'NCBI', '4.9', 'None', 'Unicycler v. v0.4.7', 'None', '4427', '4239', '2', 'Yes', 'Gene', '4531', '4239', '104', '176.1x', 'Full', '11', '188', '0 of 188', '89 of 188', '108 of 188', '27 of 188', '32 of 188', '8 7 7 (5S 16S 23S)', '8 7 7 (5S 16S 23S)', 'None', 'Illumina MiSeq', '71', 'None']

    table_dict = {}
    # Populate the dict with data
    for metadata_i in range(0,len(metadata)):
        columns_i = metadata_i
        # If we're starting the next row of metadata
        if metadata_i >= len(columns):
            columns_i = metadata_i % len(columns)
        # Add key-value pair
        key = columns[columns_i]
        value = metadata[metadata_i]
        # Check if already present, if not add as list
        if key not in table_dict:
            table_dict[key] = [value]
        # Otherwise append, creating a list of values
        else:
            table_dict[key].append(value)

    return table_dict

@pytest.fixture(scope="module")
def pubmed_table_data():
    '''Return a dictionary containing the expected database values of the Pubmed Table'''
    columns = ['id', 'Pubmed_id', 'PubmedPublishDate', 'PubmedEPublishDate', 'PubmedSource',
    'PubmedFullSource', 'PubmedAuthorList', 'PubmedTitle', 'PubmedVolume', 'PubmedIssue',
    'PubmedPages', 'PubmedDOI', 'PubmedPubStatus', 'PubmedRecordStatus', 'PubmedLangList',
    'PubmedTypeList', 'PubmedComment']

    # Currently testing a pubmed file that is empty
    #metadata = []

    table_dict = {}
    # Populate the dict with data
    for i in range(0,len(columns)):
        key = columns[i]
        value = ''
        #value = metadata[i]
        table_dict[key] = value

    return table_dict

@pytest.fixture(scope="module")
def sra_table_data():
    '''Return a dictionary containing the expected database values of the SRA Table'''
    columns = ['id', 'SRA_id', 'SRABioProjectAccession', 'SRABioSampleAccession', 'SRAExperimentAccession',
    'SRARunAccession', 'SRASampleAccession', 'SRAExperimentName', 'SRAExperimentStatus',
    'SRAExperimentVersion', 'SRAIsPublic', 'SRASampleName', 'SRAStaticDataAvailable',
    'SRAStudyAcc', 'SRAStudName', 'SRATitle', 'SRAOrganismName', 'SRAOrganismTaxID',
    'SRAClusterName', 'SRAInstrumentModel', 'SRALibraryName', 'SRALibraryLayout',
    'SRALibrarySelection', 'SRALibrarySource', 'SRALibraryStrategy', 'SRAPlatform',
    'SRATotalBases', 'SRATotalSize', 'SRATotalSpots', 'SRATotalRuns', 'SRACreateDate',
    'SRAUpdateDate', 'SRACenterName', 'SRAContactName', 'SRALabName', 'SRASubmitterAccession', 'SRAComment']

    metadata = ['1', '9179237', 'PRJNA269675', 'SAMN12991206', 'SRX6977651', 'SRR10259780',
    'SRS5502739', 'Shotgun 2019 Sample 199', 'public', '1', 'true', '', 'true', 'SRP051099',
    'Pathogenic microorganism Genome sequencing', 'Shotgun 2019 Sample 199', 'None', '632',
    'public', 'MinION', '2019 Sample 199 Library 02', 'SINGLE', 'unspecified', 'GENOMIC',
    'WGS', 'OXFORD_NANOPORE', '617169107', '500796667', '53647', '1', '2019/10/12',
    '2019/10/11', 'SRCAMB', 'Alexander Bogun', 'Science Department', 'SRA977701', 'None',
    '2', '9179236', 'PRJNA269675', 'SAMN12991206', 'SRX6977650', 'SRR10259781', 'SRS5502739',
    'Shotgun 2019 Sample 199', 'public', '1', 'true', '', 'true', 'SRP051099',
    'Pathogenic microorganism Genome sequencing', 'Shotgun 2019 Sample 199', 'None', '632',
    'public', 'Illumina MiSeq', '2019 Sample 199 Library 01', 'PAIRED', 'unspecified', 'GENOMIC',
    'WGS', 'ILLUMINA', '220972916', '128084615', '414515', '1', '2019/10/12', '2019/10/11',
    'SRCAMB', 'Alexander Bogun', 'Science Department', 'SRA977701', 'None']

    table_dict = {}
    # Populate the dict with data
    for metadata_i in range(0,len(metadata)):
        columns_i = metadata_i
        # If we're starting the next row of metadata
        if metadata_i >= len(columns):
            columns_i = metadata_i % len(columns)
        # Add key-value pair
        key = columns[columns_i]
        value = metadata[metadata_i]
        # Check if already present, if not add as list
        if key not in table_dict:
            table_dict[key] = [value]
        # Otherwise append, creating a list of values
        else:
            table_dict[key].append(value)

    return table_dict
