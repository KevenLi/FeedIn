# -*- coding: utf-8 -*-
'''
Created on 2014��12��3��

@author: ���
'''
import unittest
from feeding.modules.module import Output
from xml.etree import ElementTree
from feeding.model import Context
from feeding.dotdict2 import DotDict2


class Test(unittest.TestCase):
    
    def test_output_default_output(self):
        setting = ElementTree.Element("module")
        setting.attrib['type'] = 'output'
        
        item1 = DotDict2()
        item1['a'] = 'a content'
        item1['b.1'] = 'b content'
        
        context = Context()
        context.items.append(item1)
        
        self.target = Output(setting) 
        self.target.execute(context)
        
        self.assertEqual(context.items[0]['a'], 'a content')
        self.assertEqual(context.items[0]['b'], 'b content')

    def test_output_depth_default(self):
        doc = ElementTree.Element("module")
        doc.attrib['type'] = 'output'
        # attrib['depth'] default to 1, only output the first depth        
                
                
        self.target = Output(doc)
        context = Context()
        item = DotDict2() # dict item
        item['a.1.b'] = 'd'
        
        item2 = DotDict2()
        item2['content'] = 'abcddd' # string item
        context.items.append(item)
        context.items.append(item2)
        self.target.execute(context);
        self.assertEqual(context.items[0]['a'], 'd')
        self.assertEqual(context.items[1]['content'], 'abcddd')
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_output_default_output']
    unittest.main()