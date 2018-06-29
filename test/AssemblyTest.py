OUTPUT_DIR = "../NCBImeta_ouput/"
EMAIL = "ktmeaton@gmail.com"
DATABASE = "yersinia_pestis_db.sqlite"
TABLES = ["Assembly"]
SEARCH_TERMS = {"Assembly": "Yersinia pestis[Orgn]"}

TABLE_COLUMNS = {"Assembly": [
                            {"AssemblyAccession" : "AssemblyAccession"},
                            {"AssemblyName" : "AssemblyName"},
                            {"Organism" : 'Organism'},
                            {"AssemblyStatus" : 'AssemblyStatus'},
                            {"AssemblyType" : 'AssemblyType'},
                            {"SubmitterOrganization" : 'SubmitterOrganization'},
                            {"TaxonomicID" : 'Taxid'},
                            {"SpeciesTaxonomicID" : 'SpeciesTaxid'},
                            {"SpeciesName" : 'SpeciesName'},
                            {"BioSampleAccession" : 'BioSampleAccn'},
                            {"BioSampleID" : 'BioSampleId'},
                            {"AssemblyCoverage" : 'Coverage'},
                            {"SubmissionDate" : 'SubmissionDate'},
                            {"ReleaseDate" : 'SeqReleaseDate'},
                            {"WGSAccession" : 'WGS'},
                            {"Chromosomes" : ["Stat", "chromosome_count", "category"]},
                            {"Replicons" : ["Stat", "replicon_count", "category"]},
                            {"NonChromosomalReplicons" : ["Stat", "non_chromosome_replicon_count", "category"]},
                            {"ContigCount": ["Stat", "contig_count", "category"]},
                            {"ContigN50" : ["Stat", "contig_n50", "category"]},
                            {"ContigL50" : ["Stat", "contig_l50", "category"]},
                            {"Scaffolds" : ["Stat", "scaffold_count", "category"]},
                            {"ScaffoldN50" : ["Stat", "scaffold_n50", "category"]},
                            {"ScaffoldL50" : ["Stat", "scaffold_l50", "category"]},
                            {"TotalLength" : ["Stat", "total_length", "category"]},
                            {"UngappedLength" : ["Stat", "ungapped_length", "category"]},
                            {"RefSeqID" : 'RsUid'},
                            {"GenbankID" : 'GbUid'},
                            {"RefSeqCategory" : 'RefSeq_category'},
                            {"FTPGenbank" : 'FtpPath_GenBank'},
                            {"FTPRefSeq" : 'FtpPath_RefSeq'},
                            {"FTPAssemblyReport" : 'FtpPath_Assembly_rpt'},
                            {"FTPStatsReport" : 'FtpPath_Stats_rpt'},
                            {"GenbankBioprojectAccession" : ["GB_BioProjects","BioprojectAccn"]},
                            {"RefseqBioprojectAccession" : ["RS_BioProjects","BioprojectAccn"]},
                            {"Infraspecies" : ["InfraspeciesList","Biosource","Sub_value"]}
                        ]}
