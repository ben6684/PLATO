from django import forms
from django.db import connection, transaction
from django.shortcuts import get_object_or_404,render_to_response

from plato.models import User,File,Image
import datetime

from os import remove

#######################################################################################################
######################################## Upload Media and source ######################################
#######################################################################################################

######################################## Upload Audio Media ###########################################

def upd_audio_solo_db(form,user,mf,ns=-1):
	"""
	\brief  update a non musical audio sound in the db !
	"""
	#new thing : try to just delete some info AND put everything in the add_audio_solo_db
	cpright = form.cleaned_data['owner']
	if not cpright:
		cpright= user.login
	type_audio = form.cleaned_data['type_audio']
	desc = form.cleaned_data['desc']
	permanent =  form.cleaned_data['permanent']
	
	instru = form.cleaned_data['instrument']
	accent = form.cleaned_data['accent']
	mute = form.cleaned_data['mute']
	vibrato = form.cleaned_data['vibrato']
	instrus = form.cleaned_data['instrument_ens']
	
	note= form.cleaned_data['note']
	
	type_ens = form.cleaned_data['type_ensemble']

	#src = form.cleaned_data['src']
	#tsrc = form.cleaned_data['tsrc']

	
	IsV = "TRUE"
	date_del = datetime.date(9999,12,12)
	if not permanent:
		IsV = "FALSE"
		date_del =  form.cleaned_data['date_del']
	cursor = connection.cursor()

	table="solo"
	if type_audio.id_type_audio ==2:# ensemble musique
		table="ensemble"		
	elif type_audio.id_type_audio ==3:# isolated musique
		table="isolated_notes"
	elif type_audio.id_type_audio ==4:# one note musique
		table="one_note"
	
	cursor.execute("""UPDATE %s SET description_mma = '%s',  date_delete_possible_mma = '%s', permanent_mma = '%s', copyright_mma = '%s', id_type_audio = '%s', modify_date = '%s'
		WHERE id_mma=%s """%(table,desc,date_del,IsV,cpright,type_audio.id_type_audio,datetime.date.today(),mf.id_mma))

	cursor.execute("""DELETE FROM inst_compose_ens WHERE id_mma='%s'"""%(mf.id_mma))
	cursor.execute("""DELETE FROM note_compose_audio  WHERE id_mma='%s'"""%(mf.id_mma))
	cursor.execute("""DELETE FROM mma_belong_source  WHERE id_mma='%s'"""%(mf.id_mma))
	add_audio_solo_db(form,user,mf.nm_mma,ns,False)
	
 

def upd_audio_nm_db(form,user,mf):
	"""
	\brief  update a non musical audio sound in the db !
	"""
	cpright = form.cleaned_data['owner']
	if not cpright:
		cpright= user.login
	
	desc = form.cleaned_data['desc']
	typee = form.cleaned_data['typee']
	permanent =  form.cleaned_data['permanent']
	IsV = "TRUE"
	date_del = datetime.date(9999,12,12)
	if not permanent:
		IsV = "FALSE"
		date_del =  form.cleaned_data['date_del']

	cursor = connection.cursor()
	
	cursor.execute("""UPDATE other_sound SET description_mma = '%s',  date_delete_possible_mma = '%s', permanent_mma = '%s', copyright_mma = '%s', modify_date='%s'  WHERE id_mma=%s """%(desc,date_del,IsV,cpright,datetime.date.today(),mf.id_mma))
	
	if typee:
		cursor.execute("""UPDATE other_sound set  id_type_other_sound = '%s' WHERE id_mma=%s """%(typee.id_type_other_sound,mf.id_mma))
		
	cursor.close()
	
	transaction.commit_unless_managed()

def upd_gimg_db(form,user,mf,sn=-1,ns=-1):

	"""
	\brief  add a musical solo in the db !
	"""
	cpright = form.cleaned_data['owner']
	if not cpright:
		cpright= user.login
	desc = form.cleaned_data['desc']
	permanent =  form.cleaned_data['permanent']
	
	IsV = "TRUE"
	date_del = datetime.date(9999,12,12)
	if not permanent:
		IsV = "FALSE"
		date_del =  form.cleaned_data['date_del']
	cursor = connection.cursor()

	cursor.execute("""UPDATE image SET description_mma = '%s',  date_delete_possible_mma = '%s', permanent_mma = '%s', copyright_mma = '%s', modify_date='%s' WHERE id_mma=%s """%(desc,date_del,IsV,cpright,datetime.date.today(),mf.id_mma))
	
	if ns != -1:		
		cursor.execute("""DELETE FROM mma_belong_source  WHERE id_mma='%s'"""%(mf.id_mma))
		cursor.execute("""INSERT INTO mma_belong_source (id_mma, id_source, id_image) VALUES ('%s','%s','%s')"""%(mf.id_mma,ns,mf.id_image))
		cursor.execute("""UPDATE source SET modification_date_source='%s' WHERE id_source='%s'"""%(datetime.date.today(),ns))
	if sn != -1:
		cursor.execute("""DELETE FROM mma_belong_scn  WHERE id_mma='%s'"""%(mf.id_mma))
		cursor.execute("""INSERT INTO mma_belong_scn (id_mma, id_scene, id_image) VALUES ('%s','%s','%s')"""%(mf.id_mma,sn,mf.id_image))
		
	cursor.close()
	transaction.commit_unless_managed()
	return mf

def upd_satimg_db(form,user,mf,form2,sn=-1,src=-1):

	"""
	\brief  add a musical solo in the db !
	"""
	ns = form2.cleaned_data['src']
	date_acq=form2.cleaned_data['dat_acq']
	scn = form2.cleaned_data['scene']
	cpright = form.cleaned_data['owner']
	if not cpright:
		cpright= user.login
	desc = form.cleaned_data['desc']
	permanent =  form.cleaned_data['permanent']
	
	IsV = "TRUE"
	date_del = datetime.date(9999,12,12)
	if not permanent:
		IsV = "FALSE"
		date_del =  form.cleaned_data['date_del']
	cursor = connection.cursor()

	cursor.execute("""UPDATE satellite_image SET description_mma = '%s',  date_delete_possible_mma = '%s', permanent_mma = '%s', copyright_mma = '%s', modify_date='%s' WHERE id_mma=%s """%(desc,date_del,IsV,cpright,datetime.date.today(),mf.id_mma))
	if date_acq:
		cursor.execute("""UPDATE satellite_image SET acquisition_date ='%s' WHERE id_mma = %s"""%(date_acq,mf.id_mma))	
	if src != -1:		
		cursor.execute("""DELETE FROM mma_belong_source  WHERE id_mma='%s'"""%(mf.id_mma))
		cursor.execute("""INSERT INTO mma_belong_source (id_mma, id_source, id_image,id_satellite_image) VALUES ('%s','%s','%s','%s')"""%(mf.id_mma,src,mf.id_image,mf.id_satellite_image))
		cursor.execute("""UPDATE source SET modification_date_source='%s' WHERE id_source='%s'"""%(datetime.date.today(),src))
	elif ns:
		cursor.execute("""DELETE FROM mma_belong_source  WHERE id_mma='%s'"""%(mf.id_mma))
		cursor.execute("""INSERT INTO mma_belong_source (id_mma, id_source, id_image,id_satellite_image) VALUES ('%s','%s','%s','%s')"""%(mf.id_mma,ns.id_source.id_source,mf.id_image,mf.id_satellite_image))
		cursor.execute("""UPDATE source SET modification_date_source='%s' WHERE id_source='%s'"""%(datetime.date.today(),ns))
		
	if sn != -1:
		cursor.execute("""DELETE FROM mma_belong_scn  WHERE id_mma='%s'"""%(mf.id_mma))
		cursor.execute("""INSERT INTO mma_belong_scn (id_mma, id_scene, id_image,id_satellite_image) VALUES ('%s','%s','%s','%s')"""%(mf.id_mma,sn,mf.id_image,mf.id_satellite_image))
	elif scn:
		cursor.execute("""DELETE FROM mma_belong_scn  WHERE id_mma='%s'"""%(mf.id_mma))
		cursor.execute("""INSERT INTO mma_belong_scn (id_mma, id_scene, id_image,id_satellite_image) VALUES ('%s','%s','%s','%s')"""%(mf.id_mma,scn.id_scene,mf.id_image,mf.id_satellite_image))
		
		
	cursor.close()
	transaction.commit_unless_managed()
	return mf

	
def upd_code_db(form,algo):
	
	"""
	\brief  Upd a code source in the db ! User is the person who add the algo and helpt is the README that may be added
	"""

	desc =form.cleaned_data['desc']
	name = form.cleaned_data['name']
	webp = form.cleaned_data['webp']
	
	cursor = connection.cursor()
	cursor.execute("""UPDATE algorithm SET nm_algo='%s', description_algo='%s',webpage_algo='%s', date_modification='%s' WHERE id_algo='%s'"""%(name,desc,webp,datetime.date.today(),algo.id_algo))

	cursor.close()
	transaction.commit_unless_managed()
	return 0

def upd_add_algo_f_db(form,user,name,size,na):
	"""
	\brief  add a source file in the db !
	"""

	but  =form.cleaned_data['desc']
	desc = but

	ct = form.cleaned_data['code_type']
	permanent =  form.cleaned_data['permanent']
	IsV = "TRUE"
	date_del = datetime.date(9999,12,12)
	if not permanent:
		IsV = "FALSE"
		date_del =  form.cleaned_data['date_del']

	cursor = connection.cursor()
	cursor.execute("""INSERT INTO algorithm_file (id_folder, id_file_typ, nm_file, path_file, size_file, description_file,id_typ_algo_f,date_delete_possible_file,permanent_file) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"""%("14","4",name,"/tmp/",size,desc,ct.id_typ_algo_f,date_del,IsV))

	f = get_object_or_404(AlgorithmFile, nm_file = name)
	cursor.execute("""INSERT INTO algo_correspond_algo_f (id_file, id_algorithm_file, id_algo) VALUES ('%s','%s','%s')"""%(f.id_file, f.id_algorithm_file,na))
	cursor.execute("""UPDATE algorithm SET  date_modification='%s' WHERE id_algo='%s'"""%(datetime.date.today(),na))
	
	cursor.close()
	transaction.commit_unless_managed()


def upd_page_db(form, page, user, prez=None, article=None):
	"""
	\brief Update the page infos
	"""
	
	title = form.cleaned_data['title']
	conf = form.cleaned_data['conference']
	annee = form.cleaned_data['annee']
	abstract = form.cleaned_data['abstract']
	algo = form.cleaned_data['algo']

	if title!=page.titre:
		page.titre = title
	if conf!=page.id_conf:
		page.id_conf=conf
	if annee!=page.annee:
		page.annee=annee
	if algo!=page.id_algo:
		page.id_algo=algo
	if abstract!=page.abstract:
		page.abstract=abstract

	page.save()
	return page

def upd_conf(form, conf):
	"""
	\brief don't know where to call this but usefull to be able to update tge conference info
	"""

	title = form.cleaned_data['title']
	if title!=conf.titre_conf:
		conf.titre_conf = title
	conf.save()
	return conf

def upd_author(form, author):
	"""
	\brief same as upd_conf but it's important to be able to change the name of an author
	"""
	fstnm = form.cleaned_data['fst_name']
	nm = form.cleaned_data['name']
	
	if fstnm != author.fstnm:
		author.fstnm = fstnm
		author.fstnm_i = fstnm[0]
	if nm != author.nm:
		author.nm = nm

	author.save()
	return author

from django.db.models import Q
from plato.models import PageAuthor
def upd_author_to_page(p,author):
	"""
	\brief update the information about the author into the publication page
	"""
	if author:
		p.author.clear()
		la = author.split(',')
		ordr = 1
		for a in la:
			fnm=a.split(' ')
			auth = Author.objects.filter(Q(nm = unicode(fnm[1]),fstnm = unicode(fnm[0])))
			if auth:			
				pa = PageAuthor(author=auth[0], page=p, order=ordr)
				pa.save()
				ordr=ordr+1


