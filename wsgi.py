import os
import sys
from datetime import datetime

from eventCheckIn import create_app

app_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_path)

application = create_app()


@application.context_processor
def functions():
    return dict(strftime=datetime.strftime)
