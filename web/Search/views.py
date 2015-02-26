from django.shortcuts import render
import elasticsearch
from django.shortcuts import render_to_response
from django.template import RequestContext
import elasticsearch

# Create your views here.
def search(request):
    if request.method == 'POST':
        return search_result(request)
    return render(request, 'search.html')

def search_result(request):
    keyword = request.POST.get('keyword')
    es = elasticsearch.Elasticsearch()
    condition = {'query' : {'term' : {'content':keyword }}}
#     condition =  {'query' : 
#                   {'bool':
#                                      {'multi_match' : 
#                   {'query' : keyword}, 
#                   'fields': ['title', 'content', 'channel']
#                   }
#                    }
#                  }

    #condition = {'query' : {'match': {'title':keyword}}}
    #condition = {'query' : { "filtered" : { 'query' : {'match':{'title' : keyword}}}}}
    condition = {
                 'query' : { 
                             "filtered" : { 
                                          'query' : {
                                                     'multi_match':{ 'query' : keyword, 
                                                    'fields':['title', 'content']} }
                                           }
                            },
                 'sort':[{'_ts' : {'order': 'desc'}}, 
                         "_score"]
                 }
    q = 'content:' + keyword
    ret = es.search('guba', 'thread', body=condition)
    
    #ret = es.search('guba', 'thread', q=q)
    docs = [x['_source'] for x in ret['hits']['hits']]
    for doc in docs:
        doc['updatetime'] = doc['_ts']
    return render_to_response('search_result.rtp', {'hits' : docs, 'keyword' : keyword}, 
                              context_instance=RequestContext(request))