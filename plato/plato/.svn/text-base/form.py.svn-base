# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.db.models import Q, Max
from plato.models import *
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

######SOME UTILITIES FONCTIONS THAT CAN BE USED IN ALL THE FORMS ######

class filesize(str):
	"""
	Class that enable to transform '2.5MB' in bits size :
		print filesize('2.5MB').bytesize() # 2621440
		print filesize(1024).bytesize() # 1024
		print filesize('1024KB').bytesize() # 1048576
	"""
	SUFFIXES = ['KB','MB','GB','TB','PB','EB','ZB','YB'] 
	def bytesize(self):
		try:
			exp = self.SUFFIXES.index(self.__str__()[-2:])
			return int(float(self.__str__()[:-2])*1024**(exp+1)) 
		except ValueError:
			return self

class ContentTypeRestrictedFileField(forms.FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):        
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
	if data:
		file = data.file
		try:
			content_type = file.content_type
			if content_type in self.content_types:
				if file._size > self.max_upload_size:
					raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
			else:
				raise forms.ValidationError(_('Filetype not supported.'))
		except AttributeError:
			pass        
            
		return data

#### FORMULARS ####

################ Person #######################
#create a formular class for generating a formular
class LoginForm(forms.Form):
	log = forms.CharField(max_length=200,label = "Login",)
	pwd = forms.CharField(max_length=200, label = "password", widget= forms.PasswordInput())
	
class NusrForm(forms.Form):
	nom = forms.CharField(max_length=200,label = "* Last Name",widget=forms.TextInput(attrs={'size':'80'}))
	prenom = forms.CharField(max_length=200,label = "* First Name",widget=forms.TextInput(attrs={'size':'80'}))
	webp = forms.URLField(max_length=200, label = "Webpage", required=False,widget=forms.TextInput(attrs={'size':'80'}))
	email = forms.EmailField(max_length=200,label = "Email", required=False,widget=forms.TextInput(attrs={'size':'80'}))
	tel = forms.CharField(max_length=20, label = "Telephone", required=False)	
	profil = forms.ImageField(label="profil picture", required=False)	
	boss = forms.ModelChoiceField(queryset=User.objects.filter(status=1).filter(actif=True) ,label="Referent",required=False,help_text="let empty if you're a permanent or if your referent isn't in the list")
	site = forms.CharField(max_length=200,label="* Office",)
	status = forms.ModelChoiceField(queryset=UserStatus.objects.all() ,label="* Status")
	bio = forms.CharField(label = "English biography",required=False,widget=forms.Textarea())
	bio_fr = forms.CharField(label = "Biographie française",required=False,widget=forms.Textarea())
	group = forms.ModelMultipleChoiceField(queryset = Group.objects.filter(type_group=1), widget=forms.CheckboxSelectMultiple, label="Projects",required=False)	

class NgrpForm(forms.Form):
	nom = forms.CharField(max_length=200,label = "* Project name",)
	description = forms.CharField(max_length=20000,label = "Project description",required=False,widget=forms.Textarea() )
	profil = forms.ImageField(label="Project profil picture", required=False)
	date_exp  = forms.DateField(label="Expiration date", required=False)
	KW = forms.CharField(max_length=2000,label = "* Keywords",widget=forms.TextInput(attrs={'size':'80'}),help_text="separate words with commas")
	website = forms.URLField(max_length=2000,label = "Project website",required=False)
	email = forms.CharField(max_length=2000,label = "Project email",required=False)
	members = forms.ModelMultipleChoiceField(queryset = User.objects.filter(actif=True),label="* Members",widget=forms.SelectMultiple(attrs={"size":"40","style":"width:200px"}))
	isvis = forms.ModelChoiceField(queryset = TypeGroup.objects.all(),initial=get_object_or_404(TypeGroup,id_type_group=1), label="Project type",required=False)

################ MEDIA #######################
	
class AddFiles(forms.Form):
	name_ens = forms.ModelChoiceField(queryset= EnsFile.objects.all(),label = "* Name")

class UpdFile(forms.Form):
	name = forms.CharField(max_length=500,label = "* Name")
	desc = forms.CharField(max_length=2000000,label = "Description",required=False)
	date_del = forms.DateField(label="Delation date",required=False, initial= datetime.date.today()+datetime.timedelta(days=1))
	KW = forms.CharField(max_length=500,label = "Keywords",required=False,widget=forms.TextInput(attrs={'size':'80'}),help_text="separate words with commas")
	grp = forms.ModelChoiceField(queryset= Group.objects.all(),label = "Linked to a project",required=False)
	public = forms.BooleanField(initial=True, label="Public ?",required=False)

class AddFiles_type(forms.Form):
	type_ens = forms.ModelChoiceField(queryset= TypeEnsFile.objects.all(),label = "* Type",widget=forms.Select(attrs={"onchange":"show_ensfile(this.value);show_complementary(this.value);"}))

class AddMedia(forms.Form):
	name = forms.CharField(max_length=500,label = "* Name")
	desc = forms.CharField(max_length=2000000,label = "Description",required=False,widget=forms.Textarea())
	type_ens = forms.ModelChoiceField(queryset= TypeEnsFile.objects.all(),label = "* Type",widget=forms.Select(attrs={"onchange":"show_complementary(this.value);"}))
	cpyright= forms.ModelChoiceField(queryset= Copyright.objects.all(),label = "Copyright",required=False)
	origin = forms.CharField(max_length=500,label = "Origin",required=False)
	date_del = forms.DateField(label="Delation date",required=False, initial= datetime.date.today()+datetime.timedelta(days=1),help_text = "if empty equal permanent")
	KW = forms.CharField(max_length=500,label = "Keywords",required=False,widget=forms.TextInput(attrs={'size':'80'}),help_text="separate words with commas")
	grp = forms.ModelChoiceField(queryset= Group.objects.all(),label = "Linked to a project",required=False)
	public = forms.BooleanField(initial=False, label="Public ?",required=False)

class UpdMedia(forms.Form):
	name = forms.CharField(max_length=500,label = "* Name")
	origin = forms.CharField(max_length=500,label = "Origin",required=False)
	cpyright= forms.ModelChoiceField(queryset= Copyright.objects.all(),label = "Copyright",required=False)
	desc = forms.CharField(max_length=2000000,label = "Description",required=False)
	date_del = forms.DateField(label="Delation date",required=False, initial= datetime.date.today()+datetime.timedelta(days=1))
	KW = forms.CharField(max_length=500,label = "Keywords",required=False,widget=forms.TextInput(attrs={'size':'80'}),help_text="separate words with commas")
	grp = forms.ModelChoiceField(queryset= Group.objects.all(),label = "Linked to a project",required=False)
	public = forms.BooleanField(initial=True, label="Public ?",required=False)
	
class AddImage(forms.Form):
	type_image = forms.ModelChoiceField(queryset= TypeImage.objects.exclude(id_type_image=3),label = "Type",required=False)

class AddSatellite(forms.Form):
	sat = forms.ModelChoiceField(queryset= Satellite.objects.all(),label = "* Satellite")

class AddSound(forms.Form):
	type_sound = forms.ModelChoiceField(queryset= TypeSound.objects.all(),label = "Type",required=False)
	instrument = forms.ModelMultipleChoiceField(queryset = Instrument.objects.all(), label="Instruments",required=False,widget=forms.SelectMultiple(attrs={"size":"10","style":"width:200px"}))
	note = forms.ModelMultipleChoiceField(queryset = Note.objects.all(), label="Notes",required=False,widget=forms.SelectMultiple(attrs={"size":"10","style":"width:200px"}))

################ CODE #######################

class AddCodeForm(forms.Form):
	name = forms.CharField(label="* Tool Name",max_length=200,widget=forms.TextInput(attrs={'size':'80'}))
	code_type = forms.ModelChoiceField(queryset = TypeTool.objects.all(), label="Tool type",required=False)
	author = forms.CharField(label ="Authors",help_text="d'ont copy/paste",widget=forms.TextInput(attrs={'size':'80'}),required=False)
	version = forms.CharField(label="Version", max_length=20,required=False,widget=forms.TextInput(attrs={'size':'2'}))
	licence = forms.ModelChoiceField(queryset = License.objects.all(), label="License",required=False)
	webp = forms.CharField(label="Webpage",max_length=2000,required=False,widget=forms.TextInput(attrs={'size':'80'}))
	help_file = ContentTypeRestrictedFileField(label = "README File",required=False,help_text="README or a text file that explain your application",content_types=['text/plain'],max_upload_size=filesize('1MB').bytesize())
	desc = forms.CharField(max_length=200000000,label = "Description",widget=forms.Textarea(),required=False,help_text="describe with: <ul><li>goal</li><li>input/output/parameter</li><li>help texte</li></ul>")
	gpe = forms.ModelChoiceField(queryset = Group.objects.all(), label="Project",required=False,help_text="if the source is related to a particular project")
	links = forms.CharField(label="Video link",max_length=2000,help_text="(youtube, dailymotion, ...)" ,required=False,widget=forms.TextInput(attrs={'size':'80'}))
	KW = forms.CharField(max_length=500,label = "Keywords",required=False,widget=forms.TextInput(attrs={'size':'80'}),help_text="separate words with commas")
	public = forms.BooleanField(initial=True, label="Public ?",required=False)
	

class TypeAlgoForm(forms.Form):
	algo_name = forms.CharField(label ="Tool Type")

class LicenseForm(forms.Form):
	license_name = forms.CharField(label ="Tool License")

class UpdCodeForm(forms.Form):
	name = forms.CharField(label="Tool Name",max_length=200,widget=forms.TextInput(attrs={'size':'80'}))
	code_type = forms.ModelChoiceField(queryset = TypeTool.objects.all().order_by('nm_type_tool'), label="Tool type",required=False)
	author = forms.CharField(label ="Authors",help_text="d'ont copy/paste",widget=forms.TextInput(attrs={'size':'80'}),required=False)
	version = forms.CharField(label="Version", max_length=20,required=False)
	licence = forms.ModelChoiceField(queryset = License.objects.all(), label="License",required=False)
	webp = forms.CharField(label="Webpage",max_length=2000,required=False,widget=forms.TextInput(attrs={'size':'80'}))
	help_file = ContentTypeRestrictedFileField(label = "README File",required=False,help_text="README or a text file that explain your application",content_types=['text/plain'],max_upload_size=filesize('1MB').bytesize())
	desc = forms.CharField(max_length=200000000,label = "Description",widget=forms.Textarea(),required=False,help_text="describe with: <ul><li>goal</li><li>input/output/parameter</li><li>help texte</li></ul>")
	gpe = forms.ModelChoiceField(queryset = Group.objects.all(), label="Project",required=False,help_text="if the source is related to a particular project")
	links = forms.CharField(label="Video link",help_text="(youtube, dailymotion, ...)",max_length=2000 ,required=False,widget=forms.TextInput(attrs={'size':'80'}))
	KW = forms.CharField(max_length=500,label = "Keywords",required=False,widget=forms.TextInput(attrs={'size':'80'}),help_text="separate words with commas")
	public = forms.BooleanField(initial=True, label="Public ?",required=False)

################ PUBLI #######################
	
class AddPageForm(forms.Form):
	title = forms.CharField(label="* Title",max_length=2000,widget=forms.TextInput(attrs={'size':'80'}))
	
	author = forms.CharField(label ="* Authors",help_text="name then family name separeted with commass",widget=forms.TextInput(attrs={'size':'80'}))
	conference = forms.CharField(label="Report type",help_text="d'ont copy/paste",required=False)
	
	annee = forms.IntegerField(label="Year",initial=datetime.date.today().year,required=False)
	mois = forms.IntegerField(label="Month",initial=datetime.date.today().month,required=False)
	abstract = forms.CharField(label="Abstract",max_length=2000000, widget=forms.Textarea(),required=False)
	article = ContentTypeRestrictedFileField(label ="Report File",required=False,content_types=['text/plain'],max_upload_size=filesize('10MB').bytesize())
	prez = ContentTypeRestrictedFileField(label ="Presentation",required=False,content_types=['text/plain'],max_upload_size=filesize('10MB').bytesize())
	algo = forms.ModelMultipleChoiceField(queryset = Tool.objects.all(), label="Tool",required=False,widget=forms.SelectMultiple(attrs={"size":"10","style":"width:500px"}))
	demo = forms.ModelMultipleChoiceField(queryset = Demo.objects.all(), label="Demos",required=False,widget=forms.SelectMultiple(attrs={"size":"10","style":"width:500px"}))
	gpe = forms.ModelChoiceField(queryset = Group.objects.all(), label="Project",required=False,help_text="if the source is related to a particular project")
	links = forms.CharField(label="Video link",help_text="(youtube, dailymotion, ...)",max_length=2000,required=False,widget=forms.TextInput(attrs={'size':'80'}))
	KW = forms.CharField(max_length=500,label = "Keywords",required=False,widget=forms.TextInput(attrs={'size':'80'}),help_text="separate words with commas")

class UpdPageForm(forms.Form):
	#title = forms.CharField(label="* Title",max_length=2000,widget=forms.TextInput(attrs={'size':'80'}))
	#author = forms.CharField(label ="* Authors",help_text="d'ont copy/paste",widget=forms.TextInput(attrs={'size':'80'}))
	#conference = forms.CharField(label="Conference/Journal title",required=False)	
	#annee = forms.IntegerField(label="Year",initial=datetime.date.today().year,required=False)
	#mois = forms.IntegerField(label="Month",initial=datetime.date.today().month,required=False)
	abstract = forms.CharField(label="Abstract",max_length=2000000, widget=forms.Textarea(),required=False)
	algo = forms.ModelMultipleChoiceField(queryset = Tool.objects.all(), label="Tool",help_text='<a href="">',required=False,widget=forms.SelectMultiple(attrs={"size":"10","style":"width:500px"}))
	demo = forms.ModelMultipleChoiceField(queryset = Demo.objects.all(), label="Demos",required=False,widget=forms.SelectMultiple(attrs={"size":"10","style":"width:500px"}))
	gpe = forms.ModelChoiceField(queryset = Group.objects.all(), label="Project",required=False,help_text="if the source is related to a particular project")
	links = forms.CharField(label="Video link",help_text="(youtube, dailymotion, ...) separate with commas",max_length=2000 ,required=False,widget=forms.TextInput(attrs={'size':'80'}))
	KW = forms.CharField(max_length=500,label = "Keywords",help_text="separate with commas",required=False,widget=forms.TextInput(attrs={'size':'80'}))

class AddConf(forms.Form):
	title = forms.CharField(label="Title",max_length=2000)

class AddAlgoOnPage(forms.Form):
	name = forms.CharField(label="* Tool Name",max_length=200,widget=forms.TextInput(attrs={'size':'80'}))
	code_type = forms.ModelChoiceField(queryset = TypeTool.objects.all().order_by('nm_type_tool'), label="Tool type",required=False)
	version = forms.CharField(label="Version", max_length=20,required=False)
	licence = forms.ModelChoiceField(queryset = License.objects.all(), label="License",required=False)
	desc = forms.CharField(max_length=2000000,label = "Description",required=False,widget=forms.Textarea())
	help_file = ContentTypeRestrictedFileField(label = "README File",required=False,help_text="Put here your README or a text file that explain your application you can complete the information with the fields below",content_types=['text/plain'],max_upload_size=filesize('1MB').bytesize())
	public = forms.BooleanField(initial=True, label="Public ?",required=False)

years = [(i, str(i)) for i in range( Page.objects.all().aggregate(Max('annee'))['annee__max'],1970,-1)]
years.insert(0,(None,''))
#[range(datetime.datetime.now().year,1970,-1)]
l_m = ('','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec')
months = [(i,i) for i in l_m]
	
class PublicationFilter(forms.Form):
	year = forms.ChoiceField(choices=years,label="Year",required=False)
	mois = forms.ChoiceField(choices=months,label="Month",required=False)
	author = forms.CharField(label="Authors",max_length=200,required=False)
	search = forms.CharField(label="Search word",max_length=200,required=False)

############### DEMO ####################

class AddDemo(forms.Form):
	name = forms.CharField(label="* Demo Name",max_length=200,widget=forms.TextInput(attrs={'size':'80'}))
	tool = forms.ModelChoiceField(queryset = Tool.objects.all(), label="Tool",required=False)
	desc = forms.CharField(max_length=200000000,label = "Description",widget=forms.Textarea(),required=False)
	cmd = forms.CharField(label="* cmd",max_length=200,widget=forms.TextInput(attrs={'size':'80'}))
	organisation = forms.CharField(label="* Es organisation",max_length=4)
	estimate_time = forms.CharField(label="Time estimation",max_length=20,required=False)
	manager = forms.ModelChoiceField(queryset = User.objects.filter(actif=True), label="manager",required=False)
	
################ OTHER ###################

class ReportError(forms.Form):
	titre = forms.CharField(label="Title",required=False,widget=forms.TextInput(attrs={'size':'100'}))
	msg = forms.CharField(max_length=2000000,label = "Message",required=False,widget=forms.Textarea(attrs={'cols':'75','rows':'30'}))


class PubliForm(forms.Form):	
	publi = forms.ModelMultipleChoiceField(queryset = Page.objects.all(), label="Publications",required=False,widget=forms.SelectMultiple(attrs={"size":"10","style":"width:500px"}))

class DemoForm(forms.Form):
	demo = forms.ModelMultipleChoiceField(queryset = Demo.objects.all(), label="Demos",required=False,widget=forms.SelectMultiple(attrs={"size":"10","style":"width:500px"}))
	
class EnsfileForm(forms.Form):
	ensfile = forms.ModelMultipleChoiceField(queryset = EnsFile.objects.all(), label="Media",required=False,widget=forms.SelectMultiple(attrs={"size":"10","style":"width:500px"}))

class ToolForm(forms.Form):	
	tool = forms.ModelMultipleChoiceField(queryset = Tool.objects.all(), label="Tools",required=False,widget=forms.SelectMultiple(attrs={"size":"10","style":"width:500px"}))
