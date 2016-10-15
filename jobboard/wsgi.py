"""
WSGI config for jobboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
"""
import os, sys

sys.path.append('/var/www')

from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'jobboard.settings'
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobboard.settings")

application = get_wsgi_application()
"""
"""
import os, sys

sys.path.append('/var/www')

os.environ['DJANGO_SETTINGS_MODULE'] = 'jobboard.settings'

import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    #environ['SCRIPT_NAME'] = '/'
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    return _application(environ, start_response)
"""
import os
import sys
 
path = '/var/www/'
if path not in sys.path:
    sys.path.append(path)
 
sys.path.append('/var/www/workshops/sap/')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'jobboard.settings'

import django
django.setup()
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
