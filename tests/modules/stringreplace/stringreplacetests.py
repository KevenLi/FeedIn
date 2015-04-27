# -*- coding: utf-8 -*-
'''
Created on 2014��11��28��

@author: ���
'''
import unittest
from feedin.modules import StringReplaceBuilder
from feedin.model import Context

class StringReplaceTest(unittest.TestCase):


    def test_execute_string(self):
        module_setting = {
                          'id' : 'stringreplace',
                          'type' : 'stringreplace',
                          'conf' : {}
                          }
        module_setting['conf']['Replace'] = 'abc'
        module_setting['conf']['With'] = "123"
        
        builder = StringReplaceBuilder()
        self.target = builder.build(module_setting)
        context = Context()
        context.items.append('abcddd')
        self.target.execute(context);
        self.assertEqual(context.items[0], '123ddd')
        
    def test_execute_string_multi(self):
        module_setting = {
                  'id' : 'stringreplace',
                  'type' : 'stringreplace',
                  'conf' : {}
                  }
        module_setting['conf']['Replace'] = 'abc'
        module_setting['conf']['With'] = "123"
        
        builder = StringReplaceBuilder()
        self.target = builder.build(module_setting)
        context = Context()
        context.items.append('abcddd')
        context.items.append("abc")
        context.items.append('ddd')
        self.target.execute(context);
        self.assertEqual(context.items[0], '123ddd')
        self.assertEqual(context.items[1], '123')
        self.assertEqual(context.items[2], 'ddd')
    
    def test_execute_dotdict2(self):
        module_setting = {
              'id' : 'stringreplace',
              'type' : 'stringreplace',
              'conf' : {}
          }
        module_setting['conf']['Replace'] = 'abc'
        module_setting['conf']['With'] = "123"
        
        builder = StringReplaceBuilder()
        self.target = builder.build(module_setting)
        context = Context()
        context.items.append('abcddd')
        self.target.execute(context);
        self.assertEqual(context.items[0], '123ddd')
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_execute']
    unittest.main()