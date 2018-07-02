# Metadata Selection from NCBI Schema

The schema files are designed to act as a text 'menu' for users to select desired metadata to retrieve. Lines from the schema can be copy and pasted into the configuration file, into the dictionary of their respective table.    

The schema is of the following format:    

    {"AssemblyAccession" : "AssemblyAccession"}    

This is a python dictionary (associative array, hash, etc.) with the left side of the colon as the key, and the right side as the value.    

The left side (key) will be the name of the column in the final table and can be changed to whatever the user desires. However, please avoid putting spaces in your column names.    

The right side is a keyword specific to the biopython API and should not be altered. It's format takes several options.    

## 1) Retrieving a simple node value with biopython from the metadata xml.

User selects:

    {"AssemblyAccession" : "AssemblyAccession"}

XML from NCBI:

    <AssemblyAccession> GCA_003086155.1 </AssemblyAccession>

Retrieves Accession Number "GCA_003086155.1" and stores it under column "AssemblyAccession".    


## 2) Retrieving an attribute value (not a node value)

User selects:
    
    {"ExperimentAccession" : ["Experiment", "acc"]}

XML from NCBI:    

    <EXPERIMENT alias="EXT00317997" accession="SRX4321294">

Retrieves accession "SRX4321294" and stores it under "ExperimentAccession"    
The value in this case, is a list of 2 elements:    

    ["Experiment", "acc"]
    
The first value ("Experiment"), is the name of the node.
The second value ("acc") is the attribute value to target.    

** Note that the attribute value name does not match the attribute name
provided by NCBI. The biopython API occasionally renames attributes.

## 3) Retrieving a simple node value by specifying an associated attribute.

User selects:

    {"CollectionDate": ["Attribute","collection_date","attribute_name"]}

XML from NCBI:
    
    <Attribute display_name="collection date" harmonized_name="collection_date" attribute_name="collection date"> 2006 </Attribute>
    <Attribute display_name="host taxonomy ID" harmonized_name="host_taxid" attribute_name="host taxid"> 10090 </Attribute>

Retrieves collection date 2006 and stores it under "CollectionDate".     
The value in this case, is a list of 3 elements:    

    ["Attribute","collection_date","attribute_name"]    
    
The first value ("Attribute"), is the name of the node.    
The second value ("collection date") is the attribute value to target.    
The third value ("attribute name") is the attribute type to target.    

## 4) Retrieving a simple node value that does not have a unique name or unique attributes.

User selects:    

    {"GenbankBioprojectAccession" : ["GB_BioProjects","BioprojectAccn"]}

XML from NCBI:    
In the following example, note how the node "BioprojectAccn" is not a unique name, as there is both a GenBank and RefSeq Bioproject Accession.    

    <GB_BioProjects>
      <Bioproj>
        <BioprojectAccn>PRJNA31257</BioprojectAccn>
        <BioprojectId>31257</BioprojectId>
      </Bioproj>
    </GB_BioProjects>

   
    <RS_BioProjects>
      <Bioproj>
        <BioprojectAccn>PRJNA168</BioprojectAccn>
        <BioprojectId>168</BioprojectId>
    </Bioproj>
    </RS_BioProjects>

Retrieves accession number "PRJNA31257" and stores it under "GenbankBioprojectAccession".    
The value in this case, is a list of 2 elements:    

    ["GB_BioProjects","BioprojectAccn"]

This can be built from any number of elements, and provides a directional path to follow to find a node.    
Note that it must be IN ORDER, but can skip intermediate values (ex. node <Bioproj> is missing from the list). This has not been extensively tested yet.    
