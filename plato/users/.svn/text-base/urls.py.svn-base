from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('users.views',
					   
    url(r'^$', 'index',name='idx'),	
	url(r'^members/$', 'show_users',name='usrs'),	
	url(r'^change_lang/$','change_lang',name='change_lang'),
	url(r'^(?P<log>\w+)/$', 'usr',name='usr'),

							
     # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

