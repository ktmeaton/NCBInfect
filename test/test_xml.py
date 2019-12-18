import pytest                               # Testing suite
from ncbimeta import NCBImetaUtilities      # Utility Functions
from lxml import etree                      # XML Parsing

def test_lxml(assembly_xml):
    '''Test the functionality of the lxml module'''
    column_name =  'AssemblyAccession'
    column_payload =  ['AssemblyAccession']
    column_value = ""
    root = etree.fromstring(assembly_xml, )
    tag_xpath = './/' + "Meta"
    # Step 1 going to iterate through column_payload values
    working_root = root
    column_dict = {}
    # Iterate over each path element in the column_payload list
    for i in range(0,len(column_payload)):
        # Construct an xpath recursive search query
        tag_xpath = ".//" + column_payload[i]
        # recursively search for the tag
        working_root = working_root.findall(tag_xpath)

    print(working_root)
    print(working_root[0].text)
    column_value = working_root[0].text
    column_dict[column_name] = column_value
    print(column_dict)


    #print("Findall: ", root.findall(tag_xpath))  # XPath, recursive.
    #print("Iterfind: ", root.iterfind(tag_xpath))
    #print("Findtext: ", root.findtext(tag_xpath).strip())
    #print(assembly_xml)
    assert 0

#iterfind() iterates over all Elements that match the path expression
#findall() returns a list of matching Elements
#find() efficiently returns only the first match
#findtext() returns the .text content of the first match
