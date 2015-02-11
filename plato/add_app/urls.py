from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('add_app.views',
					   
    url(r'^$', 'add_app',name='add_app'),
	url(r'^upd/(?P<na>\w+)/$','upd_app',name='upd_tool'),
	url(r'^publi_code/$','publi_code',name='publi_code'),
	url(r'^demo_code/$','demo_code',name='demo_code'),
	url(r'^ensfile_code/$','ensfile_code',name='ensfile_code'),
    url(r'^autoAuthor/$', 'autoAuthor2',name='autoAuthor2'),
    url(r'^del_file/$', 'del_file_algo',name='del_file_algo'),	
	url(r'^del/a/(?P<na>\w+)/$','del_tool',name='del_tool'),	   
)
