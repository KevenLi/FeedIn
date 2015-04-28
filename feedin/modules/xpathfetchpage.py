from module import Module

import urllib2
import urlparse

from StringIO import StringIO
import gzip
from lxml import html
from lxml import etree
from feedin import util
from feedin.dotdict2 import DotDict2
from module import ModuleBuilder

class XPathFetchPage(Module):
    EXTRACT_TYPE_DICT = 'dict'
    EXTRACT_TYPE_TEXT = 'text'
    EXTRACT_TYPE_HTML = 'html'
    CHARSETS = ['utf8', 'gb2312', 'GB18030']
    '''
    classdocs
    '''
    def __init__(self, setting, context=None):
        super(XPathFetchPage, self).__init__(setting, context)
        self.URL = setting['conf']['URL']
        self.ExtractXPath = setting['conf']['xpath']['value']
        self.html5 = setting['conf']['html']['value'] == 'true' if 'html5' in setting['conf'] else False
        self.useAsString = setting['conf']['useAsString']['value'] == 'true' if 'useAsString' in setting['conf'] else False
        self.ExtractMethod = setting['conf']['ExtractMethod'] if 'ExtractMethod' in setting['conf'] else XPathFetchPage.EXTRACT_TYPE_DICT
    
    def execute(self, context=None):
        url = self.URL
        if 'subkey' in self.URL:   # a subkey assigned
            key = self.URL['subkey'].lstrip('item.')
            url = context.items[0][key]
        else:
            url = self.URL['value']
        
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
        
        decoding_error = None  # last decoding error, will be raised if cannot decode the content
        decoded_content = None # decoded
        for charset in XPathFetchPage.CHARSETS:
            try:
                decoded_content = unicode(content, charset)
            except UnicodeDecodeError as e:
                decoding_error = e
        
        if not decoded_content and decoding_error:
            raise decoding_error
                
                
            
        root = html.fromstring(decoded_content)
        comments = root.xpath('//comment()')
        for c in comments:
            p = c.getparent()
            if p is not None:
                p.remove(c)
        #root = doc.getroot()
        context.last_result = []
        for element in root.xpath(self.ExtractXPath):
            for link_element in element.iter("a"):
                link_element.set("href", urlparse.urljoin(url, link_element.get("href")))
            
            if self.ExtractMethod == XPathFetchPage.EXTRACT_TYPE_TEXT:
                new_item =  etree.tostring(element, method='text', encoding=unicode)
            elif self.useAsString == True:
                new_item =  etree.tostring(element, method='html', encoding=unicode)
            else:
                element_dic = util.etree_to_dict2(element)
                new_item = DotDict2(element_dic)
            context.items.append(new_item)
            context.last_result.append(new_item)
        
class XPathFetchPageBuilder(ModuleBuilder):
    def build(self, module_config, context=None):
        return XPathFetchPage(module_config, context)