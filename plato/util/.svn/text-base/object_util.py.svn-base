# -*- coding: utf-8 -*-
from PIL import Image
from django.shortcuts import  redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from plato.models import KW

import os
from sys import stderr

####################### DECORATOR #############################
def is_logged(function=None):
	"""
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
	def _dec(view_func):
		def _view(request, *args, **kwargs):
			if request.session.get('login',None):
				return view_func(request, *args, **kwargs)
			else:
				return redirect('idx')

		_view.__name__ = view_func.__name__
		_view.__dict__ = view_func.__dict__
		_view.__doc__ = view_func.__doc__

		return _view

	if function is None:
		return _dec
	else:
		return _dec(function)

################## STRING/UNICODE MANAGEMENT #######

# We got a huge issue with this, because the database 
def str_s(s):
	s.encode('latin-1',errors='ignore').decode('latin-1')
	return s


################## GET PATH ########################
def get_plato_path():
	"""
	\brief function that return the first part of the path ! 
	"""
	return "/tsi/"

################# DATE VERIFICATION ################


def check_date(date):
	"""
	check if the date for delation added in any formular is not from befroee today !
	"""
	import datetime
	if date < datetime.date.today():
		return date
	else:
		return datetime.date.today()


################## PAGINATION ######################
def pagination(obj,pigi,nb_elt=10):
	"""
	Function that does the pagination. Using tool from django to do so.
	Very generic, can be used everywhere
	"""
	paginator = Paginator(obj,nb_elt)
	try:
		pago = int(pigi)
	except ValueError:
		pago=1
	try:
	    o = paginator.page(pago)
	except (EmptyPage,InvalidPage):
		o = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
	    o = paginator.page(1)
	return o

	
############## HACHOIR METADATA ########################
from hachoir_core.error import HachoirError
from hachoir_core.stream import InputIOStream
from hachoir_parser import guessParser,createParser
from hachoir_metadata import extractMetadata
from hachoir_core.cmd_line import unicodeFilename


def metadata_for_filelike(filelike):
	"""
	\brief : extract metadata for a FILE object (loaded from a <input>)
	\input{filelike : File Object}
	\output{None if there's a problem, a python dictionnary elsewhere}
	"""
	try:
		filelike.seek(0)
	except (AttributeError, IOError):
		return None
	stream = InputIOStream(filelike, None, tags=[])
	parser = guessParser(stream)

	if not parser:
		print >>stderr, "Unable to parse file"
		return None

	try:
		metadata = extractMetadata(parser)
	except HachoirError:
		print "Metadata extraction error: %s" % unicode(err)
		metadata = None
	if not metadata:
		print "Unable to extract metadata"
		return None

	return metadata

def metadata_for_file(filename):
	"""
	\brief : extract metadata for a filename (path + filename)
	\input{filelike : string object of the filename}
	\output{None if there's a problem, a python dictionnary elsewhere}
	"""
	if not isinstance(filename,unicode):
		import sys
		enc = sys.getfilesystemencoding()
	    #filename, realname = unicodeFilename(filename), filename
		filename, realname = unicode(filename,enc), filename
	else:
		filename, realname = filename, filename
	parser = createParser(filename, realname)
	if not parser:
		print >>stderr, "Unable to parse file"
		return None
	
	try:
		metadata = extractMetadata(parser)
	except HachoirError:	
		print "Metadata extraction error: %s" % unicode(err)
		metadata = None
	if not metadata:
		print "Unable to extract metadata"
		return None
	return metadata

def test_3D_extension(filename):
	"""
	\brief test if the filename is a 3D extension
	\input{just the filename}
	\output{True if the media is a good extention, False otherwise}
	"""
	
	# We need to make a test for extention :
	import  os
	extension = (os.path.splitext(filename)[1]).upper()
	ext_ok=['.3DMF','.3DM','.3DS','.ABC','.AC','.AMF','.AN8','.AOI','.B3D','.BLEND','.BLOCK','.C4D','.CAL3D','.CCP4','.CFL','.COB','.CORE3D','.CTM','.DAE','.DFF','.DPM','.DTS','.EGG','.FACT','.FBX','.G','.GLM','.JAS','.LWO','.LWS','.LXO','.MA','.MAX','.MB','.MD2','.MD3','.MDX','.MESH','.M','.MM3D','.MPO','.MRC','.NIF','.OBJ','.OFF','.PLY','.PRC','.POV','.RWX','.SIA','.SIB','.SKP','.SLDASM','.SLDPRT','.SMD','.U3D','.VIMPROJ','.WRL','.VUE','.WINGS','.W3D','.X','.X3D','.Z3D']
	if extension in ext_ok:
		return True
	else:
		return False

def test_hachoir_extension(filename):
	"""
	\brief test if the filename passed is in hachoir metadata accepted
	\input{just the filename}
	\output{True if the media is a good extention, False otherwise}
	"""
	
	# We need to make a test for extention :
	import  os
	extension = os.path.splitext(filename)[1]
	ext_ok=['.3do','.3ds','.7z','.a','.ace','.aif','.aifc','.aiff','.ani','.apm','.asf','.au','.avi','.bin','.bmp','.bz2','.cab','.cda','.chm','.class','.cur','.deb','.der','.dll','.doc','.dot','.emf','.exe','.flv','.gif','.gz','.ico','.jar','.jpeg','.jpg','.laf','.lnk','.m4a','.m4b','.m4p','.m4v','.mar','.mid','.midi','.mka','.mkv','.mod','.mov','.mp1','.mp2','.mp3','.mp4','.mpa','.mpe','.mpeg','.mpg','.msi','.nst','.oct','.ocx','.odb','.odc','.odf','.odg','.odi','.odm','.odp','.ods','.odt','.ogg','.ogm','.otg','.otp','.ots','.ott','.pcf','.pcx','.pdf','.png','.pot','.pps','.ppt','.ppz','.psd','.ptm','.pyc','.pyo','.qt','.ra','.rar','.rm','.rpm','.s3m','.sd0','.snd','.so','.stc','.std','.sti','.stw','.swf','.sxc','.sxd','.sxg','.sxi','.sxm','.sxw','.tar','.tga','.tif','.tiff','.torrent','.ts','.ttf','.vob','.wav','.wma','.wmf','.wmv','.wow','.xcf','.xla','.xls','.xm','.zip','.zs1','.zs2','.zs3','.zs4','.zs5','.zs6','.zs7','.zs8','.zs9','.zst','.3DO','.3DS','.7Z','.A','.ACE','.AIF','.AIFC','.AIFF','.ANI','.APM','.ASF','.AU','.AVI','.BIN','.BMP','.BZ2','.CAB','.CDA','.CHM','.CLASS','.CUR','.DEB','.DER','.DLL','.DOC','.DOT','.EMF','.EXE','.FLV','.GIF','.GZ','.ICO','.JAR','.JPEG','.JPG','.LAF','.LNK','.M4A','.M4B','.M4P','.M4V','.MAR','.MID','.MIDI','.MKA','.MKV','.MOD','.MOV','.MP1','.MP2','.MP3','.MP4','.MPA','.MPE','.MPEG','.MPG','.MSI','.NST','.OCT','.OCX','.ODB','.ODC','.ODF','.ODG','.ODI','.ODM','.ODP','.ODS','.ODT','.OGG','.OGM','.OTG','.OTP','.OTS','.OTT','.PCF','.PCX','.PDF','.PNG','.POT','.PPS','.PPT','.PPZ','.PSD','.PTM','.PYC','.PYO','.QT','.RA','.RAR','.RM','.RPM','.S3M','.SD0','.SND','.SO','.STC','.STD','.STI','.STW','.SWF','.SXC','.SXD','.SXG','.SXI','.SXM','.SXW','.TAR','.TGA','.TIF','.TIFF','.TORRENT','.TS','.TTF','.VOB','.WAV','.WMA','.WMF','.WMV','.WOW','.XCF','.XLA','.XLS','.XM','.ZIP','.ZS1','.ZS2','.ZS3','.ZS4','.ZS5','.ZS6','.ZS7','.ZS8','.ZS9','.ZST']
	if extension in ext_ok:
		return True
	else:
		return False
	
def metadata_obj(filelike):
	"""
	\brief metadata extract info form a media (or a stream objects like a fileupload) and put it into a dictionnary
	\input{filelike : a file object passed by the user (a test for extention compatibility should be done before)}
	\output{dict : a dictionnary containing all the metadata that HACHOIR was able to extract}
	"""
	if test_hachoir_extension(filelike.name):
		metadata = metadata_for_filelike(filelike)
		if metadata:
			data = dict([
				(data.key, data.values[0].value)
				for data in metadata
				if data.values
				])
		else:
			data=None
	elif test_3D_extension(filelike.name):# 3D not in the extention 
		data = {'mime_type':'model'}
	else:
		data = None
		
	return data


def metadata_name(filename):
	"""
	\brief metadata extract info form a media (or a stream objects like a fileupload) and put it into a dictionnary
	\input{filename : name a media (a test for extention compatibility should be done before)}
	\output{dict : a dictionnary containing all the metadata that HACHOIR was able to extract}

	"""
	if test_hachoir_extension(filename):
		metadata = metadata_for_file(filename)
		if metadata:
			data = dict([
				(data.key, data.values[0].value)
				for data in metadata
				if data.values
				])
		else:
			data=None
	elif test_3D_extension(filename):# 3D not in the extention 
		data = {'mime_type':'model'}
	else:
		data=None
	return data


##### Test extention for filename #####

def test_audio_extension(filename):
	"""
	\brief test if the filename is an audio extension
	\input{just the filename}
	\output{True if the media is a good extention, False otherwise}
	"""
	
	# We need to make a test for extention :
	import  os
	extension = os.path.splitext(filename)[1]
	ext_ok=['.aif','.aifc','.aiff','.au','.cda','.m4a','.m4b','.m4p','.mid','.midi','.mka','.mkv','.mod','.mp1','.mp2','.mp3','.mpa','.nst','.odm','.ogg','.ptm','.ra','.s3m','.snd','.wav','.wma','.wow','.xm','.AIF','.AIFC','.AIFF','.AU','.CDA','.M4A','.M4B','.M4P','.MID','.MIDI','.MKA','.MKV','.MOD','.MP1','.MP2','.MP3','.MPA','.NST','.ODM','.OGG','.PTM','.RA','.S3M','.SND','.WAV','.WMA','.WOW','.XM']
	if extension in ext_ok:
		return True
	else:
		return False
	

def test_image_extension(filename):
	"""
	\brief test if the filename is an image extension
	\input{just the filename}
	\output{True if the media is a good extention, False otherwise}
	"""
	
	# We need to make a test for extention :
	import  os
	extension = os.path.splitext(filename)[1]
	ext_ok=['.apm','.bmp','.gif','.ico','.jpeg','.jpg','.odi','.pcx','.png','.ppm','.psd','.tga','.tif','.tiff','.wmf','.xcf','.APM','.BMP','.GIF','.ICO','.JPEG','.JPG','.ODI','.PCX','.PNG','.PPM','.PSD','.TGA','.TIF','.TIFF','.WMF','.XCF']
	if extension in ext_ok:
		return True
	else:
		return False

def test_pdf_extension(filename):
	"""
	\brief test if the filename is a text extension
	\input{just the filename}
	\output{True if the media is a good extention, False otherwise}
	"""
	
	# We need to make a test for extention :
	import  os
	extension = os.path.splitext(filename)[1]
	ext_ok=['.pdf','.doc','.zip','.gz','.tar','.7z','.abw','.docx','.ppt','.pptx','.html','.odt','.tex','.txt','.wps','.xml','.ps','.odp','.pps','.PDF','.DOC','.ZIP','.GZ','.TAR','.7Z','.ABW','.DOCX','.PPT','.PPTX','.HTML','.ODT','.TEX','.TXT','.WPS','.XML','.PS','.ODP','.PPS']
	if extension in ext_ok:
		return True
	else:
		return False
	
######################### IMAGE THUMBNAILING #####################


def thumb_image(f, size=255):
	"""
	\brief : thumbnail image
	\input{f : the complete path to the image file (path+filename), <size> : optional size of the desire thumbnail (255 by default)}
	\output{0 if ok, -1 if not an image}
	"""
	size = size,size
	from PIL import Image
	if test_image_extension(f):
		im = Image.open(f)
		im.thumbnail(size, Image.ANTIALIAS)
		outfile = os.path.splitext(f)[0] + ".THUMB" + os.path.splitext(f)[1]
		im.save(outfile)
	else:
		return -1
	return 0
			
def thumb_profil(log):
	"""
	thumb the profile image => directly into the personal folder
	"""
	path = get_plato_path()
	from PIL import Image
	size = 100,200
	im = Image.open('/%s/plato_users/%s/profil_BIG.jpg'%(path,log))
	im.thumbnail(size, Image.ANTIALIAS)
	im.save('/%s/plato_users/%s/profil.jpg'%(path,log),"JPEG")


############################## HANDLE UPDLOAD ###########################
### Better Than the other below ###
def management_file(F,f,nom=None,chmod=None):
	"""
	\brief{management is a function for handling file data added, need F, the File objects added to the DB, and f, the file itself}
	"""
	# First: find the path in function ofthe authorisation
	
	path = get_plato_path()
	if F.group:
		if F.visible:
			path = path + "plato_projects/" + str(F.group.name_group) + "/public/" 
				
		else:
			path = path + "plato_projects/" + str(F.group.name_group) + "/private/"	
	else:
		if F.ensfile:
			path = path + "plato_users/" + str(F.ensfile.manager.login) + "/"
		elif F.manager:
			path = path + "plato_users/" + str(F.manager.login) + "/"
		else:
			path = path + "plato_tmp/"

	if nom:
		path = path + nom + "/"
		
	# Then : try to add the file, if the folder doesn't exist it will raise an error, create the folder
	flag=True
	error=""
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except:
			flag=False
			error ="Impossible to create the path, the ZFS encountered a problem, Sorry !"
	if flag:
		if chmod:
			try:
				os.chmod(path,chmod)
			except:
				error = "Impossible to change the rights on the files, impossible to add this data, Sorry, change the right and try again !"
		if not error:
			with open(path+'%s'%(f.name), 'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
				destination.close()
			if F.type_file.id_type_file == 1: # it's an Image
				thumb_image(path+'%s'%(f.name))
	else:
		return {'flag':False, 'error':error}
	return {'flag':True, 'error':error}

import time
import random
import socket
import hashlib
def guid( *args ):
	"""
	Generates a universally unique ID.
	Any arguments only create more randomness.
	"""
	t = long( time.time() * 1000 )
	r = long( random.random()*100000000000000000L )
	try:
		a = socket.gethostbyname( socket.gethostname() )
	except:
		# if we can't get a network address, just imagine one
		a = random.random()*100000000000000000L
	data = str(t)+' '+str(r)+' '+str(a)+' '+str(args)
	data = hashlib.md5(data).hexdigest()

	return data

def handle_uploaded_file_demo(f,folder="/"):
	"""
	The files used in the demo shouldn't be saved, so they're saved in /tmp/
	"""
	flag=True
	base_folder = "/tsi/plato_tmp/"
	input_f = '/%s/%s/%s' %(base_folder,folder,f.name)
	input_folder = '/%s/%s/'%(base_folder,folder)
	if not os.path.exists(input_folder):
		try:
			os.makedirs(input_folder)
			os.chmod(input_folder,0777)
		except OSError:
			flag=False
	if flag:
		with open(input_f, 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
		destination.close()
		return input_f
	else:
		return "error"
	
def handle_uploaded_profil(f,log,g=False):
	# dans le futur => svg sous /tmp => thumbnail au bon endroit => sup de /tmp
	# + test d'existance !

	import os
	path=get_plato_path()
	if g:
		path=path+"plato_projects/"
	else:
		path = path+"plato_users/"

	#flago = os.path.exists('/%s/%s/'%(path,log))
	#flagi = os.path.exists('/%s/'%(path))
	if os.path.exists('/%s/%s/'%(path,log)):
		with open('/%s/%s/profil_BIG.jpg' %(path,log), 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
			destination.close()
			thumb_profil(log)
	else:
		os.makedirs('/%s/%s/'%(path,log))
		handle_uploaded_profil(f,log)


############################## RM DIR #####################################

def rm_dirs(path):
	"""
	\brief Generic function to erase the directory located at ''path''
	"""
	flag_err = {'flag':True,'error':None}
	if os.path.exists(path):
		try:
			#rmdir(path)
			import shutil
			shutil.rmtree(path)
		except:
			flag_err={'flag':False, 'error':"impossible to delete your folder in /tsi/plato_tmp/, but it's complete on PLATO so PLEASE delete it yourself !"}
			return flag_err
		return flag_err
	else:		
		flag_err={'flag':True, 'error':"the folder in /tsi/plato_tmp/ doesn't exist, so it may be already deleted, so it may be ok, please verify."}
		return flag_err
	
########################### Update dir ####################################
import os
from shutil import *
def copytree2(src, dst, symlinks=False, ignore=None):
	"""
	function that copy a full folder on plato_tmp on plato ! 
	"""
	names = os.listdir(src)
	cpy_err={'flag':True, 'error':None}
	if ignore is not None:
		ignored_names = ignore(src, names)
	else:
		ignored_names = set()

	if not os.path.exists(dst):
		try:
			os.makedirs(dst)
		except:
			cpy_err= {'flag':False, 'error':"Impossible to create a directory, PLATO is accountered a problem, contact the administrator"}
			return cpy_err
	
	for name in names:
		if name in ignored_names:
			continue
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		try:
			if symlinks and os.path.islink(srcname):
				linkto = os.readlink(srcname)
				os.symlink(linkto, dstname)
			elif os.path.isdir(srcname):
				copytree(srcname, dstname, symlinks, ignore)
			else:
				copy2(srcname, dstname)
			# XXX What about devices, sockets etc.?
		except (IOError, os.error) as why:
	        # errors.append((srcname, dstname, str(why)))
			cpy_err={'flag':False,'error':str(why)}
			return cpy_err
		# catch the Error from the recursive copytree so that we can
		# continue with other files
		except Error as err:
			cpy_err={'flag':False,'error':str(err.args[0])}
			return cpy_err
		    # errors.extend(err.args[0])
	try:
		copystat(src, dst)
	except OSError as why:
		# errors.extend((src, dst, str(why)))
		cpy_err={'flag':False,'error':str(why)}
		return cpy_err
	# if errors:
	#     raise Error(errors)
	
	return cpy_err

def change_nm(src,dst):
	"""
	\brief If the name of an ens_file, tool, publi is changed, we need to change the name of the directory insed
	"""
	import os
	try:
		os.rename(src,dst)
	except:
		print "this is a mistake"
		return -1

	return 0

def change_grp_all_f(src,dst):
	"""
	\brief if there is a change of groups or public, we need to change the directory. For example, from /tsi/plato/plato_users/login/data/plop/ TO /tsi/plato/plato_projects/group/public/data/plop/
	"""
	copytree2(src,dst)
	rm_dirs(src)
	return 0
	
	


####### OLD management of the uploaded files: Kept them for avoiding some issues but should be delete ########

# def handle_uploaded_file_image(f,nom):
# 	if test_image_extension(f.name):
# 		try:
# 			with open('/tmp/perso/%s/%s' %(nom, f.name), 'wb+') as destination:
# 				for chunk in f.chunks():
# 					destination.write(chunk)
# 				destination.close()
# 				thumb_image("/tmp/perso/%s/%s"%(nom, f.name))
# 		except:
# 			import os
# 			os.makedirs('/tmp/perso/%s/'%(nom))
# 			handle_uploaded_file_image(f,nom)
# 	else:
# 		return -1
	
# def handle_uploaded_file_path(f,path):
# 	with open(path+'%s'%( f.name), 'wb+') as destination:
# 		for chunk in f.chunks():
# 			destination.write(chunk)
# 	destination.close()
# 	# if test_image_extension(f.name):
# 	# 	thumb_image("%s/%s"%(path, f.name))


# def handle_uploaded_file(f,nom):
# 	with open('/tmp/perso/%s/%s' %(nom, f.name), 'wb+') as destination:
# 		for chunk in f.chunks():
# 			destination.write(chunk)
# 	destination.close()
	
# def handle_uploaded_pdf(f,nom):
# 	if test_pdf_extension(f.name):
# 		try:
# 			with open('/tmp/perso/%s/%s' %( nom,f.name), 'wb+') as destination:
# 				for chunk in f.chunks():
# 					destination.write(chunk)
# 				destination.close()
# 		except:
# 			import os
# 			os.makedirs('/tmp/perso/%s/'%(nom))
# 			handle_uploaded_pdf(f,nom)
# 	else:
# 		return -1

#######################################################################################
		############ USEFULL GENERIC OBJECT UTIL FUNCTION #################
#######################################################################################

# import re
# def titlecase(s):
# 	"""
# 	\brief{Function that change the case for title, but used for every keywords and helping comparison}
# 	"""
# 	return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(),s)
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
def titlecase(s):
	return ' '.join(c.capitalize() for c in s.lower().split(' '))

def compa_type(t_ef, t_f):
	"""
	\brief{compare the ensfile type and the file type}
	\in{two integers corresponding to the id of the type in the DB}
	\out{return true if it's equal, false otherwise}
	"""
	if t_ef==1 and t_f==2:
		return True
	if t_ef in [2,3,4] and t_f ==1:
		return True
	if t_ef == 5 and t_f == 3:
		return True
	if t_ef==6 and t_f == 4:
		return True
	return False

def def_typ(mede):
	"""
	\brief{def_type use metadata dictionnary for returning the MIME type of the uploaded file}
	"""
	if mede:
		mime=mede['mime_type'].split('/')
		typ_mime = mime[0]
	else:
		#could be cause by : not a referenced type or hachoir failed.
		typ_mime='other'
		
	typ=0
	if typ_mime=='image':
		typ=1
	elif typ_mime=='audio':
		typ=2
	elif typ_mime=='video':
		typ=3
	elif typ_mime=='model':
		typ=4
	elif typ_mime=='text':
		typ=5
	elif typ_mime=='application':
		typ=6
	else:
		typ=7

	return typ

def add_kw(obj,kw):
	"""
	\brief{add_kw is a generic version for adding keyword to ANY kind of objects (model object)}
	\in{the object, and a list of keywords separate by a coma}
	\out{None}
	"""
	if kw:
		kw = kw.replace(';',',')
		kw = kw.split(',')
		for k in kw:
			k=k.lstrip()
			k=k.rstrip()
			K = KW.objects.filter(nm_kw__iexact=k)
			if K:
				obj.KW.add(K[0])
			else:
				kk = KW(nm_kw = k)
				kk.save()
				obj.KW.add(kk)
		obj.save()

def maj_prenom(value):
	"""
	\brief{here to put in uppercase composed firstname}
	"""
	db = value.split('-')
	if len(db)==2:
		out = db[0][0]+". - "+db[1][0]+"."
	else:
		out = value[0]+"."

table_en=['* Tool Name','Tool type','Authors','Version','License',
		  'Webpage','README File','Description','Project',
		  'Video link','Keywords','* Last Name','* First Name',
		  'Email','Telephone','profil picture','Referent','* Office',
		  '* Status','Biographie','Projects', '* Project name','Project description',
		  'Project profil picture','Expiration date','* Keywords','Project website',
		  'Project email','* Members','Project type',
		  '* Name','Delation date','Linked to a project','Public ?','* Type','* Public ?',
		  'Copyright','Origin','Type','* Satellite','Instruments','Notes','Tool Type',
		  'Tool License','Tool Name','* Title','* Authors','Report type','Year','Month',
		  'Report File','Presentation','Tool','Abstract','Title','Message','Search word',
		  'Visible ?']

table_fr=["* Nom de l'outil","Type de l'outil","Auteurs","Version","Licence","Page web","Fichier README","Description","Projet","Lien Vidéo","Mots clefs","* Nom","* Prénom","Courriel","Téléphone","Image de profil","Référent","* Bureau","* Status","Biographie","Projets","* Nom du projet","Description","Image de profil","Date d'expiration","* Mots clefs","Site Web","Courriel","* Membres","Type de Projet","* Nom","Date de suppression","liéer à un projet","Publique ?","* Type","* Publique?","Copyright","Origine","Type","* Satellite","Instruments","Notes","Type d'outil","Licence d'outil","Nom d'outil","* Titre","* Auteurs","Type de rapport","Année","Mois","Fichier de rapport","Présentation","Outil","Résumé","Titre",'Message',"Chercher","Visible ?"]


def trans_fr(label):
	"""
	translate the label by finding the index into the english table and then return the one from the french table
	"""
	try:
		#we try to find the label correspondante in french
		index_label_en = table_en.index(label)
	except:
		#if the label doesn't exists, then return the english label
		return label
	#otherwise return the french value of label
	return table_fr[index_label_en]

	

def trans_label_fr(form):
	"""
	\brief{translate the form label for each label in the form and translate it in the good langage, here in french}
	"""
	for field in form.fields:
		form.fields[field].label = trans_fr(form.fields[field].label)
	return form
	
def return_referer(request):
	if request.META.has_key('HTTP_REFERER'):
		return redirect(request.META['HTTP_REFERER'])
	else:
		return redirect('idx')
