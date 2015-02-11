from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('cg.views',
	url(r'^$','v3d',name='3D'),
	url(r'^(?P<nef>\w+)/$','v3df',name='3df'),
)
