from django import forms
from django.db import connection, transaction
from django.shortcuts import get_object_or_404
import datetime
from plato.models import User, Group, Author
"""
\brief n_users is a file defining fonction/method (stupid object langage) that handle add/modify/delete information on users !
\author : B. Petitpas
"""
		
def add_user(form,log):
	"""
	\brief add a user : To add a user, no need to fill a person before because with the inheritance a user will create automaticaly a person !
	\author : B. Petitpas
	"""
	# form.cleaned_data['field'] => get the data in the form field filled by the user
	# Normally the data into the fields are validated in the view so we get only good data

	# Get the infos And then add them to the data base !
	fstnm = form.cleaned_data['prenom']
	nm = form.cleaned_data['nom']
	webp = form.cleaned_data['webp']
	if not webp:
		webp = "http://perso.telecom-paristech.fr/~%s/"%log #even if it's empty, it's something => i'm not sure if it's really a good idea ...
	email =form.cleaned_data['email']
	if not email:
		email = "%s.%s@telecom-paristech.fr"%(fstnm,nm)#even if it's wrong, it's something !
	site = form.cleaned_data['site']
	status = form.cleaned_data['status']
	date_exp = datetime.date(9999,12,12) # expiration date by default => means indefinitively !
	today = datetime.date.today() # for calculation
	if status.id_user_status == 2: # CDD => max = 7 years
		date_exp = datetime.date(today.year + 7,today.month,today.day)
	elif status.id_user_status == 3: # phd => max = 4 years
		date_exp = datetime.date(today.year + 4,today.month,today.day)
	elif status.id_user_status == 4: # post-doc => max = 3 years
		date_exp = datetime.date(today.year + 3,today.month,today.day)
	elif status.id_user_status == 5: # stagiaire => max = 1 years
		date_exp = datetime.date(today.year + 1,today.month,today.day)		
	date= str(date_exp)
	tel = form.cleaned_data['tel']
	boss = form.cleaned_data['boss']
	bio = form.cleaned_data['bio']
	bio_fr = form.cleaned_data['bio_fr']
	group = form.cleaned_data['group']

	# Add the data to the database 
	# test to see if the user already exists :
	User_ = User.objects.filter(login=log,fstnm_person = fstnm, nm_person = nm)
	if User_:
		for g in group:
			g.users.add(User_[0])
			g.save()
		return User_[0]

	# if the user doesn't exist then add it to the database
	usr = User(fstnm_person = fstnm, nm_person = nm, email_person = email, webpage_person = webp, telephone=tel, status = status, office = site, account_expiration_date = date_exp,login = log, biographie=bio, biographie_fr=bio_fr)
	if boss:
		usr.id_boss = boss.id_user
	for g in group:
		g.users.add(usr)
		g.save()
	usr.save()

	#### Test for a mathc between a new user and a former author (added by someone else!) ####
	##### Not working really fine ####
	t_author = Author.objects.filter(nm__iexact=nm).filter(fstnm__istartswith=fstnm[0])
	if t_author: # if the author exists, then link the author to the new user 
		a = t_author[0]
		a.id_user = usr
		a.fstnm=fstnm
		a.save()
	else: # if the author doesn't exist, the nadd it into the database
		n_a = Author(nm = nm, fstnm=fstnm, fstnm_i = fstnm[0],id_user=usr) 
		n_a.save()
	################### End test ##############################################################

	
	return usr
	
def upd_user(form,log):
	"""
	\brief update info of a user : To upd a user, no need to fill a person before because with the inheritance a user will create automaticaly a person !
	\author : B. Petitpas
	"""

	# Get the data from the form 
	fstnm = form.cleaned_data['prenom']
	nm = form.cleaned_data['nom']
	webp = form.cleaned_data['webp']
	if not webp:
		webp = "http://perso.telecom-paristech.fr/~%s/"%log #even if it's empty, it's something
	email =form.cleaned_data['email']
	if not email:
		email = "%s.%s@telecom-paristech.fr"%(fstnm,nm)#even if it's wrong, it's something
	site = form.cleaned_data['site']
	status = form.cleaned_data['status']
	date_exp = datetime.date(9999,12,12) # expiration date by default
	today = datetime.date.today() # for calculation
	if status.id_user_status == 2: # CDD => max = 7 years
		date_exp = datetime.date(today.year + 7,today.month,today.day)
	elif status.id_user_status == 3: # phd => max = 4 years
		date_exp = datetime.date(today.year + 4,today.month,today.day)
	elif status.id_user_status == 4: # post-doc => max = 3 years
		date_exp = datetime.date(today.year + 3,today.month,today.day)
	elif status.id_user_status == 5: # stagiaire => max = 1 years
		date_exp = datetime.date(today.year + 1,today.month,today.day)		
	date= str(date_exp)
	tel = form.cleaned_data['tel']
	boss = form.cleaned_data['boss']
	bio = form.cleaned_data['bio']
	bio_fr = form.cleaned_data['bio_fr']

	# Get the user info !
	usr = get_object_or_404(User,login=log)

	# update the info with the infos 
	usr.fstnm_person = fstnm
	usr.nm_person =nm
	usr.webpage_person = webp
	usr.email_person = email
	usr.status = status
	usr.office = site
	usr.account_expiration_date = date_exp
	usr.telephone=tel
	usr.id_boss = boss
	usr.biographie = bio
	usr.biographie_fr = bio_fr	
	lst_g = usr.group_users.all()
	for g in lst_g:
		g.users.remove(usr)
	group = form.cleaned_data['group']
	for g in group:
		g.users.add(usr)

	# save the user into the database
	usr.save()
