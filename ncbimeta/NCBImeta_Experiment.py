from Bio import Entrez
from ncbimeta import NCBImetaUtilities
import xml.etree.ElementTree as ET

# Basic
Entrez.email = "ktmeaton@gmail.com"
handle = Entrez.efetch(db="bioproject", id="269675", rettype="xml", retmode="xml")
#handle = Entrez.esummary(db="biosample",id = "12991206")
#handle = Entrez.esummary(db="assembly", id = "5025191")
handle_xml = handle.read()
print(handle_xml)
