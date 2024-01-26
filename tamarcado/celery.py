from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tamarcado.settings.dev")


app = Celery("tamarcado", broker="redis://redis:6379/0", backend="redis://redis:6379/0")


app.autodiscover_tasks()