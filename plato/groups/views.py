# -*- coding: utf-8 -*-
# Create your views here.
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from plato.models import Group, User

from util.object_util import is_logged
from util.views import *
from groups.n_groups import *

from plato.form import NgrpForm

##############################################################################################
	######################### WIKI_GROUP : Working On Groups ########################################
##############################################################################################


def vgrps(request):
	"""
	\brief view all the group
	"""
	if request.session.has_key('login'):
		me = get_object_or_404(User,login=request.session['login'])
		ngrp = me.group_users.all().values_list('id_group')
	
		grps = Group.objects.filter(~Q(type_group__id_type_group=2) | Q(id_group__in = ngrp)).order_by('-date_creation')
	else:
		grps = Group.objects.exclude(type_group__id_type_group=2).order_by('-date_creation')
		
	grps = pagination(grps, request.GET.get('page','1'))		
	return render_to_response('groups/groups.html', {'gpes':grps},context_instance=RequestContext(request))

def vgrp(request, ngpe):
	"""
	\brief View group info
	\author{B.Petitpas}
	\date{16/05/2012}
	\version{1}
	"""
	g = get_object_or_404(Group,id_group=ngpe)
	f = False

	if request.session.has_key('login'):
		me = get_object_or_404(User,login=request.session['login'])
		if g.manager == me:# if the connected person is the boss => can modify and delete the group !
			f= True
	else:
		me = get_object_or_404(User,login='guest')
	if g.type_group.id_type_group == 1: # if the group is public => show classicaly
		return render_to_response('groups/group.html', {'gpe':g, 'f':f},context_instance=RequestContext(request))
	else: # we should verify if the user is in the group 
		if me in [u for u in g.users.all()] : #the user is a member 
			return render_to_response('groups/group.html', {'gpe':g, 'f':f},context_instance=RequestContext(request))
		else:
			return return_referer(request) #redirect(request.META['HTTP_REFERER'])
		
	return redirect('usr', log=request.session['login'])

