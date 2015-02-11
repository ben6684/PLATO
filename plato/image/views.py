
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse

import datetime
from django.db.models import Q,Max

from util.object_util import *
from plato.models import Image,User,File, EnsFile
import plato

##############################################################################################
	################################# IMAGE #########################################
##############################################################################################

def vimg(request):
	"""
	brief method that render the main image page
	"""
	return render_to_response('image/image.html',context_instance=RequestContext(request))


def vimgsrc(request,ti):
	"""
	brief method that render the image sources info !!
	"""
	if ti=="generic":
		img_src = EnsFile.objects.filter(type_ens_file__id_type_ensfile =2)
	elif ti=="medical":
		img_src = EnsFile.objects.filter(type_ens_file__id_type_ensfile =3)
	elif ti=="satellite":
		img_src = EnsFile.objects.filter(type_ens_file__id_type_ensfile =4)
	else:
		return redirect('idx')

	
	
	me=get_object_or_404(User, login='guest')
	if request.session.has_key('login'):
		me = get_object_or_404(User,login=request.session['login'])
		img_src = img_src.filter(Q(all_f=True)|Q(group__in=me.group_users.all())).filter(actif=True).order_by('-date_modification','name_ensfile')
	else:
		img_src = img_src.filter(all_f=True).filter(actif=True).filter(public=True).order_by('-date_modification','name_ensfile')

	img_src=pagination(img_src,request.GET.get('page','1'))
	return render_to_response('image/gimagesrc.html',{
		'Img': img_src,
		'me':me,
		},context_instance=RequestContext(request))

# def img_more(request):
# 	"""
# 	view function that recieve a GET signal from an AJAX function and return some HTML to show
# 	"""
# 	if request.GET.has_key('id_mma'):
# 		ide = request.GET['id_mma']
# 		if ide:
# 			f= get_object_or_404(File, id_file = ide)
# 			print f.path
# 			thumb = os.path.splitext(f.path)[0] + ".THUMB" + os.path.splitext(f.path)[1]#str(f.path)#+".THUMB"
# 			try:
# 				open(thumb)
# 				HTML="""<img src="/root/%s"> """%(thumb)
# 			except:
# 				HTML="""<img src="/root/%s" width="255px"> """%(f.path)
# 			return HttpResponse(HTML)

			
def vimgs(request,nc):
	"""
	brief method that render the file in a source 
	"""

	img_src = plato.models.Image.objects.filter(file__ensfile__id_ensfile__exact=nc)
	ef = get_object_or_404(EnsFile, id_ensfile = nc)
	ef.vc += 1
	ef.save()
	
	if request.session.has_key('login'):
		me = get_object_or_404(User,login=request.session['login'])
		img_src = img_src.filter(Q(file__all_f=True)|Q(file__group__in=me.group_users.all())).filter(file__actif=True).order_by('-file__date_modification','file__name_file')
	elif ef.public==True:
		me=get_object_or_404(User, login='guest')
		img_src = img_src.filter(file__all_f=True).filter(file__actif=True).order_by('-file__date_modification','file__name_file')
	else:
		return return_referer(request)
	
	
	img_src=pagination(img_src,request.GET.get('page','1'),50)

	return render_to_response('image/gimage.html',{
		'Img': img_src,
		'me':me,
		'ef':ef,
		},context_instance=RequestContext(request))
