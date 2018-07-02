OUTPUT_DIR = "..\\NCBImeta_output"
EMAIL = "myemailname@domain.com"
DATABASE = "my_organism_db.sqlite"
TABLES = ["Assembly","BioSample"]
SEARCH_TERMS = {"Assembly": "Yersinia pestis[Orgn]",
                "BioSample": "Yersinia pestis[Orgn] AND biosample assembly[Filter]"}

TABLE_COLUMNS = {
   "Assembly" : [
                {"AssemblyAccession" : "AssemblyAccession"},
                {"BioSampleAccession" : 'BioSampleAccn'},
                {"Organism" : 'Organism'}
                ],
  "BioSample" : [
                {"Accession": "Accession"},
                {"BioProject": ["Link","label"]},
                {"SRAAccession": ["Id","SRA","db"]},
                {"BioSampleTitle": "Title"}
                ]
                }
