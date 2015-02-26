# -*- coding: utf-8 -*-
'''
Created on 2014��11��21��

@author: ���
'''
import unittest
from lxml.etree import Element
from feeding import util


class Test(unittest.TestCase):

    def test_etree_to_dict(self):
        root = Element('div')
        root.append(Element('a', {'href': 'http://aaa.bbb/'}))
        result = util.etree_to_dict2(root)
        self.assertEqual(result['a']['href'], "http://aaa.bbb/")
        

    def test_etree_to_dict2(self):
        root = Element('div')
        root.append(Element('a', {'href': 'http://aaa.bbb/'}))
        root.append(Element('a', {'href': 'http://ccc.ddd/'}))
        result = util.etree_to_dict2(root)
        self.assertEqual(result['a']['0']['href'], "http://aaa.bbb/")
        self.assertEqual(result['a']['1']['href'], "http://ccc.ddd/")
        
    def test_etree_to_dict3(self):
        root = Element('div')
        cite1 = Element('cite')
        cite1.text = "123"
        root.append(cite1)
        result = util.etree_to_dict2(root)
        self.assertEqual(result['cite'], "123")
        
    def test_etree_to_dict4(self):
        root = Element('div')
        cite1 = Element('cite')
        cite1.text = "123"
        root.append(cite1)
        cite2 = Element('cite')
        cite2.text = "456"
        root.append(cite2)
        
        cite3 = Element('cite', {'class': 'author'})
        cite3.text = 'cite3'
        root.append(cite3)
        result = util.etree_to_dict2(root)
        self.assertEqual(result['cite']['0'], "123")
        self.assertEqual(result['cite']['1'], '456')
        self.assertEqual(result['cite']['2']['content'], 'cite3')
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_etree_to_dict4']
    unittest.main()