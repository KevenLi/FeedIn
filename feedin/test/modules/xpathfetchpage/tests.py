# -*- coding: utf-8 -*-
'''
Created on 2014��11��12��

@author: ���
'''
import unittest
from feeding.modules.module import XPathFetchPage
from xml.etree import ElementTree
from feeding.model import Context

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_xpath(self):
        doc = ElementTree.Element("module")
        doc.attrib['type'] = 'xpathfetchpage'
        doc.attrib['URL'] = 'http://guba.eastmoney.com/default_1.html'
        doc.attrib['ExtractXPath'] = "//ul[@class='newlist']/li"
        
        self.target = XPathFetchPage(doc)
        context = Context()
        self.target.execute(context);
        print len(context.items)
        self.assertTrue(len(context.items) > 0, "Cannot retrieve elements in page")
        print context
    
    def test_localfile_table(self):
        module_setting = ElementTree.Element("module")
        module_setting.attrib['type'] = 'xpathfetchpage'
        module_setting.attrib['URL'] = 'test.html'
        module_setting.attrib['ExtractXPath'] = "//div[@id='content']/table[@class='table1']/tr"
        self.target= XPathFetchPage(module_setting)
        context = Context()
        self.target.execute(context);
        self.assertEqual(len(context.items), 3)
        self.assertEqual(context.items[1]['td.0.a.content'], 'Example to feedin')
    

    def test_mixtext_with_br(self):
        module_setting = ElementTree.Element("module")
        module_setting.attrib['type'] = 'xpathfetchpage'
        module_setting.attrib['URL'] = 'test_mixtext_with_br.html'
        module_setting.attrib['ExtractXPath'] = "//div"
        self.target= XPathFetchPage(module_setting)
        context = Context()
        self.target.execute(context);
        self.assertEqual(len(context.items), 1)
        self.assertEqual(context.items[0]['content'], '\r\nabc\r\ndef\r\nggg\r\n')
    
    def test_proxy(self):
        proxy = 'localhost:8080'
        doc = ElementTree.Element("module")
        doc.attrib['type'] = 'xpathfetchpage'
        doc.attrib['URL'] = 'http://guba.eastmoney.com/default_1.html'
        doc.attrib['ExtractXPath'] = "//ul[@class='newlist']/li"
        
        self.target = XPathFetchPage(doc)
        context = Context(http_proxy = proxy)
        self.target.execute(context);
        print len(context.items)
        self.assertTrue(len(context.items) > 0, "Cannot retrieve elements in page")
        print context.items

if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.test_proxy']
    unittest.main()