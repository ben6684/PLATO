from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('demo.views',
					   
    url(r'^$', 'vdemos',name='vdemos'),
    url(r'^add/$', 'add_demo_info',name='add_demo'),
    #url(r'^del/$', 'del_file_demo',name='del_file_demo'),	
    url(r'^(?P<nd>\w+)/$', 'vdemo',name='vdemo'),	
    url(r'^upd/(?P<nd>\w+)/$', 'upd_demo_info',name='upd_demo'),	
    url(r'^upd_publi/(?P<nd>\w+)/$', 'add_publis_to_demo',name='add_demo_publi'),	
)
