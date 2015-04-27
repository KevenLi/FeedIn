# -*- coding: utf-8 -*-

from module import Module, ModuleBuilder
class Rename(Module):
    
    rules = None
    def __init__(self, setting, context=None):
        super(Rename, self).__init__(setting, context)
        self.rules = []
        for element in setting['conf']["RULE"]:
            source = element['field']['value']
            if source.find('item.') == 0:
                source = source.replace('item.', '', 1)
                
            rule = {'source': source,
                    'operator': element['op']['value'],
                    'dest': element['newval']['value'] }
            self.rules.append(rule)
    
    def execute(self, context=None):
        for item in context.items:
            for rule in self.rules:
#                 value = util.get_value(rule['source'], item)
                if rule['operator'] == 'copy':
                    try:
                        item[rule['dest']] = item[rule['source']]
                    except KeyError:
                        pass
                if rule['operator'] == 'rename':
                    try:
                        item.move(rule['source'], rule['dest'])
                    except KeyError:
                        pass
#                 try:
#                     item.set(rule['dest'], value)
#                 except AttributeError:
#                     pass
                
#                 if rule['operator'] == 'rename':
#                     try:
#                         item.delete(rule['source']['subkey'])
#                     # TypeError catches pseudo subkeys, e.g. summary.content
#                     except (KeyError, TypeError):
#                         # ignore if the target doesn't have our field
#                         # todo: issue a warning if debugging?
#                         pass

class RenameBuilder(ModuleBuilder):
    def build(self, module_config, context=None):
        return Rename(module_config, context)