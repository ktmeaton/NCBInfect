OUTPUT_DIR = "."
EMAIL = "ktmeaton@gmail.com"
DATABASE = "yersinia_pestis_db.sqlite"
TABLES = ["Assembly"]
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
							  "BioprojectAccn",
							  "chromosome_count"],
				 "BioSample": ["accession"]}
