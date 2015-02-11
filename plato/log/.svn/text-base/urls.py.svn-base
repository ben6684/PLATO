from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('log.views',

    url(r'^$', 'loggin',name='logg'),				   
	url(r'^disconnect/$', 'disconnect',name='dc'),					   
										
     # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
