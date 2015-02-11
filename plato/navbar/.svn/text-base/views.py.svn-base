# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse
from django.db.models import Q
from django.core.urlresolvers import reverse

from plato.models import User, Group, EnsFile
from util import auth, object_util
from util.object_util import *
from util.views import *

import datetime

# def user_info(user,login,list_grp):
	
# 	# the information case:
# 	HTML="""
# 	<div id="fiche">
# 	<div id="foto">
# 	<img src="/plato/plato_users/%s/profil.jpg" width="100px" alt=" " onerror="this.onerror=null;this.src='/users/static/images/empty-face.jpg';" >
# 	</div>
# 	<div id="lefty">
# 	<h3> Personal Information </h3>
	
# 	<table style="margin-top:25px; text-align:left;" align="center">
# 	<tr><td> Name </td><td> : </td><td> %s</td></tr>
# 	<tr><td> First name</td><td> : </td><td> %s </td></tr>"""%(user.login,user.nm_person,user.fstnm_person)
# 	HTML+="""
# 	<tr><td> Webpage</td><td> : </td><td> <a href=%s> %s </a></td></tr>
# 	<tr><td> Email</td><td> : </td><td> %s</td></tr>
# 	<tr><td> Location</td><td> : </td><td> %s</td></tr>
# 	<tr><td> Status</td><td> : </td><td> %s</td></tr>"""%(user.webpage_person,user.webpage_person,user.email_person,user.office,user.status.nm_user_status)

# 	if user.account_expiration_date < datetime.date(9000,1,1):
# 		HTML+="""<tr><td> Expiration date</td><td> : </td><td> %s</td></tr>"""%(user.account_expiration_date)
		
# 	HTML+="""<tr><td> Telephone</td><td> : </td><td> %s</td></tr>"""%(user.telephone)
# 	if user.id_boss:
# 		boss = get_object_or_404(User,id_user=user.id_boss)
# 		HTML+="""<tr><td> Referent</td><td> : </td><td> <a href="/users/%s/"> %s %s</a></td></tr>"""%(boss.login,boss.fstnm_person,boss.nm_person)

# 	HTML+="""</table>"""

# 	if user.login == login:
# 		HTML+="""<p align='center'><a href="/users/%s/update/"> Update info </a></p>"""%(user.login)

# 	HTML+="""</div> <div id="righty"><h3>Involved in project :</h3>"""
	
# 	gpe = user.group_users.all()
# 	if not gpe:
# 		HTML+=""" <p style="text-align:center; font-size:24px;"> don't belong to any groupe</p>"""
# 	else:
# 		HTML+="""<table style="margin-top:25px; text-align:left;" align="center">"""
# 		for g in gpe:
# 			if g.type_group==1 or g.id_group in list_grp:# i don't display the group if they're not visible except if the connected person is in the group
# 				HTML+="""<tr><td><a href="/groups/%s/"> %s </a></td>"""%(g.id_group,g.name_group)
# 				if user.login== login:
# 					HTML+="""<td><input type="button" value="Quit" onclick="quit_group( '%s' , %s ) "></td>"""%(user.login,g.id_group)
# 				HTML+="""</tr>"""
# 		HTML+="""</table>"""
# 	HTML+="""</div></div>"""
# 	return HTML

# def group_info(gpe,me):
# 	HTML="""<div id="fiche">
# 	<div id="foto">
# 	<img src="/plato/projects/%s/profil.jpg" height="80px" alt=" " onerror="this.onerror=null;this.src='/users/static/images/logo_telecom.png';">
# 	</div>
# 	<div id="lefty">
# 	<h3> Group information </h3>
	
# 	<table style="margin-top:25px; text-align:center;" align="center">
# 	<tr> <td> Name </td><td>:</td> <td> %s </td></tr>
# 	<tr> <td> Webpage </td><td>:</td> <td> <a href=%s>%s</a></td></tr>
# 	<tr> <td> Email </td><td>:</td> <td> %s</td></tr>"""%(gpe.name_group,gpe.name_group,gpe.website,gpe.website,gpe.email)
# 	if gpe.date_del < datetime.date(9000,1,1):
# 		HTML+="""<tr><td> Expiration date</td><td> : </td><td> %s</td></tr>"""%(gpe.date_del)
# 	HTML+="""<tr> <td> Description </td><td>:</td> <td> %s</td></tr>
# 	<tr> <td> Keywords </td><td>: </td> <td> """%(gpe.desc_group)
# 	for kw in gpe.KW.all():
# 		HTML+="""<a href="/search?KW=%s">%s</a>, """%(unicode(kw),unicode(kw))
# 	HTML+="""</td></tr>
# 	</table>
# 	<div style="margin-top:50px">"""
# 	if gpe.manager == me:
# 		HTML+="""
# 		<p align='center'><a href="/group/%s/update/"> Edit Group </a></p>
# 		<p align='center'><a href="/group/%s/delete/"> Delete Group </a></p>
# 		"""%(gpe.id_group,gpe.id_group)
# 	HTML+="""</div></div><div id="righty">
# 	<h3>members of the group :</h3>
# 	<table align='center' style="margin-top:15px;">"""
# 	for u in gpe.users.all():
# 		if u.actif:
# 			HTML+=""" <tr><td> <a href="/users/%s/"> %s %s </a></td>"""%(u.login,u.fstnm_person,u.nm_person)
# 			if gpe.manager == me:
# 				HTML+="""<td> </td><td> <a href="/groups/%s/%s/delete/"> delete </a></td>"""%(gpe.id_group,u.login)
# 			HTML+="""</tr>"""
# 	HTML+="""</table></div><div id="bottomy">
# 	  <p align="center"> <b>Plato group manager</b> : <a href="/users/%s/"> %s %s </a></p></div>
# 	</div>"""%(gpe.manager.login,gpe.manager.nm_person,gpe.manager.fstnm_person)
# 	return HTML
	
def show_tools(me,user=None,gpe=None,c=False):

	# Show Sources codes
	if user:
		algos = Tool.objects.filter(manager= user).order_by('-date_modification')
	elif gpe:
		algos = Tool.objects.filter(group=gpe).order_by('-date_modification')
	else:
		algos = Tool.objects.all().order_by('-date_modification')

	if not c:
		algos=algos.filter(visible=True)
		
	HTML="""<table align='center'>"""
		
	if not algos:
		HTML+=""" <p style="text-align:center; font-size:24px;"> No Tool added</p>"""
	else:
		for a in algos:
			HTML+="""<div id="object">
			<h3><a href="/app/%s">%s</a></h3>
			<div id="objectlogo">
			<img src="/users/static/images/application.png">
			</div>
			<div id="objectcontent">
			Description : %s
			"""%(a.id_tool,a.name_tool, a.desc_tool)
			if a.manager == me:
				HTML+="""<input type="button" value="Modify" onclick="self.location.href='/add_app/upd/%s/'"> <input type="button" value="Delete" onclick="del_algo(%s)"> """%(a.id_tool, a.id_tool)
			HTML+="""</div></div> """
	HTML+=""" """
	return HTML

def show_publis(me,user=None,gpe=None):
	this_year =  datetime.datetime.now().year
	#Publication
	if user:
		page = Page.objects.filter(flag_suppr=False).filter(author__id_user = user).order_by('-annee','-mon')
	elif gpe:
		page = Page.objects.filter(flag_suppr=False).filter(group=gpe).order_by('-annee','-mon')
	else:
		page = Page.objects.filter(flag_suppr=False).order_by('-annee','-mon')
	HTML=""" """
	if not page:
		HTML=""" <p style="text-align:center; font-size:24px;"> No publication added</p>"""
		return HttpResponse(HTML)

	cpt_annee = this_year+1
	for p in page:
		if p.annee != cpt_annee:
			cpt_annee = p.annee
			HTML+= """ <h4> %s </h4> """%(cpt_annee)

		HTML+="""<div id="article">
		"""
		if p.abstract:
			HTML+="""<div id="article-infos"><h3><a href="/publi/%s/">%s </a></h3><author> """%(p.id_page,p.titre)
		else:
			HTML+="""<div id="article-infos"><h3>%s</h3><author> """%(p.titre)
		it=1
		c = p.author.count()
		for a in p.author.all():
			if a.id_user:
				HTML+="""<a href="/users/%s/">%s. %s</a>"""%(a.id_user.login,a.fstnm_i, a.nm)
			else:
				HTML+="""%s. %s"""%(a.fstnm_i, a.nm)
			if it <c:
				HTML+=""", """
				it=it+1
			else:
				HTML+="""</author><br>"""
		if p.id_conf:
			HTML+="""<conf>%s %s</conf><br>
			</div>
			<div id="article-dl">"""%(p.id_conf.titre_conf, p.annee)
		elif p.conf_raw:
			HTML+="""<conf>%s %s %s</conf><br>
			</div>
			<div id="article-dl">"""%(p.conf_raw,p.mois,p.annee)
		else:
			HTML+="""<conf>%s %s</conf><br>
			</div>
			<div id="article-dl">"""%(p.mois,p.annee)
		if p.id_article:
			HTML+="""<a href="/util/download/%s" target="_blank"><img src="/users/static/images/f_pdf_32.png"></a>"""%(p.id_article.id_file)
		if p.id_presentation:
			HTML+="""<a href="/util/download/%s" target="_blank"><img src="/users/static/images/prez_32.png"></a>"""%(p.id_presentation.id_file)
		if me.id_user in p.author.values_list('id_user',flat=True):
			HTML+="""<input type="button" value="modify" onclick="self.location.href='/add_publi/upd/%s/'">"""%(p.id_page)
			if p.vc == 0:# not in the tsi publications
				HTML+="""<input type="button" value="Delete" onclick="self.location.href='/add_publi/del/p/%s/'">"""%(p.id_page)
				
				
		HTML+="""	&nbsp;</div></div>"""
	return HTML
	
def show_ens_media(me,user=None,gpe=None):
	
	#ens media
	if user:
		media = EnsFile.objects.filter(manager = user).order_by('-date_modification')
	elif gpe:
		media = EnsFile.objects.filter(group = gpe).order_by('-date_modification')
	else:
		media = EnsFile.objects.all().order_by('-date_modification')

	HTML=""" """
	if not media:
		HTML+=""" <p style="text-align:center; font-size:24px;"> No media added</p>"""
	else:
		for m in media:
			if m.all_f:
				HTML+="""<div id="object">
				<a href="/data/%s"><h3>%s</h3></a>
				<div id="objectlogo">"""%(m.id_ensfile,m.name_ensfile)
				HTML+="""<img src="/users/static/images/lena.jpg"><br>
				<img src="/users/static/images/audio.png">"""
				HTML+="""
				</div>
				<div id="formodif%s">

				<div id="objectcontent">
				<ul>
				<li> Description :  %s </li>
				<li> Manager : %s %s </li>
				<li> Origin : %s </li>
				<li> Copyright : %s </li>
				<li> Creation date : %s </li>
				<li> Modification date : %s </li>
				</ul>
				</div>
				"""%(m.id_ensfile,m.desc_ensfile,m.manager.fstnm_person,m.manager.nm_person,m.origin, m.copyright, m.date_creation,m.date_modification)
				if me == m.manager:
					HTML+="""
					<div id="objectcontentmore">
					<input type="button"  value="Delete" onclick="del_media(%s)">
					<input type="button"  value="Modify" onclick="m_media(%s)"><br>	
					</div>
					"""%(m.id_ensfile, m.id_ensfile)
				HTML+="""</div></div> """
	return HTML

def usr_selected(request,log):
	"""
	\brief Catch the ajax request send by the nav bar => fill the information and display them into the good div
	\author{B.Petitpas}
	"""
	id=-1
	HTML=""
	if request.is_ajax():
		if request.GET.has_key('id'):
			id=request.GET['id']
		else:
			return HttpResponse("")
	else:
		return HttpResponse("")
	if id!=-1:
		#global informations
		user = get_object_or_404(User,login=log)
		# below : the connected person info
		if request.session.has_key('login'):
			me = get_object_or_404(User,login=request.session['login'])
			c=True
		else:
			me = get_object_or_404(User,login='guest')
			c=False
		#list_grp = me.group_users.all().values_list('id_group', flat=True)
		if id=='2':
			HTML = show_tools(me,user=user,c=c)
		elif id=='3':
			HTML = show_publis(me,user=user)
		elif id=='4':
			HTML = show_ens_media(me,user=user)
		else:
			return HttpResponse("")
		return HttpResponse(HTML)
	else:
		return HttpResponse("")
			

def gpe_selected(request,id_gpe):
	"""
	\brief Catch the ajax request send by the nav bar => fill the information and display them into the good div
	\author{B.Petitpas}
	"""
	id=-1
	HTML=""
	if request.is_ajax():
		if request.GET.has_key('id'):
			id=request.GET['id']
		else:
			return HttpResponse("")
	else:
		return HttpResponse("")
	if id!=-1:
		group = get_object_or_404(Group, id_group=id_gpe)
		if request.session.has_key('login'):
			me = get_object_or_404(User,login=request.session['login'])
			c=True
		else:
			me = get_object_or_404(User,login='guest')
			c=False
		if id=='2':
			HTML = show_tools(me,gpe=group,c=c)
		elif id=='3':
			HTML = show_publis(me,gpe=group)
		elif id=='4':
			HTML = show_ens_media(me,gpe=group)
		else:
			return HttpResponse("")
		return HttpResponse(HTML)
	else:
		return HttpResponse("")
			
