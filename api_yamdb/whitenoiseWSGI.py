from whitenoise import WhiteNoise
import os
from django.core.wsgi import get_wsgi_application
import api_yamdb.settings as settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
application = get_wsgi_application()


application = WhiteNoise(application, root=settings.STATIC_ROOT)
