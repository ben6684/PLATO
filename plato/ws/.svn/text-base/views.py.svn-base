# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse

from util.object_util import *
from plato.models import User


def add_data_from_inline(request):
	if request.GET.has_key('login'):
		try:
			log = get_object_or_404(User,login=request.GET['login'])
			html = "le user est .... "
			html += log.login
			return HttpResponse(html)
		except:
			return HttpResponse("PROUT")
	else:
		return HttpResponse("PROUT")
