# -*- coding: utf-8 -*-
'''
Created on 2014��11��12��

@author: ���
'''

from xml.etree import ElementTree
from modules.module import ModuleFactory
from model import Context

class Engine(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def create(self, setting):
        
        return Job(setting)

        
class Job(object):
    modules_tree_root = None
    
    def __init__(self, setting):
        xml_doc = ElementTree.parse(setting)
        elements = xml_doc.findall("Parsing/modules/module")
        
        modules = {}
        module_factory = ModuleFactory()
        for element in elements:
            modules[element.get('id')] = module_factory.buildModule(element)
        
        self.modules_tree_root = modules.pop('output')  # the root of module_tree must be 'output'
        self.__walk_through_tree(self.modules_tree_root, modules)
            
        pass
    
    def __walk_through_tree(self, module_node = None, module_dict = None):
        if module_node.input_name:
            input_module = module_dict.pop(module_node.input_name)
            if input_module is None:
                raise Exception
            module_node._dependents.append(input_module)
            self.__walk_through_tree(input_module, module_dict)
            
    def __walk_through_execute(self, module_node = None, context = None):
        if module_node._dependents:
            for module in module_node._dependents:
                self.__walk_through_execute(module, context)
        module_node.execute(context)
        
    
    def execute(self, context=None):
        if context is None:
            context = Context()
        
        self.context = context;
        self.__walk_through_execute(self.modules_tree_root, context)


                
        
        
    