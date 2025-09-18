import contextlib
import os
import sys
import logging
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.config')
import django
django.setup()

app = Celery('loonflow')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

import json
import requests
from django.conf import settings
from io import StringIO


logger = logging.getLogger('django')



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task
def test_task(a, b):
    print('a:', a)
    print('b:', b)
    print(a+b)


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        try:
            # for python2
            stdout = StringIO.StringIO()
        except Exception:
            stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old



