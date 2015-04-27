# -*- coding: utf-8 -*-

from module import Module, ModuleBuilder
from feedin import Context
from feedin import DotDict2

class Loop(Module):
    def __init__(self, setting, context=None):
        super(Loop, self).__init__(setting, context)
        self.assign_to = setting['conf']['assign_to']['value']
        self.module_setting = setting['conf']['embed']['value']
        engine = self._context['engine']
        self.module = engine._module_factory.buildModule(self.module_setting['type'], self.module_setting, None)
        
    def execute(self, context=None):
        for item in context.items:
#             if self.for_each == "item":
#                 item_data = item
#             elif self.for_each.startswith("item."):
#                 item_data_key = self.for_each.lstrip("item.")
#                 item_data = item_data_key
            loop_context = Context()
            loop_context.items = [item]
            self.module.execute(loop_context)
            if len(loop_context.last_result) == 0:
                pass
            elif len(loop_context.last_result) == 1:
                item[self.assign_to] = loop_context.last_result[0]
            else:
                item[self.assign_to] = DotDict2(loop_context.last_result)
            
            
            
class LoopBuilder(ModuleBuilder):
    def build(self, module_config, context=None):
        return Loop(module_config, context)
