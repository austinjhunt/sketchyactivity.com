import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'sketchyactivitybackend.settings'
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

