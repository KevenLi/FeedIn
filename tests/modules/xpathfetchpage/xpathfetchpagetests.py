# -*- coding: utf-8 -*-
'''
Created on 2014��11��12��

@author: ���
'''
import unittest
from feedin.modules import XPathFetchPageBuilder
from feedin.model import Context


class XPathFetchPageTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_xpath(self):
        module_setting = {
                  'id':'xpathfetchpage',
                  'type':'xpathfetchpage',
                  'conf':{}
                  }
        module_setting['conf']['URL'] = {'value' :'http://guba.eastmoney.com/default_1.html'}
        module_setting['conf']['xpath'] = {'value' : "//ul[@class='newlist']/li"}
        
        builder = XPathFetchPageBuilder()
        self.target = builder.build(module_setting)
        context = Context()
        self.target.execute(context);
        print len(context.items)
        self.assertTrue(len(context.items) > 0, "Cannot retrieve elements in page")
        print context
    
    def test_localfile_table(self):
        module_setting = {
                          'id':'xpathfetchpage',
                          'type':'xpathfetchpage',
                          'conf':{}
                          }
                
        module_setting['conf']['URL'] = {'value': 'https://raw.githubusercontent.com/kevenli/FeedIn/master/tests/modules/xpathfetchpage/test.html'}
        module_setting['conf']['xpath'] = {'value': "//div[@id='content']/table[@class='table1']/tr"}
        
        builder = XPathFetchPageBuilder()
        self.target = builder.build(module_setting)
        
        context = Context()
        self.target.execute(context);
        self.assertEqual(len(context.items), 3)
        self.assertEqual(context.items[1]['td.0.a.content'], 'Example to feedin')
    

    def test_mixtext_with_br(self):
        module_setting = {
                          'id':'xpathfetchpage',
                          'type':'xpathfetchpage',
                          'conf':{}
                          }
        module_setting['conf']['URL'] = {'value': 'https://raw.githubusercontent.com/kevenli/FeedIn/master/tests/modules/xpathfetchpage/test_mixtext_with_br.html'}
        module_setting['conf']['xpath'] = {'value': "//div"}
        
        builder = XPathFetchPageBuilder()
        self.target = builder.build(module_setting)

        context = Context()
        self.target.execute(context);
        self.assertEqual(len(context.items), 1)
        self.assertEqual(context.items[0]['content'], '\r\nabc\r\ndef\r\nggg\r\n')
    
#     def test_proxy(self):
#         proxy = 'localhost:8080'
#         module_setting = {
#                           'id':'xpathfetchpage',
#                           'type':'xpathfetchpage',
#                           'conf':{}
#                          }
#         module_setting['conf']['URL'] = 'http://guba.eastmoney.com/default_1.html'
#         module_setting['conf']['ExtractXPath'] = "//ul[@class='newlist']/li"
#         
#         builder = XPathFetchPageBuilder()
#         self.target = builder.build(module_setting)
#         
#         from tests.proxy.startproxy import start_server
#         thread = threading.Thread(target = start_server)
#         thread.run()
#         
#         context = Context(http_proxy = proxy)
#         self.target.execute(context);
#         print len(context.items)
#         self.assertTrue(len(context.items) > 0, "Cannot retrieve elements in page")
#         print context.items

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_proxy']
    unittest.main()