# Create your views here.
#a view is supposed to send a http object with the content of the page that will be shown in the templates

from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django import forms
from django.db import connection, transaction
from django.db.models import Q
from django.template import RequestContext
from django.core.urlresolvers import reverse

from plato.models import User, Group, EnsFile, Page, Tool, KW
from util import auth, object_util
from util.object_util import *
from util.views import *

import datetime

from plato.form import *


##############################################################################################
	###################################### INDEX ########################################
##############################################################################################

#def check_login(request):
def index(request, error=None):
	"""
	\brief{just render the index page, with the last publication, tools and data and the most viewed publication, tools and data}
	"""

	# publications are always render ! 
	lp = Page.objects.filter(flag_suppr=False).order_by('-id_page')[:5]

	# if logged => render all the tools, only the visible otherwise !
	if request.session.has_key('login'):
		lt = Tool.objects.all().order_by('-date_creation')[:5]
	else:
		lt = Tool.objects.filter(visible=True).order_by('-date_creation')[:5]

	# if logged => render all the data, public ones otherwise
	
	if request.session.has_key('login'):
		me = get_object_or_404(User,login = request.session['login'])
		lef = EnsFile.objects.filter(Q(public=True)|Q(group__in=me.group_users.all())).order_by('-date_creation')[:5]
	else:
		lef = EnsFile.objects.filter(public=True).order_by('-date_creation')[:5]

	ld = Demo.objects.all().order_by('-date_creation')[:5]

	if not request.session.has_key('lang'):
		request.session['lang'] = 'en' # create the 'lang' key in the cookies for multi langage support

	return render_to_response('users/index.html',{'lp': lp,'lt': lt,'lef': lef, 'ld':ld,'error_message':error}, context_instance=RequestContext(request))


##############################################################################################
	######################### Shows Users and User information ###########################
##############################################################################################
def show_users(request):
	"""
	\brief{view all the TSI personal, usrs are the currents persons, olds are the alumni }
	"""
	usrs = User.objects.exclude(nm_person__exact="guest").filter(actif=True).order_by('status','nm_person')
	olds = User.objects.exclude(nm_person__exact="guest").exclude(actif=True).order_by('status','nm_person')
	return render_to_response('users/usrs.html',{
		'usrs': usrs,
		'olds': olds,
		},context_instance=RequestContext(request))
	

def usr(request, log):
	"""
	\brief{View of personal info of the log person }
	\input{log : String that contains the log information}
	\author{B.Petitpas}
	\date{03/05/2012}
	\version{1}
	"""
	user = get_object_or_404(User,login=log)
	boss  = None
	if user.id_boss:
		boss = get_object_or_404(User,id_user=user.id_boss) # get the boss information
	flag = False
	if request.session.has_key('login'):
		if log == request.session['login']:
			flag= True # flag equal true if the connected person is the person that you want to see
		#sess = request.session.load()
	return render_to_response('users/usr.html',{
		'User': user,
		'f'   : flag,
		'boss': boss,
		},context_instance=RequestContext(request))


#error function 
def display_error(request,error):
	if not error:
		return render_to_response('error_msg.html',{'error_message' : "fill the formular please" },context_instance=RequestContext(request))
	else:
		return render_to_response('error_msg.html',{'error_message' : error},context_instance=RequestContext(request))
		


#function to change the langage into the cookie 'put that cookie down!'
def change_lang(request):
	"""
	take the 
	"""
	
	if request.GET.has_key('value'):
		v = request.GET['value']
		if v == 'fr': #french selected
			request.session['lang']='fr'
		else:
			request.session['lang']='en'
	#return HttpResponse(v)
	return return_referer(request)
	#return redirect(request.META['HTTP_REFERER'])
