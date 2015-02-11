# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django import forms
from django.db import connection, transaction
from django.db.models import Q
from django.template import RequestContext
from django.core.urlresolvers import reverse

from plato.models import User, Group, EnsFile
from util import auth, object_util
from util.object_util import *
from util.views import *

from add_user.n_users import *

from groups.views import *
from add_user.views import *
from users.views import *

import datetime

from plato.form import *


def loggin(request):
	"""
	\brief This is a fonction that get the information given by the users on the authorisation page and check the name of the user in the db and the pwd in the ldap
	\param[in] request: is the http request object 
	\param[in] login: user's login
	\param[in] pwd: usr's password
	\author{B.Petitpas}
	\date{02/05/2012}
	\version{1}
	"""

	#to do => accpete only 1 connection to ldap per seconde ! and only 10 from a single IP adress !
	#request = object_util.create_session(request)
    #try to get a user object with a login check in the db
	if request.method == 'POST': #the form has been submitted
		form = LoginForm(request.POST)
		if form.is_valid(): #validation rules pass
			log = form.cleaned_data['log']
			pwd = form.cleaned_data['pwd']
			usr_ = User.objects.filter(login=log)
			if not usr_:
				#check if the person exist in ldap
				server   = "ldap.enst.fr"
				userdn   = "uid=" + log + ",ou=People,dc=enst,dc=fr"
				status,errmsg,info = auth.check_user_pwd(request,server,userdn,pwd,True)
				if status > 0 :# the user exists in the ldap (the person is a tsi member) => creta a new user in PLATO database
					request.session['login']=log
					request.session['name']=info['name']
					request.session['fstname']=info['first_name']
					request.session['actif']=False
					#request.session.set_expiry(36000)
					
					if info.has_key('status'): # update from the 24 sept 2013 : verify that you've got a tsi status (meaning that you are : permaneent, phd, cdd, post-doc)!
						request.session['status']=info['status']
					else: # for person of tsi without a selected status (student, intern)
						request.session['status']=''
						
					return redirect('usr_n',log = log)
				else:
					# reshow the login/pwd page
					#request.META['HTTP_REFERER']
					return return_referer(request)
					# if request.META.has_key('HTTP_REFERER'): # return the last page visited 
					# 	return redirect(request.META['HTTP_REFERER'])
					# else:
					# 	return redirect('idx')
			else:
				# Check user password
				server   = "ldap.enst.fr"
				userdn   = "uid=" + log + ",ou=People,dc=enst,dc=fr"
				status,errmsg,info = auth.check_user_pwd(request,server,userdn,pwd,True)
				
				if status < 0: #ldap not accessible
					return return_referer(request)
					# if request.META.has_key('HTTP_REFERER'):
					# 	return redirect(request.META['HTTP_REFERER'])
					# else:
					# 	return redirect('idx')
					
				elif status ==0: #not a good password
					return return_referer(request)
					# if request.META.has_key('HTTP_REFERER'):
					# 	return redirect(request.META['HTTP_REFERER'])
					# else:
					# 	return redirect('idx')
					
				else: #it's working 
					usr_ = get_object_or_404(User,login=log)
					request.session['login']=log
					request.session['status']=info['status']
					request.session['name']=info['name']
					request.session['fstname']=info['first_name']
					request.session['actif']=usr_.actif
					return redirect('usr', log=log)
		else:
			return return_referer(request)
			# if request.META.has_key('HTTP_REFERER'):
			# 	return redirect(request.META['HTTP_REFERER'])
			# else:
			# 	return redirect('idx')
	# else:
	# 	if request.session.get('login',None):
	# 		return redirect('usr', log=request.session['login'])
	# 	else:
	# 		form = LoginForm() #show the formular if it's not submitted
	# 		return redirect('idx')

	return redirect('idx')


def disconnect(request):
	"""
	\brief{delete all the connexion information after clicking on disconnect}
	"""
	try:
		del request.session['login']
		del request.session['status']
		del request.session['name']
		del request.session['fstname']
		del request.session['actif']
		# del request.session
		# del request 
	except KeyError:
		pass
	return redirect('idx')
