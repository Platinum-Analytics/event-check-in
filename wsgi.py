import os
import sys

from eventCheckIn.__init__ import create_app

app_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_path)


application = create_app("config.py")
