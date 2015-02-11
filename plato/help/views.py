# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template import RequestContext

def help(request):
	"""
	Show all the latest publication
	"""
	return render_to_response('help/help.html',context_instance=RequestContext(request))

def start(request):
	"""
	Show all the latest publication
	"""
	return render_to_response('help/start.html',context_instance=RequestContext(request))


def help_add_data(request):
	return render_to_response('add_data/help.html',context_instance=RequestContext(request))
