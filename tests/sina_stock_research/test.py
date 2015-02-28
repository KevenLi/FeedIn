import unittest
import feedin


class Test(unittest.TestCase):

    def setUp(self):
        self.engine = feedin.Engine()

    def test_start(self):
        setting_file = 'feed.xml'
        feedjob = self.engine.create(setting_file)
        self.assertIsNotNone(feedjob, "feedjob should not be none")
        self.assertIsNotNone(feedjob.modules_tree_root, "feedjob should have mudule")
        feedjob.execute()
        print feedjob.context.items
        for item in feedjob.context.items:
            for key in item.keys():
                print key + ':' + item[key]
            print '\r\n'


if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.test_start']
    unittest.main()