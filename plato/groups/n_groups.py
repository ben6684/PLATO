# -*- coding: utf-8 -*-
from django import forms
from django.db import connection, transaction
from django.shortcuts import get_object_or_404
import datetime
from plato.models import User, Group,KW
from util.object_util import *
"""
\brief Grpusr is a file defining fonction/method (stupid object langage) that handle add/modify/delete information on users and on groups!
\author : B. Petitpas
"""


def add_grp(form,log):
	"""
	\brief add a group
	\author : B. Petitpas
	"""
	name = form.cleaned_data['nom']
	desc = str_s(form.cleaned_data['description'])
	members = form.cleaned_data['members']
	date = form.cleaned_data['date_exp']
	if not date:
		date = datetime.date(9999,12,12)
	web = form.cleaned_data['website']
	email = form.cleaned_data['email']
	keyw = form.cleaned_data['KW']
	boss = get_object_or_404(User,login=log)
	#isvis = type_group!
	isvis = form.cleaned_data['isvis']
	
	
	g = Group(name_group= name, desc_group=desc, date_del = date, date_creation = datetime.date.today(), date_modification =datetime.date.today(), email = email, website= web, manager=boss, type_group = isvis)
	g.save()
	for m in members:
		g.users.add(m)
	if not boss in members:
		g.users.add(boss)
	add_kw(g,keyw)
	return g
	
def upd_grp(form,log,ngpe):
	"""
	\brief update info on a group
	\author : B. Petitpas
	"""
	name = form.cleaned_data['nom']
	desc = str_s(form.cleaned_data['description'])
	desc = desc.decode('latin-1')
	members = form.cleaned_data['members']
	date = form.cleaned_data['date_exp']
	if not date:
		date = datetime.date(2099,12,31)
	email = form.cleaned_data['email']
	web = form.cleaned_data['website']
	keyw = form.cleaned_data['KW']
	isvis = form.cleaned_data['isvis']
		
	gpe = get_object_or_404(Group,id_group=ngpe)
	gpe.name_group = name
	gpe.desc_group = desc
	gpe.date_del = date
	gpe.date_modification = datetime.date.today()
	gpe.email = email
	gpe.website = web
	gpe.type_group = isvis

	gpe.users.clear()
	gpe.KW.clear()
	
	for m in members:
		gpe.users.add(m)
	add_kw(gpe, keyw)
	return gpe

# def del_grp(g):
# 	"""
# 	\brief delete info on a group
# 	\input a GroupUsers object
# 	\author : B. Petitpas
# 	"""
# 	# we delete info on pers_belong_group then we delete the GroupUsers
# 	# We can't use the delete operation of django because of the oid

# 	cursor = connection.cursor()

# 	gg=get_object_or_404(GroupUsers, id_group = g.id_group)
	
# 	cursor.execute("""DELETE FROM group_users WHERE id_group = '%s' """%(g.id_group))
# 	cursor.execute("""DELETE FROM authorisation WHERE id_gpe = '%s' """%(g.id_group))
	
# 	cursor.close()
# 	transaction.commit_unless_managed()	
	

# def del_usrIgrp(g,u):
# 	"""
# 	\brief delete a user in a group and a group for a user !
# 	\input a GroupUsers object and a user object
# 	\author : B. Petitpas
# 	"""
	
# 	cursor = connection.cursor()
# 	cursor.execute("""DELETE FROM pers_belong_grp WHERE id_group = '%s' AND id_person='%s'"""%(g.id_group,u.id_person))
# 	cursor.execute("""UPDATE group_users SET modification_date='%s' WHERE id_group=%s"""%(datetime.date.today(),g.id_group))
# 	cursor.close()
# 	transaction.commit_unless_managed()
