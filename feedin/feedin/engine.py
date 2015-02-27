# -*- coding: utf-8 -*-
'''
Created on 2014��11��12��

@author: ���
'''

from xml.etree import ElementTree
from modules import ModuleFactory
from modules import FetchPageBuilder
from modules import XPathFetchPageBuilder
from modules import OutputBuilder
from modules import RenameBuilder
from modules import LoopBuilder
from model import Context

class Engine(object):
    '''
    classdocs
    '''

    _module_factory = None

    def __init__(self):
        '''
        Constructor
        '''
        self._module_factory = ModuleFactory()
        # init inline module builders
        
        self._module_factory.registerModuleBuilder('fetchpage', FetchPageBuilder())
        self._module_factory.registerModuleBuilder('xpathfetchpage', XPathFetchPageBuilder())
        self._module_factory.registerModuleBuilder('output', OutputBuilder())
        self._module_factory.registerModuleBuilder('rename', RenameBuilder())
        self._module_factory.registerModuleBuilder('loop', LoopBuilder())
        
    def create(self, setting):
        return Job(self, setting)

        
class Job(object):
    modules_tree_root = None
    
    def __init__(self, engine, setting):
        xml_doc = ElementTree.parse(setting)
        elements = xml_doc.findall("Parsing/modules/module")
        
        modules = {}
        module_factory = engine._module_factory
        build_context = {'engine': engine}
        for element in elements:
            module = module_factory.buildModule(element.get('type'), element, build_context)
            modules[element.get('id')] = module
            module._engine = engine
        
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


                
        
        
    