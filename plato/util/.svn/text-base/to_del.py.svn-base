# -*- coding: utf-8 -*-
# from django.db import connection, transaction #temporary import for managing slim stupidity
# from django.shortcuts import get_object_or_404
# from django.template import RequestContext

# from platon.models import OtherSound, Multimedia, Algorithm, Ensemble,Solo, Image, OneNote, IsolatedNotes,ToolInfoView,User, MmaSrc2, Source,Group, Author,Page,User,Tool,AlgoCorrespondAlgoF,AlgorithmFile,File #temporary import for managing slim stupidity
# def modif_other_sound():
# 	#Find the creator of the data and save it in the database (because the former way to find it was STUPID !)
# 	cursor = connection.cursor()
# 	aud = OtherSound.objects.all()
# 	for a in aud:		
# 		cursor.execute("""SELECT oid FROM other_sound WHERE id_other_sound=%s"""%a.id_other_sound)
# 		oid = cursor.fetchone()
# 		cursor.execute("""SELECT "user".id_person FROM "user", created_object WHERE oid_created_object=%s AND "user".id_user=created_object.id_user"""%oid)
# 		id_person = cursor.fetchone()
# 		cursor.execute("""UPDATE other_sound set id_person=%s WHERE id_other_sound='%s'""",[id_person,a.id_other_sound])
# 		transaction.commit_unless_managed()

# def modif_ensemble_music():
# 	#Find the creator of the data and save it in the database (because the former way to find it was STUPID !)
# 	cursor = connection.cursor()
# 	aud = Ensemble.objects.all()
# 	for a in aud:		
# 		cursor.execute("""SELECT oid FROM ensemble WHERE id_ensemble=%s"""%a.id_ensemble)
# 		oid = cursor.fetchone()
# 		cursor.execute("""SELECT "user".id_person FROM "user", created_object WHERE oid_created_object=%s AND "user".id_user=created_object.id_user"""%oid)
# 		id_person = cursor.fetchone()
# 		cursor.execute("""UPDATE ensemble set id_person=%s WHERE id_ensemble='%s'""",[id_person,a.id_ensemble])
# 		transaction.commit_unless_managed()

# def modif_solo():
# 	#Find the creator of the data and save it in the database (because the former way to find it was STUPID !)
# 	cursor = connection.cursor()
# 	aud = Solo.objects.all()
# 	for a in aud:		
# 		cursor.execute("""SELECT oid FROM solo WHERE id_solo=%s"""%a.id_solo)
# 		oid = cursor.fetchone()
# 		cursor.execute("""SELECT "user".id_person FROM "user", created_object WHERE oid_created_object=%s AND "user".id_user=created_object.id_user"""%oid)
# 		id_person = cursor.fetchone()
# 		cursor.execute("""UPDATE solo set id_person=%s WHERE id_solo='%s'""",[id_person,a.id_solo])
# 		transaction.commit_unless_managed()
		
# def modif_image():
# 	#Find the creator of the data and save it in the database (because the former way to find it was STUPID !)
# 	cursor = connection.cursor()
# 	aud = Image.objects.all()
# 	for a in aud:		
# 		cursor.execute("""SELECT oid FROM image WHERE id_mma=%s"""%a.id_mma)
# 		oid = cursor.fetchone()
# 		cursor.execute("""SELECT "user".id_person FROM "user", created_object WHERE oid_created_object=%s AND "user".id_user=created_object.id_user"""%oid)
# 		id_person = cursor.fetchone()
# 		cursor.execute("""UPDATE image set id_person=%s WHERE id_mma='%s'""",[id_person,a.id_mma])
# 		transaction.commit_unless_managed()

# def modif_audio():
# 	solo = Solo.objects.all()
# 	on = OneNote.objects.all()
# 	isn = IsolatedNotes.objects.all()
# 	cursor = connection.cursor()
# 	for s in solo:
# 		try:
# 			inst = s.id_instrument
# 			cursor.execute("""INSERT INTO inst_compose_ens (id_mma, id_instrument) VALUES ('%s', '%s')"""%(s.id_mma, inst.id_instrument))
# 			if s.id_mute:
# 				cursor.execute("""UPDATE inst_compose_ens SET id_mute='%s' WHERE id_mma='%s' AND id_instrument='%s'"""%(s.id_mute.id_mute, s.id_mma, s.id_instrument.id_instrument))
# 			if s.id_accent:
# 				cursor.execute("""UPDATE inst_compose_ens SET id_accent='%s' WHERE id_mma='%s' AND id_instrument='%s'"""%(s.id_accent.id_accent, s.id_mma, s.id_instrument.id_instrument))
# 			if s.id_vibrato:
# 				cursor.execute("""UPDATE inst_compose_ens SET id_vibrato='%s' WHERE id_mma='%s' AND id_instrument='%s'"""%(s.id_vibrato.id_vibrato, s.id_mma, s.id_instrument.id_instrument))
# 		except:
# 			pass
# 	for s in on:
# 		if s.id_instrument:
# 			cursor.execute("""INSERT INTO inst_compose_ens (id_mma, id_instrument) VALUES ('%s', '%s')"""%(s.id_mma, s.id_instrument))
# 			if s.id_mute:
# 				cursor.execute("""UPDATE inst_compose_ens SET id_mute='%s' WHERE id_mma='%s' AND id_instrument='%s'"""%(s.id_mute, s.id_mma, s.id_instrument))
# 			if s.id_accent:
# 				cursor.execute("""UPDATE inst_compose_ens SET id_accent='%s' WHERE id_mma='%s' AND id_instrument='%s'"""%(s.id_accent, s.id_mma, s.id_instrument))
# 			if s.id_vibrato:
# 				cursor.execute("""UPDATE inst_compose_ens SET id_vibrato='%s' WHERE id_mma='%s' AND id_instrument='%s'"""%(s.id_vibrato, s.id_mma, s.id_instrument))
# 		try:
# 			note = s.id_note
# 			cursor.execute("""INSERT INTO note_compose_audio (id_mma, id_note) VALUES ('%s','%s')"""%(s.id_mma, s.id_note.id_note))
# 			if s.one_note_octave:
# 				cursor.execute("""UPDATE note_compose_audio SET octave='%s' WHERE id_mma='%s' AND id_note='%s'"""%(s.one_note_octave, s.id_mma, note.id_note))
# 			if s.one_note_symbol:
# 				cursor.execute("""UPDATE note_compose_audio SET symbol='%s' WHERE id_mma='%s' AND id_note='%s'"""%(s.one_note_symbol, s.id_mma, note.id_note))
# 		except:
# 			pass
# 	for s in isn:
# 		if s.id_instrument:
# 			cursor.execute("""INSERT INTO inst_compose_ens (id_mma, id_instrument) VALUES ('%s', '%s')"""%(s.id_mma, s.id_instrument))
# 			if s.id_mute:
# 				cursor.execute("""UPDATE inst_compose_ens SET id_mute='%s' WHERE id_mma='%s' AND id_instrument='%s'"""%(s.id_mute, s.id_mma, s.id_instrument))
# 			if s.id_accent:
# 				cursor.execute("""UPDATE inst_compose_ens SET id_accent='%s' WHERE id_mma='%s' AND id_instrument='%s'"""%(s.id_accent, s.id_mma, s.id_instrument))
# 			if s.id_vibrato:
# 				cursor.execute("""UPDATE inst_compose_ens SET id_vibrato='%s' WHERE id_mma='%s' AND id_instrument='%s'"""%(s.id_vibrato, s.id_mma, s.id_instrument))
# 		i=-1
# 		f=-1
# 		try:
# 			i = s.id_fst_note.id_note
# 			if s.id_lst_note:
# 				f=s.id_lst_note
# 		except:
# 			pass
# 		if i !=-1 and f!=-1:
# 			i+=1
# 			while i <= f:
# 				cursor.execute("""INSERT INTO note_compose_audio (id_mma, id_note) VALUES (%s,%s)"""%(str(s.id_mma), str(i)))
# 				print "so :"+str(s.id_mma)+" correpond : "+str(i)
# 				i+=1
# 		try:
# 			if s.id_lst_note:
# 				cursor.execute("""INSERT INTO note_compose_audio (id_mma, id_note, octave, symbol) VALUES ('%s','%s','%s','%s')"""%(s.id_mma, s.id_lst_note, s.last_note_octave, s.last_note_symbol))
# 		except:
# 			pass
# 		try:
# 			fst_note = s.id_fst_note
# 			cursor.execute("""INSERT INTO note_compose_audio (id_mma, id_note, octave, symbol) VALUES ('%s','%s','%s','%s')"""%(s.id_mma, fst_note.id_note, s.fst_note_octave, s.fst_note_symbol))
# 		except:
# 			pass
				
# 	cursor.close()
# 	transaction.commit_unless_managed()

# def modif_tool():
# 	src=ToolInfoView.objects.all()
# 	cursor = connection.cursor()
# 	for s in src:		
# 		if s.login:
# 			u = get_object_or_404(User,login=s.login)
# 			cursor.execute("""UPDATE algorithm SET id_user='%s', date_creation='%s' WHERE id_algo='%s'"""%(u.id_user, s.date_created_object, s.id_algo))
# 			cursor.execute("""SELECT oid FROM algorithm WHERE id_algo=%s"""%s.id_algo)
# 			oid = cursor.fetchone()
# 			cursor.execute("""SELECT date_modified_object FROM modified_object WHERE oid_modified_object=%s"""%oid)
# 			modif = cursor.fetchone()
# 			if modif:
# 				cursor.execute("""UPDATE algorithm SET date_modification='%s' WHERE id_algo='%s'"""%(modif,s.id_algo))
# 			else:
# 				cursor.execute("""UPDATE algorithm SET date_modification='%s' WHERE id_algo='%s'"""%(s.date_created_object,s.id_algo))
# 		else:
# 			print("heuuu")
# 	cursor.close()
# 	transaction.commit_unless_managed()

# def modif_mma():
# 	mul = Multimedia.objects.all()
# 	cursor = connection.cursor()
# 	for m in mul:
# 		cursor.execute("""SELECT oid FROM multimedia WHERE id_mma=%s"""%m.id_mma)
# 		oid=cursor.fetchone()
		
# 		cursor.execute("""SELECT date_created_object FROM created_object WHERE oid_created_object=%s"""%oid)
# 		create = cursor.fetchone()
# 		if create:
# 			c = create[0].date()
# 			cursor.execute("""UPDATE multimedia SET creation_date='%s' WHERE id_mma='%s'"""%(c,m.id_mma))
			
# 		cursor.execute("""SELECT date_modified_object FROM modified_object WHERE oid_modified_object=%s"""%oid)
# 		modif = cursor.fetchone()
# 		if modif:
# 			modif = modif[0].date()
# 			cursor.execute("""UPDATE multimedia SET modify_date='%s' WHERE id_mma='%s'"""%(modif,m.id_mma))
# 		elif create:
# 			c = create[0].date()
# 			cursor.execute("""UPDATE multimedia SET modify_date='%s' WHERE id_mma='%s'"""%(c,m.id_mma))
# 	cursor.close()
# 	transaction.commit_unless_managed()

# def modif_group():
# 	grp = Group.objects.all()
# 	cursor = connection.cursor()
# 	for g in grp:
# 		cursor.execute("""SELECT oid FROM "group" WHERE id_group=%s"""%g.id_group)
# 		oid=cursor.fetchone()
		
# 		cursor.execute("""SELECT date_created_object FROM created_object WHERE oid_created_object=%s"""%oid)
# 		create = cursor.fetchone()
# 		if create:
# 			c = create[0].date()
# 			cursor.execute("""UPDATE "group" SET creation_date='%s' WHERE id_group='%s' """%(c,g.id_group))
		
# 		cursor.execute("""SELECT date_modified_object FROM modified_object WHERE oid_modified_object=%s"""%oid)
# 		modif = cursor.fetchone()
# 		if modif:
# 			m = modif[0].date()
# 			cursor.execute("""UPDATE "group" SET modification_date='%s' WHERE id_group='%s' """%(m,g.id_group))			
# 		elif create:
# 			c = create[0].date()
# 			cursor.execute("""UPDATE "group" SET modification_date='%s' WHERE id_group='%s' """%(c,g.id_group))
# 	cursor.close()
# 	transaction.commit_unless_managed()

# def modif_source():
# 	src = Source.objects.all()
# 	cursor = connection.cursor()
# 	for s in src:
# 		cursor.execute("""SELECT oid FROM source WHERE id_source='%s' """%s.id_source)
# 		oid=cursor.fetchone()
		
# 		cursor.execute("""SELECT date_modified_object FROM modified_object WHERE oid_modified_object=%s"""%oid)
# 		modif = cursor.fetchone()
# 		if modif:
# 			m = modif[0]
# 			cursor.execute("""UPDATE source SET modification_date_source='%s' WHERE id_source='%s' """%(m,s.id_source))
# 		elif s.creation_date_source:
# 			cursor.execute("""UPDATE source SET modification_date_source='%s' WHERE id_source='%s' """%(s.creation_date_source,s.id_source))
# 	cursor.close()
# 	transaction.commit_unless_managed()
		
# def fill_auth():
	
# 	cursor = connection.cursor()
# 	cursor.execute(""" DELETE FROM authorisation""")
	
# 	mul = Multimedia.objects.all()
# 	for m in mul:
# 		cursor.execute("""INSERT INTO authorisation (id_mma, id_auth_type, all_flag) VALUES ('%s','%s','%s')"""%(m.id_mma,"2","True"))
# 		try:
# 			cursor.execute("""INSERT INTO authorisation (id_mma, id_auth_type, id_person) VALUES ('%s','%s','%s')"""%(m.id_mma,"3",m.id_person.id_person))
# 		except:
# 			pass

	
# 	src = Source.objects.all()
# 	for s in src:
# 		cursor.execute("""INSERT INTO authorisation (id_source, id_auth_type, all_flag) VALUES ('%s','%s','%s')"""%(s.id_source,"2","True"))
# 		mmasrc = MmaSrc2.objects.filter(id_source= s.id_source)
# 		if mmasrc:
# 			id_perso = 0
# 			for m in mmasrc:
# 				if m.id_person != id_perso and m.id_person!= None:
# 					id_perso = m.id_person
# 					cursor.execute("""INSERT INTO authorisation (id_source, id_auth_type, id_person) VALUES ('%s','%s','%s')"""%(s.id_source,"3",id_perso))
		
		
# 	algo = Algorithm.objects.all()
# 	for a in algo:
# 		cursor.execute("""INSERT INTO authorisation (id_algo, id_auth_type, all_flag) VALUES ('%s','%s','%s')"""%(a.id_algo,"2","True"))
# 		if a.id_user:
# 			cursor.execute("""INSERT INTO authorisation (id_algo, id_auth_type, id_person) VALUES ('%s','%s','%s')"""%(a.id_algo,"3",a.id_user.id_person))
	
# 	cursor.close()
# 	transaction.commit_unless_managed()

# def fill_author():
# 	"""
# 	fill the new table author

# 	"""
# 	# ps = Page.objects.all()
# 	# for p in ps:
# 	# 	for pp in p.author.all():
# 	# 		a=Author(titre="Dr", fstnm=pp.fstnm_person, nm =pp.nm_person )
# 	# 		a.save()
# 	users = User.objects.all()
# 	for u in users:
# 		a = Author(fstnm = u.fstnm_person, fstnm_i=u.fstnm_person[0] , nm = u.nm_person, id_user = u)
# 		a.save()

# def fill_tool():
# 	"""
# 	Fill tool: the new way to manage the tool
# 	"""
# 	#RAJOUTER MODIF AUTHORISATION
	
# 	cursor = connection.cursor()
# 	algos = Algorithm.objects.all()
# 	for a in algos:
# 		t = Tool(nm_algo = a.nm_algo, v_algo = a.version_algo, s_desc_algo = a.description_algo, webpage_algo = a.webpage_algo, id_user=a.id_user, date_creation=a.date_creation, date_modification = a.date_modification)
# 		t.save()
# 		afs= AlgoCorrespondAlgoF.objects.filter(id_algo=a.id_algo)
# 		print afs
# 		for aff in afs:
# 			#af = get_object_or_404(AlgorithmFile,id_algorithm_file=aff.id_algorithm_file)
# 			#cursor.execute("""INSERT INTO file (id_file,id_folder,id_file_typ,nm_file,path_file,size_file,description_file,permanent_file, external_file) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"""%(af.id_file,af.id_folder,af.id_file_typ,af.nm_file, af.path_file,af.size_file,af.description_file,af.permanent_file,af.external_file))
# 			#cursor.execute("""INSERT INTO tool_files (tool_id, file_id) VALUES ('%s','%s')"""%(t.id_algo,af.id_file ))
# 			f = File.objects.filter(id_file = aff.id_file).distinct()
# 			print f
# 			t.files.add(f[0])
# 			t.save()
# #t.save()
#         for f in t.files.all():
# 			print f
# 	cursor.close()
# 	transaction.commit_unless_managed()

# ############################Some test###########################
			
# # from django.forms.widgets import TextInput,flatatt
# # from django.utils.html import escape
# # class AutoCompleteField(TextInput):
# # 	def __init__(self, url='', options='{paramName: "text"}', attrs=None):
# # 		self.url = url
# # 		self.options = options
# #                 if attrs is None:
# #                     attrs = {}
# #                 self.attrs = attrs
# # 	def value_from_datadict(self, data, files, name):
# # 		val = data.get(name, None)
# # 		if val=="-1":
# # 			val = None
# # 		return val
	
# # 	def render(self, name, value=None, attrs=None):
# # 		final_attrs = self.build_attrs(attrs, name=name)
# # 		if value:
# # 			final_attrs['value'] = escape(value)
# # 		if not self.attrs.has_key('id'):
# #                     final_attrs['id'] = 'id_%s' % name
# # 		return (u'<input type="text" name="%(name)s" id="%(id)s"/> <div class="autocomplete" id="box_%(name)s"></div>'
# #                         '<script type="text/javascript">'
# #                         'new Ajax.Autocompleter(\'%(id)s\', \'box_%(name)s\', \'%(url)s\', %(options)s);'
# #                         '</script>') % {'attrs'	: flatatt(final_attrs),
# #                                         'name'	: name,
# #                                         'id'	: final_attrs['id'],
# #                                         'url'	: self.url,
# # 										'value': value, 
# #                                         'options' : self.options}





# 	#author = forms.CharField(label ="* Authors and Co-author", max_length=200 ,widget=AutoCompleteField(url='/add_page/autoAuthor/'))
# 	#author = forms.CharField(label ="* Authors and Co-author", max_length=200 ,widget=forms.TextInput(attrs={'autocomplete':"off","onkeyup":"autoAuthor('id_form_page-author', 'choices', this.value);",'size':'35'}))
	



# # from autocomplete.views import autocomplete, AutocompleteSettings
# # class AuthorAutoComplete(AutocompleteSettings):
# # 	search_fields = ('^nm')

# # autocomplete.register(Page.author,AuthorAutoComplete)

# # from autocomplete.widgets import *


# #author = forms.MultipleChoiceField(widget=MultipleAutocompleteWidget(Page.author))

# #######################################################################################
# from django.db import connections
# import datetime
# def dictfetchall(cursor):
#     "Returns all rows from a cursor as a dict"
#     desc = cursor.description
#     return [
#         dict(zip([col[0] for col in desc], row))
#         for row in cursor.fetchall()
#     ]
# def plato_dev2plato_test():
# 	cursor_dev = connections['plato_dev'].cursor()
# 	cursor_test = connections['plato_test'].cursor()
# 	#### USER ####	
# 	# cursor_dev.execute("""SELECT * FROM "user" ORDER BY id_user""")
# 	# users_dev = dictfetchall(cursor_dev)
# 	# for u in users_dev:
# 	# 	if u['webpage_person']==None:
# 	# 		u['webpage_person'] = "http://perso.telecom-paristech.fr/~%s/"%(u['login'])
# 	# 	if u['email_person'] == None:
# 	# 		u['email_person'] = "%s.%s@telecom-paristech.fr"%(u['nm_person'],u['fstnm_person'])
# 	# 	cursor_test.execute("""INSERT INTO "user" (fstnm_person, nm_person, email_person, webpage_person,id_user_status,account_expiration_date,"login") VALUES ('%s','%s','%s','%s','%s','%s','%s') """%(u['fstnm_person'],u['nm_person'],u['email_person'],u['webpage_person'],u['id_user_status'],u['account_expiration_date'],u['login']))
# 	# cursor_test.close()
# 	# transaction.commit_unless_managed(using='plato_test')
# 	##### END USER #####

# 	##### AUTHOR #####
# 	# cursor_test.execute("""SELECT * FROM "user" ORDER BY id_user""")
# 	# users = dictfetchall(cursor_test)
# 	# for u in users:
# 	# 	cursor_test.execute("""INSERT INTO author (fstnm,fstnm_i,nm,id_user) VALUES ('%s','%s','%s','%s')"""%(u['fstnm_person'],u['fstnm_person'][0],u['nm_person'],u['id_user']))
# 	# cursor_test.close()
# 	# transaction.commit_unless_managed(using='plato_test')
# 	##### END AUTHOR #####
		
# 	##### GROUP #####
# 	## first : take care of the Group only
# 	## In a second time : take care of person inside each group !
# 	# cursor_dev.execute("""SELECT * FROM group_users ORDER BY id_group""")
# 	# group_dev = dictfetchall(cursor_dev)
#     #for g in group_dev:
# 	# 	if g['e_mail_group']==None:
# 	# 		g['e_mail_group']=''
# 	# 	if g['website_group']==None:
# 	# 		g['website_group']=''
# 	# 	if g['expiration_date_group']==None:
# 	# 		g['expiration_date_group']=datetime.date(9999,12,12)
# 	# 	if g['description_group']==None:
# 	# 		g['description_group']=''
						
# 	# 	cursor_dev.execute("""SELECT oid FROM "group" WHERE id_group=%s"""%g['id_group'])
# 	# 	oid=cursor_dev.fetchone()
# 	# 	c=datetime.date(2008,1,10)
# 	# 	cursor_dev.execute("""SELECT date_created_object FROM created_object WHERE oid_created_object=%s"""%oid)
# 	# 	create = cursor_dev.fetchone()
# 	# 	if create:
# 	# 		c = create[0].date()
# 	# 	m=datetime.date(2008,1,10)
# 	# 	cursor_dev.execute("""SELECT date_modified_object FROM modified_object WHERE oid_modified_object=%s"""%oid)
# 	# 	modif = cursor_dev.fetchone()
# 	# 	if modif:
# 	# 		m = modif[0].date()
# 	# 	elif create:
# 	# 		m = create[0].date()

# 	# 	cursor_dev.execute("""SELECT "login" FROM "user" WHERE id_person=%s"""%g['id_person'])
# 	# 	mana = cursor_dev.fetchone()[0]
# 	# 	cursor_test.execute("""SELECT id_user FROM "user" WHERE "login"='%s'"""%mana)
# 	# 	id_mana = cursor_test.fetchone()[0]

# 	# 	cursor_test.execute("""INSERT INTO "group" (name_group, desc_group, date_del, date_creation, date_modification, email, website,id_user, id_type_group) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s') """%(g['nm_group'], g['description_group'].replace("'", r"\'").replace("%", r"%%"),g['expiration_date_group'],c,m,g['e_mail_group'], g['website_group'],id_mana,'1'))
# 	# for g in group_dev:
# 	# 	cursor_test.execute("""SELECT id_group FROM "group" WHERE "name_group"='%s'"""%g['nm_group'])
# 	# 	id_ng = cursor_test.fetchone()[0]
# 	# 	cursor_dev.execute("""SELECT * FROM pers_belong_grp WHERE id_group='%s' """%g['id_group'])
# 	# 	users_group_dev = dictfetchall(cursor_dev)
# 	# 	for ug in users_group_dev:
# 	# 		cursor_dev.execute("""SELECT "login" FROM "user" WHERE id_person='%s' """%ug['id_person'])
# 	# 		log = cursor_dev.fetchone()[0]
# 	# 		cursor_test.execute("""SELECT id_user FROM "user" WHERE "login"='%s' """%log)
# 	# 		id_nu = cursor_test.fetchone()
# 	# 		if id_nu:
# 	# 			id_nu=id_nu[0]
# 	# 			cursor_test.execute("""SELECT * FROM group_user WHERE group_id='%s' AND user_id='%s' """%(id_ng,id_nu))
# 	# 			test = cursor_test.fetchone()
# 	# 			if not test:
# 	# 				cursor_test.execute("""INSERT INTO group_user (group_id,user_id) VALUES ('%s','%s')"""%(id_ng,id_nu))
# 	# cursor_test.close()
# 	# transaction.commit_unless_managed(using='plato_test')
# 	##### END GROUP #####

# 	##### ENSFILE #####
# 	# cursor_dev.execute("""SELECT source.*, src_belong_typ.id_typ_src FROM source LEFT JOIN src_belong_typ ON source.id_source=src_belong_typ.id_source""")
# 	# src = dictfetchall(cursor_dev)
# 	# for s in src:
# 	# 	if s['origin_source']==None:
# 	# 		s['origin_source']="NULL"
# 	# 	cursor_dev.execute("""SELECT oid FROM source WHERE id_source='%s' """%s['id_source'])
# 	# 	oid=cursor_dev.fetchone()
# 	# 	if s['creation_date_source']==None:
# 	# 		cursor_dev.execute("""SELECT date_created_object FROM created_object WHERE oid_created_object=%s"""%oid)
# 	# 		crea = cursor_dev.fetchone()
# 	# 		if crea:
# 	# 			s['creation_date_source']=crea[0]
# 	# 		else:
# 	# 			s['creation_date_source']=datetime.date(2008,1,10)
# 	# 	cursor_dev.execute("""SELECT date_modified_object FROM modified_object WHERE oid_modified_object=%s"""%oid)
# 	# 	modif = cursor_dev.fetchone()
# 	# 	if modif:
# 	# 		m = modif[0]
# 	# 	else:
# 	# 		m= s['creation_date_source']

# 	# 	typ=7
# 	# 	son=(1,6,7,8,10)
# 	# 	img=(2,5,12)
# 	# 	vid=(4,9,11)
# 	# 	if s['id_typ_src'] in son:
# 	# 		typ=1
# 	# 	if s['id_typ_src'] in img:
# 	# 		typ=2
# 	# 	if s['id_typ_src'] in vid:
# 	# 		typ=5
# 	# 	if s['id_typ_src']==3:
# 	# 		typ=4
# 	# 	if s['id_typ_src']==13:
# 	# 		typ=3
					
# 	# 	date_del=datetime.date(9999,12,12)
# 	# 	cursor_test.execute("""INSERT INTO ens_file (name_ensfile, origin, id_user, date_creation, date_modification,date_del, all_f, type_ens_file) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s') """%(s['nm_source'],s['origin_source'],912, s['creation_date_source'], m, date_del,'TRUE',typ))
		
# 	# transaction.commit_unless_managed(using='plato_test')

# 	##### END ENSFILE #####
# 	##### INSTRUMENTS #####
	
# 	# cursor_dev.execute("""SELECT * FROM instrument LEFT JOIN register on register.id_register = instrument.id_register""")
# 	# inst = dictfetchall(cursor_dev)
# 	# for i in inst:
# 	# 	cursor_test.execute("""INSERT INTO instrument (nm_instrument, nm_register) VALUES ('%s','%s')"""%(i['nm_instrument'],i['nm_register']))
# 	# transaction.commit_unless_managed(using='plato_test')	
	
# 	##### END INSTRUMENTS #####

# 	##### FILE #####
# 	## Enfin LE morceau qui va etre bien dure.
# 	## on va spliter le probleme en plusieurs morceaux : sound, image, videos. 

# 	##### SOUND ######
# 	## Choosing the good query is the key and tricky part of this
# 	##### SOLO ######
# 	#cursor_dev.execute("""SELECT * FROM solo/ensemble/isolated_notes/one_note
# 	# ##### IMAGE ######
# 	#cursor_dev.execute("""SELECT * FROM image
# 	# ##### VIDEO ######
# 	# cursor_dev.execute("""SELECT * FROM animated_image
# 	# cursor_dev.execute("""SELECT * FROM image
# 	# LEFT JOIN mma_belong_source ON mma_belong_source.id_mma = image.id_mma
# 	# LEFT JOIN source ON source.id_source = mma_belong_source.id_source
# 	# LEFT JOIN mma_correspond_file ON mma_correspond_file.id_mma = image.id_mma
# 	# LEFT JOIN file ON file.id_file = mma_correspond_file.id_file
# 	# LEFT JOIN file_folder ON file_folder.id_folder = file.id_folder
# 	# LEFT JOIN fileserver ON fileserver.id_fileserver = file_folder.id_fileserver;""")
# 	# #LEFT JOIN instrument ON isolated_notes.id_instrument=instrument.id_instrument
# 	# #LEFT JOIN register on register.id_register = instrument.id_register;""")
# 	# audio = dictfetchall(cursor_dev)
# 	# for a in audio :
# 	# 	#petit test de duplication
# 	# 	# cursor_dev.execute("""SELECT acquisition_date FROM satellite_image WHERE id_mma = '%s'"""%a['id_mma'])
# 	# 	# test = cursor_dev.fetchone()
# 	# 	# if test:
# 	# 	# 	print "piloupe"
# 	# 	# 	acq_date=test[0]
# 	# 	# else:
# 	# 	# 	acq_date=None
# 	# 	if a['id_typ_image']==1:
# 	# 		# reste test pour vier icon et preview !
# 	# 		ext = a['nm_file']
# 	# 		#path = a['nm_fileserver']+"/"+a['path_folder']+"/"+a['path_file']+"/"+a['nm_file']
# 	# 		print a['nm_mma']+" "+str(a['size_file'])
# 	# 		cursor_test.execute("""SELECT id_file FROM file WHERE  name_file='%s' AND size_file='%s'"""%(a['nm_mma'],a['size_file']))
# 	# 		id_file = cursor_test.fetchone()

# 	# 		if id_file:
# 	# 			id_file=id_file[0]
			
# 	# 			ext = ext[-3:]
# 	# 			if ext != "JPG":
# 	# 				cursor_test.execute("""SELECT id_satellite FROM satellite WHERE nm_satellite='%s' """%a['nm_source'])
# 	# 				id_satellite= cursor_test.fetchone()[0]
# 	# 				cursor_test.execute("""UPDATE  image SET id_type_image='%s', id_satellite='%s' WHERE file_id = '%s' """%('3',id_satellite,id_file))
# 	# 			else:
# 	# 				print id_file
# 	# 				cursor_test.execute("""DELETE FROM image WHERE file_id = '%s' """%id_file)
# 	# transaction.commit_unless_managed(using='plato_test')
		
# 	# 	#fill all the field before adding them !
# 	# 	#solo, etc ... MARCHE POUR TOUT
# 	# 	if a['id_file_typ']==6:
# 	# 		a['id_file_typ']=5
# 	# 	if a['id_file_typ']==4:
# 	# 		a['id_file_typ']=6
# 	# 	if a['id_file_typ']==8:
# 	# 		a['id_file_typ']=4
# 	# 	#source => ensfile
# 	# 	if a['nm_source']!=None and a['id_mma']!=None:
# 	# 		cursor_test.execute("""SELECT id_ensfile FROM ens_file WHERE name_ensfile = '%s'"""%(a['nm_source']))
# 	# 		id_ensfile = cursor_test.fetchone()[0]
#     #         #id_user ?
# 	# 		print a['id_mma']
# 	# 		cursor_dev.execute("""SELECT oid FROM animated_image WHERE id_mma=%s"""%a['id_mma'])
# 	# 		oid = cursor_dev.fetchone()
# 	# 		cursor_dev.execute("""SELECT "user"."login" FROM "user", created_object WHERE oid_created_object=%s AND "user".id_user=created_object.id_user"""%oid)
# 	# 		log = cursor_dev.fetchone()
# 	# 		cursor_test.execute("""SELECT id_user FROM "user" WHERE "login" = '%s'"""%(log))
# 	# 		id_user = cursor_test.fetchone()[0]
#     #         #date_crea and date_modif
# 	# 		cursor_dev.execute("""SELECT oid FROM multimedia WHERE id_mma=%s"""%a['id_mma'])
# 	# 		oid=cursor_dev.fetchone()
# 	# 		c=m=datetime.date(2008,1,10)
# 	# 		cursor_dev.execute("""SELECT date_created_object FROM created_object WHERE oid_created_object=%s"""%oid)
# 	# 		create = cursor_dev.fetchone()
# 	# 		if create:
# 	# 			c = create[0].date()			
# 	# 		cursor_dev.execute("""SELECT date_modified_object FROM modified_object WHERE oid_modified_object=%s"""%oid)
# 	# 		modif = cursor_dev.fetchone()
# 	# 		if modif:
# 	# 			m = modif[0].date()
# 	# 		elif create:
# 	# 			m = create[0].date()
# 	# 		#path
# 	# 		path = a['nm_fileserver']+"/"+a['path_folder']+"/"+a['path_file']+"/"+a['nm_file']
# 	# 		date_del =datetime.date(9999,12,12)
# 	# 		if a['date_delete_possible_mma']:
# 	# 			date_del = a['date_delete_possible_mma']
# 	# 		name = a['nm_mma'].replace("'","''")
#     #         #mane = name.replace("\\'","\'")
# 	# 		if a['description_mma']:
# 	# 			desc = a['description_mma'].replace("'","''")
# 	# 		else:
# 	# 			desc = a['description_mma']
# 	# 		path = path.replace("'","''")
# 	# 		# if acq_date:
# 	# 		# 	cursor_test.execute("""INSERT INTO file (name_file, desc_file, size_file, path, id_type_file, id_ensfile, id_user,date_creation,date_modification, date_del, all_f, acquisition_date) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"""%(name,desc,a['size_file'],path,a['id_file_typ'],id_ensfile,id_user,c,m,date_del,'TRUE',acq_date))
# 	# 		# else:
# 	# 		cursor_test.execute("""INSERT INTO file (name_file, desc_file, size_file, path, id_type_file, id_ensfile, id_user,date_creation,date_modification, date_del, all_f) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"""%(name,desc,a['size_file'],path,a['id_file_typ'],id_ensfile,id_user,c,m,date_del,'TRUE'))
# 	# 		id_file = cursor_test.lastrowid
# 	# 		# print id_file
#             ##### => Now specialize the file ... #####
# 			# ###### VIDEOS #######
# 			# if not a['duration']:
# 			# 	a['duration']='00:00:00'

# 			# cursor_test.execute("""INSERT INTO video (file_id, duration) VALUES ('%s','%s')"""%(id_file,a['duration']))

# 			# ###### IMAGES #######
# 			#fill the image table 
# 			# if a['id_typ_image']==1:
# 			# 	a['id_typ_image']=3
# 			# if a['id_typ_image']==3:
# 			# 	a['id_typ_image']=1
				
# 			#cursor_test.execute("""INSERT INTO image (file_id, id_type_image) VALUES ('%s','%s')"""%(id_file,a['id_typ_image']))
# 			# print id_file
# 			# #now fill the sound table
# 			# if a['id_type_audio']==1:
# 			# 	id_type_sound = 3
# 			# if a['id_type_audio']==2:
# 			# 	id_type_sound = 1
# 			# if a['id_type_audio']==3:
# 			# 	id_type_sound = 4
# 			# if a['id_type_audio']==4:
# 			# 	id_type_sound = 2

# 			# if a['duration_audio']==None:
# 			# 	a['duration_audio']='00:00:00'
# 			# cursor_test.execute("""INSERT INTO sound (file_id, id_type_sound, duration) VALUES ('%s','%s','%s')"""%(id_file, id_type_sound, a['duration_audio']))
			

# 			# now : sound_instrument et/ou sound_note
# 			# ### SOLO / ISOLATED NOTES / ONE NOTE #####
# 			# #solo = instrument easy ...
# 			# if a['nm_instrument'] != None and  a['nm_instrument'] != 'None':
# 			# 	cursor_test.execute("""SELECT id_instrument FROM instrument WHERE nm_instrument='%s' AND nm_register='%s' """%(a['nm_instrument'],a['nm_register']))
# 			# 	id_instrument = cursor_test.fetchone()[0]
# 			# 	cursor_test.execute("""INSERT INTO sound_instrument (sound_id, instrument_id) VALUES ('%s','%s')"""%(id_file, id_instrument))
# 			# ### ENSEMBLE #####
# 			# import re
# 			# if a['ensemble_code']!=None and  a['ensemble_code']!='None':
# 			# 	all_code = re.findall('..',a['ensemble_code'])
# 			# 	for c in all_code:
# 			# 		cursor_dev.execute("""SELECT id_instrument FROM instrument WHERE code_instrument = '%s' """%c)
# 			# 		id_instrument = cursor_dev.fetchone()
# 			# 		if id_instrument:
# 			# 			id_instrument = id_instrument[0]-61
# 			# 			cursor_test.execute("""INSERT INTO sound_instrument (sound_id, instrument_id) VALUES ('%s','%s')"""%(id_file, id_instrument))

# 		#### ISOLATED NOTES #####
# 		# fst = a['id_fst_note']
# 		# lst = a['id_lst_note']
# 		# if fst!='None' and fst!=None :
# 		# 	lst = 7
# 		# elif lst!='None' and lst!=None :
# 		# 	fst=1
# 		# if fst!='None' and fst!=None and lst!='None' and lst!=None:
# 		# 	while fst <= lst:
# 		# 		cursor_test.execute("""INSERT INTO sound_note (sound_id, note_id) VALUES (%s,%s)"""%(id_file,fst))
# 		# 		fst+=1
# 		#### ONE NOTE #####
# 		# if a['nm_note'] != None and  a['nm_note'] != 'None':
# 		# 	cursor_test.execute("""INSERT INTO sound_note (sound_id, note_id) VALUES ('%s','%s')"""%(id_file, a['id_note']))

		
# 	#transaction.commit_unless_managed(using='plato_test')	
# 	##### END FILE #####

# 	# ##### TOOL ######
# 	#### ALGORITHM #####

# 	# cursor_dev.execute("""SELECT * FROM toolbox;""")
# 	# algos = dictfetchall(cursor_dev)
# 	# for a in algos:

# 	# 	cursor_dev.execute("""SELECT oid FROM toolbox WHERE id_toolbox='%s' """%a['id_toolbox'])
# 	# 	oid = cursor_dev.fetchone()[0]
			
# 	# 	cursor_dev.execute("""SELECT "user"."login" FROM "user", created_object WHERE oid_created_object=%s AND "user".id_user=created_object.id_user"""%oid)
# 	# 	log = cursor_dev.fetchone()[0]
# 	# 	cursor_test.execute("""SELECT id_user FROM "user" WHERE "login" = '%s'"""%(log))
# 	# 	id_user = cursor_test.fetchone()[0]
		
# 	# 	c=m=datetime.date(2008,1,10)
# 	# 	cursor_dev.execute("""SELECT date_created_object FROM created_object WHERE oid_created_object=%s"""%oid)
# 	# 	create = cursor_dev.fetchone()
# 	# 	if create:
# 	# 		c = create[0].date()			
# 	# 	cursor_dev.execute("""SELECT date_modified_object FROM modified_object WHERE oid_modified_object=%s"""%oid)
# 	# 	modif = cursor_dev.fetchone()
# 	# 	if modif:
# 	# 		m = modif[0].date()
# 	# 	elif create:
# 	# 		m = create[0].date()
# 	# 	name = a['nm_toolbox'].replace("'","''").replace("\r","   ").replace("\n","<br>").replace("%","").replace("(",",").replace(")",",")
# 	# 	if a['description_toolbox']:
# 	# 		desc = a['description_toolbox'].replace("'","''").replace("\r","   ").replace("\n","<br>").replace("%","").replace("(",",").replace(")",",")
# 	# 	else:
# 	# 		desc = a['description_toolbox']
			
# 	# 	cursor_test.execute("""INSERT INTO tool (name_tool,version_tool,s_desc_tool,webpage_tool,id_user,date_creation,date_modification,all_f) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"""%(name,a['version_toolbox'],desc,a['webpage_toolbox'],id_user,c,m,'TRUE'))
# 	# 	cursor_test.execute("""SELECT id_tool FROM tool WHERE name_tool='%s' AND s_desc_tool='%s' """%(name,desc))
# 	# 	id_tool = cursor_test.fetchone()[0]
# 	# 	print "tool id = "+str(id_tool)
		
# 	# 	cursor_dev.execute("""SELECT * FROM algo_f_belong_toolbox
# 	# 	JOIN algorithm_file ON algorithm_file.id_file = algo_f_belong_toolbox.id_file
# 	# 	LEFT JOIN file_folder ON file_folder.id_folder = algorithm_file.id_folder
# 	# 	LEFT JOIN fileserver ON fileserver.id_fileserver = file_folder.id_fileserver
# 	# 	WHERE algo_f_belong_toolbox.id_toolbox = '%s';"""%a['id_toolbox'])
# 	# 	afs = dictfetchall(cursor_dev)#cursor_dev.fetchall()
# 	# 	# afs= AlgoCorrespondAlgoF.objects.filter(id_algo=a.id_algo)
		
# 	# 	for af in afs:
# 	# 		# ### FILE ####
# 	# 		path = af['nm_fileserver']+"/"+af['path_folder']+"/"+af['path_file']+"/"+af['nm_file']
# 	# 		path = path.replace("'","''")
# 	# 		date_del =datetime.date(9999,12,12)
# 	# 		if af['date_delete_possible_file']:
# 	# 			date_del = af['date_delete_possible_file']
# 	# 		name = af['nm_file'].replace("'","''").replace("\r","   ").replace("\n","<br>").replace("%","").replace("(",",").replace(")",",")
# 	# 		if af['description_file']:
# 	# 			desc = af['description_file'].replace("'","''").replace("\r","   ").replace("\n","<br>").replace("%","").replace("(",",").replace(")",",")
# 	# 		else:
# 	# 			desc = af['description_file']
				
# 	# 		if af['id_file_typ']==6:
# 	# 			af['id_file_typ']=5
# 	# 		if af['id_file_typ']==4:
# 	# 			af['id_file_typ']=6
# 	# 		if af['id_file_typ']==8:
# 	# 			af['id_file_typ']=4
				
# 	# 		cursor_test.execute("""SELECT id_file FROM file WHERE name_file='%s' AND path='%s'"""%(name,path))
# 	# 		test = cursor_test.fetchone()
# 	# 		if test:
# 	# 			id_file = test[0]
# 	# 		else:			
# 	# 			cursor_test.execute("""INSERT INTO file (name_file, desc_file, size_file, path, id_type_file,id_user,date_creation,date_modification, date_del, all_f) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') """%(name,desc,af['size_file'],path,af['id_file_typ'],id_user,c,m,date_del,'TRUE'))
# 	# 			#print name+ " "+path
# 	# 			cursor_test.execute("""SELECT id_file FROM file WHERE name_file='%s' AND path='%s'"""%(name,path))
# 	# 			id_file = cursor_test.fetchone()[0]
	
# 	# 		# ### TOOL FILE ###
# 	# 		print "id_tool = "+str(id_tool)+" et id_file = "+str(id_file)
# 	# 		cursor_test.execute("""SELECT tool_id FROM tool_files WHERE tool_id='%s' AND file_id='%s' """%(id_tool,id_file))
# 	# 		if not cursor_test.fetchone():
# 	# 			cursor_test.execute("""INSERT INTO tool_files (tool_id,file_id) VALUES ('%s','%s') """%(id_tool,id_file))
# 	# 		else:
# 	# 			print "plop"
# 	# 		#af = get_object_or_404(AlgorithmFile,id_algorithm_file=aff.id_algorithm_file)
# 	# 		#cursor.execute("""INSERT INTO file (id_file,id_folder,id_file_typ,nm_file,path_file,size_file,description_file,permanent_file, external_file) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"""%(af.id_file,af.id_folder,af.id_file_typ,af.nm_file, af.path_file,af.size_file,af.description_file,af.permanent_file,af.external_file))
# 	# 		#cursor.execute("""INSERT INTO tool_files (tool_id, file_id) VALUES ('%s','%s')"""%(t.id_algo,af.id_file ))
# 	# 		# f = File.objects.filter(id_file = aff.id_file).distinct()
# 	# 		# t.files.add(f[0])
# 	# 		# t.save()
			

#     #     # for f in t.files.all():
# 	# 	# 	print f
			
# 	# transaction.commit_unless_managed(using='plato_test')

# 	##### END TOOL #####


# 	# ##### Redo some of my shit ! ########
# 	# cursor_test.execute("""SELECT file_id FROM image """)
# 	# ids= dictfetchall(cursor_test)
	
# 	# for id_ in ids:
# 	# 	cursor_test.execute("""SELECT oid FROM image WHERE file_id='%s'"""%id_['file_id'])
# 	# 	oid = cursor_test.fetchone()[0]
# 	# 	cursor_test.execute("""SELECT id_file FROM file WHERE oid='%s' """%id_['file_id'])
# 	# 	id_file = cursor_test.fetchone()[0]
# 	# 	cursor_test.execute("""UPDATE image SET file_id='%s' WHERE oid='%s'  """%(id_file,oid))
			
# 	# transaction.commit_unless_managed(using='plato_test')
	
# 	# cursor_test.execute("""SELECT file_id FROM sound """)
# 	# ids= dictfetchall(cursor_test)
# 	# for id_ in ids:
# 	# 	cursor_test.execute("""SELECT oid FROM sound WHERE file_id='%s' """%id_['file_id'])
# 	# 	oidd = cursor_test.fetchone()[0]
# 	# 	cursor_test.execute("""SELECT id_file FROM file WHERE oid='%s' """%id_['file_id'])
# 	# 	test = cursor_test.fetchone()
# 	# 	if test:
# 	# 		id_file =test[0]
# 	# 		print str(oidd)+" = "+str(id_file)
			
# 	# 		cursor_test.execute("""SELECT oid FROM sound_instrument WHERE sound_id='%s' """%id_['file_id'])
# 	# 		if cursor_test.fetchone():
# 	# 			print "plop"
# 	# 			cursor_test.execute("""UPDATE sound_instrument SET sound_id='%s' WHERE sound_id ='%s' """%(id_file,id_['file_id']))

# 	# 		cursor_test.execute("""SELECT oid FROM sound_note WHERE sound_id='%s' """%id_['file_id'])
# 	# 		if cursor_test.fetchone():
# 	# 			print "plip"
# 	# 			cursor_test.execute("""UPDATE sound_note SET sound_id='%s' WHERE sound_id='%s' """%(id_file,id_['file_id']))
			
# 	# 		cursor_test.execute("""UPDATE sound SET file_id='%s' WHERE oid='%s' """%(id_file,oidd))

# 	# transaction.commit_unless_managed(using='plato_test')
# 	# cursor_test.execute("""SELECT file_id FROM video """)
# 	# ids= dictfetchall(cursor_test)
	
# 	# for id_ in ids:
# 	# 	cursor_test.execute("""SELECT oid FROM video WHERE file_id='%s'"""%id_['file_id'])
# 	# 	oid = cursor_test.fetchone()[0]
# 	# 	cursor_test.execute("""SELECT id_file FROM file WHERE oid='%s' """%id_['file_id'])
# 	# 	id_file = cursor_test.fetchone()[0]
# 	# 	cursor_test.execute("""UPDATE video SET file_id='%s' WHERE oid='%s'  """%(id_file,oid))
			
# 	# transaction.commit_unless_managed(using='plato_test')
	
