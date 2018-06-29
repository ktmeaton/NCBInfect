OUTPUT_DIR = "../NCBImeta_ouput/"
EMAIL = "ktmeaton@gmail.com"
DATABASE = "yersinia_pestis_db.sqlite"
TABLES = ["BioProject"]
SEARCH_TERMS = {"BioProject": "Yersinia pestis[Orgn]"}

TABLE_COLUMNS = {"BioProject": [
                    {"BioProjectAccession" : "Project_Acc"},
                    {"TargetScope" : "Project_Target_Scope"},
                    {"TargetCapture" : "Project_Target_Capture"},
                    {"TargetMaterial" : "Project_Target_Material"},
                    {"Description" : "Project_Description"},
                    {"MethodType" : "Project_MethodType"},
                    {"Name" : "Project_Name"},
                    {"Title" : "Project_Title"},
                    {"OrganismLabel" : "Organism_Label"},
                    {"OrganismStrain" : "Organism_Strain"},
                    {"Type" : "Project_Type"},
                    {"DataType" : "Project_Data_Type"},
                    {"Supergroup" : "Supergroup"},
                    {"TaxonomicID" : "TaxId"},
                    {"RegistrationDate" : "Registration_Date"},
                    {"SequencingStatus" : "Sequencing_Status"},
                    {"RelevanceMedical" : "Relevance_Medical"},
                    {"SubmitterOrganization" : "Submitter_Organization"}
                    ]}
