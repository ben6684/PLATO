# -*- coding: utf-8 -*-
# Create your views here.
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from plato.models import User,EnsFile
from plato.form import *
from util.object_util import *
#from util.addobject import *
from add_data import *
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import datetime

from django.db.models import Q,Max


@is_logged
def add_data(request):
	return render_to_response('add_data/add_data.html',context_instance=RequestContext(request))

def add_multimedia(f,me,ef,form_son,form_sat):
	"""
	Take a fil and some additionnal form, ef the ensefile where the file should be linked to.
	
	"""
	mede = metadata_obj(f)
	fil = add_file_db(me, f, mede, ef.id_ensfile)
	# verifier fil bien ajouté 
	
	if ef.type_ens_file.id_type_ensfile == 1:
		if form_son.is_valid():
			add_son_db(fil,form_son, mede)
	elif ef.type_ens_file.id_type_ensfile == 2:
		add_img_db(fil,2)
	elif ef.type_ens_file.id_type_ensfile == 3:
		add_img_db(fil,3)
	elif ef.type_ens_file.id_type_ensfile == 4:
		if form_sat.is_valid():
			add_sat_db(fil,form_sat)
	elif ef.type_ens_file.id_type_ensfile == 5:
		add_vid_db(fil,mede)
	elif ef.type_ens_file.id_type_ensfile == 7: # it's a multimodal ensfile, so had any thing 	
		add_obj_db(fil,mede)
		
	flag_add = management_file(fil,f,"data/"+ef.name_ensfile)
	# flag_add is a dict with 2 key : flag (true if management ok, false otherwise) and error (empty if flag ok, the error in adding otherwise)
	if not flag_add['flag']:
		fil.delete()
	return flag_add
					
@is_logged
def add_file_to_ensfile(request):

	if request.GET.has_key('tef'):
		tef =request.GET['tef']
		HTML=""
		if tef:
			me = get_object_or_404(User, login=request.session['login'])
			form_files = AddFiles(prefix='form_files')
			form_files.fields['name_ens'].queryset = EnsFile.objects.filter(type_ens_file=tef).filter(Q(all_f=True)|Q(group__in=me.group_users.all()))
			if request.session['lang']=='fr':
				form_files=trans_label_fr(form_files)
			HTML= form_files.as_table()
		return HttpResponse(HTML)
	
	if request.method=='POST':
		# if the form is filled and validate  : 
		form = AddFiles(request.POST, request.FILES, prefix ='form_files')
		form_son = AddSound(request.POST,prefix='form_more_sound')
		form_sat = AddSatellite(request.POST,prefix='form_more_satellite')
		if form.is_valid(): #validation rules pass
			#Here : need to extract the files, the metadata, hte user, the info into the form	
			if request.FILES.has_key('files') or request.FILES.has_key('dir'):
				me = get_object_or_404(User, login=request.session['login'])
				multimedia=request.FILES.getlist('files')
				if not multimedia:
					multimedia = request.FILES.getlist('dir')
				ens_ = form.cleaned_data['name_ens']
				for f in multimedia:
					mede = metadata_obj(f)
					typ = def_typ(mede)
					if compa_type(ens_.type_ens_file.id_type_ensfile, typ) or (ens_.type_ens_file.id_type_ensfile == 7):
                        #we had an XXX to an XXX gathering or a multimodal ensfile
						flag_add=add_multimedia(f,me,ens_,form_son,form_sat)
						if not flag_add['flag']:
							return render_to_response('add_data/add_files.html', {
								'form':form,
								'error_message':flag_add['error'],
								},context_instance=RequestContext(request))
					else: # type file AND type_ensfile don't correspond !
						form= AddFiles_type(prefix='form_type')
						return render_to_response('add_data/add_files.html', {
							'form':form,
							'error_message':"You can't had a media different from the original (a sound in an image gathering)",
							},context_instance=RequestContext(request))
						
				return redirect('/data/%s/'%(ens_.id_ensfile))
			else:
				return render_to_response('add_data/add_files.html', {
					'form':form,
					'error_message':"You should had a file",
					},context_instance=RequestContext(request))
		else:
			err = form.errors
			return render_to_response('add_data/add_files.html', {
				'form':form,
				'error_message':err,
				},context_instance=RequestContext(request))
	else:
		# just show the form !
		form= AddFiles_type(prefix='form_type')
		if request.session['lang']=='fr':
			form=trans_label_fr(form)
		return render_to_response('add_data/add_files.html', {
			'form':form,
			},context_instance=RequestContext(request))

@is_logged
def more_files(request):
	
	if request.GET.has_key('type'):
		type=request.GET['type']
		HTML=""
		if type:
			if type=='1':
				form_more = AddSound(prefix='form_more_sound')
				if request.session['lang']=='fr':
					form_more=trans_label_fr(form_more)
			elif type=='4':
				form_more = AddSatellite(prefix='form_more_satellite')
				if request.session['lang']=='fr':
					form_more=trans_label_fr(form_more)
			else:
				return HttpResponse("")
			
			HTML= form_more.as_table()
		return HttpResponse(HTML)


@is_logged
def add_ensfile(request):

	if request.method=='POST':
		# if the form is filled and validate  : 
		form = AddMedia(request.POST,prefix='form_media')
		form_son = AddSound(request.POST,prefix='form_more_sound')
		form_sat = AddSatellite(request.POST,prefix='form_more_satellite')
		if form.is_valid(): #validation rules pass
			if request.FILES.has_key('files') or request.FILES.has_key('dir'):
				me = get_object_or_404(User, login=request.session['login'])
				ef = add_ensfile_db(form, me)				
				multimedia=request.FILES.getlist('files')
				if not multimedia:
					multimedia = request.FILES.getlist('dir')
				for f in multimedia:
					flag_add = add_multimedia(f,me,ef,form_son,form_sat)
					if not flag_add['flag']:
						ef.delete()
						return render_to_response('add_data/add_new_files.html', {
							'form':form,
							'error_message':flag_add['error'],
							},context_instance=RequestContext(request))
				return redirect('/data/%s/'%(ef.id_ensfile))
			else:
				return render_to_response('add_data/add_new_files.html', {
					'form':form,
					'error_message':"You should had a file",
					},context_instance=RequestContext(request))
		else:
			return render_to_response('add_data/add_new_files.html', {
				'form':form,
				'error_message':form.errors,
				},context_instance=RequestContext(request))
	else:
		# just show the form !
		form= AddMedia(prefix='form_media')
		if request.session['lang']=='fr':
			form=trans_label_fr(form)
		return render_to_response('add_data/add_new_files.html', {
			'form':form,
			},context_instance=RequestContext(request))

class tutu(object):
	def __init__(self,name,size):
		self.name =name
		self.size = size
	

def recursive_add_db(path,me,ef,form_son,form_sat,prec=None):
	"""
	This function is adding 
	"""
	import os
	names = os.listdir(path)
	for name in names:
		tmp_name = os.path.join(path,name)
		if os.path.isdir(tmp_name):
			if prec:
				pprec = prec + name + "/"
			else:
				pprec = name + "/"
			#tmp_name is a directory => must go deeper recursivly
			recursive_add_db(tmp_name,me,ef,form_son,form_sat,pprec)
		else:
			#tmp_name is a file => must know the name and the size OR create a File object
			if prec:
				nname = prec + name
			else:
				nname = name
				
			f = tutu(nname, os.path.getsize(tmp_name))
			mede =metadata_name(tmp_name)
					
			fil = add_file_db(me, f, mede, ef.id_ensfile,name)
			#IF NOT FIL ?
			######## => to do monday #########
			
			if ef.type_ens_file.id_type_ensfile == 1:
				if form_son.is_valid():
					add_son_db(fil,form_son, mede)
			elif ef.type_ens_file.id_type_ensfile == 2:
				add_img_db(fil,2)
			elif ef.type_ens_file.id_type_ensfile == 3:
				add_img_db(fil,3)
			elif ef.type_ens_file.id_type_ensfile == 4:
				if form_sat.is_valid():
					add_sat_db(fil,form_sat)
			if ef.type_ens_file.id_type_ensfile in [2,3,4] and def_typ(mede) == 1: # it's an Image
				thumb_image(tmp_name)
			#elif ef.type_ens_file.id_type_ensfile == 5:
			#	add_vid_db(fil,form,mede)
			#management_file(fil,f,"data/"+ef.name_ensfile)
			
	return 0

import os 
@is_logged
def add_ensfile_from_plato(request):

	if request.method=='POST':
		# if the form is filled and validate  : 
		form = AddMedia(request.POST,prefix='form_media')
		form_son = AddSound(request.POST,prefix='form_more_sound')
		form_sat = AddSatellite(request.POST,prefix='form_more_satellite')
		if form.is_valid(): #validation rules pass

			me = get_object_or_404(User, login=request.session['login'])
			ef = add_ensfile_db(form, me)				
			
			# => ici appeller la fonction qui ajoute le
			#src = "/tsi/plato_users/TMP/"+ef.name_ensfile+"/" # Old source folder => new one 
			src = "/tsi/plato_tmp/"+ef.name_ensfile+"/"
			if not os.access(src, os.R_OK):
				ef.delete()
				return render_to_response('add_data/add_new_files_from_plato.html', {
					'form':form,
					'error_message':"The folder you add at %s is not readable, please change the permission"%(src),
					},context_instance=RequestContext(request))
	
			dst = path_from_ensfile(ef)
			# => test existance du dossier source, vérifier le chmod ! 
			
			cpy_err = copytree2(src, dst) # cpy_err is a dict containning a flag = flase if copytree2 failed with a field error containing the error !
			if not cpy_err['flag']:
				ef.delete()
				return render_to_response('add_data/add_new_files_from_plato.html', {
					'form':form,
					'error_message':cpy_err['error'],
					},context_instance=RequestContext(request))
			
			recursive_add_db(dst,me,ef,form_son,form_sat)# can't failed ish !
			# create thumb
			rm_err= rm_dirs(src)
			if not rm_err['flag']:
				return render_to_response('add_data/add_new_files_from_plato.html', {
					'error_message':rm_err['error'],
					},context_instance=RequestContext(request))			
			return redirect('/data/%s/'%(ef.id_ensfile))
		else:		
			return render_to_response('add_data/add_new_files_from_plato.html', {
				'form':form,
				'error_message':form.errors,
				},context_instance=RequestContext(request))
	else:		
		# just show the form !
		form= AddMedia(prefix='form_media')
		if request.session['lang']=='fr':
			form=trans_label_fr(form)	
		return render_to_response('add_data/add_new_files_from_plato.html', {
			'form':form,
			},context_instance=RequestContext(request))

	
def upd_file_in_ensfile(ef,path):
	"""
	\brief Find all the files related to the tool AND change theirs path with the new !
	"""
	import os
	fs = File.objects.filter(ensfile=ef)
	for f in fs:
		nm_f = os.path.split(f.path)[1]
		f.path = path + nm_f
		f.save()
	
@is_logged
@csrf_exempt
def upd_ens_file(request,id_ens):
	"""
	\brief : take the form create in vall, now use it and add it ! 
	"""
	if request.POST:
		ef = get_object_or_404(EnsFile, id_ensfile = id_ens)
		form = UpdMedia(request.POST, prefix ='form_upd_media')
		if form.is_valid():
			n_name = form.cleaned_data['name']
			n_orig = form.cleaned_data['origin']
			n_cpy = form.cleaned_data['cpyright']
			n_desc = form.cleaned_data['desc']
			n_ddel = form.cleaned_data['date_del']
			n_kw = form.cleaned_data['KW']
			n_grp = form.cleaned_data['grp']
			public = form.cleaned_data['public']
			src_path = path_from_ensfile(ef)
			if n_name!=ef.name_ensfile:
				ef.name_ensfile = n_name
				ef.save()
				dst=path_from_ensfile(ef)
				change_nm(src_path,dst)
				upd_file_in_ensfile(ef,dst)				
			ef.desc_ensfile = n_desc
			ef.copyright = n_cpy
			ef.origin = n_orig
			ef.date_modification = datetime.date.today()
			ef.date_del = n_ddel
			
			if n_grp and n_grp!=ef.group: # the group selected is different from the older which can be empty
				ef.group = n_grp
			elif ef.group and not n_grp: #there was a group but not anymore => plato_users !
				ef.group = None
			if public!=ef.public: # test if the data became publi or private AND had a group selected !
				ef.public=public
				
			ef.save()
			dst = path_from_ensfile(ef) #find the new path
			if src_path != dst:
				change_grp_all_f(src_path,dst) # move the file
				upd_file_in_ensfile(ef,dst)	#chnage path in files
				
			if n_kw:
				ef.KW.clear()
				add_kw(ef,n_kw)			
			ef.save()

	return return_referer(request)
	

@is_logged
@csrf_exempt
def upd_file(request,id_file):
	"""
	\brief : take the form create in vall, now use it and add it ! 
	"""
	if request.POST:
		ef = get_object_or_404(File, id_file = id_file)
		form = UpdFile(request.POST, prefix ='form_upd_file')
		if form.is_valid():
			n_name = form.cleaned_data['name']
			n_desc = form.cleaned_data['desc']
			n_ddel = form.cleaned_data['date_del']
			n_kw = form.cleaned_data['KW']
			n_grp = form.cleaned_data['grp']
			n_public = form.cleaned_data['public']
			ef.name_file = n_name
			ef.desc_file = n_desc
			ef.date_modification = datetime.date.today()
			ef.date_del = n_ddel
			ef.group = n_grp
			if n_grp:
				ef.public = n_public
			else:
				ef.public = True
			ef.KW.clear()
			add_kw(ef,n_kw)
			ef.save()
		else:
			return render_to_response("error.html", {
				'error_message':form.errors,
				},context_instance=RequestContext(request))
		
	return return_referer(request)		
	

#################### DELATION ################


@is_logged
def del_media(request,nm):
	"""
	\brief : del a media, whatever the media (even if for the moment only the sound are managed)
	"""
	err  = del_media_db(nm)
	if not err['flag']:
		return render_to_response("error.html", {
			'error_message':err['error'],
			},context_instance=RequestContext(request))
	
	return return_referer(request)
	

@is_logged
def del_media_file(request,nf):
	"""
	\brief : del a file in a media (whatever the file and the media)
	"""
	err = del_media_file_db(nf)
	if not err['flag']:
		return render_to_response("error.html", {
			'error_message':err['error'],
			},context_instance=RequestContext(request))
	return return_referer(request)			
