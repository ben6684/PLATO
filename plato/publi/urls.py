from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('publi.views',
					   
    url(r'^$', 'vpages',name='vpages'),			   
    url(r'^(?P<np>\w+)/$', 'vpage',name='vpage'),

)
