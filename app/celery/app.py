from celery import Celery

celery = Celery(
    'app',
    broker='redis://:0502@localhost:1010/0',
    backend='redis://:0502@localhost:1010/1',
)

# обязательно импортируем задачи, чтобы воркер их видел
import app.celery.tasks

# или автодисквери
# celery.autodiscover_tasks(['app.celery.tasks'])
