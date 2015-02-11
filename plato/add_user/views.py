# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django import forms
from django.db import connection, transaction
from django.db.models import Q
from django.template import RequestContext
from django.core.urlresolvers import reverse

from plato.models import User, Group, EnsFile, Page, Tool
from util import auth, object_util
from util.object_util import *
from util.views import *

from add_user.n_users import *

from groups.views import *
from users.views import *

import datetime

from plato.form import *

##############################################################################################
	######################### Working On Users ##########################################
##############################################################################################
	
def nusr(request, log):
	"""
	\brief Form for saving an existing member of TSI in database
	\author{B.Petitpas}
	\date{03/05/2012}
	\version{1}
	"""
	if(log==request.session['login']):#you can't change information if it's not yours ! 
	    #try to get a user object with a login check in the db
		if request.method == 'POST': #the form has been submitted
			form = NusrForm(request.POST,request.FILES)
			if form.is_valid(): #validation rules pass
				sta = form.cleaned_data['status']
				# if request.session['status']!="permanent" and not form.cleaned_data['boss']:# the user is not permanent and didn't choose a referent=> go pick one !
				# 	return render_to_response('add_user/new_user.html', {'form': form, 'log':log, 'error_message' : "As a non permanent please choose a referent" }, context_instance=RequestContext(request))
				
				if sta.id_user_status==1 and request.session['status']!="permanent":# the user said he is a permanent but the ldap says that is not 
					return render_to_response('add_user/new_user.html', {'form': form, 'log':log, 'error_message' : "You're not permanent so choose another status" }, context_instance=RequestContext(request))	
				else: #you're perfect => ADD a new user
					# we add the image where it's supposed to be
					add_user(form,log)# go to add for adding a new user 
					if request.FILES.has_key('profil'):
						handle_uploaded_profil(request.FILES['profil'],log) #=> add the picture into the folder create for the occasion
					request.session['actif']=True #due to plato.log.view => mean now you're activated 
					return redirect('usr', log=log)
			else: #the formula is not valid
				form.fields['group'].initial = [g.pk for g in Group.objects.filter(pk__lte=5)]
				if request.session['lang']=='fr':
					form=trans_label_fr(form)	
				return render_to_response('add_user/new_user.html', {'form': form, 'log':log, 'error_message' : form.errors }, context_instance=RequestContext(request))	
			
		else:
			if request.session['status']=="permanent":#if the user is a permanent
				form = NusrForm(initial={'nom':request.session['name'], 'prenom':request.session['fstname'], 'status':get_object_or_404(UserStatus,pk=1), 'bio':"<b>%s %s</b>"%(request.session['fstname'],request.session['name'])}) #show the formular if it's not submitted
			else:
				form = NusrForm(initial={'nom':request.session['name'], 'prenom':request.session['fstname'],'bio':"<b>%s %s</b>"%(request.session['fstname'],request.session['name'])})
				form.fields['status'].queryset = UserStatus.objects.exclude(pk=1)#second security for a phd condidat not to put himself as a permanent.
			
			form.fields['group'].initial = [g.pk for g in Group.objects.filter(pk__lte=5)]
			#Translate the form
			if request.session['lang']=='fr':
				form=trans_label_fr(form)	
			return render_to_response('add_user/new_user.html', {'form': form,'log':log}, context_instance=RequestContext(request))#for cross site reference validation
	else:
		#Translate the form
		if request.session['lang']=='fr':
			form=trans_label_fr(form)	
		return render_to_response('add_user/new_user.html', {'form': form, 'log':log, 'error_message' : "You can't add a new user if you're not a member of TSI" }, context_instance=RequestContext(request))


	
def updusr(request, log):
	"""
	\brief update the user info !
	\author{B.Petitpas}
	\date{16/05/2012}
	\version{1}
	"""
	if(log==request.session['login']):#if your not the name passed in argument, you can't update 
		usr = User.objects.get(login=log)
		if request.method == 'POST': #the form has been submitted
			form = NusrForm(request.POST,request.FILES)
			if form.is_valid(): #validation rules pass
				# if request.session['status']!="permanent" and not form.cleaned_data['boss']:# the user is not permanent and didn't choose a referent=> go pick one !
				# 	return render_to_response('add_user/update.html', {'form': form, 'log':log, 'error_message' : "As a non permanent please choose a referent" }, context_instance=RequestContext(request))
				# else:#or you're a permanent and do as you want or you're a non permanent and you pick a referent
				upd_user(form,log)# go to add for adding a new user
				if request.FILES.has_key('profil'):
					handle_uploaded_profil(request.FILES['profil'],log)
				return redirect('usr', log=log)
			else: #the formula is not valid
			    #Translate the form
				if request.session['lang']=='fr':
					form=trans_label_fr(form)	
				return render_to_response('add_user/update.html', {'form': form, 'log':log, 'error_message' : form.errors }, context_instance=RequestContext(request))	
		else:
			#gpe = ListUsers.objects.filter(login=log)

			form = NusrForm(initial={'nom':usr.nm_person, 'prenom':usr.fstnm_person, 'webp':usr.webpage_person, 'email':usr.email_person, 'site':usr.office, 'status':usr.status, 'tel': usr.telephone, 'boss':usr.id_boss ,})
            #Show the form if it's not submitted
			
			#Find the biographie information and display them => if empty then it displays the language
			if usr.biographie:
				form.fields['bio'].initial=usr.biographie
			else:
				form.fields['bio'].initial = "<b>English</b>"
			if usr.biographie_fr:
				form.fields['bio_fr'].initial=usr.biographie_fr
			else:
				form.fields['bio_fr'].initial = "<b>Français</b>"

			#Fill the initial values of groups
			form.fields['group'].initial = usr.group_users.all()
			if request.session['status']!="permanent": #if the user is not a permanent
				form.fields['status'].queryset = UserStatus.objects.exclude(pk=1)#second security for a phd condidat not to put himself as a permanent.

			#Translate the form
			if request.session['lang']=='fr':
				form=trans_label_fr(form)	
			return render_to_response('add_user/update.html', {'form': form,'log':log, }, context_instance=RequestContext(request))#for cross site reference validation
	else:
		# In the case of a people trying to update an other person account => return to the user account 
		return redirect('usr', log=log)


		
