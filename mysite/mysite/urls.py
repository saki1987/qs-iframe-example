from django.conf.urls import patterns, include, url
 
from django.contrib import admin
from django.conf import settings
admin.autodiscover()
 
urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
 	#url(r'^add/$','learn.views.add',name='add'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^learn/', include('learn.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        #url(r'^qsProxy.html(.*)','../learn/templates/qsProxy.html'),
        url(r'^qsProxy.html(.*)','learn.views.qsProxy'),
    )
    urlpatterns += patterns('',
        #url(r'^qsProxy.html(.*)','../learn/templates/qsProxy.html'),
        url(r'^pay.html(.*)','learn.views.fetch_alipay'),
    )
