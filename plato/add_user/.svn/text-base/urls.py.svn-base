from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('add_user.views',
					   
  	url(r'^(?P<log>\w+)/new_user/$','nusr',name='usr_n'),
	url(r'^(?P<log>\w+)/update/$', 'updusr',name='usr_upd'),
								
     # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

