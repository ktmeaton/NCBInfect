OUTPUT_DIR = "../NCBImeta_ouput/"
EMAIL = "ktmeaton@gmail.com"
DATABASE = "yersinia_pestis_db.sqlite"
TABLES = ["Assembly","BioSample"]
SEARCH_TERMS = {"Assembly": "Yersinia pestis[Orgn]",
                "BioSample": "Yersinia pestis[Orgn]"}

TABLE_COLUMNS = {"Assembly": [
                        {"ContigCount": "contig_count"}
                        ],
                "BioSample": [
                        {"Accession": "Accession"},
                        {"BioSampleTitle": "Title"},
                        {"TaxonomyID": "Taxonomy"},
                        {"SRAAccession": "SRA"},
                        {"Infraspecies": "Infraspecies"},
                        {"ModificationDate": "ModificationDate"},
                        {"PublicationDate": "PublicationDate"},
                        {"Package": "Package"},
                        {"Date": "Date"},
                        {"Organization": "Organization"},
                        {"Organism": "Organism"},
                        {"Strain": "strain"},
                        {"CollectionDate": "collection_date"},
                        {"GeographicLocation": "geo_loc_name"},
                        {"SampleType": "sample_type"},
                        {"Host": "host"},
                        {"IsolationSource": "isolation_source"},
                        {"Biovar": "biovar"},
                        {"SubSpecies": "sub_species"},
                        {"IsolateNameAlias": "isolate_name_alias"},
                        {"BioProject": "bioproject"}
                        ]}
