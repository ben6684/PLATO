from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('util.views',
					   
    url(r'^download/(?P<file>\w+)/$', 'download', name='download_mma'),
    url(r'^download_zip/(?P<nef>\w+)/$', 'download_zip_archive', name='download_zip_archive'),
					   
    url(r'^check_dates/$', 'check_dates', name='check_dates'),
					   
	url(r'^autoKW/(?P<key>\w+)/$', 'autoKW', name='autoKW'),

    url(r'^error/$', 'report_error', name='report_error'),
    url(r'^readme/$', 'readme', name='readme'),
				 				   
    url(r'^upim/(?P<log>\w+)/$', 'upim', name='upload_image'),
					   					   
	url(r'^upd/ef/$','upd_ensfile',name='upd_ensfile'),
	url(r'^upd/m/(?P<nm>\w+)/$','upd_media',name='upd_media'),
	url(r'^upd/biblio/(?P<log>\w+)/$','upd_biblio',name='upd_biblio'),
	url(r'^suppr_connerie/$','suppr_connerie',name='suppr_connerie'),
	url(r'^suppr_tmp/$','suppr_tmp',name='suppr_tmp'),
	url(r'^change_manager/$','change_manager',name='prout'),
					   
)
