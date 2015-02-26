# -*- coding: utf-8 -*-
'''
Created on 2014��11��28��

@author: ���
'''
import unittest
from feeding.modules.module import StringReplace
from xml.etree import ElementTree
from feeding.model import Context

class StringReplaceTest(unittest.TestCase):


    def test_execute_string(self):
        doc = ElementTree.Element("module")
        doc.attrib['type'] = 'stringreplace'
        doc.attrib['Replace'] = 'abc'
        doc.attrib['With'] = "123"
        
        self.target = StringReplace(doc)
        context = Context()
        context.items.append('abcddd')
        self.target.execute(context);
        self.assertEqual(context.items[0], '123ddd')
        
    def test_execute_string_multi(self):
        doc = ElementTree.Element("module")
        doc.attrib['type'] = 'stringreplace'
        doc.attrib['Replace'] = 'abc'
        doc.attrib['With'] = "123"
        
        self.target = StringReplace(doc)
        context = Context()
        context.items.append('abcddd')
        context.items.append("abc")
        context.items.append('ddd')
        self.target.execute(context);
        self.assertEqual(context.items[0], '123ddd')
        self.assertEqual(context.items[1], '123')
        self.assertEqual(context.items[2], 'ddd')
    
    def test_execute_dotdict2(self):
        doc = ElementTree.Element("module")
        doc.attrib['type'] = 'stringreplace'
        doc.attrib['Replace'] = 'abc'
        doc.attrib['With'] = "123"
        
        self.target = StringReplace(doc)
        context = Context()
        context.items.append('abcddd')
        self.target.execute(context);
        self.assertEqual(context.items[0], '123ddd')
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_execute']
    unittest.main()