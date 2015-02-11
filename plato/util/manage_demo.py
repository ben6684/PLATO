# -*- coding: utf-8 -*-
from PIL import Image,ImageFilter
from util.object_util import *

#Paramiko is a Python implementation of the SSH protocol
import paramiko
import os

## small function not used anymore for testing demo ... but works ON the server, something that we don't want ! 
def demo_img_filter(f):
	"""
	\brief first demo with simple PIL example
	\author{B. Petitpas}
	\date{11/12/2012}
	\in{f is a filename}
	"""
	import os
	if test_image_extension(f):
		#load file
		im = Image.open(f)
		# treat file
		im = im.filter(ImageFilter.CONTOUR)
		#save outfile
		outfile = os.path.splitext(f)[0] + ".out"+os.path.splitext(f)[1]
		im.save(outfile,"JPEG")
		#return the file
		return outfile
	else:
		return -1

########## Demo create a ssh connection to the demo server =>  to lunch the 

import socket

def create_ssh_connection():
	"""
	perform a ssh conenxion
	return the ssh object
	"""
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	sock = socket.gethostname()
	if sock in ['plato-dev','plato-test','plato-prod']:
		ssh.connect('137.194.0.89',username='plato_user',password='ad42TX214')
	else:
		ssh.connect('137.194.2.63',username='plato_user',password='ad42TX214')
	return ssh

def create_sftp_connection():
	"""
	perform a ssh conenxion
	return the ssh object
	"""
	sock = socket.gethostname()
	if sock in ['plato-dev','plato-test','plato-prod']:
		transport = paramiko.Transport(('137.194.0.89', 22))
		transport.connect(username = 'plato_user', password = 'ad42TX214')
	else:
		transport = paramiko.Transport(('137.194.2.63', 22))
		transport.connect(username = 'plato_user', password = 'ad42TX214')
		
	sftp = paramiko.SFTPClient.from_transport(transport)
	return sftp

#### NOT USED ANYMORE used for testing !!!! ######
def remote_cpss(f):
	"""
	connect to petitpas machine (change it in the futur ! )
	and perform a cpss
	"""
	outfile = os.path.splitext(f)[0] + ".out"+os.path.splitext(f)[1]
	ssh = create_ssh_connection()
	ssh.exec_command('~/MobyDick_0.3/bin/mobyAcc %s 0.1 10 ~/temp.ply'%(f))

	#now copy ~/temp.ply => to outfile
	sftp = create_sftp_connection()
	sftp.get("temp.ply", '%s'%(outfile), None)
	return outfile


### Perform 
def perform_remote_demo(cmd,list_output,remote_folder):
	"""
	Perform a generic way to perform demo
	"""
	ssh = ""
	try:
		ssh = create_ssh_connection()
	except:
		return "erreur à la connexion"
	### HERE call the demo depending on the entry and params ####
	stdin, stdout, stderr = ssh.exec_command(cmd)
	#return stderr.readlines()
	#channel = ssh.invoke_shell()
	#channel.send(cmd)
	
	plop =  stdout.channel.recv_exit_status()
	#plop =  channel.recv_exit_status()
	if plop!=0:
		return stdout.readlines()

	outfile = []
	#test if remote_folder exists
	if not os.path.exists(remote_folder):
		try:
			os.makedirs(remote_folder)
			os.chmod(remote_folder,0777)
		except OSError:
			return "impossible de creer un dossier"
	#### Dependign on the number of output (here assusming 1) get sorti_prog to copy them into the tsi zfs ####
	sftp = create_sftp_connection()
	for f in list_output:
		sftp.get("%s"%(f), '%s'%(remote_folder+f), None)
		outfile.append(remote_folder+f)
		sftp.remove("%s"%(f))
	return outfile
