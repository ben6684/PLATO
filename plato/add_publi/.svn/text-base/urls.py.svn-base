from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('add_publi.views',
					   
    url(r'^$', 'add_page',name='add_publi'),
    url(r'^upd/(?P<np>\w+)/$', 'upd_page',name='upd_page'),
					   
    url(r'^del_file/(?P<np>\w+)/$', 'del_file_page',name='del_file_page'),
    url(r'^del_prez/(?P<np>\w+)/$', 'del_prez_page',name='del_prez_page'),
    url(r'^del_article/(?P<np>\w+)/$', 'del_article_page',name='del_article_page'),
					   
    url(r'^autoAuthor/$', 'autoAuthor',name='autoAuthor'),
    url(r'^autoConf/$', 'autoConf',name='autoConf'),
					   
    url(r'^del/p/(?P<np>\w+)/$','del_page',name='del_page'),
	url(r'^ensfile_publi/$','ensfile_publi',name='ensfile_publi'),
)
