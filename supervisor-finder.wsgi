import sys
import logging

sys.path.insert(0, '/home/vagrant/supervisor-finder/flask')
logging.basicConfig(stream=sys.stderr)

from supervisor import app as application
