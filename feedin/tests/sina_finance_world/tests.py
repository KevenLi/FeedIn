# -*- coding: utf-8 -*-
'''
Created on 2015��1��22��

@author: ���
'''
import unittest
import feeding.engine


class Test(unittest.TestCase):
    
    def setUp(self):
        self.engine = feeding.engine.Engine()


    def tearDown(self):
        pass

    def test_start(self):
        setting_file = 'feed.xml'
        feedjob = self.engine.create(setting_file)
        self.assertIsNotNone(feedjob, "feedjob should not be none")
        self.assertIsNotNone(feedjob.modules_tree_root, "feedjob should have mudule")
        feedjob.execute()
        print feedjob.context.items
        for item in feedjob.context.items:
            print item.text('url'), item.text('title'), item.text('content')
        #for item in feedjob.context.items:
        #    print item.text('read'), item.text('comments'), item.text('title'), item.text('url'), item.text('channel'), item.text('author')



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()