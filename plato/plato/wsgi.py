"""
WSGI config for plato project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plato.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.

#def application(environ, start_response):
#	status='200 OK'
#	output = 'Hello pfff'
#
#	response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
#
#	start_response(status, response_headers)
#
#	return [output]


#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

import sys
path = '/var/www/'
path2 = '/var/www/plato/'
if path not in sys.path:
	sys.path.append(path)
if path2 not in sys.path:
	sys.path.append(path2)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
