# -*- coding: utf-8 -*-
from django import forms
from django.db import connection, transaction
from django.shortcuts import get_object_or_404,render_to_response

from plato.models import User, File, Sound, Image, EnsFile, Tool, Author, ToolAuthor, TypeFile
import datetime
from util.object_util import *
from add_data.add_data import del_media_file_db

import os
from os import remove


# get the path from the "app" object database
def path_from_app(app):
	"""
	\brief The point of this method is to extract the path of the files from info in the page table
	\input{an app object from the database}
	\output{a string containing the path to the app object, needed for adding files}
	"""
	fpath = get_plato_path() # from util.object_util (/tsi/plato if it's plato-tsi)
	if app.group and app.visible:
		# The file is linked to a project
		path = "/%s/plato_projects/%s/public/tools/%s/"%(fpath,app.group.name_group, app.name_tool)
	elif app.group and not app.visible:
		# The file is linked to a project AND is public
		path = "/%s/plato_projects/%s/private/tools/%s/"%(fpath,app.group.name_group, app.name_tool)		
	else:
		# The file is linked to a person account 
		path = "/%s/plato_users/%s/tools/%s/"%(fpath,app.manager.login, app.name_tool)
	
	return path

############################# DEL THE APP ############################

def del_tool_db(na):
	"""
	\brief  del a tool in the db !
	\input{na is the id of the app (don't know why i'm loading a app object before and know a id...)}
	\output{no output}
	"""
	#### To do :
	# - verify del media ok
	
	a = get_object_or_404(Tool,id_tool = na)
	#get the object for destrying it
	for f in a.files.all():
		del_media_file_db(f.id_file)
		# get the files and delete them into the database
	for f in a.tool_figures.all():
		del_media_file_db(f.id_file)
		# get the figures and delete them into the database
	flag = rm_dirs(path_from_app(a))
	# know destroy the actual files into the file system
	a.demo_set.clear()
	a.delete()
	# NOW delete the object in the database

	# [TO DO] Should test if the delete is working
	
################################ ADD APP #############################

from django.db.models import Q
from plato.models import PageAuthor
def add_author_to_tool(tool,author):
	"""
	\brief add the author into PageAuthor for publication
	\input{tool: the tool object; author: the author string passed through the form}
	\output{NA}
	"""
	# split the name by commas [TO DO : test with ';' or ' ' if there's too much space ...]
	la = author.split(',')
	ordr = 1
	for a in la:
		fnm=a.split(' ') # now a is a full name, so we split into space
		# for 'jean dupond' it works fine,
		# for 'jena-claude dupond aillor' it works fine,
		# for 'jean jean petitjean of doom' will create a person name 'jean' 'jean petitjean of doom' insted of 'jean jean' 'petitjean of doom'
		try:
			fnm.remove('')# delete the space at the endbecause "jean petit, pierre legrand " => la = ['jean petit',' pierre legrand '] and a=['','pierre','legrand',''] => this step transform ['pierre','legrand'] 
		except:
			pass
				
		first_name = unicode(titlecase(fnm[0])) # titlecase is in object_util: jean => Jean
		length = len(fnm) # the number if name put by the user
		ran = range(1,length)
		list_nom = [fnm[i] for i in ran]
		name = unicode(titlecase(' '.join(list_nom)))# create the name with the rest of the name

		# improve the comparison for author retrieval
		auth = Author.objects.filter(Q(nm__iexact = name,fstnm__iexact = first_name))
		if auth:
			pa = ToolAuthor(author=auth[0], tool=tool, order=ordr) # tool is needed only for this !
		else:
			n_author=add_author_from_nm(first_name, name) # really ? add an author is not that hard !
			pa = ToolAuthor(author=n_author, tool=tool, order=ordr)
		pa.save()
		ordr=ordr+1

########################### ADD APP (i mean really) ############################

import string
def add_tool_db(form,user):
	"""
	\brief add the tool into the database
	\input{form: is the python object with all the information for adding the tool, user : user object for knowing who is the manager}
	\output{return the new tool object}
	"""

	# get the form information, if the field is empty then None is passed to the database
	desc_s =form.cleaned_data['desc']	
	name = form.cleaned_data['name']
	webp = form.cleaned_data['webp']
	code_type = form.cleaned_data['code_type']
	version = form.cleaned_data['version']
	licence = form.cleaned_data['licence']
	gpe = form.cleaned_data['gpe']
	author =form.cleaned_data['author']
	KW = form.cleaned_data['KW']
	visible = form.cleaned_data['public']
	
	date= datetime.date.today()

	#ajout des informations add the informations into 
	tool = Tool(name_tool=name, version_tool=version, desc_tool=desc_s,  webpage_tool=webp, manager=user, date_creation=date, date_modification=date, licence=licence, type_tool=code_type, group=gpe, all_f=True, visible=visible)
	tool.save()

	if author:
		add_author_to_tool(tool,author) # just up ! 
	add_kw(tool,KW) # add keyword to the tool (in util.object_util)
	
	return tool


def add_tool_f_db(user,file,mede,tool):
	"""
	\brief add the files linked to a tool
	\input{user : the manager of the files; file : the file that must added to the tool(file object); mede : python object filled with the metadata of the file, tool : the tool object}
	\output{return the file }
	"""
	
	name = os.path.splitext(file.name)[0] #name of the file 
	size = file.size #its size
	typ = def_typ(mede) # define the MIME type
	type=get_object_or_404(TypeFile, id_type_file=typ) # look for the type into the database
	path = path_from_app(tool) + file.name # then compute the path from infos in the tool
	# add the file to the database 
	f = File(name_file = name, desc_file = tool.desc_tool, size_file= size, path=path, type_file = type, manager = user,date_creation = datetime.date.today(), date_modification = datetime.date.today(), date_del=datetime.date(9999,12,12) ,group=tool.group, all_f=True,visible=tool.visible)
	f.save()
	
	return f

###################### Update tool ########################
def upd_file_in_tool(tool,path):
	"""
	\brief Find all the files related to the tool AND change theirs path with the new !
	\input{tool : the tool object; path : the string containing the new path}
	"""
	import os
	if tool.help_file: # help file 
		tool.help_file.path = path + os.path.split(tool.help_file.path)[1]
		tool.help_file.save()
	if tool.files:
		for f in tool.files.all():
			f.path = path + os.path.split(f.path)[1]
			f.save()
	if tool.tool_figures:
		for f in tool.tool_figures.all():
			f.path = path + os.path.split(f.path)[1]
			f.save()


def upd_tool_db(form,user,tool):
	"""
	\brief Update the tool information
	\input{form : containing the informations of the tool; user : the manager; tool : tool object}
	"""

	# Get the information of the form
	desc_s =form.cleaned_data['desc']
	name = form.cleaned_data['name']
	webp = form.cleaned_data['webp']
	code_type = form.cleaned_data['code_type']
	version = form.cleaned_data['version']
	licence = form.cleaned_data['licence']
	gpe = form.cleaned_data['gpe']
	date= datetime.date.today()
	author =form.cleaned_data['author']
	KW = form.cleaned_data['KW']
	visible = form.cleaned_data['public']

	# get the path of the tool (above)
	src_path=  path_from_app(tool)

	# test if the information are in the object, then update them 
	if author:
		tool.author.clear()
		add_author_to_tool(tool,author)
	if name and name != tool.name_tool:
		tool.name_tool = name
		tool.save()
		dst = path_from_app(tool) #How to find dst ? 
		change_nm(src_path,dst)#change_nm !
		upd_file_in_tool(tool,dst)
		# now change the path OF ALL the file 
	if  version and version!= tool.version_tool:
		tool.version_tool = version
	if desc_s and unicode(desc_s) != unicode(tool.desc_tool):
		tool.desc_tool=desc_s
	if webp and webp != tool.webpage_tool:
		tool.webpage_tool = webp
	if licence and licence != tool.licence:
		tool.licence = licence
	if code_type and code_type != tool.type_tool:
		tool.type_tool = code_type

	if gpe and tool.group != gpe:
		tool.group=gpe
	elif tool.group and not gpe:
		tool.group=None
	if visible != tool.visible:
		tool.visible = visible

	tool.save()
	dst = path_from_app(tool)
	if dst != src_path:
		change_grp_all_f(src_path,dst)#change_nm !
		upd_file_in_tool(tool,dst)
		
	# change_group_all_f !
	tool.date_modification = date
	
	tool.KW.clear()
	add_kw(tool,KW)
	tool.save()
		
	return tool

def upd_publi_code(form_publi,tool):
	pages = form_publi.cleaned_data['publi']
	if pages:
		tool.page_set.clear()
		tool.save()
		for p in pages:
			p.tool.add(tool)
			p.save()
		
		

def upd_demo_code(form_demo,tool):
	demos = form_demo.cleaned_data['demo']
	if demos:
		tool.demo_set.clear()
		tool.save()
		for d in demos:
			d.tool = tool
			d.save()

def upd_ensfile_code(form_ensfile,tool):
	efs = form_ensfile.cleaned_data['ensfile']
	if efs:
		tool.ensfile.clear()
		tool.save()
		for ef in efs:
			tool.ensfile.add(ef)
			tool.save()
		
		
