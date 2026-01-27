from celery import Celery
from  app.celery.tasks import *

celery = Celery(
    'app',
    broker='redis://:0502@localhost:1010/0',
    backend='redis://:0502@localhost:1010/1',
)


