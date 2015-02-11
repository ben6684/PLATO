from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('audio.views',


	url(r'^$', 'vaudioinfo',name='audio'),			
	url(r'^sound/(?P<nc>\w+)/$', 'vaudio',name='sound'),	
	url(r'^corpus/$', 'vaudiocorpusinfo',name='audio_corpus'),
	url(r'^corpus/(?P<nc>\w+)/$', 'vaudiocorpusaudioinfo',name='audio_corpus_info'),
	   







)
