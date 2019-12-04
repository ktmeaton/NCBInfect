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

    metadata = ['1', '5025191', 'GCF_009295945.1', 'SAMN12991206', '12991206', 'PRJNA224116',
                '14768768', 'PRJNA224116', 'na', '14769648', '', 'SCPM-O-DNA-18 (I-3113)', 'None',
                'Yersinia pestis (enterobacteria)', '632', 'Yersinia pestis', '632', 'ASM929594v1',
                'Complete Genome', 'haploid', '176.1', '1', '5', '4546217', '1', '4',
                '5', '0', '4546217', '1', '4759144', '4759144', 'SRCAMB', '2019/10/24 00:00', '2019/10/24 00:00',
                'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1/GCF_009295945.1_ASM929594v1_assembly_report.txt',
                'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/009/295/945/GCA_009295945.1_ASM929594v1',
                'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1',
                'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/295/945/GCF_009295945.1_ASM929594v1/GCF_009295945.1_ASM929594v1_assembly_stats.txt',
                'None']

    assembly_dict = {}
    # Populate the dict with data
    for i in range(0,len(columns)):
        key = columns[i]
        value = metadata[i]
        assembly_dict[key] = value

    return assembly_dict

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

    bioproject_dict = {}
    # Populate the dict with data
    for i in range(0,len(columns)):
        key = columns[i]
        value = metadata[i]
        bioproject_dict[key] = value

    return bioproject_dict
