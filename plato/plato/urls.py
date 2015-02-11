from django.conf.urls import patterns, include, url
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'users.views.index', name='idx'),
					   
	(r'^add_app/', include('add_app.urls')),
	(r'^add_publi/', include('add_publi.urls')),
	(r'^add_data/', include('add_data.urls')),
					   
	(r'^users/', include('users.urls')),
	(r'^add_user/', include('add_user.urls')),
					   
	(r'^log/', include('log.urls')),
					   
	(r'^groups/', include('groups.urls')),
	(r'^add_group/', include('add_group.urls')),
					   
	(r'^util/', include('util.urls')),
	(r'^navbar/', include('navbar.urls')),
	(r'^search/', include('search.urls')),
					   
	(r'^data/', include('data.urls')),
	(r'^audio/', include('audio.urls')),
	(r'^image/', include('image.urls')),
	(r'^video/', include('video.urls')),
	(r'^cg/', include('cg.urls')),
					   
	(r'^app/', include('app.urls')),
	(r'^publi/', include('publi.urls')),
	(r'^demo/', include('demo.urls')),

	(r'^ws/',include('ws.urls')),
					   
	(r'^help/',include('help.urls')),	
					   
    # url(r'^plato/', include('plato.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
		(r'^plato/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/tsi/'}),
)
urlpatterns += patterns('',
		(r'^tsi/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/tsi/'}),
)
urlpatterns += patterns('',
		(r'^demo_tmp/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/tmp/'}),
)
urlpatterns += patterns('',
		(r'^root/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/'}),
)
urlpatterns += patterns('',
		(r'^debug/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/tmp/'}),
)
urlpatterns += patterns('',
		(r'^debug2/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/'}),
)

urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
