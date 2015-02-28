# -*- coding: utf-8 -*-
'''
Created on 2014��11��12��

@author: ���
'''

class ModuleFactory():
    
    _builders = {}
    
    def registerModuleBuilder(self, module_type, module_builder):
        self._builders[module_type] = module_builder;
        
    def buildModule(self, module_type, module_config, context=None):
        builder = self._builders[module_type]
        return builder.build(module_config, context)

class Module(object):
    '''
    classdocs
    '''
    _dependents = None
    _context = None

    def __init__(self, module_setting, context=None):
        self._id = module_setting.get('id')
        self.input_name = module_setting.get('input', None)
        self._dependents = []
        self._context = context

class ModuleBuilder(object):
    def build(self, module_config, context=None):
        pass
        
