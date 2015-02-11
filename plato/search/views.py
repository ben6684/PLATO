# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q,Max,StdDev,Avg

from plato.models import User,EnsFile, File, Group,Tool,Page,KW
from util.object_util import *

def test_search_word(word):
	"""
	test_search_word : function that take a search word AND test if there is no security breach
	input : a string word
	output : true if word ok or false if the word is not allowed
	"""
	test_word = word.lower()
	test_input=[u'<input',u'Œ',u'œ',u'€']
	for w in test_input:
		test = test_word.find(w)
		if test != -1 :
			return False
	return True
	
def search(request):

	if request.GET.has_key('KW'):
		kw = request.GET['KW']
		if kw:# and test_search_word(str(kw)):
			U = User.objects.filter(Q(nm_person__icontains=kw)|Q(fstnm_person__icontains=kw))
			if request.session.has_key('login'):
				EF = EnsFile.objects.filter(KW__nm_kw__icontains=kw)
			else:
				EF= EnsFile.objects.filter(KW__nm_kw__icontains=kw).filter(public=True)
			G = Group.objects.filter(KW__nm_kw__icontains=kw)
			T = Tool.objects.filter(KW__nm_kw__icontains=kw)
			if not request.session.has_key('login'):
				T = T.filter(visible=True)
			P = Page.objects.filter(KW__nm_kw__icontains=kw)
		else:
			return render_to_response('search/search.html',context_instance=RequestContext(request))
			
	elif request.GET.has_key('search_text'):
		sw = request.GET['search_text']
		if sw is not u"" and test_search_word(sw):
			U = User.objects.filter(Q(nm_person__icontains=sw)|Q(fstnm_person__icontains=sw))
			if request.session.has_key('login'):
				EF = EnsFile.objects.filter(Q(name_ensfile__icontains=sw)|Q(desc_ensfile__icontains=sw)|Q(origin__icontains=sw))
			else:
				EF =EnsFile.objects.filter(Q(name_ensfile__icontains=sw)|Q(desc_ensfile__icontains=sw)|Q(origin__icontains=sw)).filter(public=True)
			G = Group.objects.filter(Q(name_group__icontains=sw)|Q(desc_group__icontains=sw))
			T = Tool.objects.filter(Q(name_tool__icontains=sw)|Q(desc_tool__icontains=sw))
			if not request.session.has_key('login'):
				T = T.filter(visible=True)
			P = Page.objects.filter(Q(titre__icontains=sw)|Q(conf_raw__icontains=sw)|Q(abstract__icontains=sw))
		else:
			return render_to_response('search/search.html',context_instance=RequestContext(request))
	else:
		return render_to_response('search/search.html',context_instance=RequestContext(request))
	return render_to_response('search/search.html',{
		'u': U,
		'ef': EF,
		'g':G,
		't':T,
		'p':P,
		},context_instance=RequestContext(request))
