# -*- coding: utf-8 -*-
'''
Created on 2015��1��22��

@author: ���
'''
import unittest
import feedin.engine
import os


class Test(unittest.TestCase):
    
    def setUp(self):
        self.engine = feedin.engine.Engine()


    def tearDown(self):
        pass
    
    def get_conf_file(self, file_name):
        file_dir = os.path.dirname(__file__)
        return os.path.join(file_dir, file_name)

    def test_start(self):
        setting_file = 'feed.json'
        with open(self.get_conf_file(setting_file), "r") as f:
            setting_content = f.read()
        feedjob = self.engine.create(setting_content)
        self.assertIsNotNone(feedjob, "feedjob should not be none")
        self.assertIsNotNone(feedjob.modules_tree_root, "feedjob should have mudule")
        feedjob.execute()
        print feedjob.context.items
        for item in feedjob.context.items:
            print item.text('url'), item.text('title'), item.text('description')
        #for item in feedjob.context.items:
        #    print item.text('read'), item.text('comments'), item.text('title'), item.text('url'), item.text('channel'), item.text('author')



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()