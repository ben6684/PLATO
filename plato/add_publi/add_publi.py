# -*- coding: utf-8 -*-
from django import forms
from django.db import connection, transaction
from django.shortcuts import get_object_or_404,render_to_response

from plato.models import User, File, Page, EnsFile, TypeFile, Author, PageAuthor, PageFigures,Tool, Frames,DemoPubli
import datetime
from util.object_util import *
import os
from os import remove, rmdir
from add_data.add_data import del_media_file_db, path_from_ensfile
from add_app.add_app import add_author_to_tool

def path_from_page(page,user=None):
	"""
	\brief : the point of this method is to extract the path of the files from info in the page table
	"""
	fpath = get_plato_path()
	if page.group:
		# The file is linked to a project
		path = "/%s/plato_projects/%s/public/publications/%s/"%(fpath,page.group.name_group, page.titre)
	elif not user:
		# The file is nto linkedto a group AND have to be public
		path = "/%s/plato_users/%s/publications/%s/"%(fpath,page.manager.login, page.titre)
	else:
		# The file is nto linkedto a group AND have to be public
		path = "/%s/plato_users/%s/publications/%s/"%(fpath,user.login, page.titre)
	
	return path

def add_files_to_page(user,file,mede,page):
	
	name = os.path.splitext(file.name)[0]
	size = file.size
	if mede:
		typ = def_typ(mede)
	else:
		typ = 7
	type=get_object_or_404(TypeFile, id_type_file=typ)
	if page.manager != user:
		path = path_from_page(page,user) + file.name
	else:
		path = path_from_page(page) + file.name
	
	f = File(name_file = name, size_file= size, path=path, type_file = type, manager = user,date_creation = datetime.date.today(), date_modification = datetime.date.today(), date_del=datetime.date(9999,12,12) ,group=page.group, all_f=True)
	f.save()

	return f

def del_page_db(np):
	"""
	\brief  del a source in the db !
	"""
	page = get_object_or_404(Page, id_page= np)
	for f in page.figures.all():
		del_media_file_db(f.id_file)
	if page.id_presentation:
		try:
			remove(str(page.id_presentation.path))
		except:
			print "%s doesn't exits"%(page.id_presentation.path)
		page.id_presentation.delete()
	if page.id_article:
		try:
			remove(str(page.id_article.path))
		except:
			print "%s doesn't exits"%(page.id_article.path)
		page.id_article.delete()
	patt= path_from_page(page)

	flag = rm_dirs(patt)
	page.delete()
	if flag:
		return True
	else:
		return False

def del_page_file_db(page,nf):
	f = get_object_or_404(File, id_file = nf)
	pf = get_object_or_404(PageFigures, figures = f, page = page)
	pf.delete()
	del_media_file_db(f.id_file)


####################################################################################################

def add_author_from_nm(fstnm, nm):
	"""
	\brief : add an author not into the base for publication pages

	"""
	a = Author(fstnm=fstnm, nm=nm, fstnm_i = fstnm[0])	
	P = User.objects.filter(nm_person = nm, fstnm_person = fstnm)
	if P:
		a.id_user = P[0].id_user
	a.save()
	return a

from django.db.models import Q
def add_author_to_page(p,author):
	"""
	\brief add the author into PageAuthor for publication
	"""
	la = author.split(',')
	ordr = 1
	for a in la:
		fnm=a.split(' ')
		try:
			fnm.remove('')
		except:
			pass
		
		first_name = unicode(titlecase(fnm[0]))
		length = len(fnm)
		ran = range(1,length)
		list_nom = [fnm[i] for i in ran]
		name = unicode(titlecase(' '.join(list_nom)))
		
		auth = Author.objects.filter(Q(nm =name,fstnm = first_name))
		if auth:
			pa = PageAuthor(author=auth[0], page=p, order=ordr)
			pa.save()
			ordr=ordr+1
		else:
			n_author=add_author_from_nm(first_name,name)
			pa = PageAuthor(author=n_author, page=p, order=ordr)
			pa.save()
			ordr=ordr+1

def add_conf_from_titre(titre):
	"""
	\brief : add a conference to the list !

	"""
	c = Conf(titre_conf= titre)
	c.save()
	return c

from plato.models import Conf
def add_page_db(form,user):
	"""
	\brief: add a publication page
	"""
	title = form.cleaned_data['title']
	conference = form.cleaned_data['conference']
	annee = form.cleaned_data['annee']
	mon = form.cleaned_data['mois']
	abstract = form.cleaned_data['abstract']
	algo = form.cleaned_data['algo']
	demo = form.cleaned_data['demo']
	grp = form.cleaned_data['gpe']
	KW = form.cleaned_data['KW']
	links = form.cleaned_data['links']
	
	page = Page(titre = title, conf_raw=conference, annee=annee, mon=mon, abstract=unicode(abstract), publication_date=datetime.date.today(),manager=user)
	page.save()
	
	add_kw(page,KW)
	for a in algo:
		page.tool.add(a)
	for d in demo:
		dp = DemoPubli(demo=d,page=page)
		dp.save()
	if grp:
		page.group = grp

	page.save()
	if links:
		llinks = links.split(',')
		for l in llinks:
			f = Frames(publi=page, link=l.lstrip().replace("watch?v=","embed/"))
			f.save()
	
	return page

def upd_file_in_publi(publi,path):
	"""
	\brief Find all the files related to the publi AND change theirs path with the new !
	"""
	import os
	if publi.id_presentation:
		nm_f = os.path.split(publi.id_presentation.path)[1] # name of the file
		publi.id_presentation.path = path + nm_f # new path + name file
		publi.id_presentation.save()
	if publi.id_article:
		nm_f = os.path.split(publi.id_article.path)[1]
		publi.id_article.path = path + nm_f
		publi.id_article.save()
	if publi.figures:
		for f in publi.figures.all():
			nm_f = os.path.split(f.path)[1]
			f.path = path + nm_f
			f.save()

			
def upd_page_db(page,form):
	"""
	\brief: upd a publication page except the file that will be manage elsewhere
	"""
	#title = form.cleaned_data['title']
	#conference = form.cleaned_data['conference']
	#annee = form.cleaned_data['annee']
	#mon = form.cleaned_data['mois']
	abstract = form.cleaned_data['abstract']
	algo = form.cleaned_data['algo']
	demo = form.cleaned_data['demo']
	#author = form.cleaned_data['author']
	grp = form.cleaned_data['gpe']
	links = form.cleaned_data['links']
	KW = form.cleaned_data['KW']

	src_path = path_from_page(page)

	# if author:
	# 	page.author.clear()
	# 	add_author_to_page(page,author)
	# if title and titlecase(title) != titlecase(page.titre):
	# 	page.titre = title
	# 	page.save()
	# 	dst = path_from_page(page) #How to find dst ? 
	# 	change_nm(src_path,dst)#change_nm !
	# 	upd_file_in_publi(page,dst)
	# if conference and conference != page.conf_raw:
	# 	page.conf_raw = conference
	# if annee and annee != page.annee:
	# 	page.annee = annee
	# if mon and mon != page.mon:
	# 	page.mon = mon
	if abstract and unicode(abstract) != unicode(page.abstract):
		page.abstract =unicode(abstract)
	if algo:
		page.tool.clear()
		for a in algo:
			page.tool.add(a)
	if demo:
		page.publi_demos.clear()
		for d in demo:
			dp = DemoPubli(demo=d,page=page)
			dp.save()
			
		
	if grp and grp!=page.group :
		page.group = grp
		page.save()
		dst = path_from_page(page) #How to find dst ? 
		change_grp_all_f(src_path,dst)#change_nm !
		upd_file_in_publi(page,dst)
	elif page.group and not grp :
		page.group = None
		page.save()
		dst = path_from_page(page) #How to find dst ? 
		change_grp_all_f(src_path,dst)#change_nm !
		upd_file_in_publi(page,dst)

	page.KW.clear()
	if KW:
		add_kw(page,KW)
	
	fs=page.frames_set.all().delete()
	if links:
		llinks = links.split(',')
		for l in llinks:
			f = Frames(publi=page, link=l.lstrip().replace("watch?v=","embed/").split('&')[0])
			f.save()
	
	page.save()
	return page
	
			
def add_tool_db_from_page(form_page,form_tool,user,page):
	"""
	\brief add a tool filled in the publication page
	"""
	#All the info from the addtoolonpage formula
	name = form_tool.cleaned_data['name']
	code_type = form_tool.cleaned_data['code_type']
	version = form_tool.cleaned_data['version']
	licence = form_tool.cleaned_data['licence']
	desc_s = form_tool.cleaned_data['desc']
	
	#the info from form_page:
	#author = form_page.cleaned_data['author']
	gpe = form_page.cleaned_data['gpe']
	KW = form_page.cleaned_data['KW']
	author = ",".join([unicode(a) for a in page.author.all()])
	# add tool
	
	date= datetime.date.today()

	tool = Tool(name_tool=name, version_tool=version, desc_tool=desc_s,  manager=user, date_creation=date, date_modification=date, licence=licence, type_tool=code_type, group=gpe, all_f=True)
	tool.save()

	if author:
		add_author_to_tool(tool,author)
	if KW:
		add_kw(tool,KW)

	tool.save()
	
	page.tool.add(tool)
	page.save()

	return tool

def upd_ensfile_publi(form_ensfile,page):
	efs = form_ensfile.cleaned_data['ensfile']
	if efs:
		page.ensfile.clear()
		page.save()
		for ef in efs:
			page.ensfile.add(ef)
		page.save()
		
		
