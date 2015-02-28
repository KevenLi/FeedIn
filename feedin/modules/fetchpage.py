from module import Module
from module import ModuleBuilder

from urllib2 import urlopen

class FetchPage(Module):
    '''
    classdocs
    '''
    def __init__(self, setting, context=None):
        super(FetchPage, self).__init__(setting, context)
        self.URL = setting.get("URL")
    
    def execute(self, context=None):
        f = urlopen(self.URL)
        content = unicode(f.read(), 'utf-8')
        context[0] = {'content' : content}
        pass

class FetchPageBuilder(ModuleBuilder):
    def build(self, module_config, context=None):
        return FetchPage(module_config, context)