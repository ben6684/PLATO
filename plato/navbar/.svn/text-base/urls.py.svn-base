from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('navbar.views',
					   
	url(r'^user/(?P<log>\w+)/$', 'usr_selected',name='usr_selected'),
	url(r'^group/(?P<id_gpe>\w+)/$', 'gpe_selected',name='gpe_selected'),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
