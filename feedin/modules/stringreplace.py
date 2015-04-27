# -*- coding: utf-8 -*-

from module import Module, ModuleBuilder

class StringReplace(Module):
    def __init__(self, setting, context=None):
        super(StringReplace, self).__init__(setting, context)
        self.replace = setting['conf']["Replace"]
        self.withStr = setting['conf']["With"]
    
    def execute(self, context=None):
        for i in range(len(context.items)):
            item = context.items[i]
            if isinstance(item, basestring):
                context.items[i] = item.replace(self.replace, self.withStr)
        
class StringReplaceBuilder(ModuleBuilder):
    def build(self, module_config, context=None):
        return StringReplace(module_config, context)