"""
ASGI config for SocialProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django
from channels.routing import get_default_application
from asgi_cors import asgi_cors


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SocialProject.settings")
django.setup()
app = get_default_application()
application = asgi_cors(app, allow_all=True)
