
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q,Max,StdDev,Avg

from plato.models import User,Instrument, Sound, Note, EnsFile, File
from util.object_util import *

##############################################################################################
	#################################### SHOW AUDIO  INFO ################################
##############################################################################################

	
def vaudioinfo(request):
	return render_to_response('audio/audio.html',context_instance=RequestContext(request))

# from django.views.decorators.cache import never_cache
#from django.utils import simplejson

# @never_cache
def vaudiocorpusinfo(request):
	"""
	View function to show the audio corpus (we will add album in the futur)
	"""
	
	me=get_object_or_404(User, login='guest')
	if request.session.has_key('login'):
		me = get_object_or_404(User, login=request.session['login'])
		aud_src = EnsFile.objects.filter(type_ens_file__id_type_ensfile__exact=1).filter(actif=True).filter(Q(all_f=True)|Q(group__in=me.group_users.all())).order_by('-date_modification','name_ensfile')
	else:
		aud_src = EnsFile.objects.filter(type_ens_file__id_type_ensfile__exact=1).filter(actif=True).filter(all_f=True).filter(public=True).order_by('-date_modification','name_ensfile')
		
	aud = pagination(aud_src,request.GET.get('page','1'))
	return render_to_response('audio/audio_corpus.html',{
		'Sources': aud,
		'me':me,
		},context_instance=RequestContext(request))

def vaudiocorpusaudioinfo(request,nc):
	
	ef = get_object_or_404(EnsFile, id_ensfile = nc)
	ef.vc += 1
	ef.save()
	
	me=get_object_or_404(User, login='guest')
	if request.session.has_key('login'):
		me = get_object_or_404(User, login=request.session['login'])
	elif ef.public==False:
		return return_referer(request)

	aud = Sound.objects.filter(file__ensfile__id_ensfile__exact = nc)
	if aud:
		titre = aud[0].file.ensfile.name_ensfile
	else:
		titre = '3mpty'
	aud = pagination(aud,request.GET.get('page','1'))
	return render_to_response('audio/audio_corpus_nd.html',{
		'Audio': aud,
		'me':me,
		'titre':titre,
		'ef':ef,
		},context_instance=RequestContext(request))


def vaudio(request,nc):
	
	me=get_object_or_404(User, login='guest')
	if nc=='all':
		aud_src = Sound.objects.all()
		titre = "sound"
	elif nc=="ensemble":
		aud_src = Sound.objects.filter(type_sound__id_type_sound=1)
		titre="ensemble sound"
	elif nc=="solo":
		aud_src = Sound.objects.filter(type_sound__id_type_sound=3)
		titre="solo sound"
	elif nc=="isolated":
		aud_src = Sound.objects.filter(type_sound__id_type_sound=4)
		titre="isolated notes"
	elif nc=="note":
		aud_src = Sound.objects.filter(type_sound__id_type_sound=2)
		titre = "note sound"
	elif nc=="non":
		aud_src = Sound.objects.filter(type_sound__id_type_sound__gt=4)
		titre = "Non musical file"
	else:
		redirect('platon.audio.views.vaudioinfo')

	if request.session.has_key('login'):
		me = get_object_or_404(User, login=request.session['login'])
		aud_src = aud_src.filter(file__actif=True).filter(Q(file__all_f=True)|Q(file__group__in=me.group_users.all())).order_by('-file__date_modification','file__name_file')
	else:
		aud_src = aud_src.filter(file__actif=True).filter(file__all_f=True).filter(file__ensfile__public=True).order_by('-file__date_modification','file__name_file')
		

	aud = pagination(aud_src,request.GET.get('page','1'))
	return render_to_response('audio/audio_corpus_nd.html',{
		'Audio': aud,
		'me':me,
		'titre':titre,
		},context_instance=RequestContext(request))
