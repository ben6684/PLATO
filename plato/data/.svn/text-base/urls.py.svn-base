from django.conf.urls import patterns, include, url
from django.views.static import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('data.views',
    # Examples:
    url(r'^$', 'vall', name='data'),
    url(r'^multimodal/$', 'vmulti', name='multimodal'),
    url(r'^(?P<nef>\w+)/$', 'vfiles', name='files'),

)
