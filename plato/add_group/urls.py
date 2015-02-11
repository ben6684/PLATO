from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('add_group.views',
					   
	url(r'^(?P<log>\w+)/new_group/$', 'ngrp',name='usr_ngrp'),
	url(r'^(?P<ngpe>\w+)/update/$', 'updgrp',name='grp_upd'),
					   
	url(r'^(?P<ngpe>\w+)/delete/$', 'dltgrp',name='grp_del'),
					   
	url(r'^(?P<ngpe>\w+)/(?P<log>\w+)/delete/$', 'dltuig',name='grp_del_usr'),
	url(r'^(?P<log>\w+)/(?P<ngpe>\w+)/del/$', 'dltgiu',name='usr_del_grp'),		
)
