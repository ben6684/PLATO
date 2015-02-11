	
def demo(request):
	"""
	Full view for demo managing
	"""
	demo = "plop"
	if request.methid == 'POST':
		pass
	else:
		return render_to_response('demo/blur_effect.html',{'demo':demo,}, context_instance=RequestContext(request))

def demo_blur_effect(request):
	"""
	do the PIL demo
	"""
	if request.method=='POST':
		if request.FILES.has_key('input'):
			f= request.FILES['input']
			if f.size > filesize('10MB').bytesize():
				return render_to_response('demo/blur_effect.html', {
					'error_message':"The input file is too big, it should weighted less than 10MB",
					},context_instance=RequestContext(request))
			
			name = handle_uploaded_file_demo(f)
			if name == 'error':
				return render_to_response('demo/blur_effect.html', {
					'error_message':"Small problem with the demo server please send a message to the magnificent BENOIT PETITPAS",
					},context_instance=RequestContext(request))
			
				
			output_name = demo_img_filter(name)
			output_f = """<a href="/root/%s" class="highslide"  onclick="return hs.expand(this)"> <img src='/root/%s' width='100%%'/>
			  </a> 	"""%(output_name,output_name)
			input_f = """<a href="/root/%s" class="highslide"  onclick="return hs.expand(this)"> <img src='/root/%s' width='100%%'/></a> 	"""%(name,name)
			return render_to_response('demo/blur_effect.html', {
				'response':output_f,
				'example':input_f,
				},context_instance=RequestContext(request))
	return render_to_response('demo/blur_effect.html', context_instance=RequestContext(request))

def demo_remote_ls(request):
	"""
	do the PIL demo
	"""
	if request.method=='POST':
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect('137.194.233.80',username='petitpas',password='V-e4r7jc')
		stdin,stdout,stderr = ssh.exec_command('ls')
		output_f = stdout.readlines()
		return render_to_response('demo/remote_ls.html', {
				'response':output_f,
				},context_instance=RequestContext(request))
	return render_to_response('demo/remote_ls.html', context_instance=RequestContext(request))

def demo_remote_cpss(request):
	"""
	do the PIL demo
	"""
	if request.method=='POST':
		if request.FILES.has_key('input'):
			f= request.FILES['input']
			if f.size > filesize('30MB').bytesize():
				return render_to_response('demo/remote_cpss.html', {
					'error_message':"The input file is too big, it should weighted less than 10MB",
					},context_instance=RequestContext(request))
			
			name = handle_uploaded_file_demo(f)
			if name == 'error':
				return render_to_response('demo/remote_cpss.html', {
					'error_message':"Small problem with the demo server please send a message to the magnificent BENOIT PETITPAS",
					},context_instance=RequestContext(request))
			
				
			output_name = remote_cpss(name)

			return render_to_response('demo/remote_cpss.html', {
				'response':output_name,
				'example':name,
				},context_instance=RequestContext(request))
	return render_to_response('demo/remote_cpss.html', context_instance=RequestContext(request))
