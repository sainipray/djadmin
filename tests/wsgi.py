import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

