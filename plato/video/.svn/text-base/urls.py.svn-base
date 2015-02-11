from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('video.views',
	url(r'^$', 'vvid', name='videos'),			
	url(r'^(?P<nc>\w+)/$', 'vvidinfo', name='videos'),
)
