
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q

from util.object_util import *
from plato.models import Video,User,EnsFile,File

#### This set of tools are here for render videos pages ! ####


#is_logged is a decorator for verifying that the person who tried to access this data is logged ! => not used anymore because i use the same function for plato-ext


def vvid(request):
	"""
	brief method that render the main videos page with all the videos
	"""
	# because it always use a user to render the html file; and guest has no right at all ! 
	me=get_object_or_404(User, login='guest')
	if request.session.has_key('login'):
		# the connected person ... 
		me = get_object_or_404(User,login=request.session['login'])
		# the ensfile related to the videos, the first filter is to get videos only, the second the valid videos only, and the third if you have the right to view theses objects or if it's private to a group and order by modif and name
		ef = EnsFile.objects.filter(type_ens_file__id_type_ensfile__exact = 5).filter(actif=True).filter(Q(all_f=True)|Q(group__in=me.group_users.all())).order_by('-date_modification','name_ensfile')
	else:
		# you're not logged, so you see only public info.
		ef = EnsFile.objects.filter(type_ens_file__id_type_ensfile__exact = 5).filter(actif=True).filter(all_f=True).filter(public=True).order_by('-date_modification','name_ensfile')

	# pagination is in object_util and is here to manage pagination of results. 
	ef = pagination(ef,request.GET.get('page','1')) # pagination are on object util
	return render_to_response('video/video.html',{
		'src':ef,
		'me':me,
		},context_instance=RequestContext(request))


def vvidinfo(request,nc):
	"""
	brief : method that show the ensefile video info (meaning all the files in the ensfile) !
	input : nc is the id of the ensfile
	"""
	me=get_object_or_404(User, login='guest')
	# get the ensfile object !!!
	ef = get_object_or_404(EnsFile, id_ensfile = nc)
	if request.session.has_key('login'):
		# the conencted person
		me = get_object_or_404(User,login=request.session['login'])
		# the chosen ensfile (nc IS the id of ensfile )
	elif ef.public==False:
		# the ef is not public and you're not logged (SO you're here by typing directly the adress !)
		try:
			return redirect(request.META['HTTP_REFERER'])
		except:
			return redirect('idx')
	# incremente the number of view of the ensfile (not used anymore !)
	#ef.vc += 1
	#ef.save()
	
	# now select the videos files linked to the ensfile
	vid_src = Video.objects.filter(file__ensfile = nc)
	#paginate them !
	vid = pagination(vid_src,request.GET.get('page','1'))
	return render_to_response('video/gvideo.html',{
		'Vid': vid, 
		'me':me,
		'ef':ef,
		},context_instance=RequestContext(request))
