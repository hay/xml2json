import unittest
import xml2json
import optparse 
import json
import os

xmlstring = ""
options = None

class SimplisticTest(unittest.TestCase):

    def setUp(self):
    	global xmlstring, options
    	filename = os.path.join(os.path.dirname(__file__), 'xml_ns2.xml')
    	xmlstring = open(filename).read()
    	options = optparse.Values({"pretty": False})

    def test_default_namespace_attribute(self):
		strip_ns = 0
		json_string = xml2json.xml2json(xmlstring,options,strip_ns)
		# check string
		self.assertTrue(json_string.find("{http://www.w3.org/TR/html4/}table") != -1)
		self.assertTrue(json_string.find("{http://www.w3.org/TR/html4/}tr") != -1)
		self.assertTrue(json_string.find("@class") != -1)

		# check the simple name is not exist
		json_data = json.loads(json_string)
		self.assertFalse("table" in json_data["root"])  	

    def test_strip_namespace(self):
		strip_ns = 1    	
		json_string = xml2json.xml2json(xmlstring,options,strip_ns)
		json_data = json.loads(json_string)

		# namespace is stripped
		self.assertFalse(json_string.find("{http://www.w3.org/TR/html4/}table") != -1)

		# TODO , attribute shall be kept
		#self.assertTrue(json_string.find("@class") != -1)

		#print json_data["root"]["table"]
		#print json_data["root"]["table"][0]["tr"]
		self.assertTrue("table" in json_data["root"])  			
		self.assertEqual(json_data["root"]["table"][0]["tr"]["td"] , ["Apples", "Bananas"])

if __name__ == '__main__':
    unittest.main()