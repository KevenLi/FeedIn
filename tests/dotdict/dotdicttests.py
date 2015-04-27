# -*- coding: utf-8 -*-
'''
Created on 2014��11��21��

@author: ���
'''
import unittest
from feedin.dotdict2 import DotDict2

class Test(unittest.TestCase):


    def test_set_get(self):
        target = DotDict2()
        target['a.1'] = 'a1'
        self.assertEqual(target['a']['1'], 'a1')
        self.assertEqual(target['a']['1'], target['a.1'])
    
    def test_set_get_deep(self):
        target = DotDict2()
        target['a.1.b.2'] = 'b2'
        self.assertEqual(target['a']['1']['b']['2'], 'b2')
        self.assertEqual(target['a']['1']['b']['2'],  target['a.1.b.2'])
        
    def test_set_get_simple(self):
        target = DotDict2()
        target['a'] = 'a'
        self.assertEqual(target['a'], 'a')
        
        
    def test_delete(self):
        target = DotDict2()
        target['a.1'] = 1
        target['a.2'] = 2
        target.delete('a.1')
        
        self.assertEqual(target['a']['2'], 2)
        try:
            v = target['a']['1']
            self.assertIsNotNone(v)
            self.fail("Key should not be found")
        except KeyError:
            pass
    
    def test_delete2(self):
        target = DotDict2()
        target['a'] = 'a'
        target['b.1'] = 'b1'
        target['b.2'] = 'b2'
        target.delete('b.1')
        target.delete('b.2')
        
        try:
            v = target['b']   # since b.1, b.2 has been deleted, b is empty and should also been deleted
            self.assertIsNotNone(v)
            self.fail("Key should not be found")
        except KeyError:
            pass
        
        
    def test_update(self):
        target = DotDict2()
        target.update({'a' : 'b'})
        
        self.assertEqual(target['a'], 'b')
        
    def test_dict_move(self):
        target= DotDict2()
        target.update({'a': 'b'})
        target.move('a', 'a.1')
        
        self.assertEqual(target['a']['1'], 'b')
    
    def test_text(self):
        target= DotDict2()
        target['a'] = "a text"
        self.assertEqual(target.text(), "a text")
        self.assertEqual(target.text("a"), "a text") 
        
#     def test_text_depth(self):
#         target= DotDict2()
#         target['a.1'] = "a text"
#         target['a.2'] = '.'
#         self.assertEqual(target.text(), "a text")
#         self.assertEqual(target.text("a"), "a text.") 
        
#     def test_text_html_paragraph(self):
#         target = DotDict2()
#         target['div.class'] = 'someclass'
#         
#         contentDict = DotDict2()
#         contentDict['p.1.content'] = 'paragraph #1 content'
#         contentDict['p.2.content'] = 'other'
#         
#         target['div.content'] = contentDict
#         
#         self.assertEqual(target.text('div'), 'paragraph #1 content other')

if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.test_text_html_paragraph']
    unittest.main()