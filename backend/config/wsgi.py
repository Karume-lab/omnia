"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# THIS HAS BEEN ADDED SO THAT ALL APPS CAN BE IN THE apps/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(BASE_DIR, "apps")
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
