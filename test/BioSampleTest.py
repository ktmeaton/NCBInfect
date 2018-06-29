OUTPUT_DIR = "../NCBImeta_ouput/"
EMAIL = "ktmeaton@gmail.com"
DATABASE = "yersinia_pestis_db.sqlite"
TABLES = ["BioSample"]
SEARCH_TERMS = {"BioSample": "Yersinia pestis[Orgn] AND (biosample assembly[Filter] OR biosample sra[Filter])"}

TABLE_COLUMNS = {
                "BioSample": [
                             {"Accession": "Accession"},
                             {"BioSampleTitle": "Title"},
                             {"TaxonomyID": "Taxonomy"},
                             {"SRAAccession": ["Id","SRA","db"]},
                             {"SampleName": ["Id","Sample name","db_label"]},
                             {"Infraspecies": "Infraspecies"},
                             {"ModificationDate": "ModificationDate"},
                             {"PublicationDate": "PublicationDate"},
                             {"Package": "Package"},
                             {"Date": "Date"},
                             {"Organization": "Organization"},
                             {"Organism": "OrganismName"},
                             {"Strain": ["Attribute","strain","attribute_name"]},
                             {"CollectionDate": ["Attribute","collection_date","attribute_name"]},
                             {"GeographicLocation": ["Attribute","geo_loc_name","attribute_name"]},
                             {"SampleType": ["Attribute","sample_type","attribute_name"]},
                             {"Host": ["Attribute","host","attribute_name"]},
                             {"IsolationSource": ["Attribute","isolation_source","attribute_name"]},
                             {"Biovar": ["Attribute","biovar","attribute_name"]},
                             {"SubSpecies": ["Attribute","sub_species","attribute_name"]},
                             {"IsolateNameAlias": ["Attribute","isolate-name-alias","attribute_name"]},
                             {"LatLon" : ["Attribute", "lat_lon", "attribute_name"]},
                             {"Lat" : ["Attribute", "latitude", "attribute_name"]},
                             {"Lon" : ["Attribute", "longitude", "attribute_name"]},
                             {"HostDisease" : ["Attribute", "host_disease", "attribute_name"]},
                             {"BioProject": ["Link","label"]}
                        ]}
