###########################################################################

# Not used anymore, i kept it for no reason, maybe because i'm scared of deleting if there is any problem

###########################################################################
from optparse import OptionParser, OptionGroup
import psycopg2
import os, sys
import shutil
import datetime
import errno

#################### META - DATA #######################
##### COPY FROM plato/util/object_util.py #####
from hachoir_core.error import HachoirError
from hachoir_core.stream import InputIOStream
from hachoir_parser import guessParser,createParser
from hachoir_metadata import extractMetadata
from hachoir_core.cmd_line import unicodeFilename

def metadata_for_file(filename):
	
	filename, realname = unicodeFilename(filename), filename
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
	if test_hachoir_extension(filelike):
		metadata = metadata_for_file(filelike)
		if metadata:
			data = dict([
				(data.key, data.values[0].value)
				for data in metadata
				if data.values
				])
		else:
			data=None
	else:
		data = None
		
	return data


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

class Error(EnvironmentError):
    pass

try:
    WindowsError
except NameError:
    WindowsError = None

def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

	if not os.path.exists(dst):
		os.makedirs(dst)
    errors = []
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
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def add_files_db(cur,src,dst,manager,ens_file,date_del):
	names = os.listdir(src)
	errors = []
	for name in names:
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		if os.path.isdir(srcname):
			add_files_db(cur,srcname,dstname,manager,ens_file, date_del)
		else:
			fileName, fileExtension = os.path.splitext(name)
			mede=metadata_obj(srcname)
			typ = def_typ(mede)
			cur.execute("""INSERT INTO file (name_file, size_file, path, id_user, id_ensfile, date_creation, date_modification, date_del, id_group, all_f, id_type_file) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", (fileName,os.path.getsize(srcname),dstname,manager,ens_file['id_ensfile'],datetime.date.today(),datetime.date.today(),date_del, ens_file['id_group'], ens_file['all_f'],typ))
  	
def main():
	usage="[USAGE] : %prog <options> files or path/ (end the path by a slash)"
	version = "%prog 1.0"
	description = "[DESCRIPTION] : %prog allows you to add multiple massive data to PLATO. You have two choices : Add files to an existing gathering OR add a new file gathering"
	parser = OptionParser(usage = usage, version = version, description = description)
	parser.add_option("-d", "--date_del", help="[Optional] Delation date : <jj/mm/20yy>, permanent if empty")

	group  = OptionGroup(parser, "Add files to an existing gathering")
	group. add_option("-p", "--path", help="path of the existing gathering </tsi/foo/bar/>")
	parser.add_option_group(group)

	group2 = OptionGroup(parser, "Add new file gathering")
	group2.add_option("-n","--name",help="Name of this new gathering")
	group2.add_option("-g","--group",help="[Optional] Add this gathering to an existing project/group")
	group2.add_option("-s","--secret",action="store_true",help="[Optional] To make the files private for the group, if -s is absent the files are public")
	parser.add_option_group(group2)
	parser.set_defaults(secret=False)


	(opt,arg)=parser.parse_args()

	if len(arg)<1:
		parser.error("[NO FILE FOUND] Incorrect argument, you need to add at least one file")

	if not opt.path and not opt.name:
		parser.error("[NO OPTION FOUND] --path or --name missing : You need either to add a new gathering or add files to an existing gathering")

	manager_login = os.getenv('HOME').split('/')[-1]
	#print manager_login

	path=""
	if opt.path:
		path = opt.path
	else:
		if opt.group:
			if opt.secret:
				path = "/tmp/project/%s/%s/private/"%(opt.group, opt.name)
			else:
				path = "/tmp/project/%s/%s/public/"%(opt.group, opt.name)
		else:
			path = "/tmp/perso/%s/%s/"%(manager_login,opt.name)
	#print path

	try:
		con = psycopg2.connect("dbname='plato_test' user='petitpas' password='V-e4r7jc' host='plato.enst.fr'")
	except:
		print "Database unreachable"

	cur = con.cursor()
	try:
		cur.execute("""SELECT id_user FROM "user" WHERE login=%s """,(manager_login,))
	except:
		print "No select possible, you're not a user of PLATO => GO TO plato.enst.fr"
	manager=cur.fetchone()[0]

	#### create ens_file ####

	if opt.date_del:
		dell = opt.date_del.split('/')
		date_del = datetime.date(int(dell[2]),int(dell[1]),int(dell[0]))
	else:
		date_del = datetime.date(9999,12,12)
	
	if not opt.path:

		group=None
		if opt.group:
			cur.execute("""SELECT id_group FROM "group" WHERE name_group ILIKE %s """,(opt.group,))
			group = cur.fetchone()
			if group:
				group = group[0]

		all_f = "TRUE"
		if opt.secret:
			all_f= "FALSE"

		cur.execute("""INSERT INTO ens_file (name_ensfile, id_user, date_creation, date_modification, date_del, id_group, all_f) VALUES (%s,%s,%s,%s,%s,%s,%s);""", (opt.name,manager,datetime.date.today(),datetime.date.today(),date_del, group, all_f))
		oid = cur.lastrowid
		cur.execute("""SELECT * FROM ens_file WHERE oid=%s """,(oid,))
		ens_file  = dictfetchall(cur)[0]

		#print ens_file

	else:
		fold=path.split('/')
		if fold[-2]=="public" or fold[-2]=="private":
			nm_ef=fold[-3]
		else:
			nm_ef=fold[-2]
		try:			
			cur.execute("""SELECT * FROM ens_file WHERE name_ensfile=%s """,(nm_ef,))
			ens_file  = dictfetchall(cur)[0]
			#print ens_file
		except:
			print "This path/gathering doesn't exist doesn't exists "

	# print ens_file
  	
	for a in arg:
		if a[-1]=='/':
			copytree(a,path)			
			add_files_db(cur,a,path,manager,ens_file,date_del)		
		else:
			shutil.copy2(a, path)
			fn = a.split('/')
			f = fn[-1]
			fileName, fileExtension = os.path.splitext(f)
			mede=metadata_obj(a)
			typ = def_typ(mede)
			cur.execute("""INSERT INTO file (name_file, size_file, path, id_user, id_ensfile, date_creation, date_modification, date_del, id_group, all_f, id_type_file) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", (fileName,os.path.getsize(a),path+f,manager,ens_file['id_ensfile'],datetime.date.today(),datetime.date.today(),date_del, ens_file['id_group'], ens_file['all_f'],typ))
			
	con.commit()
	cur.close()
	con.close()
			
if __name__== "__main__":
	main()
