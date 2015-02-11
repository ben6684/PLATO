# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import get_object_or_404

import plato
from plato.models import User, File, Sound, Image, EnsFile, TypeImage, TypeFile, TypeSound
import datetime
from util.object_util import *
import os
from os import remove, rmdir



def path_from_ensfile(ensfile):
	"""
	\brief : the point of this method is to extract the path of the files from info in the ensfile table
	Now it's /tmp but will be /tsi/plato in the futur
	"""
	fpath = get_plato_path()
	if ensfile.group and ensfile.public:
		# The file is linked to a project BUT is public 
		path = "/%s/plato_projects/%s/public/data/%s/"%(fpath,ensfile.group.name_group, ensfile.name_ensfile)
	if ensfile.group and not ensfile.public:
		# The file is linked to a project and private
		path = "/%s/plato_projects/%s/private/data/%s/"%(fpath,ensfile.group.name_group, ensfile.name_ensfile)
	if not ensfile.group:
		# The file is nto linkedto a group AND have to be public
		path = "/%s/plato_users/%s/data/%s/"%(fpath,ensfile.manager.login, ensfile.name_ensfile)
	
	return path

######################### ADD function ############################
def add_file_db(user,file,mede,id_ensfile,real_name=None):
	"""
	\brief plop
	"""
	name = os.path.splitext(file.name)[0]
	size = file.size
	typ = def_typ(mede)
	type=get_object_or_404(TypeFile, id_type_file=typ)

	# adding file from add_data
	ef = get_object_or_404(EnsFile, id_ensfile=id_ensfile)
	
	path = path_from_ensfile(ef)
	if real_name:
		path = path + real_name
	else:
		path = path + file.name
	
	f = File(name_file = name, desc_file = ef.desc_ensfile, size_file= size, path=path, type_file = type, ensfile = ef, manager = user,date_creation = datetime.date.today(), date_modification = datetime.date.today(), date_del=ef.date_del,group=ef.group, actif=True, visible = ef.public)
	f.save()

	return f
	
def add_ensfile_db(forms, user):
	"""
	\brief plop
	"""

	name= str_s(forms.cleaned_data['name'])
	desc = str_s(forms.cleaned_data['desc'])
	type_ = forms.cleaned_data['type_ens']
	cpy = forms.cleaned_data['cpyright']
	origin = str_s(forms.cleaned_data['origin'])
	date_del = forms.cleaned_data['date_del']
	if not date_del:
		date_del = datetime.date(9999,12,12)
	KW = forms.cleaned_data['KW']
	grp = forms.cleaned_data['grp']
	public = forms.cleaned_data['public']

	ef = EnsFile(name_ensfile = name, desc_ensfile = desc, type_ens_file= type_, copyright=cpy, origin=origin, date_del = date_del, date_creation = datetime.date.today(), date_modification = datetime.date.today(), manager = user, all_f = True, actif=True, public=public)

	ef.save()
	if grp:
		ef.group = grp
		ef.save()

	add_kw(ef,KW) #verif add kw has the right encodage !
	
	return ef

def add_son_db(f,form, mede):
	"""
	\brief plop
	"""
	duration="0:00:00"
	if mede and mede.has_key('duration'):
		duration = mede['duration']

	typ = form.cleaned_data['type_sound']
	inst = form.cleaned_data['instrument']
	note= form.cleaned_data['note']

	son = plato.models.Sound(file=f, type_sound = typ, duration = duration)
	son.save()

	if inst:
		for i in inst:
			son.instrument.add(i)
	if note:
		for n in note:
			son.note.add(n)

	son.save()

	return son

def add_vid_db(f,mede):
	"""
	\brief plop
	"""
	duration="0:00:00"
	
	if mede and mede.has_key('duration'):
		duration = mede['duration']

	vid = plato.models.Video(file=f,  duration = duration)
	vid.save()

	return vid

def add_3D_db(f,form, mede):
	"""
	\brief plop
	"""	
	vid = plato.models.Video(file=f,  duration = duration)
	vid.save()

	return vid

def add_img_db(f,type):
	"""
	\brief plop
	"""
	if type==2:
		ty = get_object_or_404(TypeImage, id_type_image=1)
	else:
		ty = get_object_or_404(TypeImage, id_type_image=2)
		
	img = plato.models.Image(file=f, type_image=ty)
	img.save()
	return img

def add_sat_db(f,forms):
	"""
	\brief plop
	"""
	typ = get_object_or_404(TypeImage, id_type_image = 3)
	img = plato.models.Image(file=f, type_image=typ, satellite=forms.cleaned_data['sat'])
	img.save()
	return img

def add_obj_db(f,mede):
	"""
	\brief{Add an obj dependaing on the type of file to a multimodal ensfile}
	"""
	if mede:
		typ = def_typ(mede)
	else:
		typ=0
		
	if typ==1: #it's an image
		obj = plato.models.Image(file=f, type_image=get_object_or_404(TypeImage, id_type_image = 1))
		obj.save()
	elif typ==2: #it's a sound
		duration="0:00:00"
		if mede and mede.has_key('duration'):
			duration = mede['duration']
		obj = plato.models.Sound(file=f, type_sound = get_object_or_404(TypeSound, id_type_sound = 8), duration = duration)		
		obj.save()
	elif typ==5: #it's a vid 
		duration="0:00:00"
		if mede and mede.has_key('duration'):
			duration = mede['duration']
		obj =  plato.models.Video(file=f,  duration = duration)
		obj.save()
		
	return True
		
######################### UPD function ############################

######################### DEL function ############################

def del_media_file_db(id_file):
	"""
	\brief : delete file in dtabase AND in the file system 
	"""
	err={'flag':True, 'error':None}
	f = get_object_or_404(File, id_file = id_file)
	if os.path.exists(f.path):
		try:
			remove(str(f.path))
		except:
			err={'flag':False, 'error': "Impossible to remove the file on %s"%(f.path)}
			return err
		if f.type_file.id_type_file == 1: # it's an Image
			thumb = os.path.splitext(f.path)[0] + ".THUMB" + os.path.splitext(f.path)[1]
			try:
				remove(str(thumb))
			except:
				err={'flag':False, 'error': "Impossible to remove the thum file on %s"%(f.path)}
				return err
	f.delete()
	return err

def del_media_db(id_ensfile):
	"""
	\brief delete ensfile by deleting all the file, the file obj AND the ensfile obj AND the directory
	"""

	ef = get_object_or_404(EnsFile, id_ensfile = id_ensfile)
	fs = File.objects.filter(ensfile = ef)
	for f in fs:
		flag_errr = del_media_file_db(f.id_file)
		if not flag_errr['flag']:
			return flag_errr
		
	#rmdir(unicode(path_from_ensfile(ef)))
	flag_err = rm_dirs(path_from_ensfile(ef))
	if flag_err['flag']: # the directories were delete perfectly
		ef.delete()
		return flag_err
	elif os.path.exists(path_from_ensfile(ef)): # the directory is not delete BUT it exists, there is a problem!
		return flag_err
	else: # the directory is not delete BECAUSE it doesn't exist ! 
		ef.delete()
		return flag_err

def del_media_from_date(ef,flag):
	"""
	\brief delete a media (not really in fact but who cares !) if the peremption date is over !
	"""
	import os
	if flag:
		# this deletion is comming from check_date! => inactivation and moving
		fs = File.objects.filter(ensfile = ef)
		for f in fs:
			f.actif=False
			f.save()
		ef.actif = False
		ef.save()
		# everything is inactif (doesn't appear anymore !)
		change_grp_all_f(path_from_ensfile(ef),"/tsi/plato/plato_projects/trash/%s/"%(ef.name_ensfile))
		# go to trash !
	else:
		# this is over !
		fs = File.objects.filter(ensfile = ef)
		for f in fs:
			f.delete()
		#import shutil
		#shutil.rmtree("/tsi/plato/plato_projects/trash/%s/"%(ef.name_ensfile))
		flag = rm_dirs("/tsi/plato/plato_projects/trash/%s/"%(ef.name_ensfile))
		if flag or not os.path.exists("/tsi/plato/plato_projects/trash/%s/"%(ef.name_ensfile)):
			ef.delete()

	return True
