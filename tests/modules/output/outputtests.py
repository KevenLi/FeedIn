# -*- coding: utf-8 -*-
'''
Created on 2014��12��3��

@author: ���
'''
import unittest
from feedin.modules import OutputBuilder
from feedin import Context
from feedin import DotDict2


class Test(unittest.TestCase):
    
    def test_output_default_output(self):
        module_setting = {
                          'id' : 'output',
                          'type': 'output',
                          'conf' : {}
                          }
       
        item1 = DotDict2()
        item1['a'] = 'a content'
        item1['b.1'] = 'b content'
        
        context = Context()
        context.items.append(item1)
        
        builder = OutputBuilder()
        self.target = builder.build(module_setting)
        self.target.execute(context)
        
        self.assertEqual(context.items[0]['a'], 'a content')
        self.assertEqual(context.items[0]['b'], 'b content')

    def test_output_depth_default(self):
        module_setting = {
                  'id' : 'output',
                  'type': 'output',
                  'conf' : {}
                  }    
                
        builder = OutputBuilder()
        self.target = builder.build(module_setting)
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