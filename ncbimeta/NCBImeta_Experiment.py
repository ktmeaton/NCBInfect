from Bio import Entrez
from xml.dom import minidom             # XML Processing
from ncbimeta import NCBImetaUtilities
import xml.etree.ElementTree as ET

# Basic
Entrez.email = "ktmeaton@gmail.com"
#handle = Entrez.esummary(db="biosample",id = "12991206")
handle = Entrez.esummary(db="assembly", id = "5025191")
handle_xml = handle.read()

# Minidom
#mini_root = minidom.parseString(handle_xml).documentElement
#working_root = mini_root
#print(mini_root.toprettyxml())
#tag_list = ["GB_BioProjects", "BioprojectAccn"]
#target_node_name = tag_list[-1]
#for tag_name in tag_list:
#    working_root = working_root.getElementsByTagName(tag_name)[0]

#print(working_root.toprettyxml())

#x = mini_root.getElementsByTagName('GB_BioProjects')
#y = x[0].getElementsByTagName("BioprojectAccn")
#print(y[0].firstChild.nodeValue)
#firstChild.nodeName = #text
#print(x.nodeName)
#print(x.nodeValue)
#print(x.childNodes)
#NCBImetaUtilities.xml_find_node(mini_root, 'BioprojectAccn', test_dict)

# ElementTree
#root = ET.fromstring(handle_xml)



#for subelement in element.GetElementsByTagName("field"):
#    if subelement.hasAttribute("frame.len"):
#        do_something()

#AssemblyGenbankBioprojectAccession : GB_BioProjects, BioprojectAccn
#["GB_BioProjects", "BioprojectAccn"]
#<eSummaryResult><DocumentSummarySet><DocumentSummary><GB_BioProjects><Bioproj><BioprojectAccn>PRJNA269675</BioprojectAccn>
