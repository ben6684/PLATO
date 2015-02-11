# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from plato.models import Group, User

from util.object_util import is_logged
from util.views import *
from groups.n_groups import *

from plato.form import NgrpForm

from django.core.mail import mail_admins, send_mail



@is_logged
def ngrp(request, log):
	"""
	\brief Create a new  group 
	\author{B.Petitpas}
	\date{16/05/2012}
	\version{1}
	"""
	if log==request.session['login'] and request.session['status']=="permanent":# this is for avoiding to add a group if you're not connected
		usr = User.objects.get(login=log)
		if request.method == 'POST': #the form has been submitted
			form = NgrpForm(request.POST,request.FILES,prefix='form_group')
			if form.is_valid(): #validation rules pass
				if Group.objects.filter(name_group = form.cleaned_data['nom']):#we should verify if the name already exists
					return render_to_response('groups/new_group.html',{'form': form, 'log':log,'error_message' : "this group already exists",}, context_instance=RequestContext(request) )
				else:
					gpe=add_grp(form,log)# go to add for adding a new user 
					if request.FILES.has_key('profil'):
						handle_uploaded_profil(request.FILES['profil'],gpe.name_group,True)

					#now send a mail to say that a group is created
					send_mail("[PLATO] New group : %s"%(gpe.name_group),"created by %s \n \n with \n %s"%(gpe.manager, "\n".join(mem.login for mem in gpe.users.all())),"New_Group@plato.enst.fr",['petitpas@telecom-paristech.fr'],fail_silently=False)
					
					return redirect('grp', ngpe=gpe.id_group)
			else: #the formula is not valid
				if request.session['lang']=='fr':
					form=trans_label_fr(form)	
				return render_to_response('groups/new_group.html', {'form': form, 'log':log, 'error_message' : form.errors ,}, context_instance=RequestContext(request))
		else:
			form = NgrpForm(prefix='form_group')
			if request.session['lang']=='fr':
				form=trans_label_fr(form)	
			return render_to_response('groups/new_group.html',{'form': form, 'log':log,} , context_instance=RequestContext(request))
   	else:
		return redirect('idx')


@is_logged
def updgrp(request, ngpe):
	"""
	\brief Update group info
	\author{B.Petitpas}
	\date{21/05/2012}
	\version{1}
	"""
	usr = get_object_or_404(User,login=request.session['login']) #we take the info on the connected guy
	gpe = get_object_or_404(Group,id_group=ngpe)
	if gpe.manager == usr or gpe.manager.id_user == user.id_boss: #the conected person IS the group manager
		if request.method == 'POST': #the form has been submitted
			form = NgrpForm(request.POST,request.FILES,prefix='form_group')
			if form.is_valid(): #validation rules pass
				gpr_n=upd_grp(form,usr.login,ngpe)# go to update group info	
				if request.FILES.has_key('profil'):
					handle_uploaded_profil(request.FILES['profil'],gpr_n.name_group,True)	
				return redirect('grp', ngpe=ngpe)
			else: #the formula is not valid
				if request.session['lang']=='fr':
					form=trans_label_fr(form)	
				return render_to_response('groups/update_group.html', {'form': form, 'ngpe':ngpe, 'error_message' : form.errors ,}, context_instance=RequestContext(request))
		else:
			kw =  ",".join([unicode(a) for a in gpe.KW.all()])
			form = NgrpForm(initial={'nom':gpe.name_group,'description':gpe.desc_group,'KW':kw,'website':gpe.website,'date_exp':gpe.date_del, 'isvis':gpe.type_group, 'email':gpe.email},prefix='form_group')
			form.fields['members'].initial = gpe.users.all()
			if request.session['lang']=='fr':
				form=trans_label_fr(form)	
			return render_to_response('groups/update_group.html',{'form': form, 'ngpe':ngpe,} , context_instance=RequestContext(request))
	else: #he is not the group manager
		return redirect('grp', ngpe=ngpe)

@is_logged
def dltgrp(request, ngpe):
	"""
	\brief delete a group 
	\author{B.Petitpas}
	\date{21/05/2012}
	\version{1}
	"""

	g = get_object_or_404(Group, id_group=ngpe)
	usr = get_object_or_404(User, login = request.session['login'])
	if g.manager== usr or g.manager.id_user == user.id_boss:# the loggued person IS the group manager
		#del_grp(g)
		g.delete()
		return redirect('usr', log=request.session['login'])
	else:
		return redirect('grp', ngpe=ngpe)

@is_logged
def dltuig(request, ngpe, log):
	"""
	\brief delete a member of a group 
	\author{B.Petitpas}
	\date{22/05/2012}
	\version{1}
	"""
	g = get_object_or_404(Group, id_group=ngpe)
	p = get_object_or_404(User, login = request.session['login'])
	u = get_object_or_404(User, login = log)
	if g.manager== p or g.manager.id_user == p.id_boss :# the loggued person IS the group manager and not the loggued person (the manager can't delete itself !)
		#del_usrIgrp(g,u)
		if u == g.manager:
			if u.id_boss:
				boss = get_object_or_404(User, id_user=u.id_boss)
				g.manager = boss
				g.save()
			else:
				boss = get_object_or_404(User, id_user='912')
				g.manager = boss
				g.save()
		g.users.remove(u)
		return redirect('grp', ngpe=ngpe)
	else:
		return redirect('grp', ngpe=ngpe)

@is_logged	
def dltgiu(request, log, ngpe):
	"""
	\brief delete a group in the user page (the user is no longer in the group)
	\author{B.Petitpas}
	\date{22/05/2012}
	\version{1}
	"""
	
	if log != request.session['login']:# the person isn't the user
		return redirect('usr', log = request.session['login'])
	else:
		g = get_object_or_404(Group, id_group=ngpe)
		u = get_object_or_404(User, login = log)
		if g.manager == u:# the loggued person IS the group manager=> can't delete itself => to modify in the futur!
			return redirect('usr', log=log)
		else:
			#del_usrIgrp(g,u)
			g.users.remove(u)
			return redirect('usr', log=log)
		
