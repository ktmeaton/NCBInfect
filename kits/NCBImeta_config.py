OUTPUT_DIR = "."
EMAIL = "ktmeaton@gmail.com"
DATABASE = "yersinia_pestis_db.sqlite"
TABLES = ["Assembly","BioSample"]
SEARCH_TERMS = {"Assembly": "Yersinia pestis[Orgn]",
                "BioSample": "Yersinia pestis[Orgn]"}

TABLE_COLUMNS = {"Assembly": ["AssemblyAccession",
                              "Organism",
                              "AssemblyStatus",
                              "SubmitterOrganization",
                              "Taxid",
                              "BioSampleAccn",
                              "Coverage",
                              "SubmissionDate",
                              "SeqReleaseDate",
                              "WGS",
                              ["GB_BioProjects","BioprojectAccn"],
                              "chromosome_count",
                              "contig_count",
                              ["InfraspeciesList","Biosource","Sub_value"]],
                 "BioSample": ["Accession"]}
