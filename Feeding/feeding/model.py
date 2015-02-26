# -*- coding: utf-8 -*-
'''
Created on 2014��11��27��

@author: ���
'''
class Context:
    items = []
    last_result = None
    
    def __init__(self, items=None, **kwargs):
        if items is not None:
            self.items = items
        else:
            self.items = []
        
        self.last_result = None
        
        self.http_proxy = None
        if 'http_proxy' in kwargs:
            self.http_proxy = kwargs['http_proxy']
        
class Feed:
    
    def __init__(self, setting):
        self.setting = setting
    
    @staticmethod
    def parseSetting(setting):
        pass