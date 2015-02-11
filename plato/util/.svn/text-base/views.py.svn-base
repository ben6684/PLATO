# -*- coding: utf-8 -*-
# Create your views here.
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse, render
from plato.models import User, EnsFile, File, Authorisation,Tool,Page
from plato.form import *

from util.object_util import *


from django.db.models import Q,Max

from django.core.mail import mail_admins, send_mail

	#################################################################
####################### UTIL :  generic fonctions #######################
	#################################################################
import socket



#generic function that download the file linked to the id_file passed to download ('file')
def download(request, file):
	"""
	\brief{method that get a id_file and use it to send a http response that open a download window ! very usefull, avoid a lot of security breaches.}
	\input{fils is the id of the file that you want to download}
	\author{B.Petitpas}
	\date{05/06/2012}
	"""
	# select the redirection page, http_referer if you download for the first time, the index page otherwise
	if request.META.has_key('HTTP_REFERER'):
		redir = request.META['HTTP_REFERER']
	else:
		redir = 'idx'

	# test private
	#if file is private AND person not in the group
	# Download IF file is visible OR user in grpe
	me=get_object_or_404(User, login='guest')
	if request.session.has_key('login'):
		me = get_object_or_404(User, login=request.session['login'])
	

	# now select the file object and download it
	import os
	try:
		fil = File.objects.filter(id_file=file)
		if not fil:
			return render_to_response('error.html',{'error_message' : "Sorry, but the file does not exist" },context_instance=RequestContext(request))
		else:
			fil = fil[0]
		if not fil.visible and socket.gethostname() == 'plato':
			return render_to_response('error.html',{'error_message' : "Sorry, but you do not have the right to download this file"},context_instance=RequestContext(request))
		# the file is in the file system => /tsi/plato etc ...
		if fil.path[0]=="/":
			my_data = open(unicode(fil.path))
			response = HttpResponse(my_data, content_type='text/plain')
			response['Content-Disposition'] = 'attachment; filename=%s'%os.path.basename(fil.path)
			return response
		elif fil.path[0:4]=="http": # the file is stored on internet
			return HttpResponseRedirect(fil.path)
		else:
			return render_to_response('error.html',{'error_message' : "Sorry, but the file is unreachable" },context_instance=RequestContext(request))
	except: 
		return render_to_response('error.html',{'error_message' : "Sorry, there is a problem with this file, it's temporary undownloadable" },context_instance=RequestContext(request))

import os
import zipfile
import StringIO
#when download a dir of zip file
def download_zip_archive(request,nef):
	"""
	\brief When clicking on a ensemble file, get all the files AND put them into the archive
	"""
	ef = get_object_or_404(EnsFile,id_ensfile=nef)
	if not ef:
		return render_to_response('error.html',{'error_message' : "Sorry, but the files do not exist" },context_instance=RequestContext(request))
	fs = File.objects.filter(ensfile__id_ensfile=nef)
	
	if request.META.has_key('HTTP_REFERER'):
		redir = request.META['HTTP_REFERER']
	else:
		redir = 'idx'
	
	size_tot = float(0)
	for f in fs:
		size_tot += float(f.size_file)

	if size_tot > 1000000000.0:
		return HttpResponse("""Too big, too many, size : %s  download it another way"""%size_tot)
  
	# Folder name in ZIP archive which contains the above files
	# E.g [thearchive.zip]/somefiles/file2.txt
	# FIXME: Set this to something better
	zip_subdir = ef.name_ensfile
	zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
	s = StringIO.StringIO()

    # The zip compressor
	zf = zipfile.ZipFile(s, "w")
	# test private
	#if file is private AND person not in the group
	# Download IF file is visible OR user in grpe
	me=get_object_or_404(User, login='guest')
	if request.session.has_key('login'):
		me = get_object_or_404(User, login=request.session['login'])
	if not ef.public and not (ef.group in me.group_users.all()):
		return render_to_response('error.html',{'error_message' : "Sorry,  but you do not have the right to download this files" },context_instance=RequestContext(request))


	for f in fs:
        # Calculate path for file in zip
		if os.path.isfile(f.path):
			fdir, fname = os.path.split(f.path)
			zip_path = os.path.join(zip_subdir, fname)

			# Add file, at correct path
			zf.write(f.path, zip_path)

    # Must close zip for all contents to be written
	zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
	resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
    # ..and correct content-disposition
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	return resp

# For Autocomplete keywords, i had to disable the csrf protection (with the django decorator)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@is_logged
def autoKW(request,key):
	"""
	\brief{find into the database the most probable keyword}
	"""
	k=key+'-KW'
	HTML=''
	if request.is_ajax() and request.POST.has_key(k):
		HTML ="<ul>"
		filt = request.POST.get(k)
		A = KW.objects.filter(nm_kw__istartswith=filt)
		for a in A:
			HTML+="""<li id="%s">%s</li>"""%(a.id_kw,a)
	return HttpResponse(HTML)

# a reecrire => juste teste et envoie vers la bonne fonction => avec un gros redirect bien sale !
# ON fait un truc qui redirige seuelement vers les bons upd_XXX !!!
@is_logged
def upd_ensfile(request):
	"""
	\brief : for updating the data YOU add
	"""
	if request.GET.has_key('id_ens'):
		id_ens = request.GET['id_ens']
		ef = get_object_or_404(EnsFile, id_ensfile = id_ens)
		form = UpdMedia(prefix='form_upd_media', initial ={'name': ef.name_ensfile, 'origin':ef.origin, 'cpyright':ef.copyright, 'desc':ef.desc_ensfile, 'date_del':ef.date_del, 'KW':", ".join([kw.nm_kw for kw in ef.KW.all()]), 'grp':ef.group, 'public':ef.public})
		
		if request.session['lang']=='fr':
			form=trans_label_fr(form)	
		HTML="""<div id="objectcontent"><form enctype="multipart/form-data" action="/add_data/upd_ens_file/%s/" method="post"><ul>"""%(ef.id_ensfile)
		# for field in form:
		# 	if field.label == "Keywords":
		# 		print field
		# 		HTML+="""<li><b><label for="id_form_upd_media-KW">%s</b></label>: %s
		# 	     <div id="autocomplete_KW_choices" class="autocomplete"></div>
		# 		 <script>new Ajax.Autocompleter("id_form_upd_media-KW", "autocomplete_KW_choices", "/util/autoKW/form_upd_media/", { tokens: ','});</script></li> """%(field.label, field)
		# 	else:
		# 		HTML+="""<li><b>%s</b>: %s</li>"""%(field.label, field )
		HTML+= form.as_ul()
		HTML+="""<p align="center"><input type="submit" value="Validate the formular"/></form></p>"""
		return HttpResponse(HTML)

# a reecrire => juste teste et envoie vers la bonne fonction => avec un gros redirect bien sale !
# ON fait un truc qui redirige seuelement vers les bons upd_XXX !!!
@is_logged
def upd_media(request,nm):
	"""
	\brief : for updating the data YOU add
	"""
	me = get_object_or_404(User,login = request.session['login'])
	f = get_object_or_404(File, id_file = nm)
	form = UpdFile(prefix='form_upd_file',initial={'name':f.name_file, 'desc':f.desc_file,'date_del':f.date_del, 'grp':f.group, 'all_f':f.all_f, 'KW':", ".join([kw.nm_kw for kw in f.KW.all()])})
	if request.session['lang']=='fr':
		form=trans_label_fr(form)	
	HTML = """<div id="objectcontent"> <form enctype="multipart/form-data" action="/add_data/upd_file/%s/" method="post"><ul>"""%(f.id_file)
	# for field in form:
	# 	if field.label == "Keywords":
	# 		HTML+="""<li><b><label for="id_form_upd_media-KW">%s</b></label>: %s
	# 		<div id="autocomplete_KW_choices" class="autocomplete"></div>
	# 		<script>new Ajax.Autocompleter("id_form_upd_media-KW", "autocomplete_KW_choices", "/util/autoKW/form_upd_media/", { tokens: ','});</script></li> """%(field.label, field)
	# 	else:
	# 		HTML+="""<li><b><label for="id_form_media-KW">%s</b></label>: %s</li>"""%(field.label, field )
	HTML+= form.as_ul()
	HTML+="""</ul><p align="center"><input type="submit" value="Validate"/></form></p></div> """
	return HttpResponse(HTML)
	#return redirect(request.META['HTTP_REFERER'])
		
#################################################################	

def upim(request,log):
	
	# from PIL import Image
	# im = Image.open("/tmp/perso/"+log+"/profil.jpg")
	# return HttpResponse(im, mimetype="image/jpg")
	print "recu !"
	redirect('idx')
##################################################################
@is_logged
def change_auth(request,checked=True):
	"""
	\brief : this funcion is here to change the visualisaion on plato Vitrine
	"""
	if request.is_ajax() and rquest.POST:
		usr = get_object_or_404(User, login = request.session['login'])

		#right now we're just testing on tool, because companion paper and ens_file would be too hard to manage

		# for companion paper => paper always visible but companion ?

		# for ens_file : if global size < 10M => ok otherwise : NO !!!
		
		if request.POST.has_key('id_tool'):
			id_tool = request.POST['id_tool']
			tool = get_object_or_404(Tool, id_tool = id_tool)
			tf = tool.tool_figures.all()
			fs = tool.files.all()
			if checked:
				tool.visible =True
				for f in tf:
					f.visible=True
					f.save()
				for f in fs:
					f.visible=True
					f.save()
				tool.save()
			else:
				tool.visible =False
				for f in tf:
					f.visible=False
					f.save()
				for f in fs:
					f.visible=False
					f.save()
				tool.save()
@csrf_exempt
@is_logged
def report_error(request):
	"""
	\brief : report error found on the beta test 
	"""
	if request.POST:
		form = ReportError(request.POST)
		if form.is_valid():
			usr = get_object_or_404(User, login = request.session['login'])
			t =form.cleaned_data['titre']
			m =form.cleaned_data['msg']
			#mail_admins(t,m)
			send_mail("[PLATO] %s : %s"%(usr.login,t),m,"plato_debug@plato-test.enst.fr",['petitpas@telecom-paristech.fr'],fail_silently=False)
			return render(request, "report_success.html")
	else:
		form = ReportError()
		if request.session['lang']=='fr':
			form=trans_label_fr(form)	
	return render(request, "report_error.html", {'form':form})

def readme(request):
	return render(request, "readme.html")


def upd_biblio(request,log):
	"""
	call upd_biblio_soap
	"""
	
	usr=get_object_or_404(User,login=log)
	import util.upd_biblio
	raiponce=util.upd_biblio.upd_biblio_soap(usr)			
	return HttpResponse(raiponce)


@is_logged
def check_dates(request):
	"""
	this function verify all the date_del !
	"""
	import datetime
	notification =""
	# A User is never delete, it's becoming inactif !! => no possibility to add anythings => just managing their own adding stuff
	users = User.objects.filter(account_expiration_date__lt=datetime.date.today()).filter(actif=True)
	for u in users:
		notification= "----------------------------------<br>%s<br>"%(u.login)
		u.actif=False
		u.save()
		#NO WARNING BITCH ! IF it's too late, it's too late MOFO ! 

	TOD = datetime.timedelta(days=100) # TOD : TIME OF DEATH, BITCH !
	TOBD = datetime.timedelta(days=466) # TOD : TIME OF BLOODY DEATH, BITCH !
	tow = datetime.timedelta(days=-42) # tow : time of warning ... 
	tow2 = datetime.timedelta(days=42) # tow : time of warning ... 
	# case 1 : date_del = today + tow :
	#          => 1 warning send OR a notification ?
	# case 2 : date_del = today + tow2 :
	#          => 2nd warning send by email to : manager, the boss, and me !
	# case 3 : date_del < today + TOD :
	#          => Become inactif and move to a protected folder !
	# case 4 : date_del < today + TOBD :
	#          => TOO LATE => DELETE MEDIA BITCHHHH !!!!


	###### CASE 2 ############
	notification += "---------------1-------------------<br>"
	
	efs = EnsFile.objects.filter(date_del=(datetime.date.today()-tow))
	for ef in efs:
		notification += ef.name_ensfile + "<br>"
		send_mail("[PLATO]:%s will be suppress"%ef.name_ensfile,"you have 142 days to regularize or it will be delete",ef.manager.email_person,['petitpas@telecom-paristech.fr'],fail_silently=False)

	###### CASE 2 ############
	notification += "----------------2------------------ <br>"
	
	efs = EnsFile.objects.filter(date_del=(datetime.date.today()-tow2))
	for ef in efs:
		notification += ef.name_ensfile + "<br>"
		send_mail("[PLATO]:%s will be suppress"%ef.name_ensfile,"you have 58 days to regularize or it will be delete",ef.manager.email_person,['petitpas@telecom-paristech.fr'],fail_silently=False)

	###### CASE 3 ############
	notification += "--------------------3--------------<br>"
	
	efs = EnsFile.objects.filter(date_del__lt=(datetime.date.today()-TOD)).filter(actif=True)
	for ef in efs:
		notification += ef.name_ensfile + "<br>"
		del_media_from_date(ef,True)

	###### CASE 4 ############
	notification += "--------------------4--------------<br>"
	
	efs = EnsFile.objects.filter(date_del__lt=(datetime.date.today()-TOBD))
	for ef in efs:
		notification += ef.name_ensfile + "<br>"
		del_media_from_date(ef,False)

	return HttpResponse(notification)

def suppr_connerie(request):
	"""
	c'est la juste pour gérer des conneries !
	"""
	rm_dirs('/tsi/plato_users/TMP/')
	return redirect('idx')

def suppr_tmp(request):
	"""
	c'est la juste pour gérer le tmp qui peut-etre plein si problème à l'upload
	"""
	filelist = [ f for f in os.listdir("/tmp/") if f.endswith(".upload") ]
	for f in filelist:
		try:
			os.remove("/tmp/%s"%f)
		except:
			pass
	if request.META.has_key('HTTP_REFERER'):
		redir = request.META['HTTP_REFERER']
	else:
		redir = 'idx'

	return redirect(redir)

def change_manager(request):
	"""
	login : masurell
	"""
	user = get_object_or_404(User, login = "masurell")
	ef = get_object_or_404(EnsFile, id_ensfile = 952)
	for f in ef.file_set.all():
		f.manager = user
		f.save()
	return redirect('idx')
