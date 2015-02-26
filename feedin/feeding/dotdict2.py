# -*- coding: utf-8 -*-
'''
Created on 2014��11��21��

@author: ���
'''

class DotDict2(dict):
    '''
    classdocs
    '''


    def __init__(self, dict_data = None, **kwargs):
        super(DotDict2, self).__init__(self, **kwargs)
        self.update(dict_data)
        
    def update(self, dict_data=None):
        if dict_data:
            for (key, value) in dict_data.items():
                self.__setitem__(key, value)

    
    def _parse_key(self, key):
        if isinstance(key, list):
            return key
        keys = key.rstrip('.').split('.') if key else []
        return keys;

    def __setitem__(self, key, value):
        key_parts = self._parse_key(key);
        if len(key_parts) == 1:
            dict.__setitem__(self, key_parts[0], value)
            return
        if key_parts[0] in self:
            item = self[key_parts[0]];
            if len(key_parts) == 2:
                item[key_parts[1]] = value;
            else:
                item[key_parts[1:]] = value;
        else:
            item = DotDict2();
            if len(key_parts) == 2:
                item[key_parts[1]] = value;
            else:
                item[key_parts[1:]] = value;
            self[key_parts[0]] = item;
    
    def __getitem__(self, key):
        key_parts = self._parse_key(key);
        item = dict.__getitem__(self, key_parts[0])
        if len(key_parts) > 1:
            for key_part in key_parts[1:]:
                item = dict.__getitem__(item, key_part)
        return item
            
        
    def delete(self, key):
        key_parts = self._parse_key(key)
        if len(key_parts) == 1:
            del(self[key_parts[0]])
            return;

        item = self[key_parts[0]]
        item.delete(key_parts[1:])
        if len(item) == 0:
            del(self[key_parts[0]])
        
    def move(self, original_key, dest_key):
        value = self[original_key]
        self.delete(original_key)
        self[dest_key] = value;
        
    def text(self, key=None):
        if key is not None:
            if isinstance(self[key], str):
                return self[key]
            if isinstance(self[key], unicode):
                return self[key]
            if self[key] is not None:
                return self[key].text() 
            return ''
        if 'content' in self.keys():
            return self['content']
        if len(self.keys())>0:
            item = self[self.keys()[0]]
            if isinstance(item, str):
                return item
            elif isinstance(item, DotDict2):
                return item.text()
    
        