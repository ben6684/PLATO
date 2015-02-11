from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('add_data.views',
	url(r'^$','add_data',name='add_data'),
					   
	url(r'^more/$','more_files',name='more_files'),
	url(r'^add_files/$','add_file_to_ensfile',name='add_files'),
	url(r'^add_new_files/$','add_ensfile',name='add_new_files'),
	url(r'^add_new_files_from_plato/$','add_ensfile_from_plato',name='add_new_files_from_plato'),

	url(r'^upd_ens_file/(?P<id_ens>\w+)/$','upd_ens_file',name='upd_ens_file'),
	url(r'^upd_file/(?P<id_file>\w+)/$','upd_file',name='upd_file'),
					   
	url(r'^del/m/(?P<nm>\w+)/$','del_media',name='del_media'),
	url(r'^del/f/(?P<nf>\w+)/$','del_media_file',name='del_media_file'),
)
