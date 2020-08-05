import os
import sys

sys.path.append('/home/huntajoseph/webapps/sketchyactivity/lib/python3.6/compressor/filters/')
sys.path.append('/home/huntajoseph/venvs/myvenv/lib/python3.6/')
sys.path.append('/home/huntajoseph/venvs/myvenv/lib/python3.6/site-packages/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

