# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.template import defaultfilters

from django.db import connection, transaction
from django.db.models import Q,Max

from plato.models import Tool,User, Page,File,ToolAuthor, Demo
from util.object_util import *

########################## Tool ###########################

def vcodes(request):
	"""
	\brief 
	"""	
	#fill_tool()
	if request.session.has_key('login'):
		me = get_object_or_404(User,login=request.session['login'])
		src = Tool.objects.all().order_by('-date_modification','name_tool')
	else:
		src = Tool.objects.filter(visible=True).order_by('-date_modification','name_tool')
		me = get_object_or_404(User,login='guest')### A CHANGER ####
	src=pagination(src,request.GET.get('page','1'))		
	return render_to_response('app/vcodes.html',{
		'src':src,
		'me':me,
		},context_instance=RequestContext(request))

def vcode(request,na):
	"""
	\brief Show more info about one particular tool
	"""
	algo = get_object_or_404(Tool,id_tool=na)
	if request.session.has_key('login'):
		me = get_object_or_404(User,login=request.session['login'])
	else:
		me = get_object_or_404(User,login='guest')### A CHANGER ####
		if not algo.visible:
			return redirect('sources_codes')
	publi =  Page.objects.filter(tool=algo)
	demo = Demo.objects.filter(tool=algo)
	algo_fig = algo.tool_figures.all().order_by('type_file__id_type_file')
	return render_to_response('app/vcode.html',{
		'a':algo,
		'publi':publi,
		'me':me,
		'algo_fig':algo_fig,
		'demos':demo,
		},context_instance=RequestContext(request))
