# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from ._celery import app as celery_app
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
__all__ = ('celery_app',)