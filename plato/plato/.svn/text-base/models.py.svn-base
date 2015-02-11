# -*- coding: utf-8 -*-

# Here's the models for the new database !
# Very useful and very easy to use
# not like the former one, extracted from the Slim's one
import os
from django.db import models

########################## GENERAL PART ##############################

class KW(models.Model):
	id_kw = models.AutoField(primary_key=True)
	nm_kw = models.CharField(max_length=500)
	class Meta:
		db_table = u'kw'
	def __unicode__(self):
		return self.nm_kw

########################### USER PART ################################
class UserStatus(models.Model):
	id_user_status = models.AutoField(primary_key=True)
	nm_user_status = models.CharField(max_length=50)
	class Meta:
		db_table=u'user_status'
	def __unicode__(self):
		return self.nm_user_status
	
class User(models.Model):
	id_user = models.AutoField(primary_key=True)
	fstnm_person = models.CharField(max_length=100)
	nm_person = models.CharField(max_length=100)
	email_person = models.CharField(max_length=200,null=True,blank=True)
	webpage_person = models.CharField(max_length=200,null=True,blank=True)
	birthdate_person = models.DateField(null=True,blank=True)
	biographie = models.TextField(null=True,blank=True)
	biographie_fr = models.TextField(null=True,blank=True)
	status = models.ForeignKey(UserStatus, db_column='id_user_status')
	office = models.CharField(max_length=20,null=True,blank=True)
	account_expiration_date = models.DateField(null=True,blank=True)
	login = models.CharField(max_length=50)
	telephone = models.CharField(max_length=20,null=True,blank=True)
	id_boss = models.IntegerField(null=True,blank=True)
	actif=models.BooleanField(default=True)
	class Meta:
		db_table = u'user'
		ordering = ['nm_person']
	def __unicode__(self):
		return unicode(self.fstnm_person)+" "+unicode(self.nm_person)
	def get_last_page(self):
		a= self.author
		return a.page_set.filter(flag_suppr=False).order_by('-annee','-mon')[:5]
	def get_last_tool(self):
		return self.tool_set.filter(public=True).order_by('-date_creation')[:5]
	def get_last_media(self):
		return self.ensfile_set.filter(public=True).order_by('-creation_date')[:5]
	def get_publi(self):
		a= self.author
		return a.page_set.filter(flag_suppr=False).order_by('-annee','-mon')
		

class TypeGroup(models.Model):
	id_type_group = models.AutoField(primary_key=True)
	nm_type_group = models.CharField(max_length=50)
	class Meta:
		db_table = u'type_group'
	def __unicode__(self):
		return self.nm_type_group

class Group(models.Model):
	id_group = models.AutoField(primary_key=True)
	name_group = models.CharField(max_length=100)
	desc_group = models.TextField(null=True,blank=True)
	users = models.ManyToManyField(User,related_name='group_users', db_table='group_user')
	date_del = models.DateField(null=True,blank=True)
	date_creation = models.DateField()
	date_modification = models.DateField()
	email = models.CharField(max_length=100,null=True,blank=True)
	website = models.CharField(max_length=100,null=True,blank=True)
	manager = models.ForeignKey(User, related_name='group_manager',db_column='id_user')
	type_group = models.ForeignKey(TypeGroup, db_column='id_type_group')
	actif=models.BooleanField(default=True)
	KW = models.ManyToManyField(KW, db_table='group_kw',related_name='group_kw',null=True,blank=True)
	class Meta:
		db_table = u'group'
		ordering = ['-date_creation']
	def __unicode__(self):
		return unicode(self.name_group)

class Author(models.Model):
	id_author = models.AutoField(primary_key=True)
	fstnm = models.CharField(max_length = 200)
	nm = models.CharField(max_length = 200)
	fstnm_i =models.CharField(max_length = 10)
	id_user = models.OneToOneField(User,db_column='id_user',null=True,blank=True)
	class Meta:
		db_table= u'author'
		ordering=['pageauthor__order']
	def __unicode__(self):
		return unicode(self.fstnm)+" "+unicode(self.nm)	
	def get_short_name(self):
		return unicode(self.fstnm_i)+". "+unicode(self.nm)	

############################# MEDIA PART ###################################

## EnsFile is a set of file with meta information about them : could be a sound corpus, an album, a collection of images ...Very generic
class Copyright(models.Model):
	id_copyright = models.AutoField(primary_key=True)
	nm_copyright = models.CharField(max_length = 50)
	class Meta:
		db_table= u'copyright'
	def __unicode__(self):
		return self.nm_copyright

class TypeEnsFile(models.Model):
	id_type_ensfile = models.AutoField(primary_key=True)
	nm_type_ensfile = models.CharField(max_length = 50)
	class Meta:
		db_table= u'type_ens_file'
	def __unicode__(self):
		return self.nm_type_ensfile
	
class EnsFile(models.Model):
	id_ensfile = models.AutoField(primary_key=True)
	name_ensfile = models.CharField(max_length = 200)
	desc_ensfile = models.TextField(null=True,blank=True)
	type_ens_file = models.ForeignKey(TypeEnsFile, db_column='id_type_ens_file')
	copyright= models.ForeignKey(Copyright, db_column='id_copyright',null=True,blank=True)
	origin = models.CharField(max_length = 2000,null=True,blank=True)
	manager = models.ForeignKey(User, db_column='id_user')
	date_creation =  models.DateField()
	date_modification = models.DateField()
	date_del = models.DateField()
	KW = models.ManyToManyField(KW, db_table='ens_file_kw',related_name='ens_file_kw',null=True,blank=True)
	group = models.ForeignKey(Group, db_column='id_group',null=True,blank=True)
	all_f = models.BooleanField(default=True) # VISIBLE FOR all TSI => NOT USED ANY MORE
	actif=models.BooleanField(default=True) # actif : si date perimer => inactif => pas visible
	vc=models.IntegerField(null=True,blank=True,default=0) #nb of views => NOT USED ANYMORE
	public = models.BooleanField(default=False) # if true => copie it to the vitrine
	class Meta:
		db_table= u'ens_file'
		ordering=['-date_modification']
	def __unicode__(self):
		return self.name_ensfile

class TypeFile(models.Model):
	id_type_file = models.AutoField(primary_key=True)
	nm_type_file = models.CharField(max_length = 50)
	class Meta:
		db_table= u'type_file'

# File is the major table that will be used everywhere !
class File(models.Model):
	id_file = models.AutoField(primary_key=True)
	name_file = models.CharField(max_length = 200)
	desc_file = models.TextField(null=True,blank=True)
	size_file = models.CharField(max_length = 20,null=True,blank=True)
	path =  models.CharField(max_length = 500)
	type_file = models.ForeignKey(TypeFile,db_column='id_type_file')
	ensfile = models.ForeignKey(EnsFile, db_column='id_ensfile',null=True,blank=True)
	manager = models.ForeignKey(User, db_column='id_user')
	date_creation =  models.DateField()
	date_modification = models.DateField()
	date_del = models.DateField()
	KW = models.ManyToManyField(KW, db_table='file_kw',related_name='file_kw',null=True,blank=True)
	group = models.ForeignKey(Group, db_column='id_group',null=True,blank=True)
	acquisition_date = models.DateField(null=True,blank=True)
	artists = models.CharField(max_length = 2000,null=True,blank=True)
	actif=models.BooleanField(default=True)
	all_f = models.BooleanField(default=True)	#NOT USED 
	visible = models.BooleanField(default=False)
	class Meta:
		db_table= u'file'
		ordering=['-date_modification']
	def __unicode__(self):
		return self.name_file
	def delete(self, *args, **kwargs):
		if self.path:
			try:
				os.remove(str(self.path))
				if self.type_file.id_type_file==1:
					os.remove(str( os.path.splitext(self.path)[0] + ".THUMB" + os.path.splitext(self.path)[1]))
			except:
				pass
		super(File, self).delete(*args, **kwargs)
	@property
	def show_thumb(self):
		return str( os.path.splitext(self.path)[0] + ".THUMB" + os.path.splitext(self.path)[1])
	def get_tool_caption(self):
		tf=self.toolfigures_set.all()
		return tf[0].legende
	def get_publi_caption(self):
		tf=self.pagefigures_set.all()
		return tf[0].legende 
	def get_demo_caption(self):
		tf=self.demoexample_set.all()
		return tf[0].legende

####### Now some particulariy of every type of file #####
class TypeImage(models.Model):
	id_type_image = models.AutoField(primary_key=True)
	nm_type_image = models.CharField(max_length = 50)
	class Meta:
		db_table= u'type_image'
	def __unicode__(self):
		return self.nm_type_image

class Satellite(models.Model):
	id_satellite = models.AutoField(primary_key=True)
	nm_satellite = models.CharField(max_length = 50)
	class Meta:
		db_table= u'satellite'
	def __unicode__(self):
		return self.nm_satellite

class Image(models.Model):
	file=  models.OneToOneField(File, primary_key=True)
	type_image = models.ForeignKey(TypeImage,db_column='id_type_image')
	satellite = models.ForeignKey(Satellite,db_column='id_satellite',null=True,blank=True)
	class Meta:
		db_table= u'image'
	def __unicode__(self):
		return self.file.name_file

class TypeSound(models.Model):
	id_type_sound = models.AutoField(primary_key=True)
	nm_type_sound = models.CharField(max_length = 50)
	class Meta:
		db_table= u'type_sound'
		ordering=['id_type_sound']
	def __unicode__(self):
		return self.nm_type_sound

class Instrument(models.Model):
	id_instrument = models.AutoField(primary_key=True)
	nm_instrument = models.CharField(max_length=50)
	nm_register = models.CharField(max_length=50)
	class Meta:
		db_table = u'instrument'
		ordering = ['nm_instrument']
	def __unicode__(self):
		if self.nm_register!= "None":
			return self.nm_instrument+" "+self.nm_register
		else:
			return self.nm_instrument
	
class Note(models.Model):
    id_note = models.IntegerField(primary_key=True)
    nm_note = models.CharField(max_length=3)
    nm_note_latin = models.CharField(max_length=3)
    class Meta:
        db_table = u'note'
    def __unicode__(self):
		return self.nm_note_latin

class Sound(models.Model):
	file= models.OneToOneField(File, primary_key=True)
	type_sound = models.ForeignKey(TypeSound,db_column='id_type_sound')
	instrument = models.ManyToManyField(Instrument, db_table='sound_instrument',null=True,blank=True)
	note = models.ManyToManyField(Note, db_table='sound_note',null=True,blank=True)
	duration = models.TimeField()
	class Meta:
		db_table= u'sound'

class Video(models.Model):
	file= models.OneToOneField(File, primary_key=True)
	duration = models.TimeField()
	link = models.CharField(max_length=2000)
	class Meta:
		db_table= u'video'
	

	
############################# TOOL PART ###################################

class TypeTool(models.Model):
	id_type_tool = models.AutoField(primary_key=True)
	nm_type_tool = models.CharField(max_length=200)
	class Meta:
		db_table= u'type_tool'
	def __unicode__(self):
		return self.nm_type_tool
	
class License(models.Model):
    id_license = models.IntegerField(primary_key=True)
    nm_license = models.CharField(max_length=50)
    class Meta:
        db_table = u'license'
    def __unicode__(self):
		return self.nm_license
	
class Tool(models.Model):
	id_tool = models.AutoField(primary_key=True)
	name_tool = models.CharField(max_length = 2000)
	version_tool = models.CharField(max_length = 20,null=True,blank=True)
	desc_tool = models.TextField(null=True,blank=True)
	help_file = models.ForeignKey(File, db_column='help_file',related_name='help_file',null=True,blank=True)
	webpage_tool = models.CharField(max_length=600,null=True,blank=True)
	manager = models.ForeignKey(User, db_column='id_user')
	date_creation = models.DateField()
	date_modification = models.DateField()
	author = models.ManyToManyField(Author, through='ToolAuthor',null=True,blank=True)
	tool_figures = models.ManyToManyField(File, through='ToolFigures' ,null=True,blank=True)
	files = models.ManyToManyField(File, db_table='tool_files',  related_name='file_used_in_tool',null=True,blank=True)
	licence = models.ForeignKey(License, db_column='id_license',null=True,blank=True)
	type_tool = models.ForeignKey(TypeTool, db_column='id_type_tool',null=True,blank=True)
	group = models.ForeignKey(Group,db_column='id_group',null=True,blank=True)
	KW = models.ManyToManyField(KW, db_table='tool_kw',related_name='tool_kw',null=True,blank=True)
	all_f = models.BooleanField(default=True) # is it accessible for everyone (even logged ones) NOT USED
	visible = models.BooleanField(default=False) # is it visible on line ? 
	vc=models.IntegerField(null=True,blank=True,default=0) #view count	
	ensfile = models.ManyToManyField(EnsFile, db_table='tool_ensfile',related_name='tool_ensfile',null=True,blank=True)
	class Meta:
		db_table = u'tool'
	def __unicode__(self):
		return self.name_tool
	def get_tool_author(self):
		return self.author.order_by('toolauthor__order')

class ToolFigures(models.Model):
 	id = models.AutoField(primary_key=True)
	figure = models.ForeignKey(File)
	tool = models.ForeignKey(Tool)
	legende = models.TextField(null=True,blank=True)
	class Meta:
		db_table= u'tool_figures'

class ToolAuthor(models.Model):
   	id = models.AutoField(primary_key=True)
	author = models.ForeignKey(Author)
	tool = models.ForeignKey(Tool)
	order= models.PositiveIntegerField(default=0)
	class Meta:
		db_table= u'tool_by_author'
		ordering=['order']

########################## PUBLICATION PART #################################
		
class Conf(models.Model):
	id_conf = models.AutoField(primary_key=True)
	titre_conf = models.CharField(max_length = 2000)
	class Meta:
		db_table= u'conf'
	def __unicode__(self):
		return self.titre_conf

class TypePage(models.Model):
	id_type_page = models.AutoField(primary_key=True)
	nm_type_page = models.CharField(max_length = 200)
	class Meta:
		db_table= u'type_page'
	def __unicode__(self):
		return self.nm_type_page

class Page(models.Model):
	id_page = models.AutoField(primary_key=True)
	titre = models.CharField(max_length = 2000)
	id_conf = models.ForeignKey(Conf, db_column='id_conf',null=True,blank=True)
	conf_raw = models.CharField(max_length = 500,null=True,blank=True)
	annee = models.IntegerField(null=True,blank=True)
	mois = models.CharField(max_length = 20,null=True,blank=True)
	mon = models.IntegerField(null=True,blank=True)
	pages = models.CharField(max_length = 200,null=True,blank=True)
	lieu = models.CharField(max_length = 200,null=True,blank=True)
	volume = models.CharField(max_length = 200,null=True,blank=True)
	number = models.CharField(max_length = 200,null=True,blank=True)
	publisher = models.CharField(max_length = 200,null=True,blank=True)
	type_page =  models.ForeignKey(TypePage,db_column='id_type_page',blank=True, null=True)		
	tool = models.ManyToManyField(Tool,db_table='page_tool',null=True,blank=True)
	abstract = models.TextField(null=True,blank=True)
	figures = models.ManyToManyField(File, through='PageFigures' ,null=True,blank=True)
	author = models.ManyToManyField(Author, through='PageAuthor',blank=True, null=True)
	id_presentation = models.ForeignKey(File,related_name='+',blank=True, null=True)
	id_article = models.ForeignKey(File,related_name='+',blank=True, null=True)
	publication_date= models.DateField(null=True,blank=True)
	manager = models.ForeignKey(User, db_column='id_user')
	group = models.ForeignKey(Group,db_column='id_group',null=True,blank=True)
	KW = models.ManyToManyField(KW, db_table='page_kw',related_name='page_kw',null=True,blank=True)
	vc=models.IntegerField(null=True,blank=True,default=0)
	ensfile = models.ManyToManyField(EnsFile, db_table='page_ensfile',related_name='page_ensfile',null=True,blank=True)
	flag_plato = models.BooleanField(default='False')# to see if the publication is from plato or not 
	flag_suppr = models.BooleanField(default='Flase')# to see if the puyblication is still on the database
	class Meta:
		db_table= u'page'
		ordering=['-annee']
	def __unicode__(self):
		return self.titre
	def order_by_author(self):
		return self.author.all().order_by('page_author__order')
	def get_demos(self):
		return self.publi_demos.all()

class PageFigures(models.Model):
	id = models.AutoField(primary_key=True)
	figures = models.ForeignKey(File)
	page = models.ForeignKey(Page)
	legende = models.TextField(null=True,blank=True)
	class Meta:
		db_table= u'page_figures'
	
class PageAuthor(models.Model):
   	id = models.AutoField(primary_key=True)
	author = models.ForeignKey(Author)
	page = models.ForeignKey(Page)
	order= models.PositiveIntegerField(default=0)
	class Meta:
		db_table= u'page_by_author'
		ordering=['order']

class Frames(models.Model):
	id_frame = models.AutoField(primary_key=True)
	tool = models.ForeignKey(Tool, db_column='id_tool',null=True, blank=True)
	publi = models.ForeignKey(Page, db_column='id_page',null=True, blank=True)
	link = models.CharField(max_length=2000)
	class Meta:
		db_table= u'frames'
	def __unicode__(self):
		return self.link
		
#################### Management #########################



class Authorisation(models.Model):
	id_auth = models.AutoField(primary_key=True)
	file= models.ForeignKey(File, db_column='id_file',null=True,blank=True)
	tool = models.ForeignKey(Tool, db_column='id_tool',null=True,blank=True)
	ens_file = models.ForeignKey(EnsFile, db_column='id_ens_file',null=True,blank=True)
	page= models.ForeignKey(Page, db_column='id_page',null=True,blank=True)
	user = models.ForeignKey(User, db_column='id_user')
	#visible = models.BooleanField(default=False)
	class Meta:
		db_table = u'authorisation'


#################### DEMO ########################


class Demo(models.Model):
	id_demo = models.AutoField(primary_key=True)
	name_demo = models.CharField(max_length = 2000)
	manager =  models.ForeignKey(User, db_column='id_user')
	tool =  models.ForeignKey(Tool,db_column='id_tool',null=True,blank=True)
	publi = models.ManyToManyField(Page,through='DemoPubli',blank=True, null=True,related_name='publi_demos')
	examples = models.ManyToManyField(File,through='DemoExample',blank=True, null=True,related_name='file_demos')
	desc_demo = models.TextField(null=True,blank=True)
	cmd = models.CharField(max_length = 2000)# always like "PLop -i %s %s -o %s" with 3 %s for : in, parameters, out
	date_creation =  models.DateField()
	organisation =  models.CharField(max_length = 4)
	estimate_time = models.CharField(max_length = 20,null=True,blank=True)
	ensfile = models.ManyToManyField(EnsFile, db_table='demo_ensfile',related_name='demo_ensfile',null=True,blank=True)
	class Meta:
		db_table = u'demo'
	def __unicode__(self):
		return self.name_demo
	def get_input(self):
		return self.es_demo_set.filter(es=True).order_by('odr')
	def get_output(self):
		return self.es_demo_set.filter(es=False).order_by('odr')
	def get_param(self):
		return self.param_demo_set.all().order_by('odr')	

class DemoPubli(models.Model):
	id = models.AutoField(primary_key=True)
	demo = models.ForeignKey(Demo)
	page = models.ForeignKey(Page)
	class Meta:
		db_table= u'demo_publi'

class DemoExample(models.Model):
	id = models.AutoField(primary_key=True)
	demo = models.ForeignKey(Demo)
	fil = models.ForeignKey(File)
	legende = models.TextField(null=True,blank=True)	
	class Meta:
		db_table= u'demo_example'
		
		
class Type_ES(models.Model):
	id_type_es = models.AutoField(primary_key=True)
	name_type_es = models.CharField(max_length = 200)
	class Meta:
		db_table=u'type_es'
	def __unicode__(self):
		return self.name_type_es

class ES_demo(models.Model):
	id_es = models.AutoField(primary_key=True)
	name_es = models.CharField(max_length = 200)
	cmd_es=models.CharField(max_length = 200,null=True,blank=True)# in reallity it's the path of the file !!!
	type_es = models.ForeignKey(Type_ES, db_column='id_type_es')# image, value etc ... 
	demo = models.ForeignKey(Demo, db_column='id_demo')
	es = models.BooleanField(default='True')#true if it's an entry, false other wise
	odr = models.IntegerField(null=True,blank=True)
	prefixed_name = models.CharField(max_length = 200,null=True,blank=True)
	class Meta:
		db_table=u'es_demo'
		
class Param_demo(models.Model):
	id_param_demo = models.AutoField(primary_key=True)
	name_param = models.CharField(max_length = 200)
	cmd_param=models.CharField(max_length = 200,null=True,blank=True)
	initial_value = models.FloatField(null=True,blank=True)
	limite_inf = models.IntegerField(null=True,blank=True)
	limite_sup = models.IntegerField(null=True,blank=True)
	demo = models.ForeignKey(Demo, db_column='id_demo')
	odr = models.IntegerField(null=True,blank=True)
	class Meta:
		db_table=u'param_demo'


######################## statistiques #############################
