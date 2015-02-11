# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q, Count

from plato.models import User, EnsFile, File, TypeEnsFile
from plato.form import UpdMedia
from util.object_util import *

##############################################################################################
	#################################### SHOW ALL DATA ##################################
##############################################################################################

from django.db import connections
def vall(request):
	"""
	Show all the ens_file data
	"""

	me=get_object_or_404(User, login='guest')
	if request.session.has_key('login'):
		me = get_object_or_404(User, login=request.session['login'])
		all_src = EnsFile.objects.filter(actif=True).order_by('-date_modification','name_ensfile')
	else:
		all_src = EnsFile.objects.filter(public=True).filter(actif=True).order_by('-date_modification','name_ensfile')
		
	all= pagination(all_src,request.GET.get('page','1'))
	return render_to_response('data/all.html',{
		'Sources': all,
		'me':me,
		},context_instance=RequestContext(request))

def vmulti(request):
	"""
	Show all the multimodal ens_file data
	"""
	
	me=get_object_or_404(User, login='guest')
	if request.session.has_key('login'):
		me = get_object_or_404(User, login=request.session['login'])
		all_src = EnsFile.objects.filter(type_ens_file__id_type_ensfile__exact=7).filter(actif=True).order_by('-date_modification','name_ensfile')
	else:
		all_src = EnsFile.objects.filter(type_ens_file__id_type_ensfile__exact=7).filter(actif=True).filter(public=True).order_by('-date_modification','name_ensfile')
		
	all= pagination(all_src,request.GET.get('page','1'))
	return render_to_response('data/multimodal.html',{
		'Sources': all,
		'me':me,
		},context_instance=RequestContext(request))


def vfiles(request,nef):
	"""
	show files of the ensfile
	"""
	
	ef = get_object_or_404(EnsFile, id_ensfile = nef)
	if ef.type_ens_file.id_type_ensfile == 1:
		return redirect('audio_corpus_info',nc=nef)
	if ef.type_ens_file.id_type_ensfile in [2,3,4]:
		return redirect('image_info',nc=nef)
	if ef.type_ens_file.id_type_ensfile == 5:
		return redirect('videos',nc=nef)
	if ef.type_ens_file.id_type_ensfile == 6:
		return redirect('3df',nef=nef)

	
	me=get_object_or_404(User, login='guest')
	if request.session.has_key('login'):
		me = get_object_or_404(User, login=request.session['login'])
		files = File.objects.filter(ensfile__id_ensfile__exact = nef).filter(actif=True).order_by('-date_modification','name_file')
	else:
		files = File.objects.filter(ensfile__id_ensfile__exact = nef).filter(actif=True).filter(visible=True).order_by('-date_modification','name_file')
	
	ef.vc = ef.vc+1
	ef.save()
	
	files=pagination(files,request.GET.get('page','1'))
	return render_to_response('data/files.html',{
		'ef':ef,
		'files': files,
		'me':me,
		},context_instance=RequestContext(request))

