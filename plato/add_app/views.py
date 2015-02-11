# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse

from django import forms

from django.template import RequestContext
from django.core.urlresolvers import reverse


from util.object_util import is_logged

from plato.form import AddCodeForm,UpdCodeForm,PubliForm,DemoForm,EnsfileForm
from plato.models import User,File,Author,Tool,Group,ToolFigures,Page,Demo
from add_app import *
from add_data.add_data import *

@is_logged
def add_app(request):
	"""
	\brief add a tool
	\input{request is the python object contenaining all the information passed through the http request}
	\output{return a page}
	"""
	Grr = Group.objects.all()
	if request.method == 'POST':
		form = AddCodeForm(request.POST,request.FILES,prefix='form_algo')
		form_publi = PubliForm(request.POST,prefix='form_publicode')
		form_demo = DemoForm(request.POST,prefix='form_democode')
		form_ensfile = EnsfileForm(request.POST,prefix='form_ensfilecode')
		if form.is_valid():
			#do something
			me=get_object_or_404(User, login = request.session['login'])
			tool=add_tool_db(form,me) # we add the code in the data base
			nm_p = "tools/%s"%(tool.name_tool)
			for f in request.FILES.getlist('files'):
				mede = metadata_obj(f)
				fil=add_tool_f_db(me,f,mede,tool)
				management_file(fil,f,nm_p)
				tool.files.add(fil)
				tool.save()
			cpt=0
			for f in request.FILES.getlist('figures'):
				mede = metadata_obj(f)	
				fil=add_tool_f_db(me,f,mede,tool)
				management_file(fil,f,nm_p)
				tf=ToolFigures(figure=fil,tool=tool)
				tf.save()
				if request.POST.has_key("legende_%s"%(cpt)):
					tf.legende = request.POST["legende_%s"%(cpt)]
					tf.save()
				cpt=cpt+1
			if request.FILES.has_key('help_file'):
				help_f = request.FILES['help_file']
				if help_f:
					mede = metadata_obj(help_f)	
					fil=add_tool_f_db(me,help_f,mede,tool)
					management_file(fil,help_f,nm_p)
					tool.help_file.add(help_f)
					tool.save()	
			if form_publi.is_valid():
				upd_publi_code(form_publi,tool)
			if form_demo.is_valid():
				upd_demo_code(form_demo,tool)
			if form_ensfile.is_valid():
				upd_ensfile_code(form_ensfile,tool)
		else:
			if request.session['lang']=='fr':
				form=trans_label_fr(form)
			return render_to_response('add_app/add_source.html', {
				'form':form,
				'error_message':form.errors,
				},context_instance=RequestContext(request))
		return redirect('sources_codes')
	else:
		form = AddCodeForm(prefix='form_algo')
		# Here i need to add the label translate if request.session['lang']=='fr'
		if request.session['lang']=='fr':
			form=trans_label_fr(form)
		return render_to_response('add_app/add_source.html', {
			'form':form,
			},context_instance=RequestContext(request))

@is_logged
def upd_app(request,na):
	"""
	add a source
	"""
	me = get_object_or_404(User, login=request.session['login'])
	tool = get_object_or_404(Tool,id_tool=na)

	#if tool not in me.tool_set.all():
	#	return redirect('idx')
	if me != tool.manager and me.id_user != tool.manager.id_boss:
		return redirect('idx')
	
	if request.method == 'POST':
		form = AddCodeForm(request.POST,request.FILES,prefix='form_algo')
		form_publi = PubliForm(request.POST,prefix='form_publicode')
		form_demo = DemoForm(request.POST,prefix='form_democode')
		form_ensfile = EnsfileForm(request.POST,prefix='form_ensfilecode')
		if form.is_valid():
			#na=upd_code_db(form,algo) # we add the code in the data base
			tool=upd_tool_db(form,me,tool) # we add the code in the data base
			nm_p = "tools/%s/"%(tool.name_tool)
			for f in request.FILES.getlist('files'):
				mede = metadata_obj(f)	
				fil=add_tool_f_db(me,f,mede,tool)
				management_file(fil,f,nm_p)
				tool.files.add(fil)
				tool.save()
			cpt=0
			for f in request.FILES.getlist('figures'):
				mede = metadata_obj(f)	
				fil=add_tool_f_db(me,f,mede,tool)
				management_file(fil,f,nm_p)
				tf=ToolFigures(figure=fil,tool=tool)
				tf.save()
				if request.POST.has_key("legende_%s"%(cpt)):
					tf.legende = request.POST["legende_%s"%(cpt)]
					tf.save()
				cpt=cpt+1
			if request.FILES.has_key('help_file'):
				help_f = request.FILES['help_file']
				if help_f:
					mede = metadata_obj(help_f)	
					fil=add_tool_f_db(me,help_f,mede,tool)
					management_file(fil,help_f,nm_p)
					tool.help_file.add(help_f)
					tool.save()
			for tf in tool.toolfigures_set.all():
				if request.POST.has_key("legende_%s"%(tf.figure.id_file)):
					tf.legende = request.POST["legende_%s"%(tf.figure.id_file)]
					tf.save()
			if form_publi.is_valid():
				upd_publi_code(form_publi,tool)
			if form_demo.is_valid():
				upd_demo_code(form_demo,tool)
			if form_ensfile.is_valid():
				upd_ensfile_code(form_ensfile,tool)
		else:
			if request.session['lang']=='fr':
				form=trans_label_fr(form)
			return render_to_response('add_app/upd_source.html', {
				'form':form,
				'error_message':form.errors,
				},context_instance=RequestContext(request))
		return redirect('sources_codes')
	else:
		author = ",".join([unicode(a) for a in tool.get_tool_author()])
		KW =  ",".join([unicode(a) for a in tool.KW.all()])
		form = AddCodeForm(prefix='form_algo',initial={'name':tool.name_tool,'code_type':tool.type_tool,'author':author,'webp':tool.webpage_tool,'licence':tool.licence,'version':tool.version_tool,'desc':tool.desc_tool,'gpe':tool.group,'pages':tool.page_set.all(), 'KW':KW, 'public': tool.visible})
		if request.session['lang']=='fr':
			form=trans_label_fr(form)
		return render_to_response('add_app/upd_source.html', {
			'form':form,
			'algo':tool,
			},context_instance=RequestContext(request))


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@is_logged
def autoAuthor2(request):
	HTML=''
	if request.POST.has_key('form_algo-author') and request.is_ajax():
		HTML ="<ul>"
		filt = request.POST.get('form_algo-author')
		A = Author.objects.raw("SELECT * FROM author WHERE nm ILIKE %s OR fstnm ILIKE %s",["%s%%"%filt,"%s%%"%filt])
		for a in A:
			HTML+="""<li id="%s">%s</li>"""%(a.id_author,a)
		
	return HttpResponse(HTML)

@is_logged
def del_file_algo(request):
	#[To do] : verify delation ok 
	if request.is_ajax() and request.GET.has_key('id'):
		nf = request.GET['id']
		del_media_file_db(nf)
	return ""


@is_logged
def del_tool(request,na):
	#[To do] : verify delation ok 
	del_tool_db(na)
	return redirect('sources_codes')


@is_logged
def publi_code(request):
	HTML=""
	if request.GET.has_key('publi'):
		ntool = request.GET['publi']
		connected = get_object_or_404(User,login = request.session['login'])
		# We give the publication of the conencted person
		form_publi = PubliForm(prefix='form_publicode')
		form_publi.fields['publi'].queryset = connected.get_publi()
		if not ntool == -1 and not ntool == '-1': # update
			tool = get_object_or_404(Tool,id_tool = ntool)
			form_publi.fields['publi'].initial = tool.page_set.all()
		HTML+= form_publi.as_table()
	return HttpResponse(HTML)	

@is_logged
def demo_code(request):
	HTML=""
	if request.GET.has_key('demo'):
		ntool = request.GET['demo']
		# We give the democation of the conencted person
		form_demo = DemoForm(prefix='form_democode')
		if not ntool == -1 and not ntool == '-1': # update
			tool = get_object_or_404(Tool,id_tool = ntool)
			form_demo.fields['demo'].initial = tool.demo_set.all()
		HTML+= form_demo.as_table()
	return HttpResponse(HTML)	

@is_logged
def ensfile_code(request):
	HTML=""
	if request.GET.has_key('ensfile'):
		ntool = request.GET['ensfile']
		# We give the democation of the conencted person
		form_ensfile = EnsfileForm(prefix='form_ensfilecode')
		if not ntool == -1 and not ntool == '-1': # update
			tool = get_object_or_404(Tool,id_tool = ntool)
			form_ensfile.fields['ensfile'].initial = tool.ensfile.all()
		HTML+= form_ensfile.as_table()
	return HttpResponse(HTML)	
