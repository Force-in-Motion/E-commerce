from celery import Celery

celery = Celery(
    'worker',
    broker='redis://:0502@localhost:1010/0',
    backend='redis://:0502@localhost:1010/1',
)

