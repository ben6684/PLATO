# -*- coding: utf-8 -*-
import urllib
from object_util import *
from HTMLParser import HTMLParser
from django.shortcuts import get_object_or_404
from plato.models import Author, User, Page, PageAuthor, File, TypeFile, TypePage

def add_author_from_publi(fstnm, nm):
	"""
	\brief : add an author not into the base for publication pages

	"""
	a = Author(fstnm=fstnm, nm=nm, fstnm_i = fstnm)	
	P = User.objects.filter(nm_person = nm)
	if P:
		for p in P:
			if p.fstnm_person[0]==fstnm[0]:
				a.id_user = p.id_user
	a.save()
	return a

class pars(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.rec_p = 0
		self.rec_i = -1
		self.rec_a =0
		self.auth =[]
		self.titre=[]
		self.conf=[]
	
	def handle_starttag(self, tag, attrs):
		if tag == 'p':
			self.rec_p=1
			self.rec_i=0
		if tag == 'i':
			self.rec_i=1
		if tag == 'a':
			self.rec_a =1
			
	def handle_endtag(self, tag):
		if tag == 'p':
			self.rec_p=0
			self.rec_a =0
		if tag == 'i':
			self.rec_i=-1
			
	def handle_data(self, data):
		if self.rec_p:
			if self.rec_i==0:
				self.auth.append(data)
			elif self.rec_i==1:
				self.titre.append(data)
			elif self.rec_i==-1 and self.rec_a==0:
				self.conf.append(data)
	
def upd_biblio_html(user):

	params = urllib.urlencode({'dept':'tsi','year':'-50'})
	f = urllib.urlopen("http://biblio.telecom-paristech.fr/cgi-bin/ws/biblio.cgi?%s"%params)
	
	parser = pars()
	parser.feed(f.read())
	l = len(parser.titre)
	for i in range(l):

		############## ADD CONF ##############
		conf = parser.conf[i]
		conf = conf.lstrip(', ')
     	############## ADD PUBLI ###############

		titre = parser.titre[i]
		page = Page(titre=titre, conf_raw = conf, manager=user)
		page.save()
		
	    ############## ADD AUTHORS ###############
		auth =parser.auth[i]
	
		auth = auth.replace(' and ',',')
		auth = auth.replace(' et ',',')
		auth = auth.replace(', ',',')
		auth = auth.rstrip(',')
		la = auth.split(',')
		cpt=1
		for a in la:
			prenom=""
			nom=""
			fnm=a.split(' ')
			try:
				fnm.remove('')
			except:
				pass
			if fnm:
				for f in fnm:
					if f[-1]=='.':
						prenom=prenom +f.rstrip('.')+" "
					else:
						nom=nom +f+" "
			
				prenom = titlecase(prenom.rstrip(' '))				
				nom = titlecase(nom.rstrip(' '))
				if nom and prenom:
					au = Author.objects.filter(nm=nom, fstnm_i__startswith=prenom[0])
					if au:
						if au[0].id_user:
							page.manager = au[0].id_user
						pa=PageAuthor(author=au[0],page=page,order=cpt)
						pa.save()
					else:
						a = Author(fstnm=prenom, nm=nom, fstnm_i = prenom)
						P = User.objects.filter(nm_person = nom, fstnm_person__startswith = prenom[0])
						if P:
							a.id_user=P[0]
							page.manager = P[0]
						a.save()
						pa=PageAuthor(author=a,page=page,order=cpt)
						pa.save()
						
						
					cpt=cpt+1
					#print "ploum"
					# print "prenom db ="+prenom
					# print "nom db ="+nom
		        #### add author ####	
				
		page.save()
#upd_biblio()

import re
def find_year_from_raw_conf():
	"""
	Some stupid function to find the date into the conf_raw
	"""
	pages = Page.objects.all()

	for p in pages:
		s=p.conf_raw
		if s:
			match=re.search(r'(?:J(anuary|u(ne|ly))|February|J(anvier|ui(n|llet))|Février|Ma(rch|y|rs|i)|A(pril|ugust|vril|oût|out)|(((Sept|Nov|Dec)em)|Octo)ber|(((Sept|Nov|Dec)em)|Octo)bre)\ ((19|20)\d{2})',s)
			if match:
				print match.group(1)
				p.mois = match.group(1)
				p.annee = match.group(2)
			else:
				match2 = re.search(r'((19|20\d{2}))',s)
				if match2:
					p.annee = match2.group()

		#p.save()

def add_author(auth,page):
	
	auth = auth.replace(' and ',',')
	auth = auth.replace(' et ',',')
	auth = auth.replace(';',',')
	auth = auth.replace(', ',',')
	auth = auth.rstrip(',')
	la = auth.split(',')
	cpt=1
	for a in la:
		prenom=""
		nom=""
		fnm=a.split(' ')
		try:
			fnm.remove('')
		except:
			pass
		if fnm:
			for f in fnm:
				f=f.strip()
				if f[-1]=='.':
					prenom=prenom +f.rstrip('.')+" "
				else:
					nom=nom +f+" "
			
			prenom = titlecase(prenom.rstrip(' '))				
			nom = titlecase(nom.rstrip(' '))
			if nom and prenom:
				au = Author.objects.filter(nm__iexact=nom, fstnm_i__istartswith=prenom[0])
				if au:
					if au[0].id_user:
						page.manager = au[0].id_user
					pa=PageAuthor(author=au[0],page=page,order=cpt)
					pa.save()
				else:
					a = Author(fstnm=prenom, nm=nom, fstnm_i = prenom)
					P = User.objects.filter(nm_person = nom, fstnm_person__startswith = prenom[0])
					if P:
						a.id_user=P[0]
						page.manager = P[0]
					a.save()
					pa=PageAuthor(author=a,page=page,order=cpt)
					pa.save()
						
						
				cpt=cpt+1	
				
	page.save()

	
import SOAPpy
class SOAPProxy(SOAPpy.SOAPProxy):
	"""Wrapper class for SOAPpy.SOAPProxy

	Designed so it will prepend the namespace to the action in the SOAPAction
	HTTP headers.
	"""

	def __call(self, name, args, kw, ns = None, sa = None, hd = None, ma = None):
		
		
		ns = ns or self.namespace
		sa = sa or self.soapaction

		# Only prepend namespace if no soapaction was given.
		if ns and not sa:
			sa = '%s#%s' % (ns, name)
		
		return SOAPpy.SOAPProxy.__call(self, name, args, kw, ns, sa, hd, ma)

def def_mm(s):
	m=0
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


import xml.etree.ElementTree as ET
def upd_biblio_soap(user):
	"""
	Same as before but with a STUPID SOAP client 

	"""
	clientSOAP = SOAPProxy("http://biblio.telecom-paristech.fr/cgi-bin/ws.cgi",namespace ="Bib/BibWS")
	# clientSOAP.config.debug=1
	# clientSOAP.config.dumpSOAPOut = 1 
	# clientSOAP.config.dumpSOAPIN = 1 
	#lp = clientSOAP.getXMLRef('dept:tsi; year:-2', 'utf8', {'lang':'fr','context':1}, {'nameFirst':0,'fnameInitial':1})
	#print lp
	tf=get_object_or_404(TypeFile,id_type_file=5)
	lp = clientSOAP.getXMLRef()
	# lp is a XML string => to parse and far away !
	root = ET.fromstring(lp)
	#f=open('/tmp/prout','w')

	#we are putting ervything to 0, and then every publication find into tsi publication are set to 1
	# then for all the remain vc = 0 page => a delete button will appear !
	ps = Page.objects.all()
	for p in ps:
		if not p.flag_plato:
			p.flag_suppr = True
			p.save()


	#new_page=""
	for child in root:
		#child = publication !
		dept = child.findtext('dept',"plop")
		#if no deptartement id filled => dept contains  "plop"
		if dept=="TSI":					
			title = child.findtext('title',"plop")
			if title!="plop":
				
				test_page = Page.objects.filter(titre__iexact=title.strip(',').rstrip())
				# il faut faire en sorte que ce test SOIT insenssible aux espaces.
				
				
				#the publication is a new one !
				if not test_page:
					#return "new page ="+title
					#new_page+=(title+"<br>")
					
					page = Page(titre=title,manager = user)
					page.save()
					# pas convaincu => a voir pour la suite ... 
					auth = child.findtext('author',"plop")
					add_author(auth,page)
			
					conf = child.findtext('journal')			
					if conf!=None:
						page.conf_raw = conf
					conf = child.findtext('booktitle')			
					if conf!=None:
						page.conf_raw = conf
			
			
					bibtex = child.find('bibtex')
					if bibtex != None:
						year = bibtex.findtext('year')
						if year!=None:
							page.annee = year
						month= bibtex.findtext('month')
						if month!=None:
							mm = def_mm(month)
							page.mon = mm
							page.mois = month
						else:
							page.mon = 0
						pages= bibtex.findtext('pages')
						if pages!=None:
							page.pages = pages
						conf = bibtex.findtext('journal')
						if conf!=None:
							page.conf_raw = conf
						KW = bibtex.findtext('keywords')#use add_kw(obj,kw)
						if KW!=None:
							add_kw(page,KW)
						volume = bibtex.findtext('volume')
						if volume!=None:
							page.volume = volume
						number = bibtex.findtext('number')
						if number!=None:
							page.number = number
						publisher = bibtex.findtext('publisher')
						if publisher!=None:
							page.publisher = publisher
						
					import datetime
					hal = child.findtext('hal',"plop")
					if hal!="plop":
						if hal and hal!=None:
							f=File(name_file=title, path="http://hal-institut-telecom.archives-ouvertes.fr/"+hal,type_file=tf,manager=page.manager,date_creation=datetime.date.today(),date_modification=datetime.date.today(),date_del=datetime.date(9999,12,12))
							f.save()
							page.id_article=f
							page.save()
			
					url = child.findtext('url',"plop")
					if url!="plop":
						if url and url!=None:
							f=File(name_file=title, path=url,type_file=tf,manager=page.manager,date_creation=datetime.date.today(),date_modification=datetime.date.today(),date_del=datetime.date(9999,12,12))
							f.save()
							page.id_article=f
							page.save()
					
					typ = child.get('bibtype')
					type_pag = TypePage.objects.filter(nm_type_page__iexact=typ)
					page.type_page=type_pag[0]
					page.vc = 1
					page.save()
					
				else:
					### The page exists => Verify any difference 
					page=test_page[0]
											
					# auth = child.findtext('author',"plop")
					# if author:
						
					# add_author(auth,page)
			
					conf = child.findtext('journal')			
					if conf!=None and page.conf_raw!=conf:
						page.conf_raw = conf
					conf = child.findtext('booktitle')			
					if conf!=None and page.conf_raw!=conf:
						page.conf_raw = conf
			
			
					bibtex = child.find('bibtex')
					if bibtex != None:
						year = bibtex.findtext('year')
						if year!=None and page.annee != year:
							page.annee = year
						month= bibtex.findtext('month')
						if month!=None and page.mon != month:
							mm = def_mm(month)
							page.mon = mm
							page.mois = month
						pages= bibtex.findtext('pages')
						if pages!=None and page.pages != pages:
							page.pages = pages
						conf = bibtex.findtext('journal')
						if conf!=None and page.conf_raw!=conf:
							page.conf_raw = conf
						# KW = bibtex.findtext('keywords')#use add_kw(obj,kw)
						# if KW!=None:
						# 	add_kw(page,KW)
						volume = bibtex.findtext('volume')
						if volume!=None and page.volume!=volume:
							page.volume = volume
						number = bibtex.findtext('number')
						if number!=None and page.number!=number:
							page.number = number
						publisher = bibtex.findtext('publisher')
						if publisher!=None and page.publisher!=publisher:
							page.publisher = publisher

					if not page.id_article:
						import datetime
						hal = child.findtext('hal',"plop")
						if hal!="plop":
							if hal and hal!=None:
								f=File(name_file=title, path="http://hal-institut-telecom.archives-ouvertes.fr/"+hal,type_file=tf,manager=page.manager,date_creation=datetime.date.today(),date_modification=datetime.date.today(),date_del=datetime.date(9999,12,12))
								f.save()
								page.id_article=f
								page.save()
			
						url = child.findtext('url',"plop")
						if url!="plop":
							if url and url!=None:
								f=File(name_file=title, path=url,type_file=tf,manager=page.manager,date_creation=datetime.date.today(),date_modification=datetime.date.today(),date_del=datetime.date(9999,12,12))
								f.save()
								page.id_article=f
								page.save()

					
					typ = child.get('bibtype')
					type_pag = TypePage.objects.filter(nm_type_page__iexact=typ)
					if page.type_page!=type_pag[0]:
						page.type_page=type_pag[0]
					page.flag_suppr = False
					page.save()

	return True
	#return new_page

def del_shit():
	for p in pages:
		if p.id_page!=11:
			del_page_db(p.id_page)
	pa= PageAuthor.objects.exclude(page_id=11)
	for p in pa:
		p.delete()
	au = Author.objects.all()
	for a in au:
		if a.id_author>124:
			a.delete()
