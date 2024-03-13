"""
WSGI config for lvlgg_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
settings_module = 'lvlgg_backend.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'lvlgg_backend.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lvlgg_backend.settings')

application = get_wsgi_application()
