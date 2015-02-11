from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('image.views',

	url(r'^$', 'vimg',name='image'),
	url(r'^type/(?P<ti>\w+)/$', 'vimgsrc',name='images'),			
	url(r'^source/(?P<nc>\w+)/$', 'vimgs',name='image_info'),					
	#url(r'^more/$', 'img_more',name='image_more'),

 )
