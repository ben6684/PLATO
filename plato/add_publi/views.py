# Create your views here.
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django import forms
from django.template import RequestContext

from plato.form import *
from plato.models import Conf, Page, Tool, Author, User, PageFigures, ToolFigures, TypePage
from add_publi import *
from add_app.add_app import add_tool_f_db
from util.views import *
from util.object_util import *
from util.upd_biblio import *

@is_logged
def add_page(request):
	"""
	Add a publication page to the database from the formular information
	"""
	user = get_object_or_404(User, login = request.session['login'])
	
	if request.GET.has_key('n_algo'):
		form4 = AddAlgoOnPage(prefix='form_algo')
		if request.session['lang']=='fr':
			form4=trans_label_fr(form4)	
			HTML="""<tr> <th>* Fichiers de l'outil</th><td><input type="file" id="id_tool_files" name="tool_files" multiple="multiple"/> </td></tr>"""
		else:
			HTML="""<tr> <th>* Tool Files</th><td><input type="file" id="id_tool_files" name="tool_files" multiple="multiple"/> </td></tr>"""			
		HTML+= form4.as_table()
		return HttpResponse(HTML)		
	
	if request.method=='POST':
		
		form = AddPageForm(request.POST,request.FILES,prefix='form_page')
		form_ensfile = EnsfileForm(request.POST,prefix='form_ensfilepubli')
		if form.is_valid():
			# add page
			page = add_page_db(form,user)
			nm_p = "publications/%s"%(page.titre)
			multimedia=None
			# add author to page 
			add_author_to_page(page,form.cleaned_data['author'])
			# add file to the page
			if request.FILES.has_key('form_page-article'):
				f= request.FILES['form_page-article']
				mede = metadata_obj(f)
				article=add_files_to_page(user,f,mede,page)
				management_file(article,f,nm_p)
				page.id_article = article
			if request.FILES.has_key('form_page-prez'):
				f= request.FILES['form_page-prez']
				mede = metadata_obj(f)
				prez=add_files_to_page(user,f,mede,page)
				management_file(prez,f,nm_p)
				page.id_presentation = prez
			# add exemple file to the page
			if request.FILES.has_key('multimedia'):
				multimedia=request.FILES.getlist('multimedia')
				cpt=0
				for f in request.FILES.getlist('multimedia'):
					mede = metadata_obj(f)
					fi = add_files_to_page(user,f,mede,page)
					management_file(fi,f,nm_p)
					pf=PageFigures(figures =fi, page=page)
					pf.save()
					if request.POST.has_key("legende_%s"%(cpt)):
						pf.legende = request.POST["legende_%s"%(cpt)]
						pf.save()
					cpt=cpt+1
			page.save()		
			if form_ensfile.is_valid():
				upd_ensfile_publi(form_ensfile,page)
				
			form4 = AddAlgoOnPage(request.POST,prefix='form_algo')
			if form4.is_valid():
				tool = add_tool_db_from_page(form,form4,user,page)
				nm_p = "tools/%s"%(tool.name_tool)
				for f in request.FILES.getlist('tool_files'):
					mede = metadata_obj(f)
					fil=add_tool_f_db(user,f,mede,tool)
					management_file(fil,f,nm_p)
					tool.files.add(fil)
					tool.save()
				if request.FILES.has_key('help_file'):
					help_f = request.FILES['help_file']
					if help_f:
						mede = metadata_obj(help_f)	
						fil=add_tool_f_db(user,help_f,mede,tool)
						management_file(fil,help_f,nm_p)
						tool.help_file.add(help_f)
				# for f in request.FILES.getlist('multimedia'):
				# 	mede = metadata_obj(f)	
				# 	fil=add_tool_f_db(user,f,mede,tool)
				# 	management_file(fil,f,nm_p)
				# 	tf=ToolFigures(figure=fil,tool=tool)
				# 	tf.save()
								
			elif form4:
				if request.session['lang']=='fr':
					form=trans_label_fr(form)	
				return render_to_response('add_publi/add_page.html',{
				'form':form,
				'error_message':form.errors,
				}, context_instance=RequestContext(request))
			else:
				pass
			return redirect('vpage',np=page.id_page)
			
	
		if request.session['lang']=='fr':
			form=trans_label_fr(form)	
		return render_to_response('add_publi/add_page.html',{
			'form':form,
			'error_message':form.errors,
		}, context_instance=RequestContext(request))

		
	form = AddPageForm(prefix='form_page')
	if request.session['lang']=='fr':
		form=trans_label_fr(form)	
	return render_to_response('add_publi/add_page.html',{
		'form':form,
		}, context_instance=RequestContext(request))


@is_logged
def upd_page(request,np):
	"""
	update the publication
	"""	
	page = get_object_or_404(Page,id_page=np)
	user = get_object_or_404(User, login = request.session['login'])	

	# tp = TypePage.objects.filter(nm_type_page__iexact='article')
	# page.type_page=tp[0]
	# page.save()
	
	# upd_biblio_soap(user)
	
	if request.method=='POST':
		form = UpdPageForm(request.POST,request.FILES,prefix='form_page')
		form_ensfile = EnsfileForm(request.POST,prefix='form_ensfilepubli')
		if form.is_valid():
			page = upd_page_db(page, form)
			nm_p = "publications/%s"%(page.titre)
			multimedia=None
			if request.FILES.has_key('form_page-article'):#if true : meaning the previous file was delete and a new one was filled
				f= request.FILES['form_page-article']
				mede = metadata_obj(f)
				article=add_files_to_page(user,f,mede,page)
				management_file(article,f,nm_p)
				page.id_article = article
			if request.FILES.has_key('form_page-prez'):
				f= request.FILES['form_page-prez']
				mede = metadata_obj(f)
				prez=add_files_to_page(user,f,mede,page)
				management_file(prez,f,nm_p)
				page.id_presentation = prez
			if request.FILES.has_key('multimedia'):
				multimedia=request.FILES.getlist('multimedia')
				cpt=0
				for f in request.FILES.getlist('multimedia'):
					mede = metadata_obj(f)
					fi = add_files_to_page(user,f,mede,page)
					management_file(fi,f,nm_p)
					pf=PageFigures(figures =fi, page=page)
					pf.save()
					if request.POST.has_key("legende_%s"%(cpt)):
						pf.legende = request.POST["legende_%s"%(cpt)]
						pf.save()
					cpt=cpt+1
			for tf in page.pagefigures_set.all():
				if request.POST.has_key("legende_%s"%(tf.figures.id_file)):
					tf.legende = request.POST["legende_%s"%(tf.figures.id_file)]
					tf.save()
			page.save()
			
			if form_ensfile.is_valid():
				upd_ensfile_publi(form_ensfile,page)
				
			form4 = AddAlgoOnPage(request.POST,prefix='form_algo')
			if form4.is_valid():
				tool = add_tool_db_from_page(form,form4,user,page)
				nm_p = "tools/%s"%(tool.name_tool)
				for f in request.FILES.getlist('tool_files'):
					mede = metadata_obj(f)
					fil=add_tool_f_db(user,f,mede,tool)
					management_file(fil,f,nm_p)
					tool.files.add(fil)
					tool.save()
				if request.FILES.has_key('help_file'):
					help_f = request.FILES['help_file']
					if help_f:
						mede = metadata_obj(help_f)	
						fil=add_tool_f_db(user,help_f,mede,tool)
						management_file(fil,help_f,nm_p)
						tool.help_file.add(help_f)							
			
			return redirect('vpage',np=page.id_page)
			
		else:
			if request.session['lang']=='fr':
				form=trans_label_fr(form)	
			return render_to_response('add_publi/upd_page.html',{
				'page':page,
				'form':form,
				'error_message':form.errors,
				}, context_instance=RequestContext(request))

				
	#fill the informationsfor update
	author = ",".join([unicode(a) for a in page.author.all()])
	links = ",".join([frame.link for frame in page.frames_set.all()])
	form = UpdPageForm(prefix='form_page',initial={'title':page.titre, 'abstract': page.abstract, 'annee': page.annee, 'mois': page.mon, 'author':author, 'conference':page.conf_raw, 'algo':page.tool.all(),'demo':page.publi_demos.all(),'gpe':page.group, 'KW':", ".join([kw.nm_kw for kw in page.KW.all()]), 'links':links})	
	if request.session['lang']=='fr':
		form=trans_label_fr(form)	
	return render_to_response('add_publi/upd_page.html',{
		'page':page,
		'form':form,
		}, context_instance=RequestContext(request))


	
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@is_logged
def autoAuthor(request):
	HTML=''
	if request.POST.has_key('form_page-author') and request.is_ajax():
		HTML ="<ul>"
		filt = request.POST.get('form_page-author')
		A = Author.objects.raw("SELECT * FROM author WHERE nm ILIKE %s OR fstnm ILIKE %s",["%s%%"%filt,"%s%%"%filt])
		for a in A:
			HTML+="""<li id="%s">%s</li>"""%(a.id_author,a)
		
	return HttpResponse(HTML)

			
@csrf_exempt
@is_logged
def autoConf(request):
	HTML=''
	if request.POST.has_key('form_page-conference') and request.is_ajax():
		HTML ="<ul>"
		filt = request.POST.get('form_page-conference')
		C = Conf.objects.raw("SELECT * FROM conf WHERE titre_conf ILIKE %s",["%s%%"%filt])
		for c in C:
			HTML+="""<li id="%s">%s</li>"""%(c.id_conf,c.titre_conf)
		
	return HttpResponse(HTML)

@is_logged
def del_file_page(request,np):
	if request.is_ajax() and request.GET.has_key('id'):
		nf = request.GET['id']
		page = get_object_or_404(Page, id_page = np)
		del_page_file_db(page,nf)
	return ""
	
@is_logged
def del_article_page(request,np):
	if request.is_ajax() and request.GET.has_key('id'):
		nf = request.GET['id']
		page = get_object_or_404(Page, id_page = np)
		page.id_article.clear()
		page.save()
		del_media_file_db(nf)
		#del_page_file_db(page,nf)
	return ""
	
@is_logged
def del_prez_page(request,np):
	if request.is_ajax() and request.GET.has_key('id'):
		nf = request.GET['id']
		page = get_object_or_404(Page, id_page = np)
		page.id_presentation.clear()
		page.save()
		del_media_file_db(nf)
		#del_page_file_db(page,nf)
	return ""

@is_logged
def del_page(request,np):
	"""
	\brief Delete the a publication 
	"""
	ret = del_page_db(np)
	if ret:
		return redirect('vpages')
	else:
		# mean the directory is not del => means no dir or dir still exists => need to del by hand 
		return redirect('vpages')

@is_logged
def ensfile_publi(request):
	HTML=""
	if request.GET.has_key('ensfile'):
		npubli = request.GET['ensfile']
		# We give the democation of the conencted person
		form_ensfile = EnsfileForm(prefix='form_ensfilepubli')
		if not npubli == -1 and not npubli == '-1': # update
			publi = get_object_or_404(Page,id_page = npubli)
			form_ensfile.fields['ensfile'].initial = publi.ensfile.all()
		HTML+= form_ensfile.as_table()
	return HttpResponse(HTML)	
