# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q

from plato.models import User, EnsFile, File, TypeEnsFile
from util.object_util import *

##########################3D###########################
def v3d(request):
	"""
	brief 3D main page
	"""
	me=get_object_or_404(User, login='guest')
	if request.session.has_key('login'):
		me = get_object_or_404(User, login=request.session['login'])
		all_src = EnsFile.objects.filter(type_ens_file__id_type_ensfile__exact=6).filter(Q(all_f=True)|Q(group__in=me.group_users.all())).filter(actif=True).order_by('-date_modification','name_ensfile')
	else:
		all_src = EnsFile.objects.filter(type_ens_file__id_type_ensfile__exact=6).filter(all_f=True).filter(public=True).filter(actif=True).order_by('-date_modification','name_ensfile')		
	all= pagination(all_src,request.GET.get('page','1'))
	return render_to_response('cg/cg.html',{
		'Sources': all,
		'me':me,
		},context_instance=RequestContext(request))

def v3df(request,nef):
	"""
	show files of the ensfile
	"""
	ef = get_object_or_404(EnsFile, id_ensfile = nef)
	me=get_object_or_404(User, login='guest')
	if request.session.has_key('login'):
		me = get_object_or_404(User, login=request.session['login'])
		files = File.objects.filter(ensfile__id_ensfile__exact = nef).filter(actif=True).filter(Q(all_f=True)|Q(group__in=me.group_users.all())).order_by('-date_modification','name_file')
	elif ef.public==True:
		files = File.objects.filter(ensfile__id_ensfile__exact = nef).filter(actif=True).filter(all_f=True).order_by('-date_modification','name_file')
	else:
		return return_referer(request)
	ef.vc += 1
	ef.save()
	files=pagination(files,request.GET.get('page','1'))
	return render_to_response('cg/cgf.html',{
		'files': files,
		'me':me,
		'ef':ef,
		},context_instance=RequestContext(request))
	
	#return render_to_response('empty.html', context_instance=RequestContext(request))


