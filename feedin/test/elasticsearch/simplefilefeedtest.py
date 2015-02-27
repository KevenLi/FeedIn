# -*- coding: utf-8 -*-
'''
Created on 2014��11��12��

@author: ���
'''
import unittest
from elasticsearch import Elasticsearch
import time
from feedin import Engine;


class SimpleFileFeedTest(unittest.TestCase):

    
    
    def setUp(self):
        self.es = Elasticsearch()
        self.engine = Engine()
        


    def tearDown(self):
        pass

    def test_loop(self):
        setting_file = 'loop.feed.xml'
        feedjob = self.engine.create(setting_file)
        self.assertIsNotNone(feedjob, "feedjob should not be none")
        self.assertIsNotNone(feedjob.modules_tree_root, "feedjob should have mudule")
        feedjob.execute()
        print feedjob.context.items
        for item in feedjob.context.items:
            timestamp = time.localtime()
            
            body = {'read_count': int(item.text('read')),
                    'comment_count': int(item.text('comments')), 
                    'title' : item.text('title'), 
                    'url' : item.text('url'), 
                    'channel' : item.text('channel'), 
                    'author' : item.text('author'), 
                    'content' : item.text('pagedetail'), 
                    'updatetime' : time.strftime('%Y-%m-%dT%H:%M:%S', timestamp)}
            self.es.index('guba', 'thread', body, item.text('url'))
            print item.text('read'), item.text('comments'), item.text('title'), item.text('url'), \
                item.text('channel'), item.text('author'), item.text('pagedetail')
    
    def test_es_chinese(self):
        self.es.index('test', 'text', id=1, body={'title': u'中文'})
        ret = self.es.get(index = 'test', id = 1, doc_type = 'text')
        self.assertEqual(u'中文', ret['_source']['title'])
        print ret['_source']['title']
        
    def test_es_search(self):
        ret = self.es.search(index = 'guba', doc_type = 'thread')
        for item in ret['hits']['hits']:
            print item['_source']['title'], item['_source']['url']

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'SimpleFileFeedTest.test_loop']
    unittest.main()