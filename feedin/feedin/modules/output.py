# -*- coding: utf-8 -*-

from module import Module
from module import ModuleBuilder

class Output(Module):
    
    fields = []
        
    def __init__(self, setting, context=None):
        super(Output, self).__init__(setting, context)
        fields = setting.find('fields')
        if fields is not None:
            for field_setting in fields:
                self.fields.append(self.OutputField(field_setting))
    
    def execute(self, context=None):
        if self.fields:
            for item in context.items:
                field_names = [x.name for x in self.fields]
                field_names.append('_id') # 如果已经指定_id 则保留
                for field in self.fields:
                    try:
                        item[field.name] = item.text(field.name)
                    except KeyError:
                        item[field.name] = ''
                for key in item.keys():
                    if key not in field_names:
                        item.delete(key)
        else:
            for item in context.items:
                for key in item.keys():
                    item[key] = item.text(key)

        pass
    
    class OutputField():
        name = None
        def __init__(self, setting):
            self.name = setting.get('name')
            
class OutputBuilder(ModuleBuilder):
    def build(self, module_config, context=None):
        return Output(module_config, context)