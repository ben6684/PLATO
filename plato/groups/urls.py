from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('groups.views',
					   
 	url(r'^$', 'vgrps',name='projects'),                      
	url(r'^(?P<ngpe>\w+)/$', 'vgrp',name='grp'),
)
