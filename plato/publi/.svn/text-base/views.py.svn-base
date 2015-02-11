# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.db.models import Q,Max
import datetime

from plato.models import Conf,User, Page, PageAuthor, Author
from plato.form import PublicationFilter
from util.object_util import *
#from util.upd_biblio import *

def def_mm(s):
	m=None
	if s=='jan':
		m=1
	if s=='feb':
		m=2
	if s=='mar':
		m=3
	if s=='apr':
		m=4
	if s=='may':
		m=5
	if s=='jun':
		m=6
	if s=='jul':
		m=7
	if s=='aug':
		m=8
	if s=='sep':
		m=9
	if s=='oct':
		m=10
	if s=='nov':
		m=11
	if s=='dec':
		m=12
	
	return m

def vpages(request):
	"""
	Show all the latest publication
	"""
	this_year = Page.objects.filter(flag_suppr=False).aggregate(Max('annee'))['annee__max']
	if request.GET.has_key('annee'):
		ide = request.GET['annee']
		if ide:
			annee = ide
	else:
		annee = this_year
		
	if request.method == 'POST':
		form = PublicationFilter(request.POST,prefix='publi_filter')
		if form.is_valid():
			year =form.cleaned_data['year']
			mois =form.cleaned_data['mois']
			author = form.cleaned_data['author']
			search = form.cleaned_data['search']
			pages = Page.objects.filter(flag_suppr=False)
			flag=False
			if year and year!='None':
				pages = pages.filter(annee=year)
				flag=True
			if mois:
				pages = pages.filter(mon = def_mm(mois))
			if author:
				pages = pages.filter(author__nm__icontains=author)
			if search:
				pages= pages.filter(Q(titre__icontains=search)|Q(conf_raw__icontains=search)|Q(abstract__icontains=search))
			
			pages = pages.order_by('-annee','-mon','titre')
			return render_to_response('publi/pages.html',{
				'pages':pages,
				'annee':annee,
				'ty':this_year,
				'form':form,
				'flag':flag,
				}, context_instance=RequestContext(request))
		else:
			if request.session['lang']=='fr':
				form=trans_label_fr(form)	
			return render_to_response('publi/pages.html',{
				'form':form,
				'error_message':form.errors,
				}, context_instance=RequestContext(request))
	else:
		form = PublicationFilter(prefix='publi_filter')
		if request.session.has_key('lang'):
			if request.session['lang']=='fr':
				form=trans_label_fr(form)
		else:
			request.session['lang']=='en'
		flag=True
		pages = Page.objects.filter(flag_suppr=False).filter(annee=annee).order_by('-mon','titre')
		return render_to_response('publi/pages.html',{
			'pages':pages,
			'annee':annee,
			'ty':this_year,
			'form':form,
			'flag':flag,	
			}, context_instance=RequestContext(request))
	
		
def vpage(request,np):
	"""
	Show the publication page
	"""
	page = get_object_or_404(Page,id_page=np)
	f = False
	if request.session.has_key('login'):
		connected = get_object_or_404(User,login=request.session['login'])
		if connected in [user.id_user for user in page.author.all()]:
			f= True
	#else:
	#page.vc = page.vc + 1
	#page.save()
	page_fig = page.figures.all().order_by('type_file__id_type_file')
	return render_to_response('publi/page.html',{
		'page':page,
		'flag':f,
		'page_fig':page_fig,
		}, context_instance=RequestContext(request))
