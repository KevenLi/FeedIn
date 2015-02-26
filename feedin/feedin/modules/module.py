# -*- coding: utf-8 -*-
'''
Created on 2014��11��12��

@author: ���
'''
from urllib2 import urlopen
from lxml import html
from lxml import etree
from feedin import util
from feedin.dotdict2 import DotDict2
from feedin.model import Context
import urllib2
import urlparse
from StringIO import StringIO
import gzip

class ModuleFactory():
    def buildModuleTree(self, modules_setting):
        pass
    
    def buildModule(self, module_setting):
        module_type = module_setting.get('type')
        if module_type == 'fetchpage':
            return FetchPage(module_setting)
        if module_type == 'output':
            return Output(module_setting)
        if module_type == "xpathfetchpage":
            return XPathFetchPage(module_setting)
        if module_type == "rename":
            return Rename(module_setting)
        if module_type == 'loop':
            return Loop(module_setting)
        if module_type == 'stringreplace':
            return StringReplace(module_setting)

class Module(object):
    '''
    classdocs
    '''
    _dependents = None

    def __init__(self, module_setting):
        self._id = module_setting.get('id')
        self.input_name = module_setting.get('input', None)
        self._dependents = []
        
    
class FetchPage(Module):
    '''
    classdocs
    '''
    def __init__(self, setting):
        super(FetchPage, self).__init__(setting)
        self.URL = setting.get("URL")
    
    def execute(self, context=None):
        f = urlopen(self.URL)
        content = unicode(f.read(), 'utf-8')
        context[0] = {'content' : content}
        pass

class XPathFetchPage(Module):
    EXTRACT_TYPE_DICT = 'dict'
    EXTRACT_TYPE_TEXT = 'text'
    EXTRACT_TYPE_HTML = 'html'
    '''
    classdocs
    '''
    def __init__(self, setting):
        super(XPathFetchPage, self).__init__(setting)
        self.URL = setting.get("URL")
        self.ExtractXPath = setting.get("ExtractXPath")
        self.ExtractMethod =  setting.get("ExtractMethod", XPathFetchPage.EXTRACT_TYPE_DICT)
    
    def execute(self, context=None):
        url = self.URL
        if url.startswith('item.') and context is not None:
            key = url.lstrip('item.')
            url = context.items[0][key]
        
        http_proxy = context.http_proxy
        if http_proxy:
            proxy_handler = urllib2.ProxyHandler({'http': http_proxy})
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener()
        response = opener.open(url)
        content = response.read()
        opener.close()
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(content)
            f = gzip.GzipFile(fileobj=buf)
            content = f.read()
            
        root = html.fromstring(content)
        #root = doc.getroot()
        context.last_result = []
        for element in root.xpath(self.ExtractXPath):
            for link_element in element.iter("a"):
                link_element.set("href", urlparse.urljoin(url, link_element.get("href")))
            
            if self.ExtractMethod == XPathFetchPage.EXTRACT_TYPE_TEXT:
                new_item =  etree.tostring(element, method='text', encoding=unicode)
            elif self.ExtractMethod == XPathFetchPage.EXTRACT_TYPE_HTML:
                new_item =  etree.tostring(element, method='html', encoding=unicode)
            else:
                element_dic = util.etree_to_dict2(element)
                new_item = DotDict2(element_dic)
            context.items.append(new_item)
            context.last_result.append(new_item)

class Rename(Module):
    
    rules = None
    def __init__(self, setting):
        super(Rename, self).__init__(setting)
        self.rules = []
        for element in setting.find("rules"):
            rule = {'source': element.get('source').lstrip('item.'),
                    'operator': element.get('operator'),
                    'dest': element.get('dest') }
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
class Loop(Module):
    def __init__(self, setting):
        super(Loop, self).__init__(setting)
        self.for_each = setting.get("ForEach")
        self.assign_which = setting.get("AssignWhich") # not use yet
        self.assign_to = setting.get("AssignTo")
        self.module_setting = setting.find("module")
        self.module = ModuleFactory().buildModule(self.module_setting)
        
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
            
class StringReplace(Module):
    def __init__(self, setting):
        super(StringReplace, self).__init__(setting)
        self.replace = setting.get("Replace")
        self.withStr = setting.get("With")
    
    def execute(self, context=None):
        for i in range(len(context.items)):
            item = context.items[i]
            if isinstance(item, basestring):
                context.items[i] = item.replace(self.replace, self.withStr)
        

class Output(Module):
    
    fields = []
        
    def __init__(self, setting):
        super(Output, self).__init__(setting)
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
