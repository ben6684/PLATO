from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('help.views',
					   
    url(r'^$', 'help',name='help'),
    url(r'^start$', 'start',name='start'),
	url(r'^add_data/$','help_add_data',name='help_add_data'),
)
