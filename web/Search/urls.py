from django.conf.urls import url, patterns

urlpatterns = patterns('Search.views', 
    url(r'', 'search'),
    url(r'user/info/', 'user_info')
)
