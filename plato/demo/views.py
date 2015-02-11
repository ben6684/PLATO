
import datetime
import socket

import paramiko #for remote ssh

from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django import forms
from django.template import RequestContext

from util.views import *
from util.object_util import handle_uploaded_file_demo, guid, is_logged
from util.manage_demo import demo_img_filter, remote_cpss, perform_remote_demo
from plato.form import filesize
from plato.models import Demo,DemoPubli


def vdemos(request):

	demos = Demo.objects.all().order_by('-date_creation')
	return render_to_response('demo/vdemos.html',{'demos':demos}, context_instance=RequestContext(request))

def vdemo(request,nd):
	"""
	show form depending on the nd
	"""
	
	demo = get_object_or_404(Demo,id_demo =nd)	
	list_input = []
	dict_input={}
	list_output = []
	dict_output={}
	list_finish=[]
	list_param = []
	outfiles = None
	cmd = None
	flag=False
	flag_ex = False

	ext_flag = True
	plop = socket.gethostname()
	if plop in ['plato-dev','plato-test','plato-prod']:
		ext_flag = False

	#### before plato-demo ext was available we should cut the access ! not anymore 12/12/14 #####
	# plop = socket.gethostname()
	# if plop not in ['plato-dev','plato-test','plato-prod']:
	# 	return render_to_response('demo/vdemo.html',{'demo':demo,'outputs':dict_output,'inputs':dict_input,'test_output':outfiles,'test_cmd':cmd,'flag':flag,'plop':"""<p style="font-size:200%;"> Not avalable yet !</p>"""}, context_instance=RequestContext(request))
	
	if request.method=='POST':
		#create a unique folder name with a strange name 
		unique_folder = guid(demo.name_demo)
		#remote folder is the name of this unique folder name on the ZFS
		if plop in ['plato-dev','plato-test','plato-prod']:
			remote_folder = "/tsi/plato_tmp/"+unique_folder+"/"
		else:# you're doing a demo from the outside ! 
			remote_folder = "/tmp/"
		cpt=0
		for inp in demo.get_input(): #Every demo, has a list of needed demo inputs
			if request.FILES.has_key('input_'+str(inp.id_es)):# locate them into the demo form page (in REQUEST.FILES)
				f= request.FILES['input_'+str(inp.id_es)] # f is the input file

				### +> Determine limite more precisly ##########
				#we determine the type and verify the size (a sound need less space than a video
				# if inp.type_es.id_type_es == 1:
				# 	limite = filesize('2MB').bytesize()
				# elif inp.type_es.id_type_es == 2:
				# 	limite = filesize('3MB').bytesize()
				# elif inp.type_es.id_type_es == 3:
				# 	limite = filesize('200MB').bytesize()
				# elif inp.type_es.id_type_es == 4:
				# 	limite = filesize('100MB').bytesize()
				# else:
				# 	limite=filesize('2MB').bytesize()
				
				# if f.size > limite: # the file is too big 
				# 	return render_to_response('demo/vdemo.html', {
				# 		'error_message':"The input file is too big, it should weighted less than 10MB",
				# 		'demo':demo,
				# 		},context_instance=RequestContext(request))

				# The file is copying into the zfs
				name = handle_uploaded_file_demo(f,unique_folder)
				# name contains the name of the file folder 
				if name == 'error':
					return render_to_response('demo/vdemo.html', {
						'error_message':"Small problem with the demo server, the ZFS is dosn for a minute or two retry in a minute",
						'demo':demo,					
						},context_instance=RequestContext(request))
				if inp.cmd_es: # cmd_es contains value for programs that need something to say it s an entry like : -l left.png -r right.png, cmd_es contains the -l etc ...
					list_input.append(inp.cmd_es+" "+name) # list_inputssi a string containing the list of inputs with the potential command
				else:
					list_input.append(name)
				dict_input[inp.name_es]=name # dict_input is the same as list_input BUT in a dictionnary
			# if no inputs are given BUT there is examples, then examples is run
			elif demo.examples.all():
				flag_ex = True
				exs = demo.examples.all()
				if inp.cmd_es:
					list_input.append(inp.cmd_es+" "+exs[cpt].path)
				else:
					list_input.append(exs[cpt].path)
				dict_input[inp.name_es]=exs[cpt].path
				cpt=cpt + 1
			#no input AND no examples : did you push run for fun ? 
			else:
				return render_to_response('demo/vdemo.html', {
					'error_message':"don't get the input",
					'demo':demo,
					},context_instance=RequestContext(request))
		# now that we have the inputs, lets do the same thing for the parameters
		for par in demo.get_param():
			if not request.POST.has_key('param_'+str(par.id_param_demo)):
				return render_to_response('demo/vdemo.html', {
					'error_message':"don't get the param",
					'demo':demo,
					},context_instance=RequestContext(request))
			p = request.POST['param_'+str(par.id_param_demo)]
			if (par.limite_sup and p > par.limite_sup) or (par.limite_inf and p < par.limite_inf):
				return render_to_response('demo/vdemo.html', {
					'error_message':"param %s too big or too small"%(par.name_param),
					'demo':demo,
					},context_instance=RequestContext(request))
			if par.cmd_param:
				list_param.append(par.cmd_param+" "+p)
			else:
				list_param.append(p)
		for outp in demo.get_output():
			if outp.prefixed_name:
				# if flag_ex:
				# 	if outp.cmd_es:
				# 		list_output.append(cmd_es+' '+unique_folder+"_"+outp.prefixed_name)
				# 	else:
				# 		list_output.append(unique_folder+"_"+outp.prefixed_name)					
				# else:
				if outp.cmd_es:
					list_output.append(outp.cmd_es+" "+unique_folder+"_"+outp.prefixed_name)
				else:
					list_output.append(unique_folder+"_"+outp.prefixed_name)
				list_finish.append(unique_folder+"_"+outp.prefixed_name)
			else:
				return render_to_response('demo/vdemo.html', {
					'error_message':"Small problem with the demo server, the database is unreachable",
					'demo':demo,					
					},context_instance=RequestContext(request))
			dict_output[outp.name_es]=remote_folder+unique_folder+"_"+outp.prefixed_name

		# Now we have list of inputs, outputs, parameters => lets construct the bash line for running 
		e = " ".join(l.replace("(","\(").replace(")","\)") for l in list_input)
		p = " ".join(l.replace("(","\(").replace(")","\)") for l in list_param)
		s = " ".join(l.replace("(","\(").replace(")","\)") for l in list_output)
		if demo.organisation=="eps":
			cmd = demo.cmd%(e,p,s)
		elif demo.organisation=="esp":
			cmd = demo.cmd%(e,s,p)
		elif demo.organisation=="pes":
			cmd = demo.cmd%(p,e,s)
		elif demo.organisation=="pse":
			cmd = demo.cmd%(p,s,e)
		elif demo.organisation=="sep":
			cmd = demo.cmd%(s,e,p)
		elif demo.organisation=="spe":
			cmd = demo.cmd%(s,p,e)
		elif demo.organisation=="es":
			cmd = demo.cmd%(e,s)
		elif demo.organisation=="se":
			cmd = demo.cmd%(s,e)
		elif demo.organisation=="e":
			cmd = demo.cmd%(e)
		elif demo.organisation=="s":
			cmd = demo.cmd%(s)
		elif demo.organisation=="p":
			cmd = demo.cmd%(p)
		# return render_to_response('demo/vdemo.html', {
		# 	'error_message':cmd,
		# 	'demo':demo,					
		# 	},context_instance=RequestContext(request))
		outfiles = perform_remote_demo(cmd,list_finish,remote_folder)
		# return render_to_response('demo/vdemo.html', {
		# 	'error_message':outfiles,
		# 	'demo':demo,					
		# 	},context_instance=RequestContext(request))		
		flag=True
		#plop
	return render_to_response('demo/vdemo.html',{'demo':demo,'outputs':dict_output,'inputs':dict_input,'test_output':outfiles,'test_cmd':cmd,'flag':flag, 'flag_ex':flag_ex, 'ext':ext_flag}, context_instance=RequestContext(request))


from util.object_util import *

# get the path from the "app" object database
def path_from_demo(demo):
	"""
	\brief The point of this method is to extract the path of the files from info in the page table
	\input{an app object from the database}
	\output{a string containing the path to the app object, needed for adding files}
	"""
	fpath = get_plato_path() # from util.object_util (/tsi/plato if it's plato-tsi)
	path = "/%s/plato_users/petitpas/demo/%s/"%(fpath,demo.name_demo.replace(" ","_"))	
	return path


def add_demo_f_db(user,file,mede,demo):
	"""
	\brief add the files linked to a tool
	\input{user : the manager of the files; file : the file that must added to the tool(file object); mede : python object filled with the metadata of the file, tool : the tool object}
	\output{return the file }
	"""
	
	name = os.path.splitext(file.name)[0] #name of the file 
	size = file.size #its size
	typ = def_typ(mede) # define the MIME type
	type=get_object_or_404(TypeFile, id_type_file=typ) # look for the type into the database
	path = path_from_demo(demo) + file.name # then compute the path from infos in the tool
	# add the file to the database 
	f = File(name_file = name, size_file= size, path=path, type_file = type, manager = user,date_creation = datetime.date.today(), date_modification = datetime.date.today(), date_del=datetime.date(9999,12,12), visible=True)
	f.save()
	
	return f


@is_logged
def upd_demo_info(request,nd):
	"""
	Just a function for me ! 
	"""
	if request.session['login'] == 'petitpas':
		demo = get_object_or_404(Demo,id_demo=nd)
		if request.method=='POST':
			form = AddDemo(request.POST,request.FILES,prefix='form_demo')
			if form.is_valid():
				moi = get_object_or_404(User,login = request.session['login'])
				manager =  form.cleaned_data['manager']
				if manager != demo.manager:
					demo.manager=manager				
				name = form.cleaned_data['name']
				if name != demo.name_demo:
					demo.name_demo=name
				tool= form.cleaned_data['tool']
				if tool != demo.tool:
					demo.tool = tool
				desc = form.cleaned_data['desc']
				if desc != demo.desc_demo:
					demo.desc_demo = desc
				cmd = form.cleaned_data['cmd']
				if cmd != demo.cmd:
					demo.cmd = cmd
				organisation = form.cleaned_data['organisation']
				if organisation != demo.organisation:
					demo.organisation = organisation
				estimate_time = form.cleaned_data['estimate_time']
				if estimate_time != demo.estimate_time:
					demo.estimate_time = estimate_time
				cpt=0
				demo.save()
				nm_p = "demo/%s"%(demo.name_demo.replace(" ","_"))
				for f in request.FILES.getlist('figures'):
					mede = metadata_obj(f)	
					fil=add_demo_f_db(moi,f,mede,demo)
					management_file(fil,f,nm_p,0777)
					tf=DemoExample(fil=fil, demo=demo)
					tf.save()
					if request.POST.has_key("legende_%s"%(cpt)):
						tf.legende = request.POST["legende_%s"%(cpt)]
						tf.save()
					cpt=cpt+1
				return redirect('vdemos')
			else:
				return render_to_response('demo/upd_demo.html', {
					'form':form,
					'demo':demo,
					'error_message':form.errors,
				},context_instance=RequestContext(request))	
		else:
			form = AddDemo(prefix='form_demo',initial={'name':demo.name_demo,'tool':demo.tool,'desc':demo.desc_demo,'cmd':demo.cmd,'organisation':demo.organisation,'estimate_time':demo.estimate_time,'manager':demo.manager})
			return render_to_response('demo/upd_demo.html', {
				'form':form,
				'demo':demo,
				},context_instance=RequestContext(request))		
	else:
		return redirect('idx')

@is_logged
def add_demo_info(request):
	"""
	Just a function for me ! 
	"""
	if request.session['login'] == 'petitpas':
		if request.method=='POST':
			form = AddDemo(request.POST,request.FILES,prefix='form_demo')
			if form.is_valid():
				moi = get_object_or_404(User,login = request.session['login'])
				name = form.cleaned_data['name']
				tool= form.cleaned_data['tool']
				desc = form.cleaned_data['desc']
				cmd = form.cleaned_data['cmd']
				organisation = form.cleaned_data['organisation']
				estimate_time = form.cleaned_data['estimate_time']
				manager =  form.cleaned_data['manager']
				demo = Demo(name_demo=name,manager=manager,tool=tool,desc_demo=desc,cmd=cmd,organisation=organisation,date_creation=datetime.date.today(),estimate_time=estimate_time)
				demo.save()
				cpt=0
				nm_p = "demo/%s"%(demo.name_demo.replace(" ","_"))
				for f in request.FILES.getlist('figures'):
					mede = metadata_obj(f)	
					fil=add_demo_f_db(moi,f,mede,demo)
					management_file(fil,f,nm_p,0777)
					tf=DemoExample(fil=fil, demo=demo)
					tf.save()
					if request.POST.has_key("legende_%s"%(cpt)):
						tf.legende = request.POST["legende_%s"%(cpt)]
						tf.save()
					cpt=cpt+1
				return redirect('vdemos')
			else:
				return render_to_response('demo/add_demo.html', {
					'form':form,
					'error_message':form.errors,
				},context_instance=RequestContext(request))	
		else:
			form = AddDemo(prefix='form_demo')
			return render_to_response('demo/add_demo.html', {
				'form':form,
				},context_instance=RequestContext(request))
	else:
		return redirect('idx')
	
	return redirect('vdemos')

# from add_data.add_data import del_media_file_db
# @is_logged
# def del_file_demo(request):
# 	if request.is_ajax() and request.GET.has_key('id'):
# 		nf = request.GET['id']
# 		flag=del_media_file_db(nf)
# 	return HttpResponse("")
		
@is_logged
def add_publis_to_demo(request,nd):
	"""
	some how a good function to link something to a publication, here juste a demo ! 
	"""

	demo = get_object_or_404(Demo,id_demo=nd)
	if request.session['login'] in ['petitpas',demo.manager.login] :
		#it's me OR the creator of the demo !
		if request.method=='POST':
			form = PubliForm(request.POST)
			if form.is_valid():
				publis = form.cleaned_data['publi']
				for p in publis:
					dp = DemoPubli(demo=demo,page=p)
					dp.save()
				return redirect('/demo/%s'%nd)
			else:
				return render_to_response('demo/add_demo_publi.html', {
					'form':form,
				'demo':demo,
					},context_instance=RequestContext(request))		
			
		else:
			form = PubliForm()
			form.fields['publi'].queryset = demo.manager.get_publi()
			return render_to_response('demo/add_demo_publi.html', {
				'form':form,
				'demo':demo,
				},context_instance=RequestContext(request))
	else:
		if request.META.has_key('HTTP_REFERER'):
			redir = request.META['HTTP_REFERER']
		else:
			redir = 'idx'
		return redirect(redir)
