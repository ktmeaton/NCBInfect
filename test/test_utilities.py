"""
NCBImeta Test - Utility Functions

@author: Katherine Eaton
"""

#-----------------------------------------------------------------------#
#                         Modules and Packages                          #
#-----------------------------------------------------------------------#

import pytest                               # Testing suite
from ncbimeta import NCBImetaUtilities      # Utility Functions
from ncbimeta import NCBImetaErrors     # NCBImeta Error classes
import os                                   # Filepath and directory operations
import sqlite3                              # Database storage and queries
from lxml import etree                      # XML Parsing
from Bio import Entrez                      # Entrez queries (NCBI)
#-----------------------------------------------------------------------#
#                           Test Function                               #
#-----------------------------------------------------------------------#

def test_check_accessory_dir(tmpdir):
    '''Test the utility function check_accessory_dir (create log/ and database/).'''
    tmpdir = tmpdir.strpath
    NCBImetaUtilities.check_accessory_dir(tmpdir)
    assert os.path.exists(os.path.join(tmpdir,"log")) and os.path.exists(os.path.join(tmpdir,"database"))

def test_table_exists(tmpdir):
    '''Test the utility function table_exists (check if Table is present in sqlite db)'''
    # Connect to database and establish cursor for commands.
    tmpdir = tmpdir.strpath
    test_db = os.path.join(tmpdir, "test.sqlite")
    conn = sqlite3.connect(test_db)
    cur = conn.cursor()

    ## Create the database with a test Table
    table_name = "TestTable"
    sql_query = "Create TABLE IF NOT EXISTS " + table_name + " (id INTEGER)"
    cur.execute(sql_query)

    # Test Function Call
    assert NCBImetaUtilities.table_exists(cur, table_name)

def test_xml_search_nodetext():
    '''Test the utility function xml_search (retrieve xml text node)'''
    test_xml = "<Root><Assembly><AssemblyAccession>GCA_003086155.1</AssemblyAccession></Assembly></Root>"
    test_root = etree.fromstring(test_xml)
    test_search_list = ['Assembly','AssemblyAccession']
    test_current_tag = test_search_list[0]
    test_column_name = 'AssemblyAccession'
    test_xml_dict = {}
    test_xml_dict[test_column_name] = []
    expect_xml_dict = {test_column_name : ['GCA_003086155.1'] }
    NCBImetaUtilities.xml_search(test_root, test_search_list, test_current_tag , test_column_name, test_xml_dict)
    #assert 0
    assert test_xml_dict == expect_xml_dict

def test_xml_search_nodeattr():
    '''Test the utility function xml_search (retrieve xml attr text)'''
    test_xml = "<Root><Experiment acc='SRX6977650'/></Root>"
    test_root = etree.fromstring(test_xml)
    test_search_list = ['Experiment', 'acc']
    test_current_tag = test_search_list[0]
    test_column_name = 'ExperimentAccession'
    test_xml_dict = {}
    test_xml_dict[test_column_name] = []
    expect_xml_dict = {test_column_name : ['SRX6977650'] }
    NCBImetaUtilities.xml_search(test_root, test_search_list, test_current_tag , test_column_name, test_xml_dict)

    assert test_xml_dict == expect_xml_dict

def test_xml_search_nodeattrtext():
    '''Test the utility function xml_search (retrieve xml attr text)'''
    #test_xml = "<Root><LIBRARY_LAYOUT><PAIRED/></LIBRARY_LAYOUT></Root>"
    test_xml = "<Root><Stats><Stat category='chromosome_count' sequence_tag='all'>1</Stat></Stats></Root>"
    test_root = etree.fromstring(test_xml)
    test_search_list = ['Stat', 'category', 'chromosome_count']
    test_current_tag = test_search_list[0]
    test_column_name = 'ChromosomeCount'
    test_xml_dict = {}
    test_xml_dict[test_column_name] = []
    expect_xml_dict = {test_column_name : ['1'] }
    NCBImetaUtilities.xml_search(test_root, test_search_list, test_current_tag , test_column_name, test_xml_dict)
    assert test_xml_dict == expect_xml_dict

def test_xml_search_nodechildnode():
    '''Test the utility function xml_search (retrieve xml attr text)'''
    test_xml = "<Root><LIBRARY_LAYOUT><PAIRED/></LIBRARY_LAYOUT></Root>"
    test_root = etree.fromstring(test_xml)
    test_search_list = ['LIBRARY_LAYOUT']
    test_current_tag = test_search_list[0]
    test_column_name = 'LibraryLayout'
    test_xml_dict = {}
    test_xml_dict[test_column_name] = []
    expect_xml_dict = {test_column_name : ['PAIRED'] }
    NCBImetaUtilities.xml_search(test_root, test_search_list, test_current_tag , test_column_name, test_xml_dict)
    assert test_xml_dict == expect_xml_dict

def test_HTTPErrorCatch(tmpdir):
    '''Test the utility function HTTPErrorCatch (catch HTTP Errors)'''
    # Test query assembly
    test_ID = '5025191'
    test_email = 'ktmeaton@gmail.com'
    Entrez.email = test_email
    test_table = 'Assembly'
    test_max_tries = 10
    test_total_tries = 10
    test_sleep_between_tries = 0
    test_kwargs = {"db":test_table.lower(), "id":test_ID}
    test_entrez_method = Entrez.esummary

    for i in range(1, test_total_tries):
        ID_handle = NCBImetaUtilities.HTTPErrorCatch(test_entrez_method, test_max_tries, test_sleep_between_tries, **test_kwargs)
    try:
        ID_record = Entrez.read(ID_handle, validate=False)
        assert 1
    except RuntimeError:
        # The ID_handle was not succesfully retrieved or the data is not correct
        assert 0

def test_sql_sanitize():
    '''Test the utility function sql_sanitize (remove problematic characters)'''
    test_name = "); drop tables --"
    test_target_name = "droptables"
    test_sanitize_name = NCBImetaUtilities.sql_sanitize(test_name)
    assert test_target_name == test_sanitize_name

def test_adv_xml_search_abs():
    '''Test the utility function adv_xml_search, navigating from root of document (use XPath query, PR #9)'''
    test_xml = '''
    <GBSeq_feature-table>
        <GBFeature>
            <GBFeature_key>source</GBFeature_key>
            <GBFeature_quals>
                <GBQualifier>
                    <GBQualifier_name>organism</GBQualifier_name>
                    <GBQualifier_value>my_name</GBQualifier_value>
                </GBQualifier>
            </GBFeature_quals>
        </GBFeature>
        <GBFeature>
            <GBFeature_key>gene</GBFeature_key>
            <GBFeature_quals>
                <GBQualifier>
                    <GBQualifier_name>gene</GBQualifier_name>
                    <GBQualifier_value>my_gene_here</GBQualifier_value>
                </GBQualifier>
            </GBFeature_quals>
        </GBFeature>
    </GBSeq_feature-table>
    '''
    test_xml_root = etree.fromstring(test_xml)
    test_payload = "XPATH, //GBSeq_feature-table/GBFeature[GBFeature_key/text() = 'source']/GBFeature_quals/GBQualifier[GBQualifier_name/text() = 'organism']/GBQualifier_value"
    test_xpath = test_payload.split(", ")[1]
    test_column_name = 'GBOrganismName'
    test_xml_dict = {test_column_name : [] }
    expect_xml_dict = {test_column_name : ['my_name'] }
    NCBImetaUtilities.adv_xml_search(test_xml_root, test_xpath, test_column_name, test_xml_dict)
    assert test_xml_dict == expect_xml_dict

def test_adv_xml_search_rel():
    '''Test the utility function adv_xml_search, navigating from tip of document (use XPath query, PR #9)'''
    test_xml ='''
    <GBSeq_feature-table>
        <GBFeature>
            <GBFeature_key>source</GBFeature_key>
            <GBFeature_quals>
                <GBQualifier>
                    <GBQualifier_name>organism</GBQualifier_name>
                    <GBQualifier_value>my_name</GBQualifier_value>
                </GBQualifier>
            </GBFeature_quals>
        </GBFeature>
        <GBFeature>
            <GBFeature_key>gene</GBFeature_key>
            <GBFeature_quals>
                <GBQualifier>
                    <GBQualifier_name>gene</GBQualifier_name>
                    <GBQualifier_value>my_gene_here</GBQualifier_value>
                </GBQualifier>
            </GBFeature_quals>
        </GBFeature>
    </GBSeq_feature-table>
    '''
    test_xml_root = etree.fromstring(test_xml)
    test_payload = "XPATH, //GBQualifier[GBQualifier_name/text() = 'organism']/GBQualifier_value"
    test_xpath = test_payload.split(", ")[1]
    test_column_name = 'GBOrganismName'
    test_xml_dict = {test_column_name : [] }
    expect_xml_dict = {test_column_name : ['my_name'] }
    NCBImetaUtilities.adv_xml_search(test_xml_root, test_xpath, test_column_name, test_xml_dict)
    assert test_xml_dict == expect_xml_dict

def test_adv_xml_search_attr():
    '''Test the utility function adv_xml_search, label conditional (use XPath query, PR #9)'''
    test_xml ='''
    <Links>
      <Link type="url" label="GEO Sample GSM3995467">https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM3995467</Link>
      <Link type="entrez" target="bioproject" label="PRJNA558013">558013</Link>
    </Links>
    '''
    test_xml_root = etree.fromstring(test_xml)
    test_payload = "XPATH, //Links/Link[@target='bioproject']/@label"
    test_xpath = test_payload.split(", ")[1]
    test_column_name = 'BioProject'
    test_xml_dict = {test_column_name : [] }
    expect_xml_dict = {test_column_name : ['PRJNA558013'] }
    NCBImetaUtilities.adv_xml_search(test_xml_root, test_xpath, test_column_name, test_xml_dict)
    assert test_xml_dict == expect_xml_dict

def test_adv_xml_search_multigood():
    '''Test the utility function adv_xml_search, multiple good node match (use XPath query, PR #9)'''
    test_xml ='''
    <RUN_SET>
        <RUN alias="E-MTAB-8370:untagged-His-run30_S9_L003" accession="ERR3549715">
            <Statistics nspots="5441517" nreads="1">
                <Read stdev="0" average="49" count="5441517" index="0"/>
            </Statistics>
        </RUN>
        <RUN alias="E-MTAB-8370:untagged-His-run30_S9_L004" accession="ERR3549716">
             <Statistics nspots="5518807" nreads="1">
                 <Read stdev="0" average="49" count="5518807" index="0"/>
             </Statistics>
        </RUN>
    </RUN_SET>
    '''
    test_xml_root = etree.fromstring(test_xml)
    test_payload = "XPATH, //RUN/@accession"
    test_xpath = test_payload.split(", ")[1]
    test_column_name = 'SRARunAccession'
    test_xml_dict = {test_column_name : [] }
    expect_xml_dict = {test_column_name : ['ERR3549715','ERR3549716'] }
    NCBImetaUtilities.adv_xml_search(test_xml_root, test_xpath, test_column_name, test_xml_dict)
    assert test_xml_dict == expect_xml_dict

def test_adv_xml_search_multibad():
    '''Test the utility function adv_xml_search, multiple bad node match (use XPath query, PR #9)'''
    test_xml ='''
    <RUN_SET>
        <RUN alias="E-MTAB-8370:untagged-His-run30_S9_L003" accession="ERR3549715">
            <Statistics nspots="5441517" nreads="1">
                <Read stdev="0" average="49" count="5441517" index="0"/>
            </Statistics>
        </RUN>
        <RUN alias="E-MTAB-8370:untagged-His-run30_S9_L004" accession="ERR3549716">
             <Statistics nspots="5518807" nreads="1">
                 <Read stdev="0" average="49" count="5518807" index="0"/>
             </Statistics>
        </RUN>
    </RUN_SET>
    '''
    test_xml_root = etree.fromstring(test_xml)
    test_payload = "XPATH, //RUN"
    test_xpath = test_payload.split(", ")[1]
    test_column_name = 'SRARun'
    test_xml_dict = {test_column_name : [] }
    with pytest.raises(NCBImetaErrors.ErrorXPathQueryMultiElement) as err_info:
        NCBImetaUtilities.adv_xml_search(test_xml_root, test_xpath, test_column_name, test_xml_dict)
