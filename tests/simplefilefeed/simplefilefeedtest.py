# -*- coding: utf-8 -*-
'''
Created on 2014��11��12��

@author: ���
'''
import unittest
import feedin.engine
import json


class SimpleFileFeedTest(unittest.TestCase):

    
    
    def setUp(self):
        self.engine = feedin.engine.Engine()


    def tearDown(self):
        pass


    def test_start(self):
        setting_file = 'sample.feed.json'
        with open(setting_file, 'r') as f:
            feed_setting = f.read()
        feedjob = self.engine.create(feed_setting)
        self.assertIsNotNone(feedjob, "feedjob should not be none")
        self.assertIsNotNone(feedjob.modules_tree_root, "feedjob should have mudule")
        feedjob.execute()
        print feedjob.context.items
        for item in feedjob.context.items:
            print item.text('read'), item.text('comments'), item.text('title'), item.text('url'), item.text('channel'), item.text('author')

    def test_fetchonly(self):
        setting_file = 'fetchonly.feed.json'
        with open(setting_file, 'r') as f:
            feed_setting = f.read()
        feedjob = self.engine.create(feed_setting)
        self.assertIsNotNone(feedjob, "feedjob should not be none")
        self.assertIsNotNone(feedjob.modules_tree_root, "feedjob should have mudule")
        feedjob.execute()
        print feedjob.context.items
    
    def test_loop(self):
        setting_file = 'loop.feed.json'
        with open(setting_file, 'r') as f:
            feed_setting = f.read()
        feedjob = self.engine.create(feed_setting)
        self.assertIsNotNone(feedjob, "feedjob should not be none")
        self.assertIsNotNone(feedjob.modules_tree_root, "feedjob should have mudule")
        feedjob.execute()
        print feedjob.context.items
        for item in feedjob.context.items:
            print item.text('read'), item.text('comments'), item.text('title'), item.text('url'), \
                item.text('channel'), item.text('author'), item.text('pagedetail')


if __name__ == "__main__":
    import sys;sys.argv = ['', 'SimpleFileFeedTest.test_loop']
    unittest.main()