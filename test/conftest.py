"""
NCBImeta Conftest
This is the pytest fixture file.

@author: Katherine Eaton
"""
# flake8: noqa

# -----------------------------------------------------------------------#
#                         Modules and Packages                          #
# -----------------------------------------------------------------------#
import pytest

# -----------------------------------------------------------------------#
#                             Fixtures                                  #
# -----------------------------------------------------------------------#

# Reminder, awk was used to help efficiently format the column and value lists
# To get the column names:
# head -n 1 test_Assembly.txt | awk 'BEGIN{FS="\t"; ORS=", "}{for (i=1;i<=NF;i++){print "\x27"$i"\x27"}}'
# To get the metadata field values:
# tail -n+2 test_Assembly.txt | awk 'BEGIN{FS="\t"; ORS=", "}{for (i=1;i<=NF;i++){print "\x27"$i"\x27"}}'


@pytest.fixture(scope="module")
def assembly_table_data():
    """Return a dictionary containing the expected database values of the Assembly Table"""

    columns = [
        "id",
        "Assembly_id",
        "AssemblyAccession",
        "AssemblyBioSampleAccession",
        "AssemblyBioSampleID",
        "AssemblyGenbankBioprojectAccession",
        "AssemblyGenbankID",
        "AssemblyRefseqBioprojectAccession",
        "AssemblyRefSeqCategory",
        "AssemblyRefSeqID",
        "AssemblyWGSAccession",
        "AssemblyInfraspecies",
        "AssemblyIsolate",
        "AssemblyOrganism",
        "AssemblySpeciesTaxonomicID",
        "AssemblySpeciesName",
        "AssemblyTaxonomicID",
        "AssemblyName",
        "AssemblyStatus",
        "AssemblyType",
        "AssemblyCoverage",
        "AssemblyChromosomes",
        "AssemblyContigCount",
        "AssemblyContigN50",
        "AssemblyContigL50",
        "AssemblyNonChromosomalReplicons",
        "AssemblyReplicons",
        "AssemblyScaffolds",
        "AssemblyScaffoldN50",
        "AssemblyScaffoldL50",
        "AssemblyTotalLength",
        "AssemblyUngappedLength",
        "AssemblySubmitterOrganization",
        "AssemblySubmissionDate",
        "AssemblyReleaseDate",
        "AssemblyFTPAssemblyReport",
        "AssemblyFTPGenbank",
        "AssemblyFTPRefSeq",
        "AssemblyFTPStatsReport",
        "AssemblyComment",
    ]

    metadata = [
        "1",
        "5025191",
        "GCF_009295945.1",
        "SAMN12991206",
        "12991206",
        "PRJNA269675",
        "14768768",
        "PRJNA224116",
        "na",
        "14769648",
        "",
        "SCPM-O-DNA-18 (I-3113)",
        "",
        "Yersinia pestis (enterobacteria)",
        "632",
        "Yersinia pestis",
        "632",
        "ASM929594v1",
        "Complete Genome",
        "haploid",
        "176.1",
        "1",
        "5",
        "4546217",
        "1",
        "4",
        "5",
        "5;5;0;0",
        "4546217",
        "1",
        "4759144",
        "4759144",
        "SRCAMB",
        "2019/10/24 00:00",
        "2019/10/24 00:00",
        "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1/GCF_009295945.1_ASM929594v1_assembly_report.txt",
        "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/009/295/945/GCA_009295945.1_ASM929594v1",
        "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1",
        "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1/GCF_009295945.1_ASM929594v1_assembly_stats.txt",
        "",
    ]

    table_dict = {}
    # Populate the dict with data
    for i in range(0, len(columns)):
        key = columns[i]
        value = metadata[i]
        table_dict[key] = value

    return table_dict


@pytest.fixture(scope="module")
def bioproject_table_data():
    """Return a dictionary containing the expected database values of the BioProject Table"""

    columns = [
        "id",
        "BioProject_id",
        "BioProjectAccession",
        "BioProjectDataType",
        "BioProjectDescription",
        "BioProjectMethodType",
        "BioProjectName",
        "BioProjectTargetCapture",
        "BioProjectTargetMaterial",
        "BioProjectTargetScope",
        "BioProjectTitle",
        "BioProjectOrganismLabel",
        "BioProjectOrganismStrain",
        "BioProjectOrganismTaxID",
        "BioProjectSpeciesTaxID",
        "BioProjectSupergroup",
        "BioProjectRegistrationDate",
        "BioProjectReleaseDate",
        "BioProjectModificationDate",
        "BioProjectRelevanceMedical",
        "BioProjectSubmitterOrganization",
        "BioProjectPublished",
        "BioProjectDatePublished",
        "BioProjectPublicationID",
        "BioProjectPublicationDB",
        "BioProjectComment",
    ]

    metadata = [
        "1",
        "269675",
        "PRJNA269675",
        "Genome sequencing and assembly",
        "Genome sequencing of bacteria from State collection of pathogenic microorganisms Obolensk. Collection includes bacteria, fungi, and cell-lines.",
        "eSequencing",
        "Bacteria",
        "eWhole",
        "eGenome",
        "eMultispecies",
        "Pathogenic microorganism Genome sequencing",
        "",
        "",
        "2",
        "-1",
        "eBacteria",
        "2014-12-09",
        "2015-03-11T00:00:00Z",
        "2014-12-09",
        "yes",
        "SRCAMB",
        "",
        "2015-12-03T00:00:00Z;2016-03-03T00:00:00Z",
        "26634751;26941146",
        "ePubmed;ePubmed",
        "",
    ]

    table_dict = {}
    # Populate the dict with data
    for i in range(0, len(columns)):
        key = columns[i]
        value = metadata[i]
        table_dict[key] = value

    return table_dict


@pytest.fixture(scope="module")
def biosample_table_data():
    """Return a dictionary containing the expected database values of the BioSample Table"""

    columns = [
        "id",
        "BioSample_id",
        "BioSampleAccession",
        "BioSampleAccessionSecondary",
        "BioSampleBioProjectAccession",
        "BioSampleSRAAccession",
        "BioSampleTitle",
        "BioSampleName",
        "BioSampleType",
        "BioSamplePackage",
        "BioSampleInfraspecies",
        "BioSampleOrganism",
        "BioSampleOrganismAlt",
        "BioSampleSubSpecies",
        "BioSampleStrain",
        "BioSampleTaxonomyID",
        "BioSampleBiovar",
        "BioSampleSerovar",
        "BioSampleCollectionDate",
        "BioSampleGeographicLocation",
        "BioSampleHost",
        "BioSampleHostDisease",
        "BioSampleHostHealthState",
        "BioSampleIsolateNameAlias",
        "BioSampleIsolationSource",
        "BioSampleLat",
        "BioSampleLatLon",
        "BioSampleLon",
        "BioSampleSubmissionDate",
        "BioSampleModificationDate",
        "BioSamplePublicationDate",
        "BioSampleOrganization",
        "BioSampleComment",
    ]

    metadata = [
        "1",
        "12991206",
        "SAMN12991206",
        "",
        "",
        "SRS5502739",
        "Microbe sample from Yersinia pestis",
        "2019 Sample 199",
        "Cell culture",
        "Microbe.1.0",
        "",
        "Yersinia pestis",
        "Yersinia pestis",
        "",
        "SCPM-O-DNA-18 (I-3113)",
        "632",
        "",
        "",
        "1984",
        "Russia: Tuva",
        "Marmota sibirica",
        "Plague",
        "",
        "",
        "",
        "",
        "",
        "",
        "2019-10-08T07:15:03.953",
        "2019-10-11T02:56:17.027",
        "2019-10-08T00:00:00.000",
        "SRCAMB",
        "",
    ]

    table_dict = {}
    # Populate the dict with data
    for i in range(0, len(columns)):
        key = columns[i]
        value = metadata[i]
        table_dict[key] = value

    return table_dict


@pytest.fixture(scope="module")
def nucleotide_table_data():
    """Return a dictionary containing the expected database values of the Nucleotide Table"""

    columns = [
        "id",
        "Nucleotide_id",
        "NucleotideAccession",
        "NucleotideAccessionVersion",
        "NucleotideBioSampleAccession",
        "NucleotideBioProjectAccession",
        "NucleotideOrganism",
        "NucleotideTaxonomy",
        "NucleotideDefinition",
        "NucleotideDivision",
        "NucleotideReferenceJournal",
        "NucleotideReferenceTitle",
        "NucleotideReferenceAuthors",
        "NucleotideLength",
        "NucleotideMoleculeType",
        "NucleotideSeqDataName",
        "NucleotideSource",
        "NucleotideStrandedness",
        "NucleotideTopology",
        "NucleotideCreateDate",
        "NucleotideUpdateDate",
        "NucleotideGenBankComment",
        "NucleotideAnnotationDate",
        "NucleotideAnnotationMethod",
        "NucleotideAnnotationPipeline",
        "NucleotideAnnotationProvider",
        "NucleotideAnnotationSoftwarerevision",
        "NucleotideAssemblyDate",
        "NucleotideAssemblyMethod",
        "NucleotideAssemblyName",
        "NucleotideCDS",
        "NucleotideCDSTotal",
        "NucleotideCDSCoding",
        "NucleotideCDSProtein",
        "NucleotideCDSWithoutProtein",
        "NucleotideCRISPRArrays",
        "NucleotideExpectedFinalVersion",
        "NucleotideFeaturesAnnotated",
        "NucleotideGenes",
        "NucleotideGenesTotal",
        "NucleotideGenesCoding",
        "NucleotideGenesRNA",
        "NucleotideGenomeCoverage",
        "NucleotideGenomeRepresentation",
        "NucleotidencRNAs",
        "NucleotidePseudoGenes",
        "NucleotidePseudoGenesTotal",
        "NucleotidePseudoGenesAmbResidues",
        "NucleotidePseudoGenesFrameshifted",
        "NucleotidePseudoGenesIncomplete",
        "NucleotidePseudoGenesInternalStop",
        "NucleotidePseudoGenesMultipleProblems",
        "NucleotiderRNAs",
        "NucleotiderRNAsComplete",
        "NucleotiderRNAsPartial",
        "NucleotideSequencingTechnology",
        "NucleotideRNAs",
        "NucleotideComment",
    ]

    metadata = [
        "1",
        "1769169004",
        "NZ_CP045153",
        "NZ_CP045153.1",
        "SAMN12991206",
        "PRJNA224116",
        "Yersinia pestis",
        "Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia",
        "Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pPCP, complete sequence",
        "CON",
        "Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation",
        "Direct Submission",
        "Bogun,A.;Kislichkina,A.;Mayskaya,N.;Platonov,M.;Sizova,A.;Skryabin,Y.;Solomentsev,V.;Ivanov,S.;Shaikhutdinova,R.;Dentovskaya,S.;Anisimov,A.",
        "9610",
        "DNA",
        "",
        "Yersinia pestis",
        "double",
        "circular",
        "25-OCT-2019",
        "04-FEB-2020",
        "REFSEQ INFORMATION: The reference sequence was derived from CP045153.; Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI RefSeq ; Annotation Date :: 02/04/2020 00:09:43 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.11 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,288 ; CDSs (total) :: 4,184 ; Genes (coding) :: 4,036 ; CDSs (with protein) :: 4,036 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 148 ; CDSs (without protein) :: 148 ; Pseudo Genes (ambiguous residues) :: 0 of 148 ; Pseudo Genes (frameshifted) :: 81 of 148 ; Pseudo Genes (incomplete) :: 74 of 148 ; Pseudo Genes (internal stop) :: 19 of 148 ; Pseudo Genes (multiple problems) :: 23 of 148 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##; COMPLETENESS: full length.",
        "02/04/2020 00:09:43",
        "Best-placed reference protein set",
        "NCBI Prokaryotic Genome Annotation Pipeline (PGAP)",
        "NCBI RefSeq",
        "4.11",
        "",
        "Unicycler v. v0.4.7",
        "",
        "",
        "4,184",
        "",
        "4,036",
        "148",
        "2",
        "Yes",
        "Gene",
        "",
        "4,288",
        "4,036",
        "104",
        "176.1x",
        "Full",
        "11",
        "",
        "148",
        "0 of 148",
        "81 of 148",
        "74 of 148",
        "19 of 148",
        "23 of 148",
        "8, 7, 7 (5S, 16S, 23S)",
        "8, 7, 7 (5S, 16S, 23S)",
        "",
        "Illumina MiSeq",
        "71",
        "",
        "2",
        "1769169003",
        "NZ_CP045152",
        "NZ_CP045152.1",
        "SAMN12991206",
        "PRJNA224116",
        "Yersinia pestis",
        "Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia",
        "Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pTP33, complete sequence",
        "CON",
        "Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation",
        "Direct Submission",
        "Bogun,A.;Kislichkina,A.;Mayskaya,N.;Platonov,M.;Sizova,A.;Skryabin,Y.;Solomentsev,V.;Ivanov,S.;Shaikhutdinova,R.;Dentovskaya,S.;Anisimov,A.",
        "33990",
        "DNA",
        "",
        "Yersinia pestis",
        "double",
        "circular",
        "25-OCT-2019",
        "04-FEB-2020",
        "REFSEQ INFORMATION: The reference sequence was derived from CP045152.; Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI RefSeq ; Annotation Date :: 02/04/2020 00:09:43 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.11 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,288 ; CDSs (total) :: 4,184 ; Genes (coding) :: 4,036 ; CDSs (with protein) :: 4,036 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 148 ; CDSs (without protein) :: 148 ; Pseudo Genes (ambiguous residues) :: 0 of 148 ; Pseudo Genes (frameshifted) :: 81 of 148 ; Pseudo Genes (incomplete) :: 74 of 148 ; Pseudo Genes (internal stop) :: 19 of 148 ; Pseudo Genes (multiple problems) :: 23 of 148 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##; COMPLETENESS: full length.",
        "02/04/2020 00:09:43",
        "Best-placed reference protein set",
        "NCBI Prokaryotic Genome Annotation Pipeline (PGAP)",
        "NCBI RefSeq",
        "4.11",
        "",
        "Unicycler v. v0.4.7",
        "",
        "",
        "4,184",
        "",
        "4,036",
        "148",
        "2",
        "Yes",
        "Gene",
        "",
        "4,288",
        "4,036",
        "104",
        "176.1x",
        "Full",
        "11",
        "",
        "148",
        "0 of 148",
        "81 of 148",
        "74 of 148",
        "19 of 148",
        "23 of 148",
        "8, 7, 7 (5S, 16S, 23S)",
        "8, 7, 7 (5S, 16S, 23S)",
        "",
        "Illumina MiSeq",
        "71",
        "",
        "3",
        "1769169002",
        "NZ_CP045151",
        "NZ_CP045151.1",
        "SAMN12991206",
        "PRJNA224116",
        "Yersinia pestis",
        "Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia",
        "Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pCD, complete sequence",
        "CON",
        "Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation",
        "Direct Submission",
        "Bogun,A.;Kislichkina,A.;Mayskaya,N.;Platonov,M.;Sizova,A.;Skryabin,Y.;Solomentsev,V.;Ivanov,S.;Shaikhutdinova,R.;Dentovskaya,S.;Anisimov,A.",
        "68343",
        "DNA",
        "",
        "Yersinia pestis",
        "double",
        "circular",
        "25-OCT-2019",
        "04-FEB-2020",
        "REFSEQ INFORMATION: The reference sequence was derived from CP045151.; Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI RefSeq ; Annotation Date :: 02/04/2020 00:09:43 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.11 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,288 ; CDSs (total) :: 4,184 ; Genes (coding) :: 4,036 ; CDSs (with protein) :: 4,036 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 148 ; CDSs (without protein) :: 148 ; Pseudo Genes (ambiguous residues) :: 0 of 148 ; Pseudo Genes (frameshifted) :: 81 of 148 ; Pseudo Genes (incomplete) :: 74 of 148 ; Pseudo Genes (internal stop) :: 19 of 148 ; Pseudo Genes (multiple problems) :: 23 of 148 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##; COMPLETENESS: full length.",
        "02/04/2020 00:09:43",
        "Best-placed reference protein set",
        "NCBI Prokaryotic Genome Annotation Pipeline (PGAP)",
        "NCBI RefSeq",
        "4.11",
        "",
        "Unicycler v. v0.4.7",
        "",
        "",
        "4,184",
        "",
        "4,036",
        "148",
        "2",
        "Yes",
        "Gene",
        "",
        "4,288",
        "4,036",
        "104",
        "176.1x",
        "Full",
        "11",
        "",
        "148",
        "0 of 148",
        "81 of 148",
        "74 of 148",
        "19 of 148",
        "23 of 148",
        "8, 7, 7 (5S, 16S, 23S)",
        "8, 7, 7 (5S, 16S, 23S)",
        "",
        "Illumina MiSeq",
        "71",
        "",
        "4",
        "1769169001",
        "NZ_CP045150",
        "NZ_CP045150.1",
        "SAMN12991206",
        "PRJNA224116",
        "Yersinia pestis",
        "Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia",
        "Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pMT, complete sequence",
        "CON",
        "Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation",
        "Direct Submission",
        "Bogun,A.;Kislichkina,A.;Mayskaya,N.;Platonov,M.;Sizova,A.;Skryabin,Y.;Solomentsev,V.;Ivanov,S.;Shaikhutdinova,R.;Dentovskaya,S.;Anisimov,A.",
        "100984",
        "DNA",
        "",
        "Yersinia pestis",
        "double",
        "circular",
        "25-OCT-2019",
        "04-FEB-2020",
        "REFSEQ INFORMATION: The reference sequence was derived from CP045150.; Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI RefSeq ; Annotation Date :: 02/04/2020 00:09:43 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.11 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,288 ; CDSs (total) :: 4,184 ; Genes (coding) :: 4,036 ; CDSs (with protein) :: 4,036 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 148 ; CDSs (without protein) :: 148 ; Pseudo Genes (ambiguous residues) :: 0 of 148 ; Pseudo Genes (frameshifted) :: 81 of 148 ; Pseudo Genes (incomplete) :: 74 of 148 ; Pseudo Genes (internal stop) :: 19 of 148 ; Pseudo Genes (multiple problems) :: 23 of 148 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##; COMPLETENESS: full length.",
        "02/04/2020 00:09:43",
        "Best-placed reference protein set",
        "NCBI Prokaryotic Genome Annotation Pipeline (PGAP)",
        "NCBI RefSeq",
        "4.11",
        "",
        "Unicycler v. v0.4.7",
        "",
        "",
        "4,184",
        "",
        "4,036",
        "148",
        "2",
        "Yes",
        "Gene",
        "",
        "4,288",
        "4,036",
        "104",
        "176.1x",
        "Full",
        "11",
        "",
        "148",
        "0 of 148",
        "81 of 148",
        "74 of 148",
        "19 of 148",
        "23 of 148",
        "8, 7, 7 (5S, 16S, 23S)",
        "8, 7, 7 (5S, 16S, 23S)",
        "",
        "Illumina MiSeq",
        "71",
        "",
        "5",
        "1769169000",
        "NZ_CP045149",
        "NZ_CP045149.1",
        "SAMN12991206",
        "PRJNA224116",
        "Yersinia pestis",
        "Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia",
        "Yersinia pestis strain SCPM-O-DNA-18 (I-3113) chromosome, complete genome",
        "CON",
        "Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation",
        "Direct Submission",
        "Bogun,A.;Kislichkina,A.;Mayskaya,N.;Platonov,M.;Sizova,A.;Skryabin,Y.;Solomentsev,V.;Ivanov,S.;Shaikhutdinova,R.;Dentovskaya,S.;Anisimov,A.",
        "4546217",
        "DNA",
        "",
        "Yersinia pestis",
        "double",
        "circular",
        "25-OCT-2019",
        "04-FEB-2020",
        "REFSEQ INFORMATION: The reference sequence was derived from CP045149.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; Bacteria and source DNA available from SRC AMB.; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI RefSeq ; Annotation Date :: 02/04/2020 00:09:43 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.11 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,288 ; CDSs (total) :: 4,184 ; Genes (coding) :: 4,036 ; CDSs (with protein) :: 4,036 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 148 ; CDSs (without protein) :: 148 ; Pseudo Genes (ambiguous residues) :: 0 of 148 ; Pseudo Genes (frameshifted) :: 81 of 148 ; Pseudo Genes (incomplete) :: 74 of 148 ; Pseudo Genes (internal stop) :: 19 of 148 ; Pseudo Genes (multiple problems) :: 23 of 148 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##; COMPLETENESS: full length.",
        "02/04/2020 00:09:43",
        "Best-placed reference protein set",
        "NCBI Prokaryotic Genome Annotation Pipeline (PGAP)",
        "NCBI RefSeq",
        "4.11",
        "",
        "Unicycler v. v0.4.7",
        "",
        "",
        "4,184",
        "",
        "4,036",
        "148",
        "2",
        "Yes",
        "Gene",
        "",
        "4,288",
        "4,036",
        "104",
        "176.1x",
        "Full",
        "11",
        "",
        "148",
        "0 of 148",
        "81 of 148",
        "74 of 148",
        "19 of 148",
        "23 of 148",
        "8, 7, 7 (5S, 16S, 23S)",
        "8, 7, 7 (5S, 16S, 23S)",
        "",
        "Illumina MiSeq",
        "71",
        "",
        "6",
        "1769094081",
        "CP045153",
        "CP045153.1",
        "SAMN12991206",
        "PRJNA269675",
        "Yersinia pestis",
        "Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia",
        "Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pPCP, complete sequence",
        "BCT",
        "Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation",
        "Direct Submission",
        "Bogun,A.;Kislichkina,A.;Mayskaya,N.;Platonov,M.;Sizova,A.;Skryabin,Y.;Solomentsev,V.;Ivanov,S.;Shaikhutdinova,R.;Dentovskaya,S.;Anisimov,A.",
        "9610",
        "DNA",
        "",
        "Yersinia pestis",
        "double",
        "circular",
        "24-OCT-2019",
        "24-OCT-2019",
        "Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI ; Annotation Date :: 10/16/2019 14:40:45 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.9 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##",
        "10/16/2019 14:40:45",
        "Best-placed reference protein set",
        "NCBI Prokaryotic Genome Annotation Pipeline (PGAP)",
        "NCBI",
        "4.9",
        "",
        "Unicycler v. v0.4.7",
        "",
        "",
        "4,427",
        "",
        "4,239",
        "188",
        "2",
        "Yes",
        "Gene",
        "",
        "4,531",
        "4,239",
        "104",
        "176.1x",
        "Full",
        "11",
        "",
        "188",
        "0 of 188",
        "89 of 188",
        "108 of 188",
        "27 of 188",
        "32 of 188",
        "8, 7, 7 (5S, 16S, 23S)",
        "8, 7, 7 (5S, 16S, 23S)",
        "",
        "Illumina MiSeq",
        "71",
        "",
        "7",
        "1769094034",
        "CP045152",
        "CP045152.1",
        "SAMN12991206",
        "PRJNA269675",
        "Yersinia pestis",
        "Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia",
        "Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pTP33, complete sequence",
        "BCT",
        "Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation",
        "Direct Submission",
        "Bogun,A.;Kislichkina,A.;Mayskaya,N.;Platonov,M.;Sizova,A.;Skryabin,Y.;Solomentsev,V.;Ivanov,S.;Shaikhutdinova,R.;Dentovskaya,S.;Anisimov,A.",
        "33990",
        "DNA",
        "",
        "Yersinia pestis",
        "double",
        "circular",
        "24-OCT-2019",
        "24-OCT-2019",
        "Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI ; Annotation Date :: 10/16/2019 14:40:45 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.9 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##",
        "10/16/2019 14:40:45",
        "Best-placed reference protein set",
        "NCBI Prokaryotic Genome Annotation Pipeline (PGAP)",
        "NCBI",
        "4.9",
        "",
        "Unicycler v. v0.4.7",
        "",
        "",
        "4,427",
        "",
        "4,239",
        "188",
        "2",
        "Yes",
        "Gene",
        "",
        "4,531",
        "4,239",
        "104",
        "176.1x",
        "Full",
        "11",
        "",
        "188",
        "0 of 188",
        "89 of 188",
        "108 of 188",
        "27 of 188",
        "32 of 188",
        "8, 7, 7 (5S, 16S, 23S)",
        "8, 7, 7 (5S, 16S, 23S)",
        "",
        "Illumina MiSeq",
        "71",
        "",
        "8",
        "1769093958",
        "CP045151",
        "CP045151.1",
        "SAMN12991206",
        "PRJNA269675",
        "Yersinia pestis",
        "Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia",
        "Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pCD, complete sequence",
        "BCT",
        "Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation",
        "Direct Submission",
        "Bogun,A.;Kislichkina,A.;Mayskaya,N.;Platonov,M.;Sizova,A.;Skryabin,Y.;Solomentsev,V.;Ivanov,S.;Shaikhutdinova,R.;Dentovskaya,S.;Anisimov,A.",
        "68343",
        "DNA",
        "",
        "Yersinia pestis",
        "double",
        "circular",
        "24-OCT-2019",
        "24-OCT-2019",
        "Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI ; Annotation Date :: 10/16/2019 14:40:45 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.9 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##",
        "10/16/2019 14:40:45",
        "Best-placed reference protein set",
        "NCBI Prokaryotic Genome Annotation Pipeline (PGAP)",
        "NCBI",
        "4.9",
        "",
        "Unicycler v. v0.4.7",
        "",
        "",
        "4,427",
        "",
        "4,239",
        "188",
        "2",
        "Yes",
        "Gene",
        "",
        "4,531",
        "4,239",
        "104",
        "176.1x",
        "Full",
        "11",
        "",
        "188",
        "0 of 188",
        "89 of 188",
        "108 of 188",
        "27 of 188",
        "32 of 188",
        "8, 7, 7 (5S, 16S, 23S)",
        "8, 7, 7 (5S, 16S, 23S)",
        "",
        "Illumina MiSeq",
        "71",
        "",
        "9",
        "1769093841",
        "CP045150",
        "CP045150.1",
        "SAMN12991206",
        "PRJNA269675",
        "Yersinia pestis",
        "Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia",
        "Yersinia pestis strain SCPM-O-DNA-18 (I-3113) plasmid pMT, complete sequence",
        "BCT",
        "Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation",
        "Direct Submission",
        "Bogun,A.;Kislichkina,A.;Mayskaya,N.;Platonov,M.;Sizova,A.;Skryabin,Y.;Solomentsev,V.;Ivanov,S.;Shaikhutdinova,R.;Dentovskaya,S.;Anisimov,A.",
        "100984",
        "DNA",
        "",
        "Yersinia pestis",
        "double",
        "circular",
        "24-OCT-2019",
        "24-OCT-2019",
        "Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI ; Annotation Date :: 10/16/2019 14:40:45 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.9 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##",
        "10/16/2019 14:40:45",
        "Best-placed reference protein set",
        "NCBI Prokaryotic Genome Annotation Pipeline (PGAP)",
        "NCBI",
        "4.9",
        "",
        "Unicycler v. v0.4.7",
        "",
        "",
        "4,427",
        "",
        "4,239",
        "188",
        "2",
        "Yes",
        "Gene",
        "",
        "4,531",
        "4,239",
        "104",
        "176.1x",
        "Full",
        "11",
        "",
        "188",
        "0 of 188",
        "89 of 188",
        "108 of 188",
        "27 of 188",
        "32 of 188",
        "8, 7, 7 (5S, 16S, 23S)",
        "8, 7, 7 (5S, 16S, 23S)",
        "",
        "Illumina MiSeq",
        "71",
        "",
        "10",
        "1769089848",
        "CP045149",
        "CP045149.1",
        "SAMN12991206",
        "PRJNA269675",
        "Yersinia pestis",
        "Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Yersiniaceae; Yersinia",
        "Yersinia pestis strain SCPM-O-DNA-18 (I-3113) chromosome, complete genome",
        "BCT",
        "Submitted (14-OCT-2019) Science Department, SRCAMB, Building 1, Obolensk, Moscow region 142279, Russian Federation",
        "Direct Submission",
        "Bogun,A.;Kislichkina,A.;Mayskaya,N.;Platonov,M.;Sizova,A.;Skryabin,Y.;Solomentsev,V.;Ivanov,S.;Shaikhutdinova,R.;Dentovskaya,S.;Anisimov,A.",
        "4546217",
        "DNA",
        "",
        "Yersinia pestis",
        "double",
        "circular",
        "24-OCT-2019",
        "24-OCT-2019",
        "Bacteria and source DNA available from SRC AMB.; The annotation was added by the NCBI Prokaryotic Genome Annotation Pipeline (PGAP). Information about PGAP can be found here: https://www.ncbi.nlm.nih.gov/genome/annotation_prok/; ; ##Genome-Assembly-Data-START## ; Assembly Method :: Unicycler v. v0.4.7 ; Genome Representation :: Full ; Expected Final Version :: Yes ; Genome Coverage :: 176.1x ; Sequencing Technology :: Illumina MiSeq; Oxford Nanopore MiniION ; ##Genome-Assembly-Data-END##; ; ##Genome-Annotation-Data-START## ; Annotation Provider :: NCBI ; Annotation Date :: 10/16/2019 14:40:45 ; Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline (PGAP) ; Annotation Method :: Best-placed reference protein set; GeneMarkS-2+ ; Annotation Software revision :: 4.9 ; Features Annotated :: Gene; CDS; rRNA; tRNA; ncRNA; repeat_region ; Genes (total) :: 4,531 ; CDSs (total) :: 4,427 ; Genes (coding) :: 4,239 ; CDSs (with protein) :: 4,239 ; Genes (RNA) :: 104 ; rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; complete rRNAs :: 8, 7, 7 (5S, 16S, 23S) ; tRNAs :: 71 ; ncRNAs :: 11 ; Pseudo Genes (total) :: 188 ; CDSs (without protein) :: 188 ; Pseudo Genes (ambiguous residues) :: 0 of 188 ; Pseudo Genes (frameshifted) :: 89 of 188 ; Pseudo Genes (incomplete) :: 108 of 188 ; Pseudo Genes (internal stop) :: 27 of 188 ; Pseudo Genes (multiple problems) :: 32 of 188 ; CRISPR Arrays :: 2 ; ##Genome-Annotation-Data-END##",
        "10/16/2019 14:40:45",
        "Best-placed reference protein set",
        "NCBI Prokaryotic Genome Annotation Pipeline (PGAP)",
        "NCBI",
        "4.9",
        "",
        "Unicycler v. v0.4.7",
        "",
        "",
        "4,427",
        "",
        "4,239",
        "188",
        "2",
        "Yes",
        "Gene",
        "",
        "4,531",
        "4,239",
        "104",
        "176.1x",
        "Full",
        "11",
        "",
        "188",
        "0 of 188",
        "89 of 188",
        "108 of 188",
        "27 of 188",
        "32 of 188",
        "8, 7, 7 (5S, 16S, 23S)",
        "8, 7, 7 (5S, 16S, 23S)",
        "",
        "Illumina MiSeq",
        "71",
        "",
    ]

    table_dict = {}
    # Populate the dict with data
    for metadata_i in range(0, len(metadata)):
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
    """Return a dictionary containing the expected database values of the Pubmed Table"""
    columns = [
        "id",
        "Pubmed_id",
        "PubmedPublishYear",
        "PubmedPubishMonth",
        "PubmedPublishDay",
        "PubmedEPublishDate",
        "PubmedPublishModel",
        "PubmedType",
        "PubmedJournalTitle",
        "PubmedJournalAbbrev",
        "PubmedJournalISSN",
        "PubmedArticleTitle",
        "PubmedAbstract",
        "PubmedVolume",
        "PubmedIssue",
        "PubmedPages",
        "PubmedDOI",
        "PubmedAuthorsLastName",
        "PubmedAuthorsForeName",
        "PubmedAuthorsAffiliation",
        "PubmedLanguage",
        "PubmedCitations",
        "PubmedRecordStatus",
        "PubmedPubStatus",
        "PubmedComment",
    ]

    # Currently testing a pubmed file that is empty
    metadata = [
        "1",
        "26634751",
        "2015",
        "Dec",
        "03",
        "",
        "Electronic",
        "Journal Article",
        "Genome announcements",
        "Genome Announc",
        "2169-8287",
        "Nineteen Whole-Genome Assemblies of Yersinia pestis subsp. microtus, Including Representatives of Biovars caucasica, talassica, hissarica, altaica, xilingolensis, and ulegeica.",
        "The etiologic agent of plague, Yersinia pestis, includes two subspecies, of which Y. pestis subsp. microtus contains the strains that cause only occasional diseases in humans that are not accompanied by human-to-human transmission. Here, we report the draft genome sequences of 19 Y. pestis strains (across 6 biovars of Y. pestis subsp. microtus).",
        "3",
        "6",
        "",
        "10.1128/genomeA.01342-15",
        "Kislichkina;Bogun;Kadnikova;Maiskaya;Platonov;Anisimov;Galkina;Dentovskaya;Anisimov",
        "Angelina A;Aleksandr G;Lidiya A;Nadezhda V;Mikhail E;Nikolai V;Elena V;Svetlana V;Andrey P",
        "State Research Center for Applied Microbiology and Biotechnology, Obolensk, Russia angelinakislichkina@yandex.ru anisimov@obolensk.org.;State Research Center for Applied Microbiology and Biotechnology, Obolensk, Russia.;State Research Center for Applied Microbiology and Biotechnology, Obolensk, Russia.;State Research Center for Applied Microbiology and Biotechnology, Obolensk, Russia.;State Research Center for Applied Microbiology and Biotechnology, Obolensk, Russia.;State Research Center for Applied Microbiology and Biotechnology, Obolensk, Russia.;State Research Center for Applied Microbiology and Biotechnology, Obolensk, Russia.;State Research Center for Applied Microbiology and Biotechnology, Obolensk, Russia.;State Research Center for Applied Microbiology and Biotechnology, Obolensk, Russia angelinakislichkina@yandex.ru anisimov@obolensk.org.",
        "eng",
        "Clin Microbiol Rev. 2004 Apr;17(2):434-64;PLoS One. 2012;7(2):e30624;Proc Natl Acad Sci U S A. 2013 Jan 8;110(2):577-82",
        "PubMed-not-MEDLINE",
        "epublish",
        "",
    ]

    table_dict = {}
    # Populate the dict with data
    for i in range(0, len(columns)):
        key = columns[i]
        value = metadata[i]
        table_dict[key] = value

    return table_dict


@pytest.fixture(scope="module")
def sra_table_data():
    """Return a dictionary containing the expected database values of the SRA Table"""

    columns = [
        "id",
        "SRA_id",
        "SRABioProjectAccession",
        "SRABioSampleAccession",
        "SRASampleAccession",
        "SRASampleName",
        "SRAExperimentAccession",
        "SRAExperimentName",
        "SRARunAccession",
        "SRARunName",
        "SRAIsPublic",
        "SRAStaticDataAvailable",
        "SRAStudyAcc",
        "SRAStudyName",
        "SRAStudyAbstract",
        "SRAOrganismName",
        "SRAOrganismTaxID",
        "SRAClusterName",
        "SRAPlatform",
        "SRAInstrumentModel",
        "SRALibraryName",
        "SRALibraryLayout",
        "SRALibrarySelection",
        "SRALibrarySource",
        "SRALibraryStrategy",
        "SRATotalBases",
        "SRATotalSize",
        "SRATotalSpots",
        "SRAFileUrl",
        "SRAFileName",
        "SRAFileSize",
        "SRAFileType",
        "SRARunPublishDate",
        "SRACenterName",
        "SRAContactEmail",
        "SRALabName",
        "SRASubmitterAccession",
        "SRAComment",
    ]

    metadata = [
        "1",
        "9179237",
        "PRJNA269675",
        "SAMN12991206",
        "SRS5502739",
        "2019 Sample 199",
        "SRX6977651",
        "2019 Sample 199 Library 02",
        "SRR10259780",
        "DNA-18.fastq",
        "true",
        "1",
        "SRP051099",
        "Pathogenic microorganism Genome sequencing",
        "Genome sequencing of bacteria from State collection of pathogenic microorganisms Obolensk. Collection includes bacteria, fungi, and cell-lines.",
        "Yersinia pestis",
        "632",
        "public",
        "OXFORD_NANOPORE",
        "MinION",
        "2019 Sample 199 Library 02",
        "SINGLE",
        "unspecified",
        "GENOMIC",
        "WGS",
        "617169107",
        "500796667",
        "53647",
        "https://sra-pub-src-2.s3.amazonaws.com/SRR10259780/DNA-18.fastq.1;https://sra-download.ncbi.nlm.nih.gov/traces/sra7/SRR/010019/SRR10259780",
        "DNA-18.fastq;SRR10259780",
        "1242738825;500797896",
        "fastq;run",
        "2019-10-12 05:13:12",
        "SRCAMB",
        "bogun62@mail.ru",
        "Science Department",
        "SRA977701",
        "",
        "2",
        "9179236",
        "PRJNA269675",
        "SAMN12991206",
        "SRS5502739",
        "2019 Sample 199",
        "SRX6977650",
        "2019 Sample 199 Library 01",
        "SRR10259781",
        "DNA-18_R1.fastq.gz",
        "true",
        "1",
        "SRP051099",
        "Pathogenic microorganism Genome sequencing",
        "Genome sequencing of bacteria from State collection of pathogenic microorganisms Obolensk. Collection includes bacteria, fungi, and cell-lines.",
        "Yersinia pestis",
        "632",
        "public",
        "ILLUMINA",
        "Illumina MiSeq",
        "2019 Sample 199 Library 01",
        "PAIRED",
        "unspecified",
        "GENOMIC",
        "WGS",
        "220972916",
        "128084615",
        "414515",
        "https://sra-pub-src-2.s3.amazonaws.com/SRR10259781/DNA-18_R1.fastq.gz.1;https://sra-pub-src-2.s3.amazonaws.com/SRR10259781/DNA-18_R2.fastq.gz.1;https://sra-download.ncbi.nlm.nih.gov/traces/sra74/SRR/010019/SRR10259781",
        "DNA-18_R1.fastq.gz;DNA-18_R2.fastq.gz;SRR10259781",
        "85491432;96393177;128086438",
        "fastq;fastq;run",
        "2019-10-12 04:18:12",
        "SRCAMB",
        "bogun62@mail.ru",
        "Science Department",
        "SRA977701",
        "",
    ]

    table_dict = {}
    # Populate the dict with data
    for metadata_i in range(0, len(metadata)):
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
def assembly_xml():
    """Return a str of the expected xml from the assembly table"""
    assembly_xml_str = """
    <eSummaryResult>
        <DocumentSummarySet status="OK">
            <DbBuild>Build191210-0555.1</DbBuild>
            <DocumentSummary uid="5025191">
                <RsUid>14769648</RsUid>
                <GbUid>14768768</GbUid>
                <AssemblyAccession>GCF_009295945.1</AssemblyAccession>
                <LastMajorReleaseAccession>GCF_009295945.1</LastMajorReleaseAccession>
                <LatestAccession/>
                <ChainId>9295945</ChainId>
                <AssemblyName>ASM929594v1</AssemblyName>
                <UCSCName/>
                <EnsemblName/>
                <Taxid>632</Taxid>
                <Organism>Yersinia pestis (enterobacteria)</Organism>
                <SpeciesTaxid>632</SpeciesTaxid>
                <SpeciesName>Yersinia pestis</SpeciesName>
                <AssemblyType>haploid</AssemblyType>
                <AssemblyClass>haploid</AssemblyClass>
                <AssemblyStatus>Complete Genome</AssemblyStatus>
                <WGS/>
                <GB_BioProjects>
                    <Bioproj>
                        <BioprojectAccn>PRJNA269675</BioprojectAccn>
                        <BioprojectId>269675</BioprojectId>
                    </Bioproj>
                </GB_BioProjects>
                <GB_Projects>
                </GB_Projects>
                <RS_BioProjects>
                    <Bioproj>
                        <BioprojectAccn>PRJNA224116</BioprojectAccn>
                        <BioprojectId>224116</BioprojectId>
                    </Bioproj>
                </RS_BioProjects>
                <RS_Projects>
                </RS_Projects>
                <BioSampleAccn>SAMN12991206</BioSampleAccn>
                <BioSampleId>12991206</BioSampleId>
                <Biosource>
                    <InfraspeciesList>
                        <Infraspecie>
                            <Sub_type>strain</Sub_type>
                            <Sub_value>SCPM-O-DNA-18 (I-3113)</Sub_value>
                        </Infraspecie>
                    </InfraspeciesList>
                    <Sex/>
                    <Isolate/>
                </Biosource>
                <Coverage>176.1</Coverage>
                <PartialGenomeRepresentation>false</PartialGenomeRepresentation>
                <Primary>14769638</Primary>
                <AssemblyDescription/>
                <ReleaseLevel>Major</ReleaseLevel>
                <ReleaseType>Major</ReleaseType>
                <AsmReleaseDate_GenBank>2019/10/24 00:00</AsmReleaseDate_GenBank>
                <AsmReleaseDate_RefSeq>2019/10/25 00:00</AsmReleaseDate_RefSeq>
                <SeqReleaseDate>2019/10/24 00:00</SeqReleaseDate>
                <AsmUpdateDate>2019/10/25 00:00</AsmUpdateDate>
                <SubmissionDate>2019/10/24 00:00</SubmissionDate>
                <LastUpdateDate>2019/10/25 00:00</LastUpdateDate>
                <SubmitterOrganization>SRCAMB</SubmitterOrganization>
                <RefSeq_category>na</RefSeq_category>
                <AnomalousList>
                </AnomalousList>
                <ExclFromRefSeq>
                </ExclFromRefSeq>
                <PropertyList>
                    <string>full-genome-representation</string>
                    <string>genbank_has_annotation</string>
                    <string>has-chromosome</string>
                    <string>has-plasmid</string>
                    <string>has_annotation</string>
                    <string>latest</string>
                    <string>latest_genbank</string>
                    <string>latest_refseq</string>
                    <string>refseq_has_annotation</string>
                </PropertyList>
                <FromType/>
                <Synonym>
                    <Genbank>GCA_009295945.1</Genbank>
                    <RefSeq>GCF_009295945.1</RefSeq>
                    <Similarity>identical</Similarity>
                </Synonym>
                <ContigN50>4546217</ContigN50>
                <ScaffoldN50>4546217</ScaffoldN50>
                <FtpPath_GenBank>ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/009/295/945/GCA_009295945.1_ASM929594v1</FtpPath_GenBank>
                <FtpPath_RefSeq>ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1</FtpPath_RefSeq>
                <FtpPath_Assembly_rpt>ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1/GCF_009295945.1_ASM929594v1_assembly_report.txt</FtpPath_Assembly_rpt>
                <FtpPath_Stats_rpt>ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1/GCF_009295945.1_ASM929594v1_assembly_stats.txt</FtpPath_Stats_rpt>
                <FtpPath_Regions_rpt/>
                <SortOrder>5C1X9954537820092959459898</SortOrder>
                <Meta>
                    <![CDATA[
                        <Stats>
                            <Stat category="alt_loci_count" sequence_tag="all">0</Stat>
                            <Stat category="chromosome_count" sequence_tag="all">1</Stat>
                            <Stat category="contig_count" sequence_tag="all">5</Stat>
                            <Stat category="contig_l50" sequence_tag="all">1</Stat>
                            <Stat category="contig_n50" sequence_tag="all">4546217</Stat>
                            <Stat category="non_chromosome_replicon_count" sequence_tag="all">4</Stat>
                            <Stat category="replicon_count" sequence_tag="all">5</Stat>
                            <Stat category="scaffold_count" sequence_tag="all">5</Stat>
                            <Stat category="scaffold_count" sequence_tag="placed">5</Stat>
                            <Stat category="scaffold_count" sequence_tag="unlocalized">0</Stat>
                            <Stat category="scaffold_count" sequence_tag="unplaced">0</Stat>
                            <Stat category="scaffold_l50" sequence_tag="all">1</Stat>
                            <Stat category="scaffold_n50" sequence_tag="all">4546217</Stat>
                            <Stat category="total_length" sequence_tag="all">4759144</Stat>
                            <Stat category="ungapped_length" sequence_tag="all">4759144</Stat>
                        </Stats>
                        <FtpSites>
                            <FtpPath type=Assembly_rpt>ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1/GCF_009295945.1_ASM929594v1_assembly_report.txt</FtpPath>
                            <FtpPath type=GenBank>ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/009/295/945/GCA_009295945.1_ASM929594v1</FtpPath>
                            <FtpPath type=RefSeq>ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1</FtpPath>
                            <FtpPath type=Stats_rpt>ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1/GCF_009295945.1_ASM929594v1_assembly_stats.txt</FtpPath>
                        </FtpSites>
                        <assembly-level>5</assembly-level>
                        <assembly-status>Complete Genome</assembly-status>
                        <representative-status>na</representative-status>
                        <submitter-organization>SRCAMB</submitter-organization>
                    ]]>
                </Meta>
            </DocumentSummary>
        </DocumentSummarySet>
    </eSummaryResult>"""

    return assembly_xml_str
