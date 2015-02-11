from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app.views',

    url(r'^$','vcodes',name ='sources_codes'),
    url(r'^(?P<na>\w+)/$','vcode',name ='vcode'),				   
)
