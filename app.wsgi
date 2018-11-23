import os

os.environ['DIH_DATABASE'] = '%DIH_DATABASE%'
os.environ['DIH_CONFIG'] = '%DIH_CONFIG%'

import sys
sys.path.insert(0, '/var/www/dih')

from dih.app import app as application
