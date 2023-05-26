import os, sys
sys.path.append('/home/guiacomercialbrasil/apps_wsgi')
sys.path.append('/home/guiacomercialbrasil/apps_wsgi/guiacomercialbrasil')
os.environ['PYTHON_EGG_CACHE'] = '/home/guiacomercialbrasil/apps_wsgi/.python-eggs'
os.environ['DJANGO_SETTINGS_MODULE'] = 'GuiaComercialBrasil.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
