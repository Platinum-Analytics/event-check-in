import os
import sys
from datetime import datetime
from flask_login import current_user

from eventCheckIn import create_app

app_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_path)

application = create_app()


# Functions usable in Jinja2
@application.context_processor
def functions():
    return dict(strftime=datetime.strftime, current_user=current_user)
